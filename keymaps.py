# SPDX-License-Identifier: GPL-3.0-or-later
"""Blender keymap registration and shortcut conflict diagnostics.

Navigation uses one modifier-agnostic mouse binding per viewport keymap.  The
modal operator validates the configured navigation modifier itself.  This is
intentional: it lets RMB navigation start even when Shift or Ctrl was already
held, without registering every possible modifier combination.
"""

from types import SimpleNamespace

import bpy

from .navigation import (
    VIEW3D_OT_uvn155_navigate,
    VIEW3D_OT_uvn155_orbit_selection,
)
from .shared import _key_label, _movement_action_map, _shortcut_label, _tr

_ADDON_KEYMAPS = []

# Blender uses mode-specific keymaps in addition to the two general 3D View
# maps.  Keeping this explicit list preserves navigation in edit, sculpt,
# paint, pose and Grease Pencil modes.
_KNOWN_MODE_KEYMAPS = {
    "Object Non-modal", "Object Mode", "Lattice", "Mesh", "Font", "Curve",
    "Curves", "Point Cloud", "Armature", "Pose", "Particle", "Metaball",
    "Sculpt", "Vertex Paint", "Weight Paint", "Image Paint", "Sculpt Curves",
    "Grease Pencil", "Grease Pencil Selection", "Grease Pencil Edit Mode",
    "Grease Pencil Draw Mode", "Grease Pencil Paint Mode",
    "Grease Pencil Sculpt Mode", "Grease Pencil Weight Paint",
    "Grease Pencil Vertex Paint", "Paint Vertex Selection (Weight, Vertex)",
    "Paint Face Mask (Weight, Vertex, Texture)",
}

_KEYMAP_SPECS = (
    ("3D View", "VIEW_3D", "WINDOW"),
    ("3D View Generic", "VIEW_3D", "WINDOW"),
) + tuple((name, "EMPTY", "WINDOW") for name in sorted(_KNOWN_MODE_KEYMAPS))

_DEFAULT_PREFS = SimpleNamespace(
    navigation_mouse="RIGHTMOUSE",
    navigation_modifier="NONE",
    navigation_keys="WASD",
    move_forward_key="W",
    move_backward_key="S",
    move_left_key="A",
    move_right_key="D",
    move_up_key="E",
    move_down_key="Q",
    sprint_key="SHIFT",
    precision_key="CTRL",
    speed_up_key="WHEELUPMOUSE",
    speed_down_key="WHEELDOWNMOUSE",
    enable_orbit_selection=True,
    orbit_mouse="RIGHTMOUSE",
    orbit_modifier="ALT",
    protect_camera_orbit=True,
    ui_language="EN",
)


def _get_prefs():
    try:
        return bpy.context.preferences.addons[__package__].preferences
    except (AttributeError, KeyError):
        # AddonPreferences can become available a moment after the add-on
        # keyconfig during extension startup.  Safe Unreal defaults are used
        # until a preference change rebuilds the keymaps.
        return _DEFAULT_PREFS


def _add_navigation_bindings(keymap, event_type, required_modifier):
    """Register navigation without swallowing Alt+RMB orbit.

    Shift and Ctrl variants are explicit so sprint/precision may be held before
    the navigation mouse button. Alt is included only when it is the configured
    navigation modifier.
    """
    base = set() if required_modifier == "NONE" else {required_modifier}
    optional = [value for value in ("SHIFT", "CTRL") if value not in base]
    combinations = {frozenset(base)}
    for value in optional:
        combinations |= {combo | {value} for combo in tuple(combinations)}
    for modifiers in sorted(combinations, key=lambda values: (len(values), sorted(values))):
        _add_exact_binding(keymap, VIEW3D_OT_uvn155_navigate.bl_idname, event_type, modifiers)


def _add_exact_binding(keymap, operator_id, event_type, modifiers):
    flags = {"shift": False, "ctrl": False, "alt": False, "oskey": False}
    for value in modifiers:
        if value in {"SHIFT", "CTRL", "ALT"}:
            flags[value.lower()] = True
    item = keymap.keymap_items.new(
        operator_id,
        event_type,
        "PRESS",
        any=False,
        shift=flags["shift"],
        ctrl=flags["ctrl"],
        alt=flags["alt"],
        oskey=False,
        head=True,
    )
    _ADDON_KEYMAPS.append((keymap, item))



def register_keymaps():
    unregister_keymaps()
    prefs = _get_prefs()
    keyconfigs = getattr(getattr(bpy.context, "window_manager", None), "keyconfigs", None)
    keyconfig = getattr(keyconfigs, "addon", None)
    if keyconfig is None:
        return

    navigation_mouse = getattr(prefs, "navigation_mouse", "RIGHTMOUSE")
    navigation_modifier = getattr(prefs, "navigation_modifier", "NONE")
    orbit_mouse = getattr(prefs, "orbit_mouse", "RIGHTMOUSE")
    orbit_modifier = getattr(prefs, "orbit_modifier", "ALT")
    orbit_modifiers = {orbit_modifier} if orbit_modifier != "NONE" else set()

    for name, space_type, region_type in _KEYMAP_SPECS:
        keymap = keyconfig.keymaps.new(
            name=name,
            space_type=space_type,
            region_type=region_type,
        )
        _add_navigation_bindings(keymap, navigation_mouse, navigation_modifier)
        if getattr(prefs, "enable_orbit_selection", True):
            _add_exact_binding(
                keymap,
                VIEW3D_OT_uvn155_orbit_selection.bl_idname,
                orbit_mouse,
                orbit_modifiers,
            )


