# Changelog

## 1.1.1

- Fixed mouse-look rotation being limited by the screen boundaries by ensuring the navigation operator properly grabs the cursor.

## 1.1.0

- Removed the perceived RMB navigation delay: mouse movement or a navigation-key press now activates navigation immediately, while a stationary short click still opens Blender's context menu.
- Added an optional **Enable RMB Click/Hold Separation** preference. Disable it to restore immediate RMB navigation.

- Restored Blender's standard RMB context menu on a short click.
- RMB hold now enters navigation mode after a configurable delay.
- Added an RMB hold-duration slider to the add-on preferences.
- Reduced the default RMB hold delay and limited its adjustable range for faster navigation.
- Added a Reset to Defaults button for all add-on preferences.

## 1.0.1

- Kept the working custom viewport navigation engine from the previously working build.
- Split the former monolithic `__init__.py` into focused modules.
- Removed the legacy `bl_info`; metadata is provided only by `blender_manifest.toml`.
- Replaced fallback preference searching with Blender's standard add-on preference access.
- Removed the custom JSON settings file, loading timer and automatic disk writes.
- Added an explicit **Save on Disk** button using Blender's standard preference-save operator.
- Removed file-system permissions because the extension no longer writes custom files.
- Replaced `_discover_keymap_specs` with a clear, explicit keymap list while preserving multi-mode viewport coverage.
- Added instructions to report bugs on the extension's Blender Extensions page.
