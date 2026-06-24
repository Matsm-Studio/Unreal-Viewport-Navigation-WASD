# SPDX-License-Identifier: GPL-3.0-or-later
"""Shared constants, translations and unit helpers."""

import bpy

_WASD_MOVE_KEYS = {"W", "A", "S", "D"}
_ARROW_MOVE_KEYS = {"UP_ARROW", "LEFT_ARROW", "DOWN_ARROW", "RIGHT_ARROW"}
_VERTICAL_MOVE_KEYS = {"Q", "E"}
_SHIFT_KEYS = {"LEFT_SHIFT", "RIGHT_SHIFT"}
_CTRL_KEYS = {"LEFT_CTRL", "RIGHT_CTRL"}
_ALL_MOVE_KEYS = _WASD_MOVE_KEYS | _ARROW_MOVE_KEYS | _VERTICAL_MOVE_KEYS
_ALL_NAV_KEYS = _ALL_MOVE_KEYS | _SHIFT_KEYS | _CTRL_KEYS
_TEXT = {
    "EN": {
        "language": "Interface language",
        "navigation": "Viewport navigation",
        "navigation_keys": "Movement keys",
        "navigate_during_tools": "Navigate while using compatible tools",
        "speed": "Speed",
        "motion": "Motion",
        "cursor_hud": "Cursor, crosshair and header",
        "base_speed": "Movement speed",
        "minimum_speed": "Minimum speed",
        "maximum_speed": "Maximum speed",
        "speed_unit": "Speed unit",
        "wheel_multiplier": "Mouse-wheel step",
        "sprint_multiplier": "Shift multiplier",
        "precision_multiplier": "Ctrl multiplier",
        "look_sensitivity": "Mouse sensitivity",
        "invert_y": "Invert Y axis",
        "movement_mode": "Forward/back movement",
        "smooth_motion": "Smooth acceleration",
        "acceleration": "Acceleration",
        "deceleration": "Deceleration",
        "update_rate": "Update rate",
        "hide_cursor": "Hide system cursor while navigating",
        "restore_cursor": "Restore cursor position on release",
        "force_perspective": "Switch to perspective view",
        "show_crosshair": "Show crosshair",
        "crosshair_style": "Crosshair style",
        "crosshair_size": "Crosshair size",
        "crosshair_gap": "Center gap",
        "crosshair_thickness": "Line thickness",
        "crosshair_color": "Crosshair color",
        "show_header_speed": "Show speed in viewport header",
        "show_header_tutorial": "Show control tutorial in viewport header",
        "controls_short_wasd": "WASD move  Q/E down/up  Shift faster  Ctrl slower  Wheel speed  Release RMB to stop",
        "controls_short_arrows": "Arrows move  Q/E down/up  Shift faster  Ctrl slower  Wheel speed  Release RMB to stop",
        "controls_short_both": "WASD/Arrows move  Q/E down/up  Shift faster  Ctrl slower  Wheel speed  Release RMB to stop",
        "controls_panel": "Controls",
        "hold_rmb": "Hold RMB + move mouse: look around",
        "move_keys_wasd": "WASD: move",
        "move_keys_arrows": "Arrow keys: move",
        "move_keys_both": "WASD / Arrow keys: move",
        "qe": "Q / E: down / up",
        "shift_ctrl": "Shift / Ctrl: fast / precision",
        "wheel": "Mouse wheel: change speed",
        "quick_settings": "Quick settings",
        "no_preferences": "Add-on preferences are unavailable",
        "version": "Version 1.0.1 — Matsm Studio",
        "engine": "Custom navigation engine. No Walk/Fly.",
        "best_keymap": "Recommended keymap: Industry Compatible",
        "unit_note": "Metric and imperial speeds respect Scene > Units > Unit Scale.",
        "header_preview": "Header preview",
        "header_none": "Both header elements are disabled.",
        "save_preferences": "Save on Disk",
        "save_preferences_hint": "Settings stay in Blender preferences until you explicitly save them",
        "preferences_saved": "Blender preferences saved",
        "preferences_save_failed": "Could not save Blender preferences: {error}",
        "error_prefs": "Could not read add-on preferences",
        "error_region": "Start navigation over the main 3D viewport region",
        "stopped": "Navigation stopped: {error}",
    },
    "PL": {
        "language": "Język interfejsu",
        "navigation": "Nawigacja viewportu",
        "navigation_keys": "Klawisze poruszania",
        "navigate_during_tools": "Nawigacja podczas używania zgodnych narzędzi",
        "speed": "Prędkość",
        "motion": "Ruch",
        "cursor_hud": "Kursor, celownik i nagłówek",
        "base_speed": "Prędkość ruchu",
        "minimum_speed": "Minimalna prędkość",
        "maximum_speed": "Maksymalna prędkość",
        "speed_unit": "Jednostka prędkości",
        "wheel_multiplier": "Skok kółka myszy",
        "sprint_multiplier": "Mnożnik Shift",
        "precision_multiplier": "Mnożnik Ctrl",
        "look_sensitivity": "Czułość myszy",
        "invert_y": "Odwróć oś Y",
        "movement_mode": "Ruch przód/tył",
        "smooth_motion": "Płynne przyspieszanie",
        "acceleration": "Przyspieszenie",
        "deceleration": "Hamowanie",
        "update_rate": "Częstotliwość odświeżania",
        "hide_cursor": "Ukryj kursor systemowy podczas nawigacji",
        "restore_cursor": "Przywróć pozycję kursora po puszczeniu",
        "force_perspective": "Przełącz widok na perspektywiczny",
        "show_crosshair": "Pokaż celownik",
        "crosshair_style": "Styl celownika",
        "crosshair_size": "Rozmiar celownika",
        "crosshair_gap": "Przerwa w środku",
        "crosshair_thickness": "Grubość linii",
        "crosshair_color": "Kolor celownika",
        "show_header_speed": "Pokazuj prędkość w nagłówku viewportu",
        "show_header_tutorial": "Pokazuj instrukcję sterowania w nagłówku viewportu",
        "controls_short_wasd": "WASD ruch  Q/E dół/góra  Shift szybciej  Ctrl wolniej  Kółko prędkość  Puść PPM, aby zakończyć",
        "controls_short_arrows": "Strzałki ruch  Q/E dół/góra  Shift szybciej  Ctrl wolniej  Kółko prędkość  Puść PPM, aby zakończyć",
        "controls_short_both": "WASD/strzałki ruch  Q/E dół/góra  Shift szybciej  Ctrl wolniej  Kółko prędkość  Puść PPM, aby zakończyć",
        "controls_panel": "Sterowanie",
        "hold_rmb": "Przytrzymaj PPM + ruszaj myszą: rozglądanie",
        "move_keys_wasd": "WASD: ruch",
        "move_keys_arrows": "Strzałki: ruch",
        "move_keys_both": "WASD / strzałki: ruch",
        "qe": "Q / E: dół / góra",
        "shift_ctrl": "Shift / Ctrl: szybko / precyzyjnie",
        "wheel": "Kółko myszy: zmiana prędkości",
        "quick_settings": "Szybkie ustawienia",
        "no_preferences": "Brak dostępu do ustawień dodatku",
        "version": "Wersja 1.0.1 — Matsm Studio",
        "engine": "Własny silnik nawigacji. Bez Walk/Fly.",
        "best_keymap": "Zalecana keymapa: Industry Compatible",
        "unit_note": "Prędkości metryczne i imperialne uwzględniają Scene > Units > Unit Scale.",
        "header_preview": "Podgląd nagłówka",
        "header_none": "Oba elementy nagłówka są wyłączone.",
        "error_prefs": "Nie można odczytać ustawień dodatku",
        "error_region": "Uruchom nawigację nad głównym obszarem viewportu 3D",
        "stopped": "Nawigacja została zatrzymana: {error}",
    },
}
_ENUM_ITEMS = {
    "navigation_keys": {
        "EN": (
            ("WASD", "WASD", "Use W, A, S and D for horizontal movement"),
            ("ARROWS", "Arrow keys", "Use the arrow keys for horizontal movement"),
            ("BOTH", "WASD + Arrow keys", "Use both WASD and the arrow keys"),
        ),
        "PL": (
            ("WASD", "WASD", "Używaj W, A, S i D do poruszania poziomego"),
            ("ARROWS", "Strzałki", "Używaj klawiszy strzałek do poruszania poziomego"),
            ("BOTH", "WASD + strzałki", "Używaj jednocześnie WASD i klawiszy strzałek"),
        ),
    },
    "movement_mode": {
        "EN": (
            ("FREE", "Free flight", "W/S moves in the viewing direction, including vertically"),
            ("LEVEL", "Level", "W/S remains parallel to the world XY plane"),
        ),
        "PL": (
            ("FREE", "Swobodny lot", "W/S porusza w kierunku patrzenia, także pionowo"),
            ("LEVEL", "Poziomy", "W/S pozostaje równolegle do płaszczyzny XY świata"),
        ),
    },
    "speed_unit": {
        "EN": (
            ("BU_S", "Blender units / s", "Speed in Blender units per second"),
            ("M_S", "Meters / s", "Meters per second"),
            ("CM_S", "Centimeters / s", "Centimeters per second"),
            ("MM_S", "Millimeters / s", "Millimeters per second"),
            ("KM_H", "Kilometers / h", "Kilometers per hour"),
            ("FT_S", "Feet / s", "Feet per second"),
            ("MPH", "Miles / h", "Miles per hour"),
        ),
        "PL": (
            ("BU_S", "Jednostki Blendera / s", "Prędkość w jednostkach Blendera na sekundę"),
            ("M_S", "Metry / s", "Metry na sekundę"),
            ("CM_S", "Centymetry / s", "Centymetry na sekundę"),
            ("MM_S", "Milimetry / s", "Milimetry na sekundę"),
            ("KM_H", "Kilometry / h", "Kilometry na godzinę"),
            ("FT_S", "Stopy / s", "Stopy na sekundę"),
            ("MPH", "Mile / h", "Mile na godzinę"),
        ),
    },
    "crosshair_style": {
        "EN": (
            ("CROSS", "Cross", "Four crosshair lines with a center gap"),
            ("CROSS_DOT", "Cross + dot", "Crosshair lines with a center dot"),
            ("DOT", "Dot", "Center dot only"),
            ("CIRCLE", "Circle", "Center circle"),
        ),
        "PL": (
            ("CROSS", "Krzyżyk", "Cztery linie z przerwą w środku"),
            ("CROSS_DOT", "Krzyżyk + punkt", "Linie celownika z punktem pośrodku"),
            ("DOT", "Punkt", "Tylko punkt pośrodku"),
            ("CIRCLE", "Okrąg", "Okrąg pośrodku"),
        ),
    },
}
_SPEED_TO_METERS = {
    "M_S": 1.0,
    "CM_S": 0.01,
    "MM_S": 0.001,
    "KM_H": 1.0 / 3.6,
    "FT_S": 0.3048,
    "MPH": 0.44704,
}
_SPEED_SUFFIX = {
    "BU_S": "BU/s",
    "M_S": "m/s",
    "CM_S": "cm/s",
    "MM_S": "mm/s",
    "KM_H": "km/h",
    "FT_S": "ft/s",
    "MPH": "mph",
}

