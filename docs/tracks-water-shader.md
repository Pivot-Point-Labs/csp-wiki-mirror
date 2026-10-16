# Water Shader

### Water shader

<img src="https://files.acstuff.ru/shared/SOUG/20220611-180033.png" width=380>

To use new CSP water shader, add:

```ini
[INCLUDE: common/materials_track.ini]

[Material_Water]
Materials = your_water_material
Type = POND                     ; Available values: LAKE, POND, POOL, SEA, OCEAN
```

For more parameters and detailed documentation open “extension/config/tracks/common/materials_track.ini” and look for “[TEMPLATE: Material_Water]”: all new parameters will be shown there with detailed description.

### Water drain

<img src="https://files.acstuff.ru/shared/hpXF/20220611-175637.png" width=380>

For water drains filling with rain use `[Material_WaterDrain]` from the same “extension/config/tracks/common/materials_track.ini”. See more: https://github.com/ac-custom-shaders-patch/acc-extension-config/blob/28463fa401fc91a0841a5757db431fd3ad9970ec/config/tracks/common/materials_track.ini#L399

### Caustics

To activate light bounding back from water, set `[BOUNCED_LIGHT] CAUSTICS = 1` (requires bounced light from Extra FX to be active).
