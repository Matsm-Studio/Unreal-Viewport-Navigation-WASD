# SPDX-License-Identifier: GPL-3.0-or-later
"""Custom modal viewport navigation operator."""

import math
import time

# Serial used to invalidate a pending one-shot context-menu request when a new
# navigation interaction starts before the popup is shown.
_CONTEXT_MENU_REQUEST_SERIAL = 0

import bpy
try:
    import blf
except ImportError:
    blf = None
from bpy.types import Operator
from mathutils import Matrix, Vector

try:
    import gpu
    from gpu_extras.batch import batch_for_shader
except ImportError:
    gpu = None
    batch_for_shader = None

from .shared import (
    _ALT_KEYS, _CTRL_KEYS, _SHIFT_KEYS, _all_action_keys, _clamp, _controls_short, _format_speed,
    _header_text, _hold_key_is_held, _key_label, _modifier_event_set, _modifier_is_held,
    _movement_action_map, _shortcut_label, _speed_to_bu, _tr,
)




def _motion_alpha(dt, response_time):
    """Frame-rate-independent response reaching 99% after response_time."""
    return 1.0 - math.exp(-4.605170186 * max(0.0, float(dt)) / max(0.001, float(response_time)))

def _camera_from_context(context):
    """Return the camera used by this 3D View only when it is in Camera View."""
    area = getattr(context, "area", None)
    space = getattr(context, "space_data", None)
    rv3d = getattr(space, "region_3d", None)
    if area is None or area.type != "VIEW_3D" or rv3d is None:
        return None
    if rv3d.view_perspective != "CAMERA":
        return None

    camera = getattr(space, "camera", None) or getattr(getattr(context, "scene", None), "camera", None)
    if camera is None or getattr(camera, "type", None) != "CAMERA":
        return None
    return camera


def _tag_all_view3d_redraw(context):
    """Refresh every 3D View so split Camera Views update immediately."""
    window_manager = getattr(context, "window_manager", None)
    windows = getattr(window_manager, "windows", ()) if window_manager is not None else ()
    for window in windows:
        screen = getattr(window, "screen", None)
        for area in getattr(screen, "areas", ()) if screen is not None else ():
            if getattr(area, "type", None) == "VIEW_3D":
                try:
                    area.tag_redraw()
                except (ReferenceError, RuntimeError):
                    pass


def _selection_center(context, exclude=None):
    """Return a stable world-space center for the selection, optionally excluding one object."""
    selected = tuple(
        obj for obj in (getattr(context, "selected_objects", ()) or ())
        if obj is not None and obj is not exclude
    )
    if not selected:
        active = getattr(context, "active_object", None)
        selected = (active,) if active is not None and active is not exclude else ()
    if not selected:
        return None

    points = []
    for obj in selected:
        matrix = getattr(obj, "matrix_world", None)
        bounds = getattr(obj, "bound_box", None)
        if matrix is not None and bounds:
            try:
                points.extend(matrix @ Vector(corner) for corner in bounds)
                continue
            except (AttributeError, ReferenceError, RuntimeError, TypeError, ValueError):
                pass
        try:
            points.append(obj.matrix_world.translation.copy())
        except (AttributeError, ReferenceError, RuntimeError):
            pass

    if not points:
        return None
    center = Vector((0.0, 0.0, 0.0))
    for point in points:
        center += point
    return center / len(points)


