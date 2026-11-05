# SPDX-License-Identifier: GPL-3.0-or-later
"""Compact 3D Viewport sidebar panel."""

from bpy.types import Panel

from .preferences import UVN155_OT_reset_default_keys, _draw_enum_picker, _ui_group_guard
from .editor_actions import VIEW3D_OT_uvn165_editor_action, resolved_editor_profile
from .navigation import VIEW3D_OT_uvn155_center_orbit
from .shared import (
    _ISSUES_URL,
    _PROJECT_URL,
    _movement_keys_label,
    _orbit_shortcut,
    _orbit_center_shortcut,
    _key_label,
    _shortcut_label,
    _tr,
)


class VIEW3D_PT_uvn155_panel(Panel):
    bl_label = "Unreal Navigation"
    bl_idname = "VIEW3D_PT_uvn155_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Unreal"

    def draw(self, context):
        layout = self.layout
        try:
            prefs = context.preferences.addons[__package__].preferences
        except (AttributeError, KeyError):
            layout.label(text=_tr(None, "no_preferences"), icon="ERROR")
            return

        with _ui_group_guard(layout, "Sidebar quick settings"):
            quick = layout.box()
            quick.label(text=_tr(prefs, "quick_setup"), icon="PREFERENCES")
            _draw_enum_picker(quick, prefs, "ui_language", "language")
            _draw_enum_picker(quick, prefs, "navigation_preset", "navigation_preset")
            quick.prop(prefs, "move_speed", text=_tr(prefs, "base_speed"))
            quick.prop(prefs, "look_sensitivity_ui", text=_tr(prefs, "look_sensitivity"), slider=True)
            quick.prop(prefs, "camera_view_navigation", text=_tr(prefs, "camera_view_navigation"))

        with _ui_group_guard(layout, "Sidebar control guide"):
            guide = layout.box()
            guide.label(text=_tr(prefs, "how_to_use"), icon="INFO")
            nav = _shortcut_label(prefs.navigation_mouse, prefs.navigation_modifier)
            guide.label(text=f"{_tr(prefs, 'navigate_action')}: {nav} + {_movement_keys_label(prefs)}")
            if prefs.enable_orbit_selection:
                guide.label(text=f"{_tr(prefs, 'orbit_shortcut_label')}: {_orbit_shortcut(prefs)}")

        with _ui_group_guard(layout, "Sidebar orbit"):
            orbit = layout.box()
            orbit.label(text=_tr(prefs, "orbit_controls_title"), icon="ORIENTATION_VIEW")
            orbit.prop(prefs, "enable_orbit_selection", text=_tr(prefs, "orbit_enable_short"))
            row = orbit.row(align=True)
            row.enabled = bool(getattr(context, "selected_objects", None))
            row.operator(VIEW3D_OT_uvn155_center_orbit.bl_idname, text=_tr(prefs, "orbit_center_button"), icon="VIEW_SELECTED")
            inside = orbit.column(align=True)
            inside.enabled = prefs.enable_orbit_selection
            inside.prop(prefs, "orbit_auto_center", text=_tr(prefs, "orbit_center_on_start"))
            inside.prop(prefs, "orbit_invert_y", text=_tr(prefs, "orbit_invert_y"))
            inside.label(text=_tr(prefs, "orbit_center_modal_hint", key=_key_label(prefs.orbit_center_key)), icon="INFO")
            if prefs.orbit_center_shortcut_enabled:
                inside.label(text=_tr(prefs, "orbit_center_global_hint", shortcut=_orbit_center_shortcut(prefs)), icon="INFO")

        with _ui_group_guard(layout, "Sidebar editor tools"):
            editor = layout.box()
            editor.label(text=_tr(prefs, "editor_shortcut_section"), icon="TOOL_SETTINGS")
            editor.prop(prefs, "enable_editor_shortcuts", text=_tr(prefs, "editor_shortcut_enable"))
            editor.label(text=f"{_tr(prefs, 'editor_shortcut_active')}: {resolved_editor_profile(prefs)}")
            row = editor.row(align=True)
            row.enabled = context.mode == "OBJECT"
            for label, action in (("Select", "SELECT"), ("Move", "MOVE"),
                                  ("Rotate", "ROTATE"), ("Scale", "SCALE")):
                op = row.operator(VIEW3D_OT_uvn165_editor_action.bl_idname, text=label)
                op.action = action
            row = editor.row(align=True)
            row.enabled = context.mode == "OBJECT"
            op = row.operator(VIEW3D_OT_uvn165_editor_action.bl_idname, text="Frame (F)", icon="VIEW_SELECTED")
            op.action = "FRAME"
            op = row.operator(VIEW3D_OT_uvn165_editor_action.bl_idname, text="Duplicate", icon="DUPLICATE")
            op.action = "DUPLICATE"
            editor.label(text=_tr(prefs, "editor_shortcut_safety"), icon="INFO")

        with _ui_group_guard(layout, "Sidebar support"):
            layout.label(text=_tr(prefs, "more_settings"), icon="PREFERENCES")
            row = layout.row(align=True)
            row.operator(UVN155_OT_reset_default_keys.bl_idname, text=_tr(prefs, "restore_default_keys"), icon="LOOP_BACK")
            link = row.operator("wm.url_open", text=_tr(prefs, "project_page"), icon="URL")
            link.url = _PROJECT_URL
            link = layout.operator("wm.url_open", text=_tr(prefs, "report_issue"), icon="URL")
            link.url = _ISSUES_URL


_UVN_REPAIR_BUILD = "1.6.5-navigation-only-expanded-2026-11-01"
