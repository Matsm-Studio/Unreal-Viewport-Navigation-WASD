# Unreal Viewport Navigation 1.1.0

Unreal Engine-style viewport navigation for **Blender 4.2 and newer**. The extension uses its own modal navigation engine and does not invoke Blender's built-in Walk/Fly operator.

> This is an independent community extension by Matsm Studio. It is not affiliated with or endorsed by Epic Games, Inc. Unreal Engine is a trademark or registered trademark of Epic Games, Inc.

## Features

- Short RMB click opens Blender's standard context menu; hold RMB to navigate.
- Adjustable RMB hold-duration threshold in the add-on preferences.
- Reset to Defaults button for restoring all add-on settings.
- Hold RMB and use WASD, arrow keys or both for game-editor-style viewport navigation.
- Q / E vertical movement, Shift sprint and Ctrl precision movement.
- Optional navigation while another compatible tool is active.
- Adjustable mouse sensitivity, acceleration and deceleration.
- Optional GPU-drawn crosshair with Cross, Cross + Dot, Dot and Circle styles.
- Independent speed and control-guide text in the viewport header.
- Speed units: BU/s, m/s, cm/s, mm/s, km/h, ft/s and mph.
- Metric and imperial speeds respect **Scene > Units > Unit Scale**.
- English interface with a built-in Polish option.

## Preferences and saving

The extension stores settings only in Blender's normal add-on preferences. It does not create a JSON settings file, does not write to a custom configuration path, and does not trigger preference saving after every change.

To explicitly make the current Blender preferences persistent, press **Save on Disk** in the extension preferences. This uses Blender's standard preference-save operator.

## Controls

| Input | Action |
|---|---|
| Hold RMB + move mouse | Look around |
| W / A / S / D or Arrow keys | Move |
| Q / E | Move down / up |
| Shift | Sprint |
| Ctrl | Precision movement |
| Mouse wheel | Change movement speed |
| Release RMB or press Esc | Stop navigation |

## Installation

1. Disable other RMB navigation add-ons to avoid keymap conflicts.
2. Install this ZIP in Blender's Extensions/Add-ons preferences.
3. Enable **Unreal Viewport Navigation**.
4. The recommended keymap is **Industry Compatible**.

Settings are available in:

- **Edit > Preferences > Extensions/Add-ons > Unreal Viewport Navigation**
- **3D Viewport > N sidebar > Unreal**

## Reporting bugs

Report bugs, compatibility problems and feature requests on the Unreal Viewport Navigation page on Blender Extensions.

## License

GNU General Public License v3.0 or later.
