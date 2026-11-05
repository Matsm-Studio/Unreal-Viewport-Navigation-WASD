# SPDX-License-Identifier: GPL-3.0-or-later
"""Unreal-style viewport navigation for Blender 4.2 and newer."""

import bpy
import importlib
import sys

_UVN_REPAIR_BUILD = "1.6.5-navigation-only-expanded-2026-11-01"


def _restore_consistent_modules():
    """Reload stale 1.6.5 submodules in dependency order before class imports.

    Blender may retain Python submodules after overwriting an extension with
    the same manifest version. Mixing old preferences with new UI once caused
    missing operators/properties and the incomplete settings screen.
    """
    for short_name in ("shared", "editor_actions", "navigation", "preferences", "keymaps", "ui"):
        full_name = f"{__name__}.{short_name}"
        existing = sys.modules.get(full_name)
        if existing is not None and getattr(existing, "_UVN_REPAIR_BUILD", None) != _UVN_REPAIR_BUILD:
            importlib.reload(existing)


_restore_consistent_modules()

from .keymaps import register_keymaps, unregister_keymaps
from .editor_actions import VIEW3D_OT_uvn165_editor_action
from .navigation import (
    VIEW3D_OT_uvn155_navigate,
    VIEW3D_OT_uvn155_orbit_selection,
    VIEW3D_OT_uvn155_center_orbit,
)
from .preferences import (
    UVN155_AddonPreferences,
    UVN155_OT_check_key_conflicts,
    UVN155_OT_reset_default_keys,
    UVN155_OT_reset_preferences,
    UVN155_OT_save_preferences,
)
# Blender can keep an older submodule in sys.modules while an extension ZIP is
# being replaced. This UI helper is optional for older 1.6.5 modules: never
# crash the entire add-on just because one helper has not yet reloaded.
from . import preferences as _preferences_module
UVN155_OT_set_sections = getattr(_preferences_module, "UVN155_OT_set_sections", None)

from .ui import VIEW3D_PT_uvn155_panel

_CLASSES = (
    UVN155_OT_save_preferences,
    UVN155_OT_set_sections,
    UVN155_OT_reset_preferences,
    UVN155_OT_reset_default_keys,
    UVN155_OT_check_key_conflicts,
    UVN155_AddonPreferences,
    VIEW3D_OT_uvn155_orbit_selection,
    VIEW3D_OT_uvn155_center_orbit,
    VIEW3D_OT_uvn155_navigate,
    VIEW3D_OT_uvn165_editor_action,
    VIEW3D_PT_uvn155_panel,
)
_CLASSES = tuple(cls for cls in _CLASSES if cls is not None)


_registered_classes = []


def register():
    # Undo partial registration if a class fails; Blender can otherwise leave
    # a broken extension half-enabled and fail the next installation attempt.
    try:
        for cls in _CLASSES:
            bpy.utils.register_class(cls)
            _registered_classes.append(cls)
        register_keymaps()
    except Exception:
        try:
            unregister_keymaps()
        finally:
            for cls in reversed(_registered_classes):
                try:
                    bpy.utils.unregister_class(cls)
                except (RuntimeError, ReferenceError, ValueError):
                    pass
            _registered_classes.clear()
        raise


def unregister():
    try:
        unregister_keymaps()
    finally:
        for cls in reversed(_registered_classes):
            try:
                bpy.utils.unregister_class(cls)
            except (RuntimeError, ReferenceError, ValueError):
                pass
        _registered_classes.clear()
