# SPDX-License-Identifier: GPL-3.0-or-later
"""Blender add-on preferences and explicit preference-save operator."""

import bpy
from bpy.props import (
    BoolProperty, EnumProperty, FloatProperty, FloatVectorProperty, IntProperty, StringProperty,
)
from bpy.types import AddonPreferences, Operator

from .shared import (
    _crosshair_style_items, _movement_mode_items, _navigation_keys_items,
    _speed_unit_items, _tr, _update_speed_unit,
)

class UVN_OT_save_preferences(Operator):
    """Save Blender preferences only after an explicit button press."""

    bl_idname = "uvn.save_preferences"
    bl_label = "Save on Disk"
    bl_description = "Save Blender preferences, including this extension's settings"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        try:
            prefs = context.preferences.addons[__package__].preferences
        except (AttributeError, KeyError):
            prefs = None
        try:
            bpy.ops.wm.save_userpref()
        except (RuntimeError, TypeError) as exc:
            self.report({"ERROR"}, _tr(prefs, "preferences_save_failed", error=exc))
            return {"CANCELLED"}

        self.report({"INFO"}, _tr(prefs, "preferences_saved"))
        return {"FINISHED"}

class UVN_OT_reset_preferences(Operator):
    """Restore every add-on preference to its declared default value."""

    bl_idname = "uvn.reset_preferences"
    bl_label = "Reset to Defaults"
    bl_description = "Restore all Unreal Viewport Navigation settings to their default values"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        try:
            prefs = context.preferences.addons[__package__].preferences
        except (AttributeError, KeyError):
            self.report({"ERROR"}, _tr(None, "error_prefs"))
            return {"CANCELLED"}

        for prop in prefs.bl_rna.properties:
            identifier = prop.identifier
            if identifier == "rna_type" or prop.is_readonly:
                continue
            try:
                prefs.property_unset(identifier)
            except (AttributeError, TypeError):
                pass

        self.report({"INFO"}, _tr(prefs, "preferences_reset"))
        return {"FINISHED"}


