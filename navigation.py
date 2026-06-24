# SPDX-License-Identifier: GPL-3.0-or-later
"""Custom modal viewport navigation operator."""

import math
import time

import bpy
from bpy.types import Operator
from mathutils import Vector

try:
    import gpu
    from gpu_extras.batch import batch_for_shader
except ImportError:
    gpu = None
    batch_for_shader = None

from .shared import (
    _ARROW_MOVE_KEYS, _CTRL_KEYS, _SHIFT_KEYS, _VERTICAL_MOVE_KEYS, _WASD_MOVE_KEYS,
    _clamp, _header_text, _navigation_keys_mode, _speed_to_bu, _tr,
)

class VIEW3D_OT_uvn_navigate(Operator):
    """Custom Unreal-style mouse-look and flight navigation."""

    bl_idname = "view3d.uvn_navigate"
    bl_label = "Unreal Viewport Navigation"
    bl_description = "Hold RMB and use WASD or arrow keys with Q/E like an Unreal Engine viewport"
    bl_options = {"GRAB_CURSOR"}

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

    @classmethod
    def poll(cls, context):
        return context.area is not None and context.area.type == "VIEW_3D"

    def invoke(self, context, event):
        try:
            prefs = context.preferences.addons[__package__].preferences
        except (AttributeError, KeyError):
            self.report({"ERROR"}, _tr(None, "error_prefs"))
            return {"CANCELLED"}

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
        mode = _navigation_keys_mode(prefs)
        self._active_move_keys = set(_VERTICAL_MOVE_KEYS)
        if mode in {"WASD", "BOTH"}:
            self._active_move_keys.update(_WASD_MOVE_KEYS)
        if mode in {"ARROWS", "BOTH"}:
            self._active_move_keys.update(_ARROW_MOVE_KEYS)
        self._active_nav_keys = self._active_move_keys | _SHIFT_KEYS | _CTRL_KEYS
        self._velocity = Vector((0.0, 0.0, 0.0))
        self._last_tick = time.perf_counter()
        self._cursor_hidden = False
        self._initial_mouse = (event.mouse_x, event.mouse_y)
        self._crosshair_shader = None

        if event.shift:
            self._pressed.add("LEFT_SHIFT")
        if event.ctrl:
            self._pressed.add("LEFT_CTRL")

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

        hz = max(30, int(prefs.update_rate))
        self._timer = self._window_manager.event_timer_add(1.0 / hz, window=self._window)
        self._window_manager.modal_handler_add(self)
        self._update_header()
        self._area.tag_redraw()
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        try:
            if event.type == "RIGHTMOUSE" and event.value == "RELEASE":
                return self._finish(context)

            if event.type in {"ESC", "WINDOW_DEACTIVATE"}:
                return self._finish(context)

            if event.type in self._active_nav_keys:
                if event.value == "PRESS":
                    self._pressed.add(event.type)
                elif event.value == "RELEASE":
                    self._pressed.discard(event.type)
                return {"RUNNING_MODAL"}

            if event.type in {"WHEELUPMOUSE", "WHEELINMOUSE"} and event.value == "PRESS":
                self._adjust_speed(True)
                return {"RUNNING_MODAL"}
            if event.type in {"WHEELDOWNMOUSE", "WHEELOUTMOUSE"} and event.value == "PRESS":
                self._adjust_speed(False)
                return {"RUNNING_MODAL"}

            if event.type in {"MOUSEMOVE", "INBETWEEN_MOUSEMOVE"}:
                dx = event.mouse_x - event.mouse_prev_x
                dy = event.mouse_y - event.mouse_prev_y

                # GRAB_CURSOR can wrap at a window edge. Convert a wrap jump
                # back into the small physical movement that caused it.
                if self._region is not None:
                    width = max(1, int(self._region.width))
                    height = max(1, int(self._region.height))
                    if abs(dx) > width * 0.5:
                        dx -= math.copysign(width, dx)
                    if abs(dy) > height * 0.5:
                        dy -= math.copysign(height, dy)

                dx = _clamp(dx, -250.0, 250.0)
                dy = _clamp(dy, -250.0, 250.0)
                if dx or dy:
                    self._apply_mouse_look(dx, dy)
                return {"RUNNING_MODAL"}

            if event.type == "TIMER":
                event_timer = getattr(event, "timer", None)
                if event_timer is None or event_timer == self._timer:
                    self._tick_motion()
                    return {"RUNNING_MODAL"}
                if self._preferences.navigate_during_tools:
                    return {"PASS_THROUGH"}
                return {"RUNNING_MODAL"}

            if self._preferences.navigate_during_tools:
                return {"PASS_THROUGH"}
            return {"RUNNING_MODAL"}

        except (ReferenceError, RuntimeError) as exc:
            self.report({"WARNING"}, _tr(self._preferences, "stopped", error=exc))
            return self._finish(context)

    def cancel(self, context):
        self._cleanup(context)

    def _read_angles_from_view(self):
        forward = self._rv3d.view_rotation @ Vector((0.0, 0.0, -1.0))
        if forward.length_squared < 1.0e-12:
            forward = Vector((0.0, 1.0, 0.0))
        else:
            forward.normalize()
        self._yaw = math.atan2(forward.y, forward.x)
        self._pitch = math.asin(_clamp(forward.z, -1.0, 1.0))

    def _apply_mouse_look(self, dx, dy):
        prefs = self._preferences
        sensitivity = float(prefs.look_sensitivity)

        self._yaw -= dx * sensitivity
        y_sign = -1.0 if prefs.invert_y else 1.0
        self._pitch += dy * sensitivity * y_sign
        self._pitch = _clamp(self._pitch, math.radians(-89.5), math.radians(89.5))
        self._yaw = (self._yaw + math.pi) % (2.0 * math.pi) - math.pi

        old_rotation = self._rv3d.view_rotation.copy()
        distance = float(self._rv3d.view_distance)
        eye_position = self._rv3d.view_location + old_rotation @ Vector((0.0, 0.0, distance))

        cp = math.cos(self._pitch)
        forward = Vector((
            cp * math.cos(self._yaw),
            cp * math.sin(self._yaw),
            math.sin(self._pitch),
        ))
        new_rotation = forward.to_track_quat("-Z", "Y")

        self._rv3d.view_rotation = new_rotation
        self._rv3d.view_location = eye_position - new_rotation @ Vector((0.0, 0.0, distance))
        self._area.tag_redraw()

    def _movement_direction(self):
        direction = Vector((0.0, 0.0, 0.0))
        rotation = self._rv3d.view_rotation

        if self._preferences.movement_mode == "LEVEL":
            forward = Vector((math.cos(self._yaw), math.sin(self._yaw), 0.0))
            right = Vector((-math.sin(self._yaw), math.cos(self._yaw), 0.0))
        else:
            forward = rotation @ Vector((0.0, 0.0, -1.0))
            right = rotation @ Vector((1.0, 0.0, 0.0))
            if forward.length_squared > 1.0e-12:
                forward.normalize()
            if right.length_squared > 1.0e-12:
                right.normalize()

        world_up = Vector((0.0, 0.0, 1.0))

        if "W" in self._pressed or "UP_ARROW" in self._pressed:
            direction += forward
        if "S" in self._pressed or "DOWN_ARROW" in self._pressed:
            direction -= forward
        if "D" in self._pressed or "RIGHT_ARROW" in self._pressed:
            direction += right
        if "A" in self._pressed or "LEFT_ARROW" in self._pressed:
            direction -= right
        if "E" in self._pressed:
            direction += world_up
        if "Q" in self._pressed:
            direction -= world_up

        if direction.length_squared > 1.0e-12:
            direction.normalize()
        return direction

    def _tick_motion(self):
        now = time.perf_counter()
        dt = _clamp(now - self._last_tick, 0.0001, 0.05)
        self._last_tick = now

        prefs = self._preferences
        direction = self._movement_direction()
        multiplier = 1.0
        if self._pressed.intersection(_SHIFT_KEYS):
            multiplier *= float(prefs.sprint_multiplier)
        if self._pressed.intersection(_CTRL_KEYS):
            multiplier *= float(prefs.precision_multiplier)

        base_speed_bu = _speed_to_bu(float(prefs.move_speed), prefs.speed_unit, bpy.context)
        target_velocity = direction * base_speed_bu * multiplier

        if prefs.smooth_motion:
            response = float(prefs.acceleration) if direction.length_squared > 1.0e-12 else float(prefs.deceleration)
            alpha = 1.0 - math.exp(-max(0.01, response) * dt)
            self._velocity = self._velocity.lerp(target_velocity, alpha)
        else:
            self._velocity = target_velocity

        if self._velocity.length_squared < 1.0e-10:
            self._velocity.zero()
            return

        self._rv3d.view_location = self._rv3d.view_location + self._velocity * dt
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
        self._area.header_text_set(_header_text(self._preferences))

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
        if prefs is None or not prefs.show_crosshair or gpu is None or batch_for_shader is None:
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

            if self._preferences is not None and self._preferences.restore_cursor_position:
                try:
                    self._window.cursor_warp(*self._initial_mouse)
                except (AttributeError, ReferenceError, RuntimeError):
                    pass

        if self._pressed is not None:
            self._pressed.clear()
        if self._active_move_keys is not None:
            self._active_move_keys.clear()
        if self._active_nav_keys is not None:
            self._active_nav_keys.clear()
