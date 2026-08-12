# SPDX-License-Identifier: GPL-3.0-or-later
"""Unreal-style viewport navigation for Blender 4.2 and newer."""

import bpy

from .keymaps import register_keymaps, unregister_keymaps
from .navigation import (
    VIEW3D_OT_uvn155_navigate,
    VIEW3D_OT_uvn155_orbit_selection,
)
from .preferences import (
    UVN155_AddonPreferences,
    UVN155_OT_choose_enum,
    UVN155_OT_check_key_conflicts,
    UVN155_OT_reset_default_keys,
    UVN155_OT_reset_preferences,
    UVN155_OT_save_preferences,
)
from .ui import VIEW3D_PT_uvn155_panel

_CLASSES = (
    UVN155_OT_choose_enum,
    UVN155_OT_save_preferences,
    UVN155_OT_reset_preferences,
    UVN155_OT_reset_default_keys,
    UVN155_OT_check_key_conflicts,
    UVN155_AddonPreferences,
    VIEW3D_OT_uvn155_orbit_selection,
    VIEW3D_OT_uvn155_navigate,
    VIEW3D_PT_uvn155_panel,
)


def register():
    for cls in _CLASSES:
        bpy.utils.register_class(cls)
    register_keymaps()


def unregister():
    unregister_keymaps()
    for cls in reversed(_CLASSES):
        bpy.utils.unregister_class(cls)
