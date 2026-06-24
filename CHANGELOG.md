# Changelog

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
