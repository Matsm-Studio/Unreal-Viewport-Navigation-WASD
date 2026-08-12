# SPDX-License-Identifier: GPL-3.0-or-later
"""Blender add-on preferences, presets and diagnostics operators."""

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, FloatVectorProperty, IntProperty, StringProperty
from bpy.types import AddonPreferences, Operator

from .shared import (
    _CROSSHAIR_STYLE_ITEMS, _HOLD_KEY_ITEMS,
    _HUD_POSITION_ITEMS, _ISSUES_URL, _KEYBOARD_KEY_ITEMS, _LANGUAGE_ITEMS,
    _MODIFIER_ITEMS, _MOUSE_BUTTON_ITEMS, _MOVEMENT_MODE_ITEMS,
    _NAVIGATION_KEYS_ITEMS, _NAVIGATION_PRESET_ITEMS, _PROJECT_URL,
    _SPEED_KEY_ITEMS, _SPEED_UNIT_ITEMS,
    _enum_items_for_property, _enum_label, _header_text, _key_label,
    _movement_keys_label, _orbit_shortcut, _shortcut_label, _tr, _update_speed_unit,
)

_APPLYING_PRESET = False


def _enum_picker_items(self, context):
    try:
        prefs = context.preferences.addons[__package__].preferences
    except (AttributeError, KeyError):
        prefs = None
    return _enum_items_for_property(prefs, getattr(self, "setting", ""))


