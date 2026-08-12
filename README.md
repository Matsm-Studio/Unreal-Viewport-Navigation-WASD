# Unreal Viewport Navigation - WASD 1.5.5

Bring Unreal Engine-style viewport navigation to Blender.

Unreal Viewport Navigation replaces Blender's default viewport navigation workflow with controls inspired by Unreal Engine, making the transition between game development and 3D content creation faster and more intuitive.

> This is an independent community extension by Matsm Studio. It is not affiliated with or endorsed by Epic Games, Inc. Unreal Engine is a trademark or registered trademark of Epic Games, Inc.

## Features

- Right Mouse Button + Mouse Look navigation.
- WASD, Arrow Keys, combined or fully custom movement controls.
- Q / E vertical movement by default.
- Shift Sprint mode with configurable multiplier.
- Ctrl Precision movement for slower, accurate navigation.
- Adjustable movement speed and mouse sensitivity.
- Mouse wheel speed control.
- Configurable acceleration, braking and Motion smoothing.
- Adjustable Motion update rate.
- Camera navigation while working in Camera View.
- Orbit Around Selection with **Alt + Right Mouse Button + Mouse Movement** by default.
- Optional camera-frame protection during orbit.
- Navigation profiles for Unreal Engine, Blender, Maya, Unity, Godot and Custom.
- Fully configurable navigation and orbit shortcuts.
- Shortcut conflict checker for Blender and other add-ons.
- Optional crosshair system with Cross, Cross + Dot, Dot, Circle and Filled Circle styles.
- Optional viewport speed display and control hints.
- Multiple HUD positions, including Split Top / Bottom mode.
- Adjustable HUD size and opacity.
- Metric and imperial speed units.
- Automatic settings saving between Blender sessions.
- 15 interface languages.

## Default Controls

| Input | Action |
|---|---|
| Hold RMB + move mouse | Look around / navigate |
| W / A / S / D | Move |
| Q / E | Move down / up |
| Shift | Sprint |
| Ctrl | Precision movement |
| Mouse Wheel | Adjust movement speed |
| Alt + RMB + move mouse | Orbit around the selected object |
| Release RMB or press Esc | Stop navigation |

Controls can be changed in the add-on preferences.

## Customization

Open **Edit > Preferences > Extensions/Add-ons > Unreal Viewport Navigation**.

The add-on includes settings for:

- Interface language.
- Program / Engine Profile.
- WASD, Arrow Keys, combined or Custom movement layouts.
- Navigation mouse button and optional additional navigation key.
- Custom Forward, Backward, Left, Right, Up and Down keys.
- Sprint and Precision keys and speed multipliers.
- Movement speed and mouse sensitivity.
- Acceleration, braking, smoothing and update rate.
- Camera View navigation.
- Orbit shortcut, sensitivity and camera protection.
- Crosshair visibility, style, size and thickness.
- HUD visibility, position, size and opacity.
- Speed display and control hints.
- Speed units and cursor behavior.

The most frequently used settings are shown first. Less common options are organized into collapsible sections to keep the interface clean.

## Navigation Profiles

Quickly switch between configurations for:

- Unreal Engine
- Blender
- Maya
- Unity
- Godot
- Custom

Profiles apply real navigation settings and controls. Custom mode allows individual key assignment.

## Camera Navigation and Orbit

Camera View can use the same navigation controls to move the active camera directly.

Orbit Around Selection is enabled by default. Hold **Alt + Right Mouse Button** and move the mouse to orbit around the selected object. Optional camera protection helps prevent accidental changes to an active camera shot.

## Motion System

The Motion system controls how navigation accelerates and brakes. You can choose a fast, responsive feel or smoother movement by adjusting acceleration, braking and update rate. Immediate Stop can prevent unwanted sliding after movement keys are released.

## Viewport Information

Navigation information can be displayed in the header or as a viewport overlay at:

- Top Left
- Top Right
- Bottom Left
- Bottom Center
- Bottom Right
- Split Top / Bottom

Speed and control hints can be enabled independently.

## Languages

The interface supports 15 languages:

English, Polish, German, Spanish, French, Italian, Brazilian Portuguese, Russian, Japanese, Simplified Chinese, Ukrainian, Czech, Dutch, Turkish and Korean.

## Why This Add-on?

Many artists and game developers work in both Blender and Unreal Engine. Unreal Viewport Navigation reduces the friction between the two applications by providing familiar controls, configurable movement behavior and a workflow designed around fast viewport navigation.

## Compatibility

**Blender 4.2 and newer.**

The extension requires Blender 4.2+ and is intended for newer compatible Blender releases as well.

## Installation

1. Download the release ZIP.
2. Open **Edit > Preferences > Extensions** in Blender.
3. Choose **Install from Disk** and select the ZIP.
4. Enable **Unreal Viewport Navigation - WASD**.
5. If another add-on uses the same shortcuts, use **Check Conflicts** in the add-on preferences.

## Website

Official GitHub repository:
https://github.com/Matsm-Studio/Unreal-Viewport-Navigation-WASD

## Support & Bug Reports

Report bugs, compatibility problems and feature requests here:
https://github.com/Matsm-Studio/Unreal-Viewport-Navigation-WASD/issues

When reporting a problem, include your Blender version, operating system, active profile, custom shortcuts if used, and exact reproduction steps.

## Author

Matsm Studio

## License

GPL-3.0-or-later. See `LICENSE`.