def unregister_keymaps():
    for keymap, item in reversed(_ADDON_KEYMAPS):
        try:
            keymap.keymap_items.remove(item)
        except (ReferenceError, RuntimeError):
            pass
    _ADDON_KEYMAPS.clear()

def refresh_keymaps():
    register_keymaps()


def _kmi_modifiers(kmi):
    return {
        name
        for name, enabled in (
            ("SHIFT", getattr(kmi, "shift", False)),
            ("CTRL", getattr(kmi, "ctrl", False)),
            ("ALT", getattr(kmi, "alt", False)),
        )
        if enabled
    }


def _our_shortcut_specs(prefs):
    nav_modifier = getattr(prefs, "navigation_modifier", "NONE")
    nav_modifiers = {nav_modifier} if nav_modifier != "NONE" else set()
    specs = [
        (
            "navigation",
            getattr(prefs, "navigation_mouse", "RIGHTMOUSE"),
            nav_modifiers,
            False,
        )
    ]
    if getattr(prefs, "enable_orbit_selection", True):
        orbit_modifier = getattr(prefs, "orbit_modifier", "ALT")
        orbit_modifiers = {orbit_modifier} if orbit_modifier != "NONE" else set()
        specs.append(("orbit", getattr(prefs, "orbit_mouse", "RIGHTMOUSE"), orbit_modifiers, False))
    return specs


def _duplicate_action_conflicts(prefs):
    assignments = {}
    for action, keys in _movement_action_map(prefs).items():
        for key in keys:
            assignments.setdefault(key, []).append(action)
    for action, value in (
        ("speed up", getattr(prefs, "speed_up_key", "WHEELUPMOUSE")),
        ("speed down", getattr(prefs, "speed_down_key", "WHEELDOWNMOUSE")),
        ("sprint", getattr(prefs, "sprint_key", "SHIFT")),
        ("precision", getattr(prefs, "precision_key", "CTRL")),
    ):
        if value != "NONE":
            assignments.setdefault(value, []).append(action)

    conflicts = []
    for key, actions in assignments.items():
        unique = sorted(set(actions))
        if len(unique) > 1:
            conflicts.append(
                _tr(
                    prefs,
                    "conflict_duplicate",
                    shortcut=_key_label(key),
                    actions=", ".join(unique),
                )
            )

    # Catch a direct collision between the two mouse-driven operators.
    specs = _our_shortcut_specs(prefs)
    if len(specs) > 1:
        nav = specs[0]
        for orbit in specs[1:]:
            if nav[1] == orbit[1] and (nav[3] or nav[2] == orbit[2]):
                conflicts.append(
                    _tr(
                        prefs,
                        "conflict_duplicate",
                        shortcut=_shortcut_label(nav[1], getattr(prefs, "navigation_modifier", "NONE")),
                        actions="navigation, orbit",
                    )
                )
                break
    return conflicts


def find_key_conflicts(context, prefs):
    """Find exact or broad mouse-shortcut overlaps in Blender keymaps."""
    conflicts = _duplicate_action_conflicts(prefs)
    seen = set()
    wm = getattr(context, "window_manager", None)
    keyconfigs = getattr(wm, "keyconfigs", None)
    if keyconfigs is None:
        return conflicts

    specs = _our_shortcut_specs(prefs)
    for config_name in ("user", "addon"):
        keyconfig = getattr(keyconfigs, config_name, None)
        if keyconfig is None:
            continue
        for keymap in keyconfig.keymaps:
            for item in keymap.keymap_items:
                if not getattr(item, "active", True):
                    continue
                operator = getattr(item, "idname", "")
                if operator.startswith("view3d.uvn155_"):
                    continue
                if getattr(item, "value", "PRESS") not in {"PRESS", "ANY", "CLICK", "CLICK_DRAG"}:
                    continue
                item_modifiers = _kmi_modifiers(item)
                for _name, event_type, modifiers, modifier_agnostic in specs:
                    if getattr(item, "type", None) != event_type:
                        continue
                    if not modifier_agnostic and item_modifiers != set(modifiers):
                        continue
                    if modifier_agnostic and modifiers and not set(modifiers).issubset(item_modifiers):
                        continue
                    shortcut = _shortcut_label(event_type, "NONE")
                    if modifiers:
                        shortcut = "+".join([*sorted(modifiers), _key_label(event_type)])
                    marker = (shortcut, operator, keymap.name)
                    if marker in seen:
                        continue
                    seen.add(marker)
                    conflicts.append(
                        _tr(
                            prefs,
                            "conflict_external",
                            shortcut=shortcut,
                            operator=operator or "unknown",
                            keymap=keymap.name,
                        )
                    )
    return conflicts
