# SPDX-License-Identifier: GPL-3.0-or-later
"""Explicit keymap registration for 3D Viewport modes.

The earlier dynamic keymap-discovery routine was removed. The list below is
intentional and readable: the two general 3D View maps plus Blender's known
viewport mode maps.
"""

import bpy

from .navigation import VIEW3D_OT_uvn_navigate

_ADDON_KEYMAPS = []

_KNOWN_MODE_KEYMAPS = {
    "Object Non-modal",
    "Object Mode",
    "Lattice",
    "Mesh",
    "Font",
    "Curve",
    "Curves",
    "Point Cloud",
    "Armature",
    "Pose",
    "Particle",
    "Metaball",
    "Sculpt",
    "Vertex Paint",
    "Weight Paint",
    "Image Paint",
    "Sculpt Curves",
    "Grease Pencil",
    "Grease Pencil Selection",
    "Grease Pencil Edit Mode",
    "Grease Pencil Draw Mode",
    "Grease Pencil Paint Mode",  # Compatibility with early/alternate names.
    "Grease Pencil Sculpt Mode",
    "Grease Pencil Weight Paint",
    "Grease Pencil Vertex Paint",
    "Paint Vertex Selection (Weight, Vertex)",
    "Paint Face Mask (Weight, Vertex, Texture)",
}

_KEYMAP_SPECS = (
    ("3D View", "VIEW_3D", "WINDOW"),
    ("3D View Generic", "VIEW_3D", "WINDOW"),
) + tuple((name, "EMPTY", "WINDOW") for name in sorted(_KNOWN_MODE_KEYMAPS))


def register_keymaps():
    keyconfig = bpy.context.window_manager.keyconfigs.addon
    if keyconfig is None:
        return

    for name, space_type, region_type in _KEYMAP_SPECS:
        keymap = keyconfig.keymaps.new(
            name=name,
            space_type=space_type,
            region_type=region_type,
        )
        keymap_item = keymap.keymap_items.new(
            VIEW3D_OT_uvn_navigate.bl_idname,
            "RIGHTMOUSE",
            "PRESS",
            any=False,
            shift=False,
            ctrl=False,
            alt=False,
            oskey=False,
            head=True,
        )
        _ADDON_KEYMAPS.append((keymap, keymap_item))


def unregister_keymaps():
    for keymap, keymap_item in reversed(_ADDON_KEYMAPS):
        try:
            keymap.keymap_items.remove(keymap_item)
        except (ReferenceError, RuntimeError):
            pass
    _ADDON_KEYMAPS.clear()
