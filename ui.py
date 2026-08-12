# SPDX-License-Identifier: GPL-3.0-or-later
"""Compact 3D Viewport sidebar panel."""

from bpy.types import Panel

from .preferences import UVN155_OT_reset_default_keys, _draw_enum_picker
from .shared import (
    _ISSUES_URL,
    _PROJECT_URL,
    _movement_keys_label,
    _orbit_shortcut,
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

        _draw_enum_picker(layout, prefs, "ui_language", "language")
        _draw_enum_picker(layout, prefs, "navigation_preset", "navigation_preset")

        guide = layout.box()
        guide.label(text=_tr(prefs, "how_to_use"), icon="INFO")
        nav = _shortcut_label(prefs.navigation_mouse, prefs.navigation_modifier)
        guide.label(text=f"{_tr(prefs, 'navigate_action')}: {nav} + {_movement_keys_label(prefs)}")
        if prefs.enable_orbit_selection:
            guide.label(text=f"{_tr(prefs, 'orbit_shortcut_label')}: {_orbit_shortcut(prefs)}")

        quick = layout.box()
        quick.label(text=_tr(prefs, "quick_setup"), icon="SETTINGS")
        quick.prop(prefs, "move_speed", text=_tr(prefs, "base_speed"))
        quick.prop(prefs, "look_sensitivity_ui", text=_tr(prefs, "look_sensitivity"), slider=True)
        quick.prop(prefs, "camera_view_navigation", text=_tr(prefs, "camera_view_navigation"))
        quick.prop(prefs, "enable_orbit_selection", text=_tr(prefs, "orbit_enable_short"))

        layout.label(text=_tr(prefs, "more_settings"), icon="PREFERENCES")
        row = layout.row(align=True)
        row.operator(UVN155_OT_reset_default_keys.bl_idname, text=_tr(prefs, "restore_default_keys"), icon="LOOP_BACK")
        op = row.operator("wm.url_open", text=_tr(prefs, "project_page"), icon="URL")
        op.url = _PROJECT_URL
        op = layout.operator("wm.url_open", text=_tr(prefs, "report_issue"), icon="ERROR")
        op.url = _ISSUES_URL