class UVN155_OT_choose_enum(Operator):
    """Language-aware selector for preference enum values."""

    bl_idname = "preferences.uvn155_choose_enum"
    bl_label = "Choose Setting"
    bl_property = "value"
    bl_options = {"INTERNAL"}

    setting: StringProperty(options={"HIDDEN", "SKIP_SAVE"})
    value: EnumProperty(items=_enum_picker_items, options={"SKIP_SAVE"})

    def invoke(self, context, _event):
        try:
            prefs = context.preferences.addons[__package__].preferences
            current = str(getattr(prefs, self.setting))
            identifiers = {item[0] for item in _enum_items_for_property(prefs, self.setting)}
            if current in identifiers:
                self.value = current
        except (AttributeError, KeyError, TypeError, ValueError):
            pass
        context.window_manager.invoke_search_popup(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        try:
            prefs = context.preferences.addons[__package__].preferences
            if self.setting not in {
                "ui_language", "navigation_preset", "navigation_mouse", "navigation_modifier", "navigation_keys",
                "move_forward_key", "move_backward_key", "move_left_key", "move_right_key",
                "move_up_key", "move_down_key", "sprint_key", "precision_key",
                "speed_up_key", "speed_down_key", "speed_unit", "movement_mode",
                "orbit_mouse", "orbit_modifier",
                "crosshair_style", "info_position",
            }:
                return {"CANCELLED"}
            setattr(prefs, self.setting, self.value)
        except (AttributeError, KeyError, TypeError, ValueError):
            return {"CANCELLED"}
        return {"FINISHED"}


def _draw_enum_picker(layout, prefs, property_name, label_key, *, enabled=True):
    row = layout.row(align=True)
    row.enabled = enabled
    row.label(text=_tr(prefs, label_key))
    op = row.operator(
        UVN155_OT_choose_enum.bl_idname,
        text=_enum_label(prefs, property_name, getattr(prefs, property_name)),
        icon="DOWNARROW_HLT",
    )
    op.setting = property_name
    return row


def _draw_foldout_header(layout, prefs, property_name, label_key, icon):
    """Draw a compact Blender-style disclosure header and return its open state."""
    box = layout.box()
    is_open = bool(getattr(prefs, property_name))
    row = box.row(align=True)
    row.prop(
        prefs, property_name,
        text=_tr(prefs, label_key),
        icon="TRIA_DOWN" if is_open else "TRIA_RIGHT",
        emboss=False,
    )
    row.label(text="", icon=icon)
    return box, is_open

# Every profile sets shortcuts and motion explicitly. Values are intentionally
# complete enough that changing a profile produces a visible, predictable result.
_PRESET_VALUES = {
    "UNREAL": {
        "navigation_mouse": "RIGHTMOUSE", "navigation_modifier": "NONE", "navigation_keys": "WASD",
        "move_forward_key": "W", "move_backward_key": "S", "move_left_key": "A", "move_right_key": "D", "move_up_key": "E", "move_down_key": "Q",
        "sprint_key": "SHIFT", "precision_key": "CTRL", "speed_up_key": "WHEELUPMOUSE", "speed_down_key": "WHEELDOWNMOUSE",
        "movement_mode": "FREE", "look_sensitivity_ui": 2.20, "smooth_motion": True, "instant_stop": True, "acceleration_time": 0.18, "deceleration_time": 0.07,
        "update_rate": 120, "sprint_multiplier": 4.0, "precision_multiplier": 0.25, "invert_y": False, "force_perspective": True,
        "camera_view_navigation": True,
        "enable_orbit_selection": True, "orbit_mouse": "RIGHTMOUSE", "orbit_modifier": "ALT", "protect_camera_orbit": True,
    },
    "BLENDER": {
        "navigation_mouse": "MIDDLEMOUSE", "navigation_modifier": "NONE", "navigation_keys": "BOTH",
        "move_forward_key": "W", "move_backward_key": "S", "move_left_key": "A", "move_right_key": "D", "move_up_key": "E", "move_down_key": "Q",
        "sprint_key": "SHIFT", "precision_key": "CTRL", "speed_up_key": "WHEELUPMOUSE", "speed_down_key": "WHEELDOWNMOUSE",
        "movement_mode": "LEVEL", "look_sensitivity_ui": 1.65, "smooth_motion": False, "instant_stop": True, "acceleration_time": 0.06, "deceleration_time": 0.04,
        "update_rate": 60, "sprint_multiplier": 3.0, "precision_multiplier": 0.20, "invert_y": False, "force_perspective": False,
        "camera_view_navigation": False,
        "enable_orbit_selection": False, "orbit_mouse": "RIGHTMOUSE", "orbit_modifier": "ALT", "protect_camera_orbit": True,
    },
    "MAYA": {
        "navigation_mouse": "MIDDLEMOUSE", "navigation_modifier": "ALT", "navigation_keys": "CUSTOM",
        "move_forward_key": "UP_ARROW", "move_backward_key": "DOWN_ARROW", "move_left_key": "LEFT_ARROW", "move_right_key": "RIGHT_ARROW", "move_up_key": "E", "move_down_key": "Q",
        "sprint_key": "SHIFT", "precision_key": "CTRL", "speed_up_key": "WHEELUPMOUSE", "speed_down_key": "WHEELDOWNMOUSE",
        "movement_mode": "LEVEL", "look_sensitivity_ui": 1.35, "smooth_motion": True, "instant_stop": True, "acceleration_time": 0.22, "deceleration_time": 0.14,
        "update_rate": 90, "sprint_multiplier": 3.0, "precision_multiplier": 0.18, "invert_y": False, "force_perspective": True,
        "camera_view_navigation": True,
        "enable_orbit_selection": True, "orbit_mouse": "RIGHTMOUSE", "orbit_modifier": "ALT", "protect_camera_orbit": True,
    },
    "UNITY": {
        "navigation_mouse": "RIGHTMOUSE", "navigation_modifier": "NONE", "navigation_keys": "WASD",
        "move_forward_key": "W", "move_backward_key": "S", "move_left_key": "A", "move_right_key": "D", "move_up_key": "E", "move_down_key": "Q",
        "sprint_key": "SHIFT", "precision_key": "CTRL", "speed_up_key": "WHEELUPMOUSE", "speed_down_key": "WHEELDOWNMOUSE",
        "movement_mode": "FREE", "look_sensitivity_ui": 2.00, "smooth_motion": True, "instant_stop": True, "acceleration_time": 0.12, "deceleration_time": 0.06,
        "update_rate": 120, "sprint_multiplier": 5.0, "precision_multiplier": 0.20, "invert_y": False, "force_perspective": True,
        "camera_view_navigation": True,
        "enable_orbit_selection": True, "orbit_mouse": "RIGHTMOUSE", "orbit_modifier": "ALT", "protect_camera_orbit": True,
    },
    "GODOT": {
        "navigation_mouse": "RIGHTMOUSE", "navigation_modifier": "NONE", "navigation_keys": "WASD",
        "move_forward_key": "W", "move_backward_key": "S", "move_left_key": "A", "move_right_key": "D", "move_up_key": "E", "move_down_key": "Q",
        "sprint_key": "SHIFT", "precision_key": "CTRL", "speed_up_key": "WHEELUPMOUSE", "speed_down_key": "WHEELDOWNMOUSE",
        "movement_mode": "LEVEL", "look_sensitivity_ui": 1.85, "smooth_motion": True, "instant_stop": True, "acceleration_time": 0.16, "deceleration_time": 0.09,
        "update_rate": 90, "sprint_multiplier": 4.0, "precision_multiplier": 0.25, "invert_y": False, "force_perspective": True,
        "camera_view_navigation": True,
        "enable_orbit_selection": True, "orbit_mouse": "RIGHTMOUSE", "orbit_modifier": "ALT", "protect_camera_orbit": True,
    },
}


def _refresh_keymaps_safe():
    try:
        from .keymaps import refresh_keymaps
        refresh_keymaps()
    except (ImportError, AttributeError, RuntimeError, ReferenceError):
        pass


def _shortcut_changed(self, _context):
    global _APPLYING_PRESET
    if _APPLYING_PRESET:
        return
    try:
        self.key_conflict_summary = ""
        self.key_conflict_details = ""
        self.key_conflict_count = 0
    except (AttributeError, TypeError):
        pass
    if getattr(self, "navigation_preset", "CUSTOM") != "CUSTOM":
        try:
            self.navigation_preset = "CUSTOM"
        except (AttributeError, TypeError, ValueError):
            pass
    _refresh_keymaps_safe()


def _setting_changed(self, _context):
    global _APPLYING_PRESET
    if _APPLYING_PRESET:
        return
    if getattr(self, "navigation_preset", "CUSTOM") != "CUSTOM":
        try:
            self.navigation_preset = "CUSTOM"
        except (AttributeError, TypeError, ValueError):
            pass


def _apply_navigation_preset(self, _context):
    global _APPLYING_PRESET
    preset = getattr(self, "navigation_preset", "CUSTOM")
    values = _PRESET_VALUES.get(preset)
    if values is None:
        return
    _APPLYING_PRESET = True
    try:
        for name, value in values.items():
            try:
                setattr(self, name, value)
            except (AttributeError, TypeError, ValueError):
                pass
        self.key_conflict_summary = ""
        self.key_conflict_details = ""
        self.key_conflict_count = 0
    finally:
        _APPLYING_PRESET = False
    _refresh_keymaps_safe()


class UVN155_OT_save_preferences(Operator):
    bl_idname = "uvn155.save_preferences"
    bl_label = "Save on Disk"
    bl_description = "Save Blender preferences, including this extension's settings"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        try: prefs = context.preferences.addons[__package__].preferences
        except (AttributeError, KeyError): prefs = None
        try:
            bpy.ops.wm.save_userpref()
        except (RuntimeError, TypeError) as exc:
            self.report({"ERROR"}, _tr(prefs, "preferences_save_failed", error=exc))
            return {"CANCELLED"}
        self.report({"INFO"}, _tr(prefs, "preferences_saved"))
        return {"FINISHED"}


class UVN155_OT_reset_preferences(Operator):
    bl_idname = "uvn155.reset_preferences"
    bl_label = "Reset to Defaults"
    bl_description = "Restore all Unreal Viewport Navigation settings to defaults"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        try: prefs = context.preferences.addons[__package__].preferences
        except (AttributeError, KeyError):
            self.report({"ERROR"}, _tr(None, "error_prefs")); return {"CANCELLED"}
        global _APPLYING_PRESET
        _APPLYING_PRESET = True
        try:
            for prop in prefs.bl_rna.properties:
                if prop.identifier == "rna_type" or prop.is_readonly: continue
                try: prefs.property_unset(prop.identifier)
                except (AttributeError, TypeError): pass
        finally:
            _APPLYING_PRESET = False
        _refresh_keymaps_safe()
        self.report({"INFO"}, _tr(prefs, "preferences_reset"))
        return {"FINISHED"}


_DEFAULT_KEY_VALUES = {
    "navigation_mouse": "RIGHTMOUSE",
    "navigation_modifier": "NONE",
    "navigation_keys": "WASD",
    "move_forward_key": "W",
    "move_backward_key": "S",
    "move_left_key": "A",
    "move_right_key": "D",
    "move_up_key": "E",
    "move_down_key": "Q",
    "sprint_key": "SHIFT",
    "precision_key": "CTRL",
    "speed_up_key": "WHEELUPMOUSE",
    "speed_down_key": "WHEELDOWNMOUSE",
    "orbit_mouse": "RIGHTMOUSE",
    "orbit_modifier": "ALT",
}


class UVN155_OT_reset_default_keys(Operator):
    bl_idname = "uvn155.reset_default_keys"
    bl_label = "Restore Default Keys"
    bl_description = "Restore the default navigation shortcuts without changing other settings"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        try:
            prefs = context.preferences.addons[__package__].preferences
        except (AttributeError, KeyError):
            self.report({"ERROR"}, _tr(None, "error_prefs"))
            return {"CANCELLED"}
        global _APPLYING_PRESET
        _APPLYING_PRESET = True
        try:
            for name, value in _DEFAULT_KEY_VALUES.items():
                setattr(prefs, name, value)
            prefs.key_conflict_summary = ""
            prefs.key_conflict_details = ""
            prefs.key_conflict_count = 0
        finally:
            _APPLYING_PRESET = False
        _refresh_keymaps_safe()
        self.report({"INFO"}, _tr(prefs, "default_keys_restored"))
        return {"FINISHED"}


class UVN155_OT_check_key_conflicts(Operator):
    bl_idname = "uvn155.check_key_conflicts"
    bl_label = "Check Shortcut Conflicts"
    bl_description = "Check active Blender and add-on keymaps for shortcuts that overlap this add-on"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        try: prefs = context.preferences.addons[__package__].preferences
        except (AttributeError, KeyError):
            self.report({"ERROR"}, _tr(None, "error_prefs")); return {"CANCELLED"}
        from .keymaps import find_key_conflicts
        conflicts = find_key_conflicts(context, prefs)
        prefs.key_conflict_count = len(conflicts)
        prefs.key_conflict_details = "\n".join(conflicts[:40])
        prefs.key_conflict_summary = _tr(prefs, "conflicts_found", count=len(conflicts)) if conflicts else _tr(prefs, "conflicts_none")
        self.report({"WARNING"} if conflicts else {"INFO"}, prefs.key_conflict_summary)
        return {"FINISHED"}


class UVN155_AddonPreferences(AddonPreferences):
    bl_idname = __package__

    ui_language: EnumProperty(name="Interface Language", items=_LANGUAGE_ITEMS, default="EN")
    navigation_preset: EnumProperty(name="Navigation Preset", items=_NAVIGATION_PRESET_ITEMS, default="UNREAL", update=_apply_navigation_preset)

    navigation_mouse: EnumProperty(name="Navigation Mouse Button", items=_MOUSE_BUTTON_ITEMS, default="RIGHTMOUSE", update=_shortcut_changed)
    navigation_modifier: EnumProperty(name="Navigation Modifier", items=_MODIFIER_ITEMS, default="NONE", update=_shortcut_changed)
    navigation_keys: EnumProperty(name="Movement Layout", items=_NAVIGATION_KEYS_ITEMS, default="WASD", update=_shortcut_changed)
    move_forward_key: EnumProperty(name="Forward", items=_KEYBOARD_KEY_ITEMS, default="W", update=_shortcut_changed)
    move_backward_key: EnumProperty(name="Backward", items=_KEYBOARD_KEY_ITEMS, default="S", update=_shortcut_changed)
    move_left_key: EnumProperty(name="Left", items=_KEYBOARD_KEY_ITEMS, default="A", update=_shortcut_changed)
    move_right_key: EnumProperty(name="Right", items=_KEYBOARD_KEY_ITEMS, default="D", update=_shortcut_changed)
    move_up_key: EnumProperty(name="Up", items=_KEYBOARD_KEY_ITEMS, default="E", update=_shortcut_changed)
    move_down_key: EnumProperty(name="Down", items=_KEYBOARD_KEY_ITEMS, default="Q", update=_shortcut_changed)
    sprint_key: EnumProperty(
        name="Sprint Key",
        description="Hold while navigating to multiply movement speed by the Sprint Multiplier",
        items=_HOLD_KEY_ITEMS, default="SHIFT", update=_shortcut_changed,
    )
    precision_key: EnumProperty(
        name="Precision Key",
        description="Hold while navigating for slower, precise movement using the Precision Multiplier",
        items=_HOLD_KEY_ITEMS, default="CTRL", update=_shortcut_changed,
    )
    speed_up_key: EnumProperty(name="Increase Speed", items=_SPEED_KEY_ITEMS, default="WHEELUPMOUSE", update=_shortcut_changed)
    speed_down_key: EnumProperty(name="Decrease Speed", items=_SPEED_KEY_ITEMS, default="WHEELDOWNMOUSE", update=_shortcut_changed)

    navigate_during_tools: BoolProperty(name="Navigate While Using Compatible Tools", default=True, update=_setting_changed)
    enable_rmb_click_hold: BoolProperty(name="Separate Click from Hold", default=True, update=_setting_changed)
    rmb_hold_duration: FloatProperty(name="Hold Delay", default=0.09, min=0.03, max=0.30, soft_max=0.20, precision=2, subtype="TIME", update=_setting_changed)

    move_speed: FloatProperty(name="Movement Speed", default=5.0, min=1.0e-9, max=1.0e12, soft_min=0.01, soft_max=1000.0, precision=3, update=_setting_changed)
    minimum_speed: FloatProperty(name="Minimum Speed", default=0.05, min=1.0e-9, max=1.0e12, soft_max=100.0, precision=3, update=_setting_changed)
    maximum_speed: FloatProperty(name="Maximum Speed", default=500.0, min=1.0e-9, max=1.0e12, soft_max=100000.0, precision=3, update=_setting_changed)
    speed_unit: EnumProperty(name="Speed Unit", items=_SPEED_UNIT_ITEMS, default="BU_S", update=_update_speed_unit)
    speed_unit_previous: StringProperty(default="BU_S", options={"HIDDEN"})
    wheel_multiplier: FloatProperty(name="Speed Step", default=1.25, min=1.01, max=4.0, precision=2, update=_setting_changed)
    sprint_multiplier: FloatProperty(name="Sprint Multiplier", default=4.0, min=1.0, max=30.0, soft_max=10.0, precision=2, update=_setting_changed)
    precision_multiplier: FloatProperty(name="Precision Multiplier", default=0.25, min=0.01, max=1.0, precision=2, update=_setting_changed)
    look_sensitivity_ui: FloatProperty(name="Mouse Sensitivity", default=2.2, min=0.1, max=20.0, soft_min=0.5, soft_max=10.0, precision=2, update=_setting_changed)
    invert_y: BoolProperty(name="Invert Y Axis", default=False, update=_setting_changed)
    movement_mode: EnumProperty(name="Forward/Back Movement", items=_MOVEMENT_MODE_ITEMS, default="FREE", update=_setting_changed)

    smooth_motion: BoolProperty(name="Smooth Acceleration and Braking", default=True, update=_setting_changed)
    instant_stop: BoolProperty(name="Stop Immediately After Releasing Movement Keys", description="Prevent residual sliding when no movement direction is held", default=True, update=_setting_changed)
    acceleration_time: FloatProperty(name="Time to Full Speed", description="Approximate time for movement to reach 99% of target speed", default=0.12, min=0.01, max=1.50, soft_max=0.60, precision=2, subtype="TIME", update=_setting_changed)
    deceleration_time: FloatProperty(name="Braking Time", description="Approximate time for movement to stop after a movement key is released", default=0.07, min=0.01, max=1.00, soft_max=0.40, precision=2, subtype="TIME", update=_setting_changed)
    update_rate: IntProperty(name="Update Rate", default=120, min=30, max=240, subtype="UNSIGNED", update=_setting_changed)

    hide_cursor: BoolProperty(name="Hide System Cursor", default=True)
    restore_cursor_position: BoolProperty(name="Restore Cursor Position", default=True)
    force_perspective: BoolProperty(name="Switch to Perspective View", default=True, update=_setting_changed)

    camera_view_navigation: BoolProperty(name="Control Active Camera in Camera View", default=True, update=_setting_changed)
    enable_orbit_selection: BoolProperty(name="Orbit Around Selection", default=True, update=_shortcut_changed)
    orbit_mouse: EnumProperty(name="Orbit Mouse Button", items=_MOUSE_BUTTON_ITEMS, default="RIGHTMOUSE", update=_shortcut_changed)
    orbit_modifier: EnumProperty(name="Orbit Modifier", items=_MODIFIER_ITEMS, default="ALT", update=_shortcut_changed)
    protect_camera_orbit: BoolProperty(name="Protect Camera Frame", default=True, update=_shortcut_changed)

    show_crosshair: BoolProperty(name="Show Crosshair", default=False)
    crosshair_style: EnumProperty(name="Crosshair Style", items=_CROSSHAIR_STYLE_ITEMS, default="CROSS")
    crosshair_size: IntProperty(name="Crosshair Size", default=14, min=3, max=100, subtype="PIXEL")
    crosshair_gap: IntProperty(name="Center Gap", default=4, min=0, max=50, subtype="PIXEL")
    crosshair_thickness: FloatProperty(name="Line Thickness", default=1.5, min=1.0, max=10.0, precision=1)
    crosshair_color: FloatVectorProperty(name="Crosshair Color", subtype="COLOR", size=4, min=0.0, max=1.0, default=(1.0, 1.0, 1.0, 0.9))
    show_navigation_hud: BoolProperty(name="Show Navigation Information", default=True)
    hud_scale: IntProperty(name="HUD Text Size", default=11, min=8, max=24, subtype="PIXEL")
    hud_opacity: FloatProperty(name="HUD Opacity", default=0.72, min=0.10, max=1.0, subtype="FACTOR")
    info_position: EnumProperty(name="Information Position", items=_HUD_POSITION_ITEMS, default="HEADER")
    show_header_speed: BoolProperty(name="Show Speed", default=True)
    show_header_tutorial: BoolProperty(name="Show Control Hints", default=True)

    key_conflict_summary: StringProperty(default="", options={"HIDDEN"})
    key_conflict_details: StringProperty(default="", options={"HIDDEN"})
    key_conflict_count: IntProperty(default=0, options={"HIDDEN"})

    # Preferences use a small everyday view plus dedicated disclosure sections.
    # Key assignment has its own section so shortcuts are never mixed with motion
    # or speed tuning.
    ui_expand_controls: BoolProperty(default=True, options={"SKIP_SAVE"})
    ui_expand_keybindings: BoolProperty(default=False, options={"SKIP_SAVE"})
    ui_expand_speed: BoolProperty(default=False, options={"SKIP_SAVE"})
    ui_expand_camera: BoolProperty(default=False, options={"SKIP_SAVE"})
    ui_expand_motion: BoolProperty(default=False, options={"SKIP_SAVE"})
    ui_expand_display: BoolProperty(default=False, options={"SKIP_SAVE"})
    ui_expand_diagnostics: BoolProperty(default=False, options={"SKIP_SAVE"})

    def draw(self, _context):
        layout = self.layout
        prefs = self

        # LANGUAGE + PROGRAM PROFILE — both selectors deliberately use the
        # same compact picker so the two primary choices are visually obvious.
        setup = layout.box()
        setup.label(text=_tr(prefs, "quick_setup"), icon="PREFERENCES")
        _draw_enum_picker(setup, prefs, "ui_language", "language")
        _draw_enum_picker(setup, prefs, "navigation_preset", "navigation_preset")
        setup.label(text=_tr(prefs, "preset_help"), icon="INFO")

        quick = setup.column(align=True)
        quick.prop(self, "move_speed", text=_tr(prefs, "base_speed"))
        quick.prop(self, "look_sensitivity_ui", text=_tr(prefs, "look_sensitivity"), slider=True)

        status = setup.box()
        status.label(text=_tr(prefs, "current_controls"), icon="INFO")
        status.label(text=f"{_tr(prefs, 'navigate_action')}: {_shortcut_label(self.navigation_mouse, self.navigation_modifier)} + {_movement_keys_label(self)}")
        status.label(text=_tr(prefs, "sprint_role", button=_key_label(self.sprint_key), multiplier=f"{self.sprint_multiplier:g}"))
        status.label(text=_tr(prefs, "precision_role", button=_key_label(self.precision_key), multiplier=f"{self.precision_multiplier:g}"))
        if self.enable_orbit_selection:
            status.label(text=f"{_tr(prefs, 'orbit_shortcut_label')}: {_orbit_shortcut(self)}")

        # Always-visible actions requested for everyday use. They are outside
        # every foldout so they never disappear when advanced sections close.
        actions = layout.row(align=True)
        actions.scale_y = 1.15
        actions.operator(UVN155_OT_reset_default_keys.bl_idname, text=_tr(prefs, "restore_default_keys"), icon="LOOP_BACK")
        op = actions.operator("wm.url_open", text=_tr(prefs, "project_page"), icon="URL")
        op.url = _PROJECT_URL

        # NAVIGATION FEEL — behavior only. No key assignment is mixed in here.
        box, opened = _draw_foldout_header(layout, prefs, "ui_expand_controls", "navigation_section", "VIEW_PAN")
        if opened:
            col = box.column(align=True)
            col.label(text=_tr(prefs, "navigation_behavior_help"), icon="INFO")
            _draw_enum_picker(col, prefs, "movement_mode", "movement_mode")
            col.prop(self, "invert_y", text=_tr(prefs, "invert_y"))
            col.prop(self, "force_perspective", text=_tr(prefs, "force_perspective"))

        # KEY BINDINGS — every assignable shortcut lives in this one place.
        box, opened = _draw_foldout_header(layout, prefs, "ui_expand_keybindings", "key_bindings", "PREFERENCES")
        if opened:
            col = box.column(align=True)
            col.label(text=_tr(prefs, "key_bindings_help"), icon="INFO")

            trigger = col.box()
            trigger.label(text=_tr(prefs, "navigation_trigger"), icon="VIEW_PAN")
            _draw_enum_picker(trigger, prefs, "navigation_mouse", "navigation_mouse")
            _draw_enum_picker(trigger, prefs, "navigation_modifier", "navigation_modifier")
            trigger.label(text=_tr(prefs, "navigation_modifier_help"), icon="INFO")

            movement = col.box()
            movement.label(text=_tr(prefs, "movement_bindings"), icon="VIEW_PAN")
            _draw_enum_picker(movement, prefs, "navigation_keys", "navigation_keys")
            movement.label(text=_tr(prefs, "movement_layout_help"), icon="INFO")
            if self.navigation_keys == "CUSTOM":
                for prop, key in (
                    ("move_forward_key", "forward_key"), ("move_backward_key", "backward_key"),
                    ("move_left_key", "left_key"), ("move_right_key", "right_key"),
                    ("move_up_key", "up_key"), ("move_down_key", "down_key"),
                ):
                    _draw_enum_picker(movement, prefs, prop, key)
            else:
                movement.label(text=f"{_tr(prefs, 'current_layout')}: {_movement_keys_label(self)}", icon="INFO")

            modifiers = col.box()
            modifiers.label(text=_tr(prefs, "modifier_bindings"), icon="DRIVER_DISTANCE")
            _draw_enum_picker(modifiers, prefs, "sprint_key", "sprint_key")
            _draw_enum_picker(modifiers, prefs, "precision_key", "precision_key")

            speed_keys = col.box()
            speed_keys.label(text=_tr(prefs, "speed_bindings"), icon="DRIVER_DISTANCE")
            _draw_enum_picker(speed_keys, prefs, "speed_up_key", "speed_up_key")
            _draw_enum_picker(speed_keys, prefs, "speed_down_key", "speed_down_key")

            orbit_keys = col.box()
            orbit_keys.label(text=_tr(prefs, "orbit_bindings"), icon="ORIENTATION_VIEW")
            _draw_enum_picker(orbit_keys, prefs, "orbit_modifier", "orbit_modifier")
            _draw_enum_picker(orbit_keys, prefs, "orbit_mouse", "orbit_mouse")
            orbit_keys.label(text=f"{_tr(prefs, 'orbit_shortcut_label')}: {_orbit_shortcut(self)}", icon="INFO")
            orbit_keys.label(text=_tr(prefs, "orbit_shortcut_help"), icon="INFO")

        # SPEED — only speed behavior is here; shortcut assignment is above.
        box, opened = _draw_foldout_header(layout, prefs, "ui_expand_speed", "speed_section", "DRIVER_DISTANCE")
        if opened:
            col = box.column(align=True)
            sprint = col.box()
            sprint.label(text=_tr(prefs, "sprint_short"), icon="DRIVER_DISTANCE")
            sprint.prop(self, "sprint_multiplier", text=_tr(prefs, "sprint_multiplier"), slider=True)
            sprint.label(text=_tr(prefs, "uses_key", button=_key_label(self.sprint_key)), icon="INFO")

            precision = col.box()
            precision.label(text=_tr(prefs, "precision_short"), icon="DRIVER_DISTANCE")
            precision.prop(self, "precision_multiplier", text=_tr(prefs, "precision_multiplier"), slider=True)
            precision.label(text=_tr(prefs, "uses_key", button=_key_label(self.precision_key)), icon="INFO")

            col.separator()
            col.prop(self, "wheel_multiplier", text=_tr(prefs, "wheel_multiplier"))

        # MOTION — advanced feel tuning; hidden until needed.
        box, opened = _draw_foldout_header(layout, prefs, "ui_expand_motion", "motion", "IPO_EASE_IN_OUT")
        if opened:
            col = box.column(align=True)
            col.label(text=_tr(prefs, "motion_help"), icon="INFO")
            col.prop(self, "smooth_motion", text=_tr(prefs, "smooth_motion"))
            motion = col.column(align=True)
            motion.enabled = self.smooth_motion
            motion.prop(self, "acceleration_time", text=_tr(prefs, "acceleration_time"), slider=True)
            motion.prop(self, "deceleration_time", text=_tr(prefs, "deceleration_time"), slider=True)
            motion.prop(self, "instant_stop", text=_tr(prefs, "instant_stop"))
            col.separator()
            col.prop(self, "update_rate", text=_tr(prefs, "update_rate"))
            col.label(text=_tr(prefs, "motion_short_note"), icon="QUESTION")

        # CAMERA / ORBIT — behavior only. The actual orbit shortcut is edited in
        # the dedicated Key bindings section above.
        box, opened = _draw_foldout_header(layout, prefs, "ui_expand_camera", "camera_orbit", "CAMERA_DATA")
        if opened:
            col = box.column(align=True)
            col.label(text=_tr(prefs, "camera_help"), icon="INFO")
            col.prop(self, "camera_view_navigation", text=_tr(prefs, "camera_view_navigation"))
            col.prop(self, "enable_orbit_selection", text=_tr(prefs, "orbit_enable_short"))
            if self.enable_orbit_selection:
                orbit = col.box()
                orbit.label(text=f"{_tr(prefs, 'orbit_shortcut_label')}: {_orbit_shortcut(self)}", icon="ORIENTATION_VIEW")
                orbit.label(text=_tr(prefs, "edit_orbit_in_keys"), icon="INFO")
                orbit.prop(self, "protect_camera_orbit", text=_tr(prefs, "protect_camera_orbit"))
                orbit.label(text=_tr(prefs, "camera_orbit_protection_note"), icon="INFO")

        # DISPLAY — HUD, cursor and crosshair are visual-only options.
        box, opened = _draw_foldout_header(layout, prefs, "ui_expand_display", "display", "HIDE_OFF")
        if opened:
            col = box.column(align=True)
            col.label(text=_tr(prefs, "display_help"), icon="INFO")
            col.prop(self, "show_navigation_hud", text=_tr(prefs, "show_navigation_info"))
            info = col.column(align=True)
            info.enabled = self.show_navigation_hud
            _draw_enum_picker(info, prefs, "info_position", "info_position", enabled=self.show_navigation_hud)
            info.prop(self, "show_header_speed", text=_tr(prefs, "show_speed_info"))
            info.prop(self, "show_header_tutorial", text=_tr(prefs, "show_controls_info"))
            if self.info_position != "HEADER":
                info.prop(self, "hud_scale", text=_tr(prefs, "hud_scale"))
                info.prop(self, "hud_opacity", text=_tr(prefs, "hud_opacity"), slider=True)
            if self.info_position == "SPLIT":
                info.label(text=_tr(prefs, "split_info_note"), icon="INFO")

            col.separator()
            col.prop(self, "hide_cursor", text=_tr(prefs, "hide_cursor"))
            col.prop(self, "restore_cursor_position", text=_tr(prefs, "restore_cursor"))
            col.prop(self, "show_crosshair", text=_tr(prefs, "show_crosshair"))
            if self.show_crosshair:
                cross = col.box()
                _draw_enum_picker(cross, prefs, "crosshair_style", "crosshair_style")
                cross.prop(self, "crosshair_size", text=_tr(prefs, "crosshair_size"))
                cross.prop(self, "crosshair_gap", text=_tr(prefs, "crosshair_gap"))
                cross.prop(self, "crosshair_thickness", text=_tr(prefs, "crosshair_thickness"))
                cross.prop(self, "crosshair_color", text=_tr(prefs, "crosshair_color"))

        # ADVANCED — rare behavior, limits and maintenance tools stay tucked away.
        box, opened = _draw_foldout_header(layout, prefs, "ui_expand_diagnostics", "advanced_and_tools", "TOOL_SETTINGS")
        if opened:
            col = box.column(align=True)
            col.label(text=_tr(prefs, "advanced_help"), icon="INFO")
            col.prop(self, "navigate_during_tools", text=_tr(prefs, "navigate_during_tools"))
            col.prop(self, "enable_rmb_click_hold", text=_tr(prefs, "enable_rmb_click_hold"))
            hold = col.column(align=True)
            hold.enabled = self.enable_rmb_click_hold
            hold.prop(self, "rmb_hold_duration", text=_tr(prefs, "rmb_hold_duration"), slider=True)

            col.separator()
            _draw_enum_picker(col, prefs, "speed_unit", "speed_unit")
            col.prop(self, "minimum_speed", text=_tr(prefs, "minimum_speed"))
            col.prop(self, "maximum_speed", text=_tr(prefs, "maximum_speed"))

            col.separator()
            col.operator(UVN155_OT_check_key_conflicts.bl_idname, text=_tr(prefs, "check_conflicts"), icon="VIEWZOOM")
            col.label(text=self.key_conflict_summary or _tr(prefs, "conflicts_not_checked"))
            if self.key_conflict_details:
                for line in self.key_conflict_details.splitlines()[:4]:
                    col.label(text=line)

            col.separator()
            col.operator(UVN155_OT_save_preferences.bl_idname, text=_tr(prefs, "save_preferences"))
            col.operator(UVN155_OT_reset_preferences.bl_idname, text=_tr(prefs, "reset_preferences"), icon="LOOP_BACK")
            op = col.operator("wm.url_open", text=_tr(prefs, "report_issue"), icon="ERROR")
            op.url = _ISSUES_URL

        layout.label(text=_tr(prefs, "version"), icon="INFO")
