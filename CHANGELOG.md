# Changelog

## 1.5.5

The biggest Unreal Viewport Navigation update so far. This release follows the previous public version, **1.1.1**.

### Navigation and controls

- Improved RMB-based game-editor-style viewport navigation.
- Added configurable navigation mouse button and optional additional navigation key.
- Added movement layouts for WASD, arrow keys, both layouts and fully custom movement keys.
- Added separate custom bindings for forward, backward, left, right, up and down.
- Added configurable Sprint and Precision keys.
- Added configurable speed-increase and speed-decrease controls.
- Added navigation while compatible Blender tools are active.
- Preserved short RMB click / hold separation with an adjustable hold delay.

### Motion

- Reworked motion smoothing so acceleration is clearly noticeable.
- Added separate time-to-full-speed and braking-time controls.
- Added immediate-stop behavior to prevent unwanted sliding after movement keys are released.
- Added configurable motion update rate.
- Added separate Sprint and Precision speed multipliers.

### Camera and orbit

- Improved navigation while looking through the active camera.
- Added optional direct control of the active camera in Camera View.
- Added Orbit Around Selection.
- **Alt + RMB + mouse movement** orbits around the selected object by default.
- Default orbit shortcut is **Alt + RMB**.
- Added configurable orbit mouse button and additional orbit key.
- Added active-camera frame protection for orbiting.
- Added Esc restore behavior when protected camera orbit is cancelled.

### Presets and custom key bindings

- Added navigation profiles for **Unreal Engine, Blender, Maya, Unity and Godot**.
- Added a **Custom** profile for fully user-defined controls.
- Profiles apply real shortcut, motion, camera and orbit settings.
- Editing a shortcut manually switches the active profile to Custom.
- Added a dedicated Key Bindings section so shortcut assignment is kept in one place.
- Added an always-visible **Restore Default Keys** action.
- Added shortcut-conflict checking for Blender and add-on keymaps.

### Preferences and usability

- Redesigned Add-on Preferences to be more compact and easier to understand.
- Added a Quick Setup area with Interface Language and Program / Engine Profile selectors.
- Moved less-used options into collapsible sections.
- Reworded ambiguous controls and added short in-context explanations.
- Kept the project-page action permanently visible.
- Added a full reset for all add-on preferences.
- Added explicit Save on Disk support using Blender's standard preference-save operator.

### Viewport information and cursor

- Added configurable navigation information with speed and control hints.
- Added positions for viewport header, top-left, top-right, bottom-left, bottom-center and bottom-right.
- Added split top / bottom mode.
- Added independent toggles for speed and control hints.
- Added HUD text size and opacity controls.
- Added Cross, Cross + Dot, Dot, Circle and Filled Circle crosshair styles.
- Added configurable crosshair size, center gap, thickness and color.
- Added cursor hiding and cursor-position restoration options.

### Languages

- Expanded the interface to **15 languages**: English, Polish, German, Spanish, French, Italian, Brazilian Portuguese, Russian, Japanese, Simplified Chinese, Ukrainian, Czech, Dutch, Turkish and Korean.
- Added translated labels for the most important selectors, controls, orbit settings and viewport information.

### Project and packaging

- Project page: https://github.com/Matsm-Studio/Unreal-Viewport-Navigation-WASD
- Bug reports: https://github.com/Matsm-Studio/Unreal-Viewport-Navigation-WASD/issues
- Removed obsolete development-only compatibility code and unused Python helpers from the release package.
- Release package contains no `__pycache__`, `.pyc`, test files or bundled third-party libraries.
- Cleaned the Blender extension manifest for publication.

## 1.1.1

- Fixed mouse-look rotation being limited by the screen boundaries by ensuring the navigation operator properly grabs the cursor.
