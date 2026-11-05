# SPDX-License-Identifier: GPL-3.0-or-later
"""Blender add-on preferences, presets and diagnostics operators."""

import bpy
import traceback
from contextlib import contextmanager
from bpy.props import BoolProperty, EnumProperty, FloatProperty, FloatVectorProperty, IntProperty, StringProperty
from bpy.types import AddonPreferences, Operator

from .shared import (
    _CROSSHAIR_STYLE_ITEMS, _HOLD_KEY_ITEMS,
    _HUD_POSITION_ITEMS, _ISSUES_URL, _KEYBOARD_KEY_ITEMS, _LANGUAGE_ITEMS,
    _MODIFIER_ITEMS, _MOUSE_BUTTON_ITEMS, _MOVEMENT_MODE_ITEMS,
    _NAVIGATION_KEYS_ITEMS, _NAVIGATION_PRESET_ITEMS, _PROJECT_URL,
    _SPEED_KEY_ITEMS, _SPEED_UNIT_ITEMS, _ORBIT_CENTER_KEY_ITEMS, _ORBIT_CENTER_MODIFIER_ITEMS,
    _enum_items_for_property, _enum_label, _header_text, _key_label,
    _movement_action_map, _movement_keys_label, _orbit_shortcut, _orbit_center_shortcut,
    _shortcut_label, _tr, _update_speed_unit,
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
                "orbit_mouse", "orbit_modifier", "orbit_center_key", "orbit_center_modifier", "editor_shortcut_profile",
                "crosshair_style", "info_position",
            }:
                return {"CANCELLED"}
            setattr(prefs, self.setting, self.value)
        except (AttributeError, KeyError, TypeError, ValueError):
            return {"CANCELLED"}
        return {"FINISHED"}


def _draw_enum_picker(layout, prefs, property_name, label_key, *, enabled=True):
    """Use Blender's native enum widget (stable across reloads and versions).

    The old modal search-popup added an extra operator dependency to every
    drop-down, so it could leave the preferences unusable after an update.
    """
    row = layout.row(align=True)
    row.enabled = enabled
    row.prop(prefs, property_name, text=_tr(prefs, label_key))
    return row


@contextmanager
def _ui_group_guard(layout, label):
    """An error in ONE section must never hide the rest of the preferences.

    Show the actual exception name/message on screen, and the full traceback
    in Blender's console so UI regressions are immediately diagnosable.
    """
    try:
        yield
    except Exception as exc:
        print(f"[Unreal Viewport Navigation 1.6.5] Preferences/{label}:")
        traceback.print_exc()
        error_box = layout.box()
        error_box.label(text=f"{label}: {type(exc).__name__}", icon="ERROR")
        error_box.label(text=str(exc)[:180] or "See Blender system console", icon="INFO")


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

def _control_reference_key_list(values):
    """Format active keys consistently for custom / WASD / arrow / BOTH layouts."""
    priority = {name: i for i, name in enumerate((
        "W", "A", "S", "D", "Q", "E", "UP_ARROW", "DOWN_ARROW",
        "LEFT_ARROW", "RIGHT_ARROW",
    ))}
    arrows = {
        "UP_ARROW": "↑", "DOWN_ARROW": "↓",
        "LEFT_ARROW": "←", "RIGHT_ARROW": "→",
    }
    return ", ".join(
        arrows.get(key, _key_label(key))
        for key in sorted(values, key=lambda k: (priority.get(k, 99), k))
    )