class VIEW3D_OT_uvn155_orbit_selection(Operator):
    """Orbit the viewport or active Camera View camera around the selection."""

    bl_idname = "view3d.uvn155_orbit_selection"
    bl_label = "Orbit Around Selection"
    bl_description = "Orbit the viewport or protected Camera View camera around the selection"
    bl_options = {"REGISTER", "UNDO", "GRAB_CURSOR", "BLOCKING"}

    _window = None
    _area = None
    _rv3d = None
    _camera = None
    _target = None
    _distance = 1.0
    _yaw = 0.0
    _pitch = 0.0
    _prefs = None
    _initial_camera_matrix = None
    _initial_view_rotation = None
    _initial_view_location = None
    _initial_view_distance = 1.0

    @classmethod
    def poll(cls, context):
        if context.area is None or context.area.type != "VIEW_3D":
            return False
        try:
            prefs = context.preferences.addons[__package__].preferences
        except (AttributeError, KeyError):
            return False
        return bool(prefs.enable_orbit_selection)

    def invoke(self, context, event):
        try:
            self._prefs = context.preferences.addons[__package__].preferences
        except (AttributeError, KeyError):
            return {"CANCELLED"}

        required_modifier = getattr(self._prefs, "orbit_modifier", "ALT")
        if required_modifier != "NONE" and not _modifier_is_held(required_modifier, event):
            return {"PASS_THROUGH"}

        rv3d = getattr(context.space_data, "region_3d", None)
        if rv3d is None:
            return {"CANCELLED"}

        self._window = context.window
        self._area = context.area
        self._rv3d = rv3d
        self._camera = _camera_from_context(context) if self._prefs.camera_view_navigation else None

        # In Camera View, exclude the camera itself from the orbit target. With
        # protection enabled a real selected target is required, preventing an
        # accidental orbit around the camera's own origin. Escape always restores
        # the original camera transform. In a normal viewport, fall back to the
        # current view pivot so orbit also works without an object selection.
        target = _selection_center(context, exclude=self._camera)
        if target is None:
            if self._camera is not None and getattr(self._prefs, "protect_camera_orbit", True):
                self.report({"WARNING"}, _tr(self._prefs, "orbit_needs_selection"))
                return {"CANCELLED"}
            try:
                target = rv3d.view_location.copy()
            except (AttributeError, ReferenceError, RuntimeError):
                return {"CANCELLED"}
        self._target = target

        if self._camera is not None:
            self._initial_camera_matrix = self._camera.matrix_world.copy()
            eye = self._camera.matrix_world.translation.copy()
        else:
            self._initial_view_rotation = rv3d.view_rotation.copy()
            self._initial_view_location = rv3d.view_location.copy()
            self._initial_view_distance = float(rv3d.view_distance)
            eye = rv3d.view_location + rv3d.view_rotation @ Vector((0.0, 0.0, rv3d.view_distance))

        offset = eye - target
        self._distance = max(1.0e-5, offset.length)
        normal = offset / self._distance
        self._yaw = math.atan2(normal.y, normal.x)
        self._pitch = math.asin(_clamp(normal.z, -1.0, 1.0))

        context.window_manager.modal_handler_add(self)
        try:
            self._window.cursor_modal_set("NONE")
        except (AttributeError, RuntimeError, TypeError):
            pass
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        orbit_mouse = getattr(self._prefs, "orbit_mouse", "LEFTMOUSE")
        if event.type == orbit_mouse and event.value == "RELEASE":
            return self._finish()
        if event.type in {"ESC", "WINDOW_DEACTIVATE"}:
            self._restore()
            return self._finish()
        if event.type in {"MOUSEMOVE", "INBETWEEN_MOUSEMOVE"}:
            dx = _clamp(event.mouse_x - event.mouse_prev_x, -250.0, 250.0)
            dy = _clamp(event.mouse_y - event.mouse_prev_y, -250.0, 250.0)
            if dx or dy:
                sensitivity = float(self._prefs.look_sensitivity_ui) * 0.001
                self._yaw -= dx * sensitivity
                y_sign = -1.0 if self._prefs.invert_y else 1.0
                self._pitch += dy * sensitivity * y_sign
                self._pitch = _clamp(self._pitch, math.radians(-89.5), math.radians(89.5))
                cp = math.cos(self._pitch)
                offset = Vector((
                    cp * math.cos(self._yaw),
                    cp * math.sin(self._yaw),
                    math.sin(self._pitch),
                )) * self._distance
                eye = self._target + offset
                rotation = (self._target - eye).to_track_quat("-Z", "Y")
                if self._camera is not None:
                    scale = self._camera.matrix_world.to_scale()
                    self._camera.matrix_world = Matrix.LocRotScale(eye, rotation, scale)
                    _tag_all_view3d_redraw(context)
                else:
                    self._rv3d.view_rotation = rotation
                    self._rv3d.view_location = self._target
                    self._rv3d.view_distance = self._distance
                    self._area.tag_redraw()
            return {"RUNNING_MODAL"}
        return {"RUNNING_MODAL"}

    def _restore(self):
        try:
            if self._camera is not None and self._initial_camera_matrix is not None:
                self._camera.matrix_world = self._initial_camera_matrix
            elif self._rv3d is not None:
                self._rv3d.view_rotation = self._initial_view_rotation
                self._rv3d.view_location = self._initial_view_location
                self._rv3d.view_distance = self._initial_view_distance
        except (AttributeError, ReferenceError, RuntimeError):
            pass

    def _finish(self):
        if self._window is not None:
            try:
                self._window.cursor_modal_restore()
            except (AttributeError, ReferenceError, RuntimeError):
                pass
        if self._area is not None:
            try:
                self._area.tag_redraw()
            except (ReferenceError, RuntimeError):
                pass
        return {"FINISHED"}


