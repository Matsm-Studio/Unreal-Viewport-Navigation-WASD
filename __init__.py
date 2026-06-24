# SPDX-License-Identifier: GPL-3.0-or-later
"""Unreal-style viewport navigation for Blender 4.2 and newer."""

import bpy

from .keymaps import register_keymaps, unregister_keymaps
from .navigation import VIEW3D_OT_uvn_navigate
from .preferences import UVN_AddonPreferences, UVN_OT_save_preferences
from .ui import VIEW3D_PT_uvn_panel

_CLASSES = (
    UVN_OT_save_preferences,
    UVN_AddonPreferences,
    VIEW3D_OT_uvn_navigate,
    VIEW3D_PT_uvn_panel,
)


def register():
    for cls in _CLASSES:
        bpy.utils.register_class(cls)
    register_keymaps()


def unregister():
    unregister_keymaps()
    for cls in reversed(_CLASSES):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass


if __name__ == "__main__":
    register()