def _control_reference_sections(prefs):
    """Live shortcut guide; never show hardcoded keys that disagree with settings.

    Returns ordered (title key, icon, rows, note) groups; safe to call outside
    Blender's drawing context and test without UI dependencies.
    """
    move = _movement_action_map(prefs)

    def pair(first, second):
        return f"{_control_reference_key_list(move[first])} / {_control_reference_key_list(move[second])}"

    nav = [
        (_shortcut_label(prefs.navigation_mouse, prefs.navigation_modifier), "guide_look"),
        (pair("forward", "backward"), "guide_forward_back"),
        (pair("left", "right"), "guide_left_right"),
        (pair("up", "down"), "guide_up_down"),
    ]
    for prop, desc in (
        ("sprint_key", "guide_sprint"),
        ("precision_key", "guide_precision"),
        ("speed_up_key", "guide_speed_up"),
        ("speed_down_key", "guide_speed_down"),
    ):
        key = getattr(prefs, prop, "NONE")
        if key != "NONE":
            nav.append((_key_label(key), desc))
    nav.append((_key_label(prefs.navigation_mouse), "guide_finish_nav"))
    nav.append(("Esc", "guide_cancel_nav"))
    sections = [("guide_navigation", "VIEW_PAN", nav, "guide_nav_note")]

    orbit = []
    if prefs.enable_orbit_selection:
        orbit.append((_orbit_shortcut(prefs), "guide_orbit_action"))
        orbit.append((_key_label(prefs.orbit_center_key), "guide_center_during"))
        orbit.append((_key_label(prefs.orbit_mouse), "guide_finish_orbit"))
        orbit.append(("Esc", "guide_cancel_orbit"))
        if prefs.orbit_wheel_zoom:
            orbit.append((_key_label("WHEELUPMOUSE"), "guide_orbit_zoom_in"))
            orbit.append((_key_label("WHEELDOWNMOUSE"), "guide_orbit_zoom_out"))
    if prefs.orbit_center_shortcut_enabled:
        orbit.append((_orbit_center_shortcut(prefs), "guide_center_viewport"))
    note = "guide_orbit_note" if prefs.enable_orbit_selection else "guide_orbit_disabled"
    sections.append(("guide_orbit", "ORIENTATION_VIEW", orbit, note))

    editor = []
    if prefs.enable_editor_shortcuts:
        from .editor_actions import editor_shortcut_specs
        for key, modifiers, action in editor_shortcut_specs(prefs):
            label = "+".join([*(_key_label(mod) for mod in modifiers), _key_label(key)])
            editor.append((label, "guide_editor_" + action.lower()))
    sections.append((
        "guide_editor", "TOOL_SETTINGS", editor,
        "guide_editor_note" if prefs.enable_editor_shortcuts else "guide_editor_disabled",
    ))
    return sections


def _draw_control_reference(layout, prefs):
    """An expandable, concise table of the controls actually configured."""
    layout.label(text=_tr(prefs, "guide_intro"), icon="INFO")
    for title, icon, rows, note in _control_reference_sections(prefs):
        group = layout.box()
        group.label(text=_tr(prefs, title), icon=icon)
        for shortcut, description_key in rows:
            # Split keeps shortcuts in their own aligned column, readable in
            # narrow Blender add-on preferences and without relying on HTML.
            columns = group.split(factor=0.38, align=True)
            columns.label(text=shortcut)
            columns.label(text=_tr(prefs, description_key))
        group.label(text=_tr(prefs, note), icon="INFO")
    layout.label(text=_tr(prefs, "guide_footer"), icon="PREFERENCES")


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


def _editor_shortcuts_changed(self, _context):
    # The editor shortcut layer is independent from motion/navigation presets.
    try:
        self.key_conflict_summary = ""
        self.key_conflict_details = ""
        self.key_conflict_count = 0
    except (AttributeError, TypeError):
        pass
    if not _APPLYING_PRESET:
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
    # Keep the original engine choice when later edits change the navigation
    # preset to CUSTOM. This only affects optional editor bindings.
    try:
        self.editor_shortcut_auto_last_profile = preset
    except (AttributeError, TypeError, ValueError):
        pass
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
    "orbit_center_key": "F",
    "orbit_center_modifier": "CTRL_ALT",
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


# Only real setting sections; keep the keyboard guide separate so that
# "Show All Settings" does not flood the screen with documentation.
_SETTING_SECTION_PROPERTIES = (
    "ui_expand_orbit", "ui_expand_controls", "ui_expand_keybindings",
    "ui_expand_editor_shortcuts", "ui_expand_speed", "ui_expand_motion", "ui_expand_camera",
    "ui_expand_display", "ui_expand_diagnostics",
)


