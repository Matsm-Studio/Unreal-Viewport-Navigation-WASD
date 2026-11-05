# SPDX-License-Identifier: GPL-3.0-or-later
"""Opt-in engine-inspired editor shortcuts, separate from modal navigation.

Only Object Mode's 3D Viewport keymap is modified.  Existing Blender hotkeys
stay intact until the user explicitly enables the editor shortcut layer.
"""

import bpy
from bpy.props import EnumProperty
from bpy.types import Operator

# Only the engine-specific differences are added to the shared set.
# These mappings are deliberately INSPIRED by the engines; they do not attempt
# to emulate unrelated engine tools/commands that Blender does not provide.
_COMMON = (
    ("W", (), "MOVE"),
    ("E", (), "ROTATE"),
    ("R", (), "SCALE"),
    ("F", (), "FRAME"),
    ("D", ("CTRL",), "DUPLICATE"),
)
_EXTRAS = {
    "UNREAL": (("G", (), "OVERLAYS"),),
    "UNITY": (("Q", (), "SELECT"), ("X", (), "ORIENTATION")),
    "GODOT": (("Q", (), "SELECT"), ("T", (), "ORIENTATION"), ("Y", (), "SNAP")),
    "MAYA": (("Q", (), "SELECT"),),
    "BASIC": (),
}
_LABELS = {
    "SELECT": "Select", "MOVE": "Move tool", "ROTATE": "Rotate tool",
    "SCALE": "Scale tool", "FRAME": "Frame Selected",
    "DUPLICATE": "Duplicate", "ORIENTATION": "Local / Global",
    "SNAP": "Toggle Snapping", "OVERLAYS": "Clean View",
}


def resolved_editor_profile(prefs):
    profile = getattr(prefs, "editor_shortcut_profile", "AUTO")
    if profile == "AUTO":
        profile = getattr(prefs, "navigation_preset", "UNREAL")
        if profile == "CUSTOM":
            # Tuning a navigation setting should not unexpectedly erase the
            # user's chosen engine shortcut profile.
            profile = getattr(prefs, "editor_shortcut_auto_last_profile", "UNREAL")
    return profile if profile in _EXTRAS else "BASIC"


def editor_shortcut_specs(prefs):
    """Return only live hotkeys; no overrides when the layer is disabled."""
    if not getattr(prefs, "enable_editor_shortcuts", False):
        return ()
    profile = resolved_editor_profile(prefs)
    return _COMMON + _EXTRAS[profile]


def editor_shortcuts_summary(prefs):
    return ", ".join(
        "+".join((*mods, key)) + " " + _LABELS[action]
        for key, mods, action in editor_shortcut_specs(prefs)
    )


class VIEW3D_OT_uvn165_editor_action(Operator):
    """Perform a Blender editor command with game-engine inspired shortcuts."""
    bl_idname = "view3d.uvn165_editor_action"
    bl_label = "Engine Editor Action"
    bl_description = "Run a Blender editing action from the optional editor shortcuts"
    bl_options = {"REGISTER"}

    action: EnumProperty(
        name="Action",
        items=tuple((a, label, label) for a, label in _LABELS.items()),
        default="MOVE",
    )

    @classmethod
    def poll(cls, context):
        area = getattr(context, "area", None)
        return bool(area and area.type == "VIEW_3D" and context.mode == "OBJECT")

    def execute(self, context):
        action = self.action
        if action in {"SELECT", "MOVE", "ROTATE", "SCALE"}:
            tool_ids = {
                "SELECT": "builtin.select_box",
                "MOVE": "builtin.move",
                "ROTATE": "builtin.rotate",
                "SCALE": "builtin.scale",
            }
            if not bpy.ops.wm.tool_set_by_id.poll():
                return {"CANCELLED"}
            try:
                bpy.ops.wm.tool_set_by_id(name=tool_ids[action])
                return {"FINISHED"}
            except RuntimeError as exc:
                self.report({"WARNING"}, str(exc))
                return {"CANCELLED"}

        if action == "FRAME":
            if not context.selected_objects or not bpy.ops.view3d.view_selected.poll():
                self.report({"INFO"}, "Select an object to frame")
                return {"CANCELLED"}
            bpy.ops.view3d.view_selected()
            return {"FINISHED"}

        if action == "DUPLICATE":
            if not context.selected_objects or not bpy.ops.object.duplicate_move.poll():
                self.report({"INFO"}, "Select an object to duplicate")
                return {"CANCELLED"}
            # Invoke Blender's own duplicate-and-move operator so Undo and
            # interactive placement continue to work like the native command.
            return bpy.ops.object.duplicate_move("INVOKE_DEFAULT")

        if action == "ORIENTATION":
            slot = context.scene.transform_orientation_slots[0]
            slot.type = "LOCAL" if slot.type != "LOCAL" else "GLOBAL"
            return {"FINISHED"}

        if action == "SNAP":
            settings = context.scene.tool_settings
            settings.use_snap = not settings.use_snap
            return {"FINISHED"}

        if action == "OVERLAYS":
            space = context.space_data
            space.overlay.show_overlays = not space.overlay.show_overlays
            return {"FINISHED"}

        return {"CANCELLED"}

_UVN_REPAIR_BUILD = "1.6.5-navigation-only-expanded-2026-11-01"
