# Fake Shadows FX

Since v0.1.37, Fake Shadows FX in Custom Shaders Patch bakes car shadows (which are stored as “body_shadow.png” in original AC) on-fly during first loading, to make sure shadows are baked with correct settings. To save time, it also stores them in cache.

By default CSP caches shadows for cars (so every skin would use the same shadow), and use all non-transparent shadow casting meshes for baking.

### Syntax

```ini
[FAKE_SHADOWS_FX]
DISALLOW_REBAKING = 0 ; set to 1 to prevent CSP from generating new fake shadows (not recommended)
CUSTOM_SKIN_SHADOWS = 0 ; change to 1 to make CSP cache shadows for different skins separately (could be
                        ; used in single skin’s extension config), for skins with custom geometry
EXCLUDE_FROM_BAKING = material:EXT_glass ; list of nodes and meshes to exclude from baking
```

That’s all the settings! I would really want for them to look the same across all cars this time.
