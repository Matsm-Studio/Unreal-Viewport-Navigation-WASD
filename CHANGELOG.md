# 1.6.5

Version **1.6.5** expands Unreal Viewport Navigation with optional game-engine-style editing shortcuts, faster access to Blender tools, more reliable orbit controls, new centering options, and a reorganized settings interface.

## Engine Editor Shortcuts

Added optional **Object Mode editing shortcuts** inspired by **Unreal Engine, Unity, Godot and Maya**:

- **W / E / R** — Move / Rotate / Scale tools.
- **F** — Frame Selected.
- **Ctrl + D** — Duplicate and Move.
- **Unreal Engine profile:** G — Toggle viewport overlays.
- **Unity profile:** Q — Select Tool; X — Local / Global orientation.
- **Godot profile:** Q — Select Tool; T — Local / Global orientation; Y — Toggle snapping.
- **Maya profile:** Q — Select Tool.
- Added **Follow Navigation Preset** and independently selectable editor shortcut profiles.
- Editor shortcuts are **disabled by default**, so Blender's existing Object Mode shortcuts remain unchanged until users opt in.

## Quick Tools

Added a **Quick Tools** section in the Unreal 3D Viewport sidebar:

- Select, Move, Rotate and Scale.
- Frame Selected.
- Duplicate.

The buttons work independently of optional editor shortcut activation.

## Orbit & Centering

- Improved orbiting around selected objects to reduce view drifting and unexpected jumps.
- Corrected the **default vertical orbit direction**; added an optional **Reverse Orbit Y** setting.
- Added **F during Orbit** to center on the selection without changing the viewing angle or zoom.
- Added a configurable **Ctrl + Alt + F** viewport shortcut for centering without first entering Orbit.
- Added a **Center Orbit on Selection** button to the Unreal sidebar.
- Added **Auto-center on Orbit Start**, optional and disabled by default.
- Improved continued orbit movement immediately after centering.
- Improved orbiting in Camera View, mouse handling, optional wheel zoom, and orbit sensitivity settings.
- Improved **Esc** cancellation to restore the view from before the orbit action.

## Controls & Keyboard Shortcuts

- Added a built-in **Controls & Keyboard Shortcuts** guide in addon preferences.
- Shows the **currently configured** navigation, orbit, speed, centering and optional editing shortcuts.
- Reflects changes to custom bindings and navigation/editor profiles.
- Added English and Polish wording for the new controls guide, with English fallback in other interface languages.

## Redesigned Settings

- Reorganized preferences into dedicated sections for Navigation, Orbit & Centering, Key Bindings, Speed, Motion, Camera & Cursor, Display, Engine Editor Shortcuts, Advanced settings, and the Controls Guide.
- Added **Show All Settings** and **Collapse Sections** controls.
- **Only Navigation starts expanded**; all other sections, including Orbit & Centering, start collapsed.
- Replaced fragile custom key-picker interactions with Blender's native dropdown controls.
- Kept options for disabled features visible, but greyed out until those features are enabled.
- Improved grouping, option labels and in-panel shortcut explanations.

## Stability & Bug Fixes

- Fixed cases where the settings panel showed only some available options or displayed errors.
- Improved compatibility when Blender had cached older extension modules from another 1.6.5 package.
- Improved class registration and cleanup after unsuccessful addon startup.
- Isolated settings sections so an error in one group is less likely to hide the others.
- Improved show/collapse controls and the visibility of the Speed section.
- Improved shortcut conflict checks, keymap handling and extension reloading behavior.
- Preserved the existing WASD navigation workflow, navigation presets, camera settings, HUD, crosshair, and supported interface languages.