def _language(prefs):
    return getattr(prefs, "ui_language", "EN") if prefs is not None else "EN"

def _tr(prefs, key, **kwargs):
    lang = _language(prefs)
    text = _TEXT.get(lang, _TEXT["EN"]).get(key, _TEXT["EN"].get(key, key))
    return text.format(**kwargs) if kwargs else text

def _navigation_keys_items(self, _context):
    return _ENUM_ITEMS["navigation_keys"].get(_language(self), _ENUM_ITEMS["navigation_keys"]["EN"])

def _movement_mode_items(self, _context):
    return _ENUM_ITEMS["movement_mode"].get(_language(self), _ENUM_ITEMS["movement_mode"]["EN"])

def _speed_unit_items(self, _context):
    return _ENUM_ITEMS["speed_unit"].get(_language(self), _ENUM_ITEMS["speed_unit"]["EN"])

def _crosshair_style_items(self, _context):
    return _ENUM_ITEMS["crosshair_style"].get(_language(self), _ENUM_ITEMS["crosshair_style"]["EN"])

def _clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))

def _scene_scale_length(context=None):
    context = context or bpy.context
    scene = getattr(context, "scene", None)
    if scene is None:
        return 1.0
    value = float(getattr(scene.unit_settings, "scale_length", 1.0))
    return value if value > 1.0e-12 else 1.0