class VIEW3D_OT_uvn155_navigate(Operator):
    """Custom Unreal-style mouse-look and flight navigation."""

    bl_idname = "view3d.uvn155_navigate"
    bl_label = "Unreal Viewport Navigation"
    bl_description = "Hold the configured navigation mouse shortcut and use the configured movement actions"
    bl_options = {"GRAB_CURSOR", "BLOCKING"}

    _timer = None
    _window = None
    _window_manager = None
    _area = None
    _region = None
    _region_pointer = 0
    _rv3d = None
    _preferences = None
    _pressed = None
    _active_move_keys = None
    _active_nav_keys = None
    _velocity = None
    _last_tick = 0.0
    _yaw = 0.0
    _pitch = 0.0
    _cursor_hidden = False
    _initial_mouse = (0, 0)
    _old_lock_rotation = False
    _draw_handle = None
    _crosshair_shader = None
    _navigation_active = False
    _hold_started_at = 0.0
    _camera_object = None
    _activation_mouse = "RIGHTMOUSE"
    _invoked_with_modifiers = False
    _action_keys = None

    @classmethod
    def poll(cls, context):
        return context.area is not None and context.area.type == "VIEW_3D"

    def invoke(self, context, event):
        global _CONTEXT_MENU_REQUEST_SERIAL
        _CONTEXT_MENU_REQUEST_SERIAL += 1
        try:
            prefs = context.preferences.addons[__package__].preferences
        except (AttributeError, KeyError):
            self.report({"ERROR"}, _tr(None, "error_prefs"))
            return {"CANCELLED"}

        # The keymap deliberately accepts any modifier so Shift/Ctrl can be
        # held before navigation starts.  Validate only the optional modifier
        # explicitly chosen for the navigation shortcut.
        required_modifier = getattr(prefs, "navigation_modifier", "NONE")
        if required_modifier != "NONE" and not _modifier_is_held(required_modifier, event):
            return {"PASS_THROUGH"}

        region = context.region
        if region is None or region.type != "WINDOW":
            region = next((item for item in context.area.regions if item.type == "WINDOW"), None)
        rv3d = getattr(context.space_data, "region_3d", None)
        if region is None or rv3d is None:
            self.report({"ERROR"}, _tr(prefs, "error_region"))
            return {"CANCELLED"}

        self._preferences = prefs
        self._window = context.window
        self._window_manager = context.window_manager
        self._area = context.area
        self._region = region
        self._region_pointer = region.as_pointer()
        self._rv3d = rv3d
        self._pressed = set()
        self._active_move_keys = set()
        self._active_nav_keys = set()
        self._velocity = Vector((0.0, 0.0, 0.0))
        self._cursor_hidden = False
        self._initial_mouse = (event.mouse_x, event.mouse_y)
        self._crosshair_shader = None
        self._navigation_active = False
        self._hold_started_at = time.perf_counter()
        self._old_lock_rotation = False
        self._camera_object = None
        self._activation_mouse = getattr(prefs, "navigation_mouse", "RIGHTMOUSE")
        self._invoked_with_modifiers = bool(event.shift or event.ctrl or event.alt)
        self._action_keys = _movement_action_map(prefs)
        if prefs.camera_view_navigation:
            self._camera_object = _camera_from_context(context)

        self._window_manager.modal_handler_add(self)

        if prefs.enable_rmb_click_hold:
            # A lightweight timer distinguishes a normal mouse click from a hold.
            # Full navigation state is initialized only after the configured delay.
            # One timer tick at the actual threshold is enough. This avoids
            # waking the modal operator 120 times per second while waiting.
            self._timer = self._window_manager.event_timer_add(
                max(0.01, float(prefs.rmb_hold_duration)),
                window=self._window,
            )
        else:
            # Immediate mode starts navigation as soon as the button is pressed.
            self._activate_navigation(event)

        return {"RUNNING_MODAL"}

    def _activate_navigation(self, event):
        if self._navigation_active:
            return

        prefs = self._preferences
        self._action_keys = _movement_action_map(prefs)
        self._active_move_keys = set().union(*self._action_keys.values())
        self._active_nav_keys = _all_action_keys(prefs) | _SHIFT_KEYS | _CTRL_KEYS | _ALT_KEYS
        self._last_tick = time.perf_counter()

        if event.shift:
            self._pressed.add("LEFT_SHIFT")
        if event.ctrl:
            self._pressed.add("LEFT_CTRL")
        if event.alt:
            self._pressed.add("LEFT_ALT")

        self._old_lock_rotation = bool(self._rv3d.lock_rotation)
        if self._old_lock_rotation:
            self._rv3d.lock_rotation = False

        if prefs.force_perspective and self._rv3d.view_perspective != "CAMERA":
            self._rv3d.view_perspective = "PERSP"

        self._read_angles_from_view()

        if prefs.hide_cursor:
            try:
                self._window.cursor_modal_set("NONE")
                self._cursor_hidden = True
            except (AttributeError, RuntimeError, TypeError):
                self._cursor_hidden = False

        self._add_draw_handler()

        # Restore the user's original navigation update-rate setting after
        # the short click/hold detection phase.
        if self._timer is not None:
            try:
                self._window_manager.event_timer_remove(self._timer)
            except (ReferenceError, RuntimeError):
                pass
        hz = max(30, int(prefs.update_rate))
        self._timer = self._window_manager.event_timer_add(1.0 / hz, window=self._window)

        self._navigation_active = True
        self._update_header()
        self._area.tag_redraw()

    @staticmethod
    def _context_menu_name(mode):
        menu_by_mode = {
            "OBJECT": "VIEW3D_MT_object_context_menu",
            "EDIT_MESH": "VIEW3D_MT_edit_mesh_context_menu",
            "EDIT_CURVE": "VIEW3D_MT_edit_curve_context_menu",
            "EDIT_SURFACE": "VIEW3D_MT_edit_curve_context_menu",
            "EDIT_TEXT": "VIEW3D_MT_edit_text_context_menu",
            "EDIT_ARMATURE": "VIEW3D_MT_armature_context_menu",
            "EDIT_METABALL": "VIEW3D_MT_edit_metaball_context_menu",
            "EDIT_LATTICE": "VIEW3D_MT_edit_lattice_context_menu",
            "POSE": "VIEW3D_MT_pose_context_menu",
            "SCULPT": "VIEW3D_MT_sculpt_context_menu",
            "PAINT_WEIGHT": "VIEW3D_MT_paint_weight_context_menu",
            "PAINT_VERTEX": "VIEW3D_MT_paint_vertex_context_menu",
            "PAINT_TEXTURE": "VIEW3D_MT_paint_texture_context_menu",
            "PARTICLE": "VIEW3D_MT_particle_context_menu",
        }
        return menu_by_mode.get(mode, "VIEW3D_MT_object_context_menu")

    def _schedule_context_menu(self):
        global _CONTEXT_MENU_REQUEST_SERIAL

        _CONTEXT_MENU_REQUEST_SERIAL += 1
        request_serial = _CONTEXT_MENU_REQUEST_SERIAL
        window = self._window
        area = self._area
        region = self._region
        mode = getattr(bpy.context, "mode", "OBJECT")
        menu_name = self._context_menu_name(mode)

        def show_menu_once():
            if request_serial != _CONTEXT_MENU_REQUEST_SERIAL:
                return None
            if window is None or area is None or region is None:
                return None
            try:
                with bpy.context.temp_override(window=window, area=area, region=region):
                    bpy.ops.wm.call_menu("INVOKE_DEFAULT", name=menu_name)
            except (ReferenceError, RuntimeError, TypeError):
                if menu_name != "VIEW3D_MT_object_context_menu":
                    try:
                        with bpy.context.temp_override(window=window, area=area, region=region):
                            bpy.ops.wm.call_menu(
                                "INVOKE_DEFAULT",
                                name="VIEW3D_MT_object_context_menu",
                            )
                    except (ReferenceError, RuntimeError, TypeError):
                        pass
            return None

        # Defer the popup very briefly so the current modal operator can leave
        # Blender's event stack first. A new navigation press invalidates this request.
        bpy.app.timers.register(show_menu_once, first_interval=0.04)

    def modal(self, context, event):
        try:
            if event.type == self._activation_mouse and event.value == "RELEASE":
                was_active = self._navigation_active
                if self._velocity is not None:
                    self._velocity.zero()
                result = self._finish(context)
                if (
                    not was_active
                    and self._preferences.enable_rmb_click_hold
                    and self._activation_mouse == "RIGHTMOUSE"
                    and getattr(self._preferences, "navigation_modifier", "NONE") == "NONE"
                    and not self._invoked_with_modifiers
                ):
                    self._schedule_context_menu()
                return result

            if event.type in {"ESC", "WINDOW_DEACTIVATE"}:
                if self._velocity is not None:
                    self._velocity.zero()
                return self._finish(context)

            prefs = self._preferences
            wheel_up = event.type in {"WHEELUPMOUSE", "WHEELINMOUSE"}
            wheel_down = event.type in {"WHEELDOWNMOUSE", "WHEELOUTMOUSE"}

            if not self._navigation_active:
                if event.type in {"MOUSEMOVE", "INBETWEEN_MOUSEMOVE"}:
                    dx = event.mouse_x - event.mouse_prev_x
                    dy = event.mouse_y - event.mouse_prev_y
                    if dx or dy:
                        self._activate_navigation(event)
                        self._apply_mouse_look(_clamp(dx, -250.0, 250.0), _clamp(dy, -250.0, 250.0))
                    return {"RUNNING_MODAL"}

                intent_keys = _all_action_keys(prefs)
                if event.type in intent_keys and event.value == "PRESS":
                    self._activate_navigation(event)
                    self._pressed.add(event.type)
                    return {"RUNNING_MODAL"}

                if event.type == "TIMER":
                    event_timer = getattr(event, "timer", None)
                    if event_timer is not None and event_timer != self._timer:
                        return {"PASS_THROUGH"}
                    if time.perf_counter() - self._hold_started_at >= float(prefs.rmb_hold_duration):
                        self._activate_navigation(event)
                    return {"RUNNING_MODAL"}
                return {"RUNNING_MODAL"}

            # Keep every keyboard/modifier state explicit. This works even when
            # the modifier was pressed after navigation started.
            if event.type in self._active_nav_keys:
                if event.value == "PRESS":
                    self._pressed.add(event.type)
                elif event.value == "RELEASE":
                    self._pressed.discard(event.type)
                # Speed actions are one-shot and should not become movement keys.
                if event.value == "PRESS" and event.type == prefs.speed_up_key:
                    self._adjust_speed(True)
                elif event.value == "PRESS" and event.type == prefs.speed_down_key:
                    self._adjust_speed(False)
                return {"RUNNING_MODAL"}

            if wheel_up or wheel_down:
                if event.type == prefs.speed_up_key or (wheel_up and prefs.speed_up_key == "WHEELUPMOUSE"):
                    self._adjust_speed(True)
                elif event.type == prefs.speed_down_key or (wheel_down and prefs.speed_down_key == "WHEELDOWNMOUSE"):
                    self._adjust_speed(False)
                elif prefs.navigate_during_tools:
                    return {"PASS_THROUGH"}
                return {"RUNNING_MODAL"}

            if event.value == "PRESS" and event.type == prefs.speed_up_key:
                self._adjust_speed(True)
                return {"RUNNING_MODAL"}
            if event.value == "PRESS" and event.type == prefs.speed_down_key:
                self._adjust_speed(False)
                return {"RUNNING_MODAL"}

            if event.type in {"MOUSEMOVE", "INBETWEEN_MOUSEMOVE"}:
                dx = event.mouse_x - event.mouse_prev_x
                dy = event.mouse_y - event.mouse_prev_y
                if self._region is not None:
                    width = max(1, int(self._region.width)); height = max(1, int(self._region.height))
                    if abs(dx) > width * 0.5: dx -= math.copysign(width, dx)
                    if abs(dy) > height * 0.5: dy -= math.copysign(height, dy)
                dx = _clamp(dx, -250.0, 250.0); dy = _clamp(dy, -250.0, 250.0)
                if dx or dy: self._apply_mouse_look(dx, dy)
                return {"RUNNING_MODAL"}

            if event.type == "TIMER":
                event_timer = getattr(event, "timer", None)
                if event_timer is None or event_timer == self._timer:
                    self._tick_motion()
                    return {"RUNNING_MODAL"}
                if prefs.navigate_during_tools:
                    return {"PASS_THROUGH"}
                return {"RUNNING_MODAL"}

            if prefs.navigate_during_tools:
                return {"PASS_THROUGH"}
            return {"RUNNING_MODAL"}

        except (ReferenceError, RuntimeError) as exc:
            self.report({"WARNING"}, _tr(self._preferences, "stopped", error=exc))
            return self._finish(context)

    def cancel(self, context):
        self._cleanup(context)

    def _read_angles_from_view(self):
        if self._camera_object is not None:
            rotation = self._camera_object.matrix_world.to_quaternion()
        else:
            rotation = self._rv3d.view_rotation
        forward = rotation @ Vector((0.0, 0.0, -1.0))
        if forward.length_squared < 1.0e-12:
            forward = Vector((0.0, 1.0, 0.0))
        else:
            forward.normalize()
        self._yaw = math.atan2(forward.y, forward.x)
        self._pitch = math.asin(_clamp(forward.z, -1.0, 1.0))

    def _apply_mouse_look(self, dx, dy):
        prefs = self._preferences
        sensitivity = float(prefs.look_sensitivity_ui) * 0.001

        self._yaw -= dx * sensitivity
        y_sign = -1.0 if prefs.invert_y else 1.0
        self._pitch += dy * sensitivity * y_sign
        self._pitch = _clamp(self._pitch, math.radians(-89.5), math.radians(89.5))
        self._yaw = (self._yaw + math.pi) % (2.0 * math.pi) - math.pi

        cp = math.cos(self._pitch)
        forward = Vector((
            cp * math.cos(self._yaw),
            cp * math.sin(self._yaw),
            math.sin(self._pitch),
        ))
        new_rotation = forward.to_track_quat("-Z", "Y")

        if self._camera_object is not None:
            matrix = self._camera_object.matrix_world.copy()
            location = matrix.translation.copy()
            scale = matrix.to_scale()
            self._camera_object.matrix_world = Matrix.LocRotScale(location, new_rotation, scale)
        else:
            old_rotation = self._rv3d.view_rotation.copy()
            distance = float(self._rv3d.view_distance)
            eye_position = self._rv3d.view_location + old_rotation @ Vector((0.0, 0.0, distance))
            self._rv3d.view_rotation = new_rotation
            self._rv3d.view_location = eye_position - new_rotation @ Vector((0.0, 0.0, distance))
        self._area.tag_redraw()

    def _movement_direction(self):
        direction = Vector((0.0, 0.0, 0.0))
        if self._camera_object is not None:
            rotation = self._camera_object.matrix_world.to_quaternion()
        else:
            rotation = self._rv3d.view_rotation

        if self._preferences.movement_mode == "LEVEL":
            forward = Vector((math.cos(self._yaw), math.sin(self._yaw), 0.0))
            right = Vector((-math.sin(self._yaw), math.cos(self._yaw), 0.0))
        else:
            forward = rotation @ Vector((0.0, 0.0, -1.0))
            right = rotation @ Vector((1.0, 0.0, 0.0))
            if forward.length_squared > 1.0e-12: forward.normalize()
            if right.length_squared > 1.0e-12: right.normalize()

        actions = self._action_keys or _movement_action_map(self._preferences)
        world_up = Vector((0.0, 0.0, 1.0))
        if self._pressed.intersection(actions["forward"]): direction += forward
        if self._pressed.intersection(actions["backward"]): direction -= forward
        if self._pressed.intersection(actions["right"]): direction += right
        if self._pressed.intersection(actions["left"]): direction -= right
        if self._pressed.intersection(actions["up"]): direction += world_up
        if self._pressed.intersection(actions["down"]): direction -= world_up
        if direction.length_squared > 1.0e-12: direction.normalize()
        return direction

    def _tick_motion(self):
        now = time.perf_counter()
        dt = _clamp(now - self._last_tick, 0.0001, 0.10)
        self._last_tick = now

        prefs = self._preferences
        direction = self._movement_direction()
        multiplier = 1.0
        if _hold_key_is_held(getattr(prefs, "sprint_key", "SHIFT"), pressed=self._pressed):
            multiplier *= float(prefs.sprint_multiplier)
        if _hold_key_is_held(getattr(prefs, "precision_key", "CTRL"), pressed=self._pressed):
            multiplier *= float(prefs.precision_multiplier)

        base_speed_bu = _speed_to_bu(float(prefs.move_speed), prefs.speed_unit, bpy.context)
        target_velocity = direction * base_speed_bu * multiplier

        if direction.length_squared <= 1.0e-12 and getattr(prefs, "instant_stop", True):
            self._velocity.zero()
            return

        if prefs.smooth_motion:
            response_time = float(prefs.acceleration_time) if direction.length_squared > 1.0e-12 else float(prefs.deceleration_time)
            # 4.605 reaches 99% of the target after response_time. This makes
            # 0.08 s and 0.30 s feel clearly different while remaining stable
            # at 30, 60, 120 and 240 Hz.
            alpha = _motion_alpha(dt, response_time)
            self._velocity = self._velocity.lerp(target_velocity, _clamp(alpha, 0.0, 1.0))
            if direction.length_squared <= 1.0e-12:
                stop_threshold = max(1.0e-6, base_speed_bu * 0.0025)
                if self._velocity.length <= stop_threshold:
                    self._velocity.zero()
        else:
            self._velocity = target_velocity

        if self._velocity.length_squared < 1.0e-12:
            self._velocity.zero()
            return

        offset = self._velocity * dt
        if self._camera_object is not None:
            matrix = self._camera_object.matrix_world.copy()
            matrix.translation = matrix.translation + offset
            self._camera_object.matrix_world = matrix
        else:
            self._rv3d.view_location = self._rv3d.view_location + offset
        self._area.tag_redraw()

    def _adjust_speed(self, faster):
        prefs = self._preferences
        factor = float(prefs.wheel_multiplier)
        speed = float(prefs.move_speed)
        speed = speed * factor if faster else speed / factor

        minimum = min(float(prefs.minimum_speed), float(prefs.maximum_speed))
        maximum = max(float(prefs.minimum_speed), float(prefs.maximum_speed))
        prefs.move_speed = _clamp(speed, minimum, maximum)
        self._update_header()

    def _update_header(self):
        if self._area is None:
            return
        prefs = self._preferences
        if prefs is None or not getattr(prefs, "show_navigation_hud", True):
            self._area.header_text_set(None)
            return
        position = getattr(prefs, "info_position", "HEADER")
        if position == "HEADER":
            text = _header_text(prefs)
        elif position == "SPLIT" and getattr(prefs, "show_header_speed", True):
            text = f"UE NAV | {_format_speed(prefs)}"
        else:
            text = None
        self._area.header_text_set(text)

    def _add_draw_handler(self):
        if self._draw_handle is not None:
            return
        try:
            self._draw_handle = bpy.types.SpaceView3D.draw_handler_add(
                self._draw_crosshair,
                (),
                "WINDOW",
                "POST_PIXEL",
            )
        except (AttributeError, RuntimeError, TypeError):
            self._draw_handle = None

    def _remove_draw_handler(self):
        if self._draw_handle is None:
            return
        try:
            bpy.types.SpaceView3D.draw_handler_remove(self._draw_handle, "WINDOW")
        except (AttributeError, ReferenceError, RuntimeError, TypeError):
            pass
        self._draw_handle = None
        self._crosshair_shader = None

    def _draw_crosshair(self):
        prefs = self._preferences
        if prefs is None:
            return

        context = bpy.context
        region = getattr(context, "region", None)
        if region is None or region.type != "WINDOW":
            return
        try:
            if region.as_pointer() != self._region_pointer:
                return
        except ReferenceError:
            return

        if prefs.show_navigation_hud:
            self._draw_navigation_hud(region)

        if not prefs.show_crosshair or gpu is None or batch_for_shader is None:
            return

        x = float(region.width) * 0.5
        y = float(region.height) * 0.5
        size = float(max(3, prefs.crosshair_size))
        gap = float(_clamp(prefs.crosshair_gap, 0, prefs.crosshair_size - 1))
        thickness = float(max(1.0, prefs.crosshair_thickness))
        color = tuple(float(component) for component in prefs.crosshair_color)
        style = prefs.crosshair_style

        try:
            if self._crosshair_shader is None:
                self._crosshair_shader = gpu.shader.from_builtin("UNIFORM_COLOR")
            shader = self._crosshair_shader

            gpu.state.blend_set("ALPHA")
            try:
                gpu.state.line_width_set(thickness)
            except (AttributeError, RuntimeError):
                pass

            if style in {"CROSS", "CROSS_DOT"}:
                line_vertices = (
                    (x - size, y), (x - gap, y),
                    (x + gap, y), (x + size, y),
                    (x, y - size), (x, y - gap),
                    (x, y + gap), (x, y + size),
                )
                batch = batch_for_shader(shader, "LINES", {"pos": line_vertices})
                shader.bind()
                shader.uniform_float("color", color)
                batch.draw(shader)

            if style == "CIRCLE":
                segments = 32
                radius = max(2.0, size * 0.45)
                vertices = []
                for index in range(segments):
                    angle_a = math.tau * index / segments
                    angle_b = math.tau * (index + 1) / segments
                    vertices.extend((
                        (x + math.cos(angle_a) * radius, y + math.sin(angle_a) * radius),
                        (x + math.cos(angle_b) * radius, y + math.sin(angle_b) * radius),
                    ))
                batch = batch_for_shader(shader, "LINES", {"pos": vertices})
                shader.bind()
                shader.uniform_float("color", color)
                batch.draw(shader)

            if style == "FILLED_CIRCLE":
                segments = 32
                radius = max(2.0, size * 0.45)
                vertices = []
                for index in range(segments):
                    angle_a = math.tau * index / segments
                    angle_b = math.tau * (index + 1) / segments
                    vertices.extend((
                        (x, y),
                        (x + math.cos(angle_a) * radius, y + math.sin(angle_a) * radius),
                        (x + math.cos(angle_b) * radius, y + math.sin(angle_b) * radius),
                    ))
                batch = batch_for_shader(shader, "TRIS", {"pos": vertices})
                shader.bind()
                shader.uniform_float("color", color)
                batch.draw(shader)

            if style in {"DOT", "CROSS_DOT"}:
                radius = max(1.5, thickness * 1.25)
                vertices = (
                    (x - radius, y - radius),
                    (x + radius, y - radius),
                    (x + radius, y + radius),
                    (x - radius, y - radius),
                    (x + radius, y + radius),
                    (x - radius, y + radius),
                )
                batch = batch_for_shader(shader, "TRIS", {"pos": vertices})
                shader.bind()
                shader.uniform_float("color", color)
                batch.draw(shader)

        except (AttributeError, RuntimeError, SystemError, ValueError):
            # Drawing must never stop navigation on an unsupported GPU/backend.
            self._crosshair_shader = None
        finally:
            try:
                gpu.state.line_width_set(1.0)
                gpu.state.blend_set("NONE")
            except (AttributeError, RuntimeError, SystemError):
                pass

    def _draw_navigation_hud(self, region):
        if blf is None or self._preferences is None:
            return
        prefs = self._preferences
        if not getattr(prefs, "show_navigation_hud", True):
            return

        position = getattr(prefs, "info_position", "HEADER")
        # HEADER uses Blender's native viewport header, exactly like the compact
        # presentation in v1.1.1. No duplicate overlay is drawn in this mode.
        if position == "HEADER":
            return

        if position == "SPLIT":
            # The top half (speed) is handled by _update_header(). The bottom
            # half contains only the control hints.
            if not getattr(prefs, "show_header_tutorial", True):
                return
            text = _controls_short(prefs)
        else:
            parts = []
            if getattr(prefs, "show_header_speed", True):
                parts.append(f"UE NAV | {_format_speed(prefs)}")
            if getattr(prefs, "show_header_tutorial", True):
                parts.append(_controls_short(prefs))
            text = " | ".join(parts)
            if not text:
                return

        font_id = 0
        size = int(_clamp(getattr(prefs, "hud_scale", 11), 8, 24))
        opacity = float(_clamp(getattr(prefs, "hud_opacity", 0.72), 0.10, 1.0))
        margin = 14.0
        top_margin = 34.0
        try:
            try:
                blf.size(font_id, size)
            except TypeError:
                blf.size(font_id, size, 72)
            try:
                blf.color(font_id, 1.0, 1.0, 1.0, opacity)
            except (AttributeError, TypeError):
                pass
            width, height = blf.dimensions(font_id, text)

            if position in {"TOP_LEFT", "TOP_RIGHT"}:
                y = max(margin, float(region.height) - height - top_margin)
            else:
                y = margin

            if position in {"TOP_LEFT", "BOTTOM_LEFT"}:
                x = margin
            elif position in {"TOP_RIGHT", "BOTTOM_RIGHT"}:
                x = max(margin, float(region.width) - width - margin)
            else:  # BOTTOM_CENTER and SPLIT
                x = max(margin, (float(region.width) - width) * 0.5)

            blf.position(font_id, x, y, 0.0)
            blf.draw(font_id, text)
        except (AttributeError, RuntimeError, TypeError, ValueError):
            pass

    def _finish(self, context):
        self._cleanup(context)
        return {"FINISHED"}

    def _cleanup(self, _context):
        if self._timer is not None and self._window_manager is not None:
            try:
                self._window_manager.event_timer_remove(self._timer)
            except (ReferenceError, RuntimeError):
                pass
            self._timer = None

        self._remove_draw_handler()

        if self._area is not None:
            try:
                self._area.header_text_set(None)
                self._area.tag_redraw()
            except (ReferenceError, RuntimeError):
                pass

        if self._rv3d is not None and self._old_lock_rotation:
            try:
                self._rv3d.lock_rotation = True
            except (ReferenceError, RuntimeError):
                pass

        if self._window is not None:
            if self._cursor_hidden:
                try:
                    self._window.cursor_modal_restore()
                except (AttributeError, ReferenceError, RuntimeError):
                    pass
                self._cursor_hidden = False

            if self._navigation_active and self._preferences is not None and self._preferences.restore_cursor_position:
                try:
                    self._window.cursor_warp(*self._initial_mouse)
                except (AttributeError, ReferenceError, RuntimeError):
                    pass

        self._navigation_active = False
        self._camera_object = None
        self._action_keys = None
        if self._velocity is not None:
            self._velocity.zero()

        if self._pressed is not None:
            self._pressed.clear()
        if self._active_move_keys is not None:
            self._active_move_keys.clear()
        if self._active_nav_keys is not None:
            self._active_nav_keys.clear()
