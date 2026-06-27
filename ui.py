# SPDX-License-Identifier: GPL-3.0-or-later
"""3D Viewport sidebar panel."""

from bpy.types import Panel

from .shared import _header_text, _movement_keys_label, _tr

class VIEW3D_PT_uvn_panel(Panel):
    bl_label = "Unreal Navigation"
    bl_idname = "VIEW3D_PT_uvn_panel"
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

        layout.prop(prefs, "ui_language", text=_tr(prefs, "language"))

        box = layout.box()
        box.label(text=_tr(prefs, "controls_panel"), icon="MOUSE_MOVE")
        col = box.column(align=True)
        col.label(text=_tr(prefs, "hold_rmb"))
        col.label(text=_movement_keys_label(prefs))
        col.label(text=_tr(prefs, "qe"))
        col.label(text=_tr(prefs, "shift_ctrl"))
        col.label(text=_tr(prefs, "wheel"))

        box = layout.box()
        box.label(text=_tr(prefs, "quick_settings"), icon="SETTINGS")
        col = box.column(align=True)
        col.prop(prefs, "navigation_keys", text=_tr(prefs, "navigation_keys"))
        col.prop(prefs, "navigate_during_tools", text=_tr(prefs, "navigate_during_tools"))
        col.separator()
        col.prop(prefs, "speed_unit", text=_tr(prefs, "speed_unit"))
        col.prop(prefs, "move_speed", text=_tr(prefs, "base_speed"))
        col.prop(prefs, "look_sensitivity_ui", text=_tr(prefs, "look_sensitivity"), slider=True)
        col.prop(prefs, "movement_mode", text=_tr(prefs, "movement_mode"))
        col.prop(prefs, "invert_y", text=_tr(prefs, "invert_y"))
        col.prop(prefs, "smooth_motion", text=_tr(prefs, "smooth_motion"))
        col.separator()
        col.prop(prefs, "hide_cursor", text=_tr(prefs, "hide_cursor"))
        col.prop(prefs, "show_crosshair", text=_tr(prefs, "show_crosshair"))
        col.prop(prefs, "show_header_speed", text=_tr(prefs, "show_header_speed"))
        col.prop(prefs, "show_header_tutorial", text=_tr(prefs, "show_header_tutorial"))

        box = layout.box()
        box.label(text=_tr(prefs, "header_preview"), icon="INFO")
        preview = _header_text(prefs)
        box.label(text=preview if preview else _tr(prefs, "header_none"))

        layout.separator()
        layout.label(text=_tr(prefs, "version"))
        layout.label(text=_tr(prefs, "engine"), icon="CHECKMARK")
        layout.label(text=_tr(prefs, "best_keymap"))