class UVN_AddonPreferences(AddonPreferences):
    bl_idname = __package__

    ui_language: EnumProperty(
        name="Interface Language",
        description="Language used by this add-on",
        items=(
            ("EN", "English", "Use English in the add-on interface"),
            ("PL", "Polski", "Używaj języka polskiego w interfejsie dodatku"),
        ),
        default="EN",
    )

    navigation_keys: EnumProperty(
        name="Movement Keys",
        description="Choose WASD, arrow keys or both for horizontal movement",
        items=_navigation_keys_items,
    )
    navigate_during_tools: BoolProperty(
        name="Navigate While Using Compatible Tools",
        description="Allow navigation while another tool is active when that tool does not use RMB or the selected movement keys",
        default=True,
    )
    enable_rmb_click_hold: BoolProperty(
        name="Enable RMB Click/Hold Separation",
        description="Short RMB click opens Blender's context menu; holding RMB starts navigation. Disable to restore immediate RMB navigation",
        default=True,
    )
    rmb_hold_duration: FloatProperty(
        name="RMB Hold Duration",
        description="Time RMB must be held before navigation starts; a shorter click opens Blender's context menu",
        default=0.09,
        min=0.03,
        max=0.30,
        soft_min=0.03,
        soft_max=0.20,
        precision=2,
        subtype="TIME",
    )

    move_speed: FloatProperty(
        name="Movement Speed",
        description="Base navigation speed in the selected unit",
        default=5.0,
        min=1.0e-9,
        max=1.0e12,
        soft_min=0.01,
        soft_max=1000.0,
        precision=3,
    )
    minimum_speed: FloatProperty(
        name="Minimum Speed",
        description="Minimum speed available through the mouse wheel",
        default=0.05,
        min=1.0e-9,
        max=1.0e12,
        soft_max=100.0,
        precision=3,
    )
    maximum_speed: FloatProperty(
        name="Maximum Speed",
        description="Maximum speed available through the mouse wheel",
        default=500.0,
        min=1.0e-9,
        max=1.0e12,
        soft_max=100000.0,
        precision=3,
    )
    speed_unit: EnumProperty(
        name="Speed Unit",
        description="Unit used for navigation speed and the viewport header",
        items=_speed_unit_items,
        update=_update_speed_unit,
    )
    speed_unit_previous: StringProperty(default="BU_S", options={"HIDDEN"})
    wheel_multiplier: FloatProperty(
        name="Mouse-wheel Step",
        description="Speed multiplier for one mouse-wheel step",
        default=1.25,
        min=1.01,
        max=4.0,
        precision=2,
    )
    sprint_multiplier: FloatProperty(
        name="Shift Multiplier",
        description="Movement speed multiplier while Shift is held",
        default=4.0,
        min=1.0,
        max=30.0,
        soft_max=10.0,
        precision=2,
    )
    precision_multiplier: FloatProperty(
        name="Ctrl Multiplier",
        description="Slow precision movement while Ctrl is held",
        default=0.25,
        min=0.01,
        max=1.0,
        precision=2,
    )
    # Legacy value kept only so existing saved preferences remain readable.
    # The interface uses look_sensitivity_ui with normal, user-friendly values.
    look_sensitivity: FloatProperty(
        name="Legacy Mouse Sensitivity",
        description="Legacy internal mouse sensitivity value",
        default=0.0022,
        min=0.0001,
        max=0.02,
        precision=4,
        options={"HIDDEN"},
    )
    look_sensitivity_ui: FloatProperty(
        name="Mouse Sensitivity",
        description="Mouse-look sensitivity; 2.20 matches the previous default",
        default=2.2,
        min=0.1,
        max=20.0,
        soft_min=0.5,
        soft_max=10.0,
        step=10,
        precision=2,
    )
    invert_y: BoolProperty(name="Invert Y Axis", default=False)
    movement_mode: EnumProperty(
        name="Forward/Back Movement",
        description="Choose free flight or level forward/back movement",
        items=_movement_mode_items,
    )
    smooth_motion: BoolProperty(name="Smooth Acceleration", default=True)
    acceleration: FloatProperty(
        name="Acceleration",
        description="How quickly movement reaches the target speed",
        default=18.0,
        min=0.1,
        max=100.0,
        soft_max=40.0,
    )
    deceleration: FloatProperty(
        name="Deceleration",
        description="How quickly movement stops after releasing a key",
        default=24.0,
        min=0.1,
        max=100.0,
        soft_max=50.0,
    )
    update_rate: IntProperty(
        name="Update Rate",
        description="Navigation timer frequency",
        default=120,
        min=30,
        max=240,
        subtype="UNSIGNED",
    )
    hide_cursor: BoolProperty(
        name="Hide System Cursor",
        description="Hide the operating-system pointer while navigating",
        default=True,
    )
    restore_cursor_position: BoolProperty(
        name="Restore Cursor Position",
        description="Return the pointer to its starting position after releasing RMB",
        default=True,
    )
    force_perspective: BoolProperty(
        name="Switch to Perspective View",
        default=True,
    )

    show_crosshair: BoolProperty(
        name="Show Crosshair",
        description="Draw a configurable crosshair in the center while navigating",
        default=False,
    )
    crosshair_style: EnumProperty(
        name="Crosshair Style",
        items=_crosshair_style_items,
    )
    crosshair_size: IntProperty(
        name="Crosshair Size",
        description="Outer crosshair radius in pixels",
        default=14,
        min=3,
        max=100,
        subtype="PIXEL",
    )
    crosshair_gap: IntProperty(
        name="Center Gap",
        description="Empty space around the crosshair center in pixels",
        default=4,
        min=0,
        max=50,
        subtype="PIXEL",
    )
    crosshair_thickness: FloatProperty(
        name="Line Thickness",
        description="Crosshair line thickness in pixels",
        default=1.5,
        min=1.0,
        max=10.0,
        precision=1,
    )
    crosshair_color: FloatVectorProperty(
        name="Crosshair Color",
        description="Crosshair color and opacity",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0, 0.9),
    )

    show_header_speed: BoolProperty(
        name="Show Header Speed",
        description="Show only the current speed portion of the viewport header",
        default=True,
    )
    show_header_tutorial: BoolProperty(
        name="Show Header Tutorial",
        description="Show the control tutorial portion of the viewport header",
        default=True,
    )

    def draw(self, _context):
        layout = self.layout
        prefs = self

        layout.prop(self, "ui_language", text=_tr(prefs, "language"))

        box = layout.box()
        box.label(text=_tr(prefs, "navigation"), icon="VIEW_PAN")
        col = box.column(align=True)
        col.prop(self, "navigation_keys", text=_tr(prefs, "navigation_keys"))
        col.prop(self, "navigate_during_tools", text=_tr(prefs, "navigate_during_tools"))
        col.prop(self, "enable_rmb_click_hold", text=_tr(prefs, "enable_rmb_click_hold"))
        hold_row = col.row()
        hold_row.enabled = self.enable_rmb_click_hold
        hold_row.prop(self, "rmb_hold_duration", text=_tr(prefs, "rmb_hold_duration"), slider=True)
        col.separator()
        col.prop(self, "look_sensitivity_ui", text=_tr(prefs, "look_sensitivity"), slider=True)
        col.prop(self, "invert_y", text=_tr(prefs, "invert_y"))
        col.prop(self, "movement_mode", text=_tr(prefs, "movement_mode"))
        col.prop(self, "force_perspective", text=_tr(prefs, "force_perspective"))

        box = layout.box()
        box.label(text=_tr(prefs, "speed"), icon="DRIVER_DISTANCE")
        col = box.column(align=True)
        col.prop(self, "speed_unit", text=_tr(prefs, "speed_unit"))
        col.prop(self, "move_speed", text=_tr(prefs, "base_speed"))
        col.prop(self, "wheel_multiplier", text=_tr(prefs, "wheel_multiplier"))
        col.prop(self, "sprint_multiplier", text=_tr(prefs, "sprint_multiplier"))
        col.prop(self, "precision_multiplier", text=_tr(prefs, "precision_multiplier"))
        row = col.row(align=True)
        row.prop(self, "minimum_speed", text=_tr(prefs, "minimum_speed"))
        row.prop(self, "maximum_speed", text=_tr(prefs, "maximum_speed"))
        col.label(text=_tr(prefs, "unit_note"), icon="INFO")

        box = layout.box()
        box.label(text=_tr(prefs, "motion"), icon="IPO_EASE_IN_OUT")
        col = box.column(align=True)
        col.prop(self, "smooth_motion", text=_tr(prefs, "smooth_motion"))
        sub = col.column(align=True)
        sub.enabled = self.smooth_motion
        sub.prop(self, "acceleration", text=_tr(prefs, "acceleration"))
        sub.prop(self, "deceleration", text=_tr(prefs, "deceleration"))
        col.prop(self, "update_rate", text=_tr(prefs, "update_rate"))

        box = layout.box()
        box.label(text=_tr(prefs, "cursor_hud"), icon="PREFERENCES")
        col = box.column(align=True)
        col.prop(self, "hide_cursor", text=_tr(prefs, "hide_cursor"))
        col.prop(self, "restore_cursor_position", text=_tr(prefs, "restore_cursor"))
        col.separator()
        col.prop(self, "show_crosshair", text=_tr(prefs, "show_crosshair"))
        crosshair = col.column(align=True)
        crosshair.enabled = self.show_crosshair
        crosshair.prop(self, "crosshair_style", text=_tr(prefs, "crosshair_style"))
        crosshair.prop(self, "crosshair_size", text=_tr(prefs, "crosshair_size"))
        crosshair.prop(self, "crosshair_gap", text=_tr(prefs, "crosshair_gap"))
        crosshair.prop(self, "crosshair_thickness", text=_tr(prefs, "crosshair_thickness"))
        crosshair.prop(self, "crosshair_color", text=_tr(prefs, "crosshair_color"))
        col.separator()
        col.prop(self, "show_header_speed", text=_tr(prefs, "show_header_speed"))
        col.prop(self, "show_header_tutorial", text=_tr(prefs, "show_header_tutorial"))

        layout.separator()
        save_box = layout.box()
        save_box.label(text=_tr(prefs, "save_preferences_hint"), icon="INFO")
        buttons = save_box.row(align=True)
        buttons.operator(UVN_OT_save_preferences.bl_idname, text=_tr(prefs, "save_preferences"))
        buttons.operator(UVN_OT_reset_preferences.bl_idname, text=_tr(prefs, "reset_preferences"), icon="LOOP_BACK")

        layout.separator()
        layout.label(text="RMB + WASD/Arrows, Q/E, Shift, Ctrl, mouse wheel")
        layout.label(text=_tr(prefs, "engine"), icon="CHECKMARK")