def _speed_to_bu(value, unit, context=None):
    """Convert a display speed to Blender units per second."""
    value = float(value)
    if unit == "BU_S":
        return value
    meters = value * _SPEED_TO_METERS.get(unit, 1.0)
    return meters / _scene_scale_length(context)

def _speed_from_bu(value_bu, unit, context=None):
    """Convert Blender units per second to the selected display unit."""
    value_bu = float(value_bu)
    if unit == "BU_S":
        return value_bu
    meters = value_bu * _scene_scale_length(context)
    factor = _SPEED_TO_METERS.get(unit, 1.0)
    return meters / factor

def _update_speed_unit(self, context):
    """Keep the physical movement speed unchanged when switching units."""
    previous = getattr(self, "speed_unit_previous", "BU_S") or "BU_S"
    current = getattr(self, "speed_unit", "BU_S") or "BU_S"

    if previous != current:
        for property_name in ("move_speed", "minimum_speed", "maximum_speed"):
            old_value = float(getattr(self, property_name))
            value_bu = _speed_to_bu(old_value, previous, context)
            new_value = _speed_from_bu(value_bu, current, context)
            setattr(self, property_name, _clamp(new_value, 1.0e-9, 1.0e12))

        self.speed_unit_previous = current

def _format_number(value):
    absolute = abs(value)
    if absolute >= 1000.0:
        return f"{value:,.1f}"
    if absolute >= 100.0:
        return f"{value:.1f}"
    if absolute >= 10.0:
        return f"{value:.2f}"
    if absolute >= 1.0:
        return f"{value:.2f}"
    if absolute >= 0.01:
        return f"{value:.3f}"
    return f"{value:.4g}"

def _format_speed(prefs):
    unit = getattr(prefs, "speed_unit", "BU_S")
    return f"{_format_number(float(prefs.move_speed))} {_SPEED_SUFFIX.get(unit, 'BU/s')}"

def _navigation_keys_mode(prefs):
    value = getattr(prefs, "navigation_keys", "WASD")
    return value if value in {"WASD", "ARROWS", "BOTH"} else "WASD"

def _controls_short(prefs):
    mode = _navigation_keys_mode(prefs).lower()
    return _tr(prefs, f"controls_short_{mode}")

def _movement_keys_label(prefs):
    mode = _navigation_keys_mode(prefs).lower()
    return _tr(prefs, f"move_keys_{mode}")

def _header_text(prefs):
    parts = []
    if getattr(prefs, "show_header_speed", True):
        parts.append(f"UE NAV | {_format_speed(prefs)}")
    if getattr(prefs, "show_header_tutorial", True):
        parts.append(_controls_short(prefs))
    return " | ".join(parts) if parts else None
