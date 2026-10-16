# Miscellaneous Options

A bunch of small things that might be interesting to configure.

### Windscreen banners

<img src="https://files.acstuff.ru/shared/PR4w/20220611-193050.png" width=380>

If your car has a semi-transparent windscreen banner, consider using `[Material_WindscreenBanner]` from “materials_interior.ini”. It would arrange everything including proper RainFX integration, optional background blurring, colorful shadows and ambient and masking pass.

### Meshes with delayed render for interior cameras

```ini
[INTERIOR_DELAYED_RENDER]
MESHES =
MATERIALS = shader:ksWindscreen?, shader:ksBrokenGlass?
```

These meshes would be rendered last, that way they wouldn’t cause problems with ExtraFX and such.

### Side bits of glass

<a href="https://acstuff.ru/u/comparison/APi" title="Click to see the comparison"><img src="https://files.acstuff.ru/shared/bhrc/20220611-211044-ks_silverstone1967-lotus_49.jpg" width=380></a>

Material `[Material_Glass]` has an extra feature for rendering certain areas facing a local point differently. It can be useful for cars like Lotus Type 49, making edges of glass look differently by blurring things behind it. Here is how to set it up:

```ini
[INCLUDE]
INCLUDE = common/materials_glass.ini   ; template for it

[Material_Glass]
Materials = glass_material
PROP_... = extEdgePosL, 0, 1, 0      ; look-at point
PROP_... = extEdgeThreshold, 0.5     ; look-at threshold
PROP_... = extEdgeRefractionBias, 4  ; how much to blur things behind glass
```

With that, all surfaces facing look-at point above threshold would get that frosted glass effect. set `extEdgeRefractionBias` to a negative value to debug the look-at values.

Those are default settings for cars with driver inside encosed cockpit (computed based on car heightmap).