class UVN155_OT_set_sections(Operator):
    """Expand or collapse all actual settings, without changing their values."""
    bl_idname = "uvn155.set_settings_sections"
    bl_label = "Expand / Collapse Settings"
    bl_options = {"INTERNAL"}

    expand: BoolProperty(name="Show All", default=True, options={"SKIP_SAVE"})

    def execute(self, context):
        try:
            prefs = context.preferences.addons[__package__].preferences
        except (AttributeError, KeyError):
            self.report({"WARNING"}, "Could not access the add-on settings")
            return {"CANCELLED"}
        for name in _SETTING_SECTION_PROPERTIES:
            setattr(prefs, name, self.expand)
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

    enable_editor_shortcuts: BoolProperty(
        name="Enable Engine Editor Shortcuts",
        description="Optional object-mode hotkeys for Blender's transform tools, focus, duplicate and engine-style viewport actions; disabled by default to protect existing Blender shortcuts",
        default=False, update=_editor_shortcuts_changed,
    )
    editor_shortcut_auto_last_profile: StringProperty(default="UNREAL", options={"HIDDEN"})
    editor_shortcut_profile: EnumProperty(
        name="Editor Shortcut Profile",
        description="Auto follows the selected navigation preset; Basic is used for Blender/Custom",
        items=(
            ("AUTO", "Follow Navigation Preset", "Use the same engine profile as navigation"),
            ("UNREAL", "Unreal Engine", "W/E/R, F, Ctrl+D and G clean view"),
            ("UNITY", "Unity", "Q/W/E/R, F, Ctrl+D and X for local/global"),
            ("GODOT", "Godot", "Q/W/E/R, F, Ctrl+D, T and Y"),
            ("MAYA", "Maya", "Q/W/E/R, F and Ctrl+D"),
            ("BASIC", "Basic", "W/E/R, F, Ctrl+D without extra engine actions"),
        ), default="AUTO", update=_editor_shortcuts_changed,
    )

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
    protect_camera_orbit: BoolProperty(name="Protect Camera Frame", default=True, update=_setting_changed)
    # New identifier deliberately ignores previous saved orbit_reverse_y
    # values. Users confirmed that enabling the OLD switch was necessary for
    # the expected camera movement, so make that direction the fresh default.
    orbit_invert_y: BoolProperty(
        name="Reverse Orbit Y",
        description="Off (default): mouse up moves the orbit camera up around the object; on: invert that direction",
        default=False,
    )
    orbit_auto_center: BoolProperty(
        name="Auto-center on Orbit Start",
        description="At the beginning of each orbit, move the selected target to the screen center without changing view angle or zoom",
        default=False,
    )
    orbit_center_shortcut_enabled: BoolProperty(
        name="Enable Center Shortcut",
        description="Bind a shortcut in the 3D Viewport for centering the selection even when not orbiting",
        default=True, update=_shortcut_changed,
    )
    orbit_center_key: EnumProperty(
        name="Orbit Center Key",
        description="Press this key during orbit; also used for the optional viewport-wide center shortcut",
        items=_ORBIT_CENTER_KEY_ITEMS, default="F", update=_shortcut_changed,
    )
    orbit_center_modifier: EnumProperty(
        name="Center Shortcut Modifiers",
        description="Modifier keys for centering from the 3D Viewport outside Orbit",
        items=_ORBIT_CENTER_MODIFIER_ITEMS, default="CTRL_ALT", update=_shortcut_changed,
    )
    orbit_separate_sensitivity: BoolProperty(
        name="Separate Alt Orbit Sensitivity",
        description="Use an independent sensitivity value; otherwise follow normal mouse sensitivity",
        default=False,
    )
    orbit_look_sensitivity_ui: FloatProperty(
        name="Alt Orbit Sensitivity", description="Used only when separate sensitivity is enabled",
        default=2.2, min=0.1, max=20.0, soft_min=0.5, soft_max=10.0, precision=2,
    )
    orbit_wheel_zoom: BoolProperty(
        name="Mouse Wheel Zoom During Alt Orbit", default=False,
    )
    orbit_zoom_strength: FloatProperty(
        name="Alt Orbit Zoom Strength", default=1.0,
        min=0.1, max=5.0, precision=2,
    )

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
    ui_expand_guide: BoolProperty(default=False, options={"SKIP_SAVE"})
    ui_expand_controls: BoolProperty(default=True, options={"SKIP_SAVE"})
    ui_expand_orbit: BoolProperty(default=False, options={"SKIP_SAVE"})
    ui_expand_keybindings: BoolProperty(default=False, options={"SKIP_SAVE"})
    ui_expand_editor_shortcuts: BoolProperty(default=False, options={"SKIP_SAVE"})
    ui_expand_speed: BoolProperty(default=False, options={"SKIP_SAVE"})
    ui_expand_camera: BoolProperty(default=False, options={"SKIP_SAVE"})
    ui_expand_motion: BoolProperty(default=False, options={"SKIP_SAVE"})
    ui_expand_display: BoolProperty(default=False, options={"SKIP_SAVE"})
    ui_expand_diagnostics: BoolProperty(default=False, options={"SKIP_SAVE"})

    def draw(self, _context):
        """Full, fault-isolated settings. Nothing silently disappears.

        Every editable setting has a native Blender property widget. Settings
        for disabled features remain visible but greyed out, so the user can
        find them and understand how to enable them.
        """
        prefs = self
        layout = self.layout

        with _ui_group_guard(layout, "Quick setup"):
            quick = layout.box()
            quick.label(text=_tr(prefs, "quick_setup"), icon="PREFERENCES")
            _draw_enum_picker(quick, prefs, "ui_language", "language")
            _draw_enum_picker(quick, prefs, "navigation_preset", "navigation_preset")
            quick.prop(prefs, "move_speed", text=_tr(prefs, "base_speed"))
            quick.prop(prefs, "look_sensitivity_ui", text=_tr(prefs, "look_sensitivity"), slider=True)
            quick.prop(prefs, "enable_orbit_selection", text=_tr(prefs, "orbit_enable_short"))

            summary = quick.box()
            summary.label(text=_tr(prefs, "current_controls"), icon="INFO")
            summary.label(text=f"{_tr(prefs, 'navigate_action')}: {_shortcut_label(prefs.navigation_mouse, prefs.navigation_modifier)} + {_movement_keys_label(prefs)}")
            if prefs.enable_orbit_selection:
                summary.label(text=f"{_tr(prefs, 'orbit_shortcut_label')}: {_orbit_shortcut(prefs)}")
            if prefs.orbit_center_shortcut_enabled:
                summary.label(text=f"{_tr(prefs, 'orbit_center_button')}: {_orbit_center_shortcut(prefs)}")

        with _ui_group_guard(layout, "Section controls"):
            bar = layout.box()
            bar.label(text=_tr(prefs, "all_settings_label"), icon="PREFERENCES")
            bar.label(text=_tr(prefs, "settings_scroll_hint"), icon="INFO")
            row = bar.row(align=True)
            op = row.operator(UVN155_OT_set_sections.bl_idname, text=_tr(prefs, "expand_settings"), icon="TRIA_DOWN")
            op.expand = True
            op = row.operator(UVN155_OT_set_sections.bl_idname, text=_tr(prefs, "collapse_settings"), icon="TRIA_RIGHT")
            op.expand = False

        with _ui_group_guard(layout, "Navigation"):
            box, opened = _draw_foldout_header(layout, prefs, "ui_expand_controls", "navigation_speed_section", "VIEW_PAN")
            if opened:
                col = box.column(align=True)
                _draw_enum_picker(col, prefs, "movement_mode", "movement_mode")
                col.prop(prefs, "invert_y", text=_tr(prefs, "invert_y"))
                col.prop(prefs, "navigate_during_tools", text=_tr(prefs, "navigate_during_tools"))
                col.prop(prefs, "force_perspective", text=_tr(prefs, "force_perspective"))
                col.label(text=f"{_tr(prefs, 'navigate_action')}: {_shortcut_label(prefs.navigation_mouse, prefs.navigation_modifier)}", icon="INFO")

        with _ui_group_guard(layout, "Orbit & centering"):
            box, opened = _draw_foldout_header(layout, prefs, "ui_expand_orbit", "orbit_controls_title", "ORIENTATION_VIEW")
            if opened:
                col = box.column(align=True)
                col.prop(prefs, "enable_orbit_selection", text=_tr(prefs, "orbit_enable_short"))
                orbit = col.column(align=True)
                orbit.enabled = prefs.enable_orbit_selection

                center = orbit.box()
                center.label(text=_tr(prefs, "orbit_pivot_title"), icon="VIEW_SELECTED")
                center.prop(prefs, "orbit_auto_center", text=_tr(prefs, "orbit_center_on_start"))
                center.label(text=_tr(prefs, "orbit_center_modal_hint", key=_key_label(prefs.orbit_center_key)), icon="INFO")

                direction = orbit.box()
                direction.label(text=_tr(prefs, "orbit_direction_title"), icon="ORIENTATION_VIEW")
                direction.prop(prefs, "orbit_invert_y", text=_tr(prefs, "orbit_invert_y"))
                direction.label(text=_tr(prefs, "orbit_y_inverts_eye" if prefs.orbit_invert_y else "orbit_y_matches_eye"), icon="INFO")
                direction.prop(prefs, "orbit_separate_sensitivity", text=_tr(prefs, "orbit_separate_sensitivity"))
                sensitivity = direction.column(align=True)
                sensitivity.enabled = prefs.orbit_separate_sensitivity
                sensitivity.prop(prefs, "orbit_look_sensitivity_ui", text=_tr(prefs, "orbit_sensitivity"), slider=True)

                zoom = orbit.box()
                zoom.prop(prefs, "orbit_wheel_zoom", text=_tr(prefs, "orbit_wheel_zoom"))
                zoom_strength = zoom.column(align=True)
                zoom_strength.enabled = prefs.orbit_wheel_zoom
                zoom_strength.prop(prefs, "orbit_zoom_strength", text=_tr(prefs, "orbit_zoom_strength"), slider=True)

        with _ui_group_guard(layout, "Keys"):
            box, opened = _draw_foldout_header(layout, prefs, "ui_expand_keybindings", "key_bindings", "PREFERENCES")
            if opened:
                col = box.column(align=True)
                nav = col.box()
                nav.label(text=_tr(prefs, "navigation_trigger"), icon="VIEW_PAN")
                _draw_enum_picker(nav, prefs, "navigation_mouse", "navigation_mouse")
                _draw_enum_picker(nav, prefs, "navigation_modifier", "navigation_modifier")

                movement = col.box()
                movement.label(text=_tr(prefs, "movement_bindings"), icon="PREFERENCES")
                _draw_enum_picker(movement, prefs, "navigation_keys", "navigation_keys")
                movement_custom = movement.column(align=True)
                movement_custom.enabled = prefs.navigation_keys == "CUSTOM"
                for prop, token in (
                    ("move_forward_key", "forward_key"),
                    ("move_backward_key", "backward_key"),
                    ("move_left_key", "left_key"),
                    ("move_right_key", "right_key"),
                    ("move_up_key", "up_key"),
                    ("move_down_key", "down_key"),
                ):
                    _draw_enum_picker(movement_custom, prefs, prop, token)
                movement.label(text=f"{_tr(prefs, 'current_layout')}: {_movement_keys_label(prefs)}", icon="INFO")

                modifiers = col.box()
                modifiers.label(text=_tr(prefs, "modifier_bindings"), icon="PREFERENCES")
                _draw_enum_picker(modifiers, prefs, "sprint_key", "sprint_key")
                _draw_enum_picker(modifiers, prefs, "precision_key", "precision_key")
                _draw_enum_picker(modifiers, prefs, "speed_up_key", "speed_up_key")
                _draw_enum_picker(modifiers, prefs, "speed_down_key", "speed_down_key")

                orbit_keys = col.box()
                orbit_keys.label(text=_tr(prefs, "orbit_controls_title"), icon="ORIENTATION_VIEW")
                _draw_enum_picker(orbit_keys, prefs, "orbit_mouse", "orbit_mouse")
                _draw_enum_picker(orbit_keys, prefs, "orbit_modifier", "orbit_modifier")
                _draw_enum_picker(orbit_keys, prefs, "orbit_center_key", "orbit_center_key")
                orbit_keys.prop(prefs, "orbit_center_shortcut_enabled", text=_tr(prefs, "orbit_center_shortcut_enabled"))
                _draw_enum_picker(orbit_keys, prefs, "orbit_center_modifier", "orbit_center_modifier", enabled=prefs.orbit_center_shortcut_enabled)
                orbit_keys.label(text=_tr(prefs, "center_shortcut_keys_note", key=_key_label(prefs.orbit_center_key), shortcut=_orbit_center_shortcut(prefs)), icon="INFO")

        with _ui_group_guard(layout, "Speed"):
            box, opened = _draw_foldout_header(layout, prefs, "ui_expand_speed", "speed_section", "DRIVER_DISTANCE")
            if opened:
                col = box.column(align=True)
                col.prop(prefs, "move_speed", text=_tr(prefs, "base_speed"))
                _draw_enum_picker(col, prefs, "speed_unit", "speed_unit")
                col.prop(prefs, "minimum_speed", text=_tr(prefs, "minimum_speed"))
                col.prop(prefs, "maximum_speed", text=_tr(prefs, "maximum_speed"))
                col.prop(prefs, "wheel_multiplier", text=_tr(prefs, "wheel_multiplier"))
                col.prop(prefs, "sprint_multiplier", text=_tr(prefs, "sprint_multiplier"), slider=True)
                col.prop(prefs, "precision_multiplier", text=_tr(prefs, "precision_multiplier"), slider=True)

        with _ui_group_guard(layout, "Motion"):
            box, opened = _draw_foldout_header(layout, prefs, "ui_expand_motion", "motion", "IPO_EASE_IN_OUT")
            if opened:
                col = box.column(align=True)
                col.prop(prefs, "smooth_motion", text=_tr(prefs, "smooth_motion"))
                easing = col.column(align=True)
                easing.enabled = prefs.smooth_motion
                easing.prop(prefs, "acceleration_time", text=_tr(prefs, "acceleration_time"), slider=True)
                easing.prop(prefs, "deceleration_time", text=_tr(prefs, "deceleration_time"), slider=True)
                col.prop(prefs, "instant_stop", text=_tr(prefs, "instant_stop"))
                col.prop(prefs, "update_rate", text=_tr(prefs, "update_rate"))

        with _ui_group_guard(layout, "Camera & cursor"):
            box, opened = _draw_foldout_header(layout, prefs, "ui_expand_camera", "camera_view_section", "CAMERA_DATA")
            if opened:
                col = box.column(align=True)
                col.prop(prefs, "camera_view_navigation", text=_tr(prefs, "camera_view_navigation"))
                col.prop(prefs, "protect_camera_orbit", text=_tr(prefs, "protect_camera_orbit"))
                col.prop(prefs, "force_perspective", text=_tr(prefs, "force_perspective"))
                col.prop(prefs, "hide_cursor", text=_tr(prefs, "hide_cursor"))
                restore = col.column(align=True)
                restore.enabled = prefs.hide_cursor
                restore.prop(prefs, "restore_cursor_position", text=_tr(prefs, "restore_cursor"))

        with _ui_group_guard(layout, "Display"):
            box, opened = _draw_foldout_header(layout, prefs, "ui_expand_display", "display", "HIDE_OFF")
            if opened:
                col = box.column(align=True)
                col.prop(prefs, "show_navigation_hud", text=_tr(prefs, "show_navigation_info"))
                hud = col.box()
                hud.enabled = prefs.show_navigation_hud
                _draw_enum_picker(hud, prefs, "info_position", "info_position")
                hud.prop(prefs, "show_header_speed", text=_tr(prefs, "show_speed_info"))
                hud.prop(prefs, "show_header_tutorial", text=_tr(prefs, "show_controls_info"))
                hud.prop(prefs, "hud_scale", text=_tr(prefs, "hud_scale"))
                hud.prop(prefs, "hud_opacity", text=_tr(prefs, "hud_opacity"), slider=True)

                col.prop(prefs, "show_crosshair", text=_tr(prefs, "show_crosshair"))
                cross = col.box()
                cross.enabled = prefs.show_crosshair
                _draw_enum_picker(cross, prefs, "crosshair_style", "crosshair_style")
                cross.prop(prefs, "crosshair_size", text=_tr(prefs, "crosshair_size"))
                cross.prop(prefs, "crosshair_gap", text=_tr(prefs, "crosshair_gap"))
                cross.prop(prefs, "crosshair_thickness", text=_tr(prefs, "crosshair_thickness"))
                cross.prop(prefs, "crosshair_color", text=_tr(prefs, "crosshair_color"))

        with _ui_group_guard(layout, "Editor hotkeys"):
            from .editor_actions import editor_shortcuts_summary, resolved_editor_profile
            box, opened = _draw_foldout_header(layout, prefs, "ui_expand_editor_shortcuts", "editor_shortcut_section", "TOOL_SETTINGS")
            if opened:
                col = box.column(align=True)
                col.prop(prefs, "enable_editor_shortcuts", text=_tr(prefs, "editor_shortcut_enable"))
                _draw_enum_picker(col, prefs, "editor_shortcut_profile", "editor_shortcut_profile")
                col.label(text=f"{_tr(prefs, 'editor_shortcut_active')}: {resolved_editor_profile(prefs)}")
                col.label(text=_tr(prefs, "editor_shortcut_safety"), icon="INFO")
                if prefs.enable_editor_shortcuts:
                    for binding in editor_shortcuts_summary(prefs).split(", "):
                        col.label(text=binding, icon="KEYINGSET")

        with _ui_group_guard(layout, "Advanced & diagnostics"):
            box, opened = _draw_foldout_header(layout, prefs, "ui_expand_diagnostics", "advanced_and_tools", "TOOL_SETTINGS")
            if opened:
                col = box.column(align=True)
                col.prop(prefs, "enable_rmb_click_hold", text=_tr(prefs, "enable_rmb_click_hold"))
                hold = col.column(align=True)
                hold.enabled = prefs.enable_rmb_click_hold
                hold.prop(prefs, "rmb_hold_duration", text=_tr(prefs, "rmb_hold_duration"), slider=True)
                col.operator(UVN155_OT_check_key_conflicts.bl_idname, text=_tr(prefs, "check_conflicts"), icon="VIEWZOOM")
                col.label(text=prefs.key_conflict_summary or _tr(prefs, "conflicts_not_checked"))
                if prefs.key_conflict_details:
                    for line in prefs.key_conflict_details.splitlines()[:5]:
                        col.label(text=line)
                col.operator(UVN155_OT_reset_preferences.bl_idname, text=_tr(prefs, "reset_preferences"), icon="LOOP_BACK")
                report = col.operator("wm.url_open", text=_tr(prefs, "report_issue"), icon="URL")
                report.url = _ISSUES_URL

        with _ui_group_guard(layout, "Controls guide"):
            box, opened = _draw_foldout_header(layout, prefs, "ui_expand_guide", "guide_title", "KEYINGSET")
            if opened:
                _draw_control_reference(box.column(align=True), prefs)

        with _ui_group_guard(layout, "Save / reset"):
            row = layout.row(align=True)
            row.operator(UVN155_OT_save_preferences.bl_idname, text=_tr(prefs, "save_preferences"), icon="FILE_TICK")
            row.operator(UVN155_OT_reset_default_keys.bl_idname, text=_tr(prefs, "restore_default_keys"), icon="LOOP_BACK")
            layout.label(text=_tr(prefs, "version"), icon="INFO")


_UVN_REPAIR_BUILD = "1.6.5-navigation-only-expanded-2026-11-01"
