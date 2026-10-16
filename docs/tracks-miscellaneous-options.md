# Miscellaneous Options

A bunch of small things that might be interesting to configure.

### Spectator flashes

CSP update 0.1.77 adds camera flashes for track spectators triggered automatically in areas with spectators when something interesting is happening close to them. To activate them, use something like:

```ini
[CONDITION_...]
NAME = CROWD_FLICKERING_NEW
INPUT = SUN
LUT = (|0=0|85=0|85=1|180=1)

[SPECTATORS]
FLASH_INTENSITY = CROWD_FLICKERING_NEW
```

Or just set a fixed value instead of condition, like 1. Or set it to 0 if flashes are inappropriate on your track (or don’t, it’s the default value).

### Distant geometry

<img src="https://files.acstuff.ru/shared/QBdC/20220509-185038-shuto_revival_project_beta-ks_audi_a1s1.jpg" width=380>

Simply use `[Material_DistantGeometry]` from “materials_track.ini” to make a mesh visible no matter how far it is. However, if it’s too far, some Z-fighting issues might start to appear. In such case you can simply draw those meshes first (by arranging draw order accordingly) in the correct order with depth testing set to `LESSEQUAL`.

### Colorful refracting glass

<img src="https://files.acstuff.ru/shared/jGjR/20200728-035856.png" width=380>

Just look for `[Material_Glass]` in “materials_glass.ini”. `MaskPass` can make glass colorful (multiplying colors behing it), and `Refraction` parameter adds refraction. Also, `RefractionBias` can be used to blur things behing the glass for some sort of frosted glass effect. Only works with meshes with transparent flag.

### Light pollution at nights

You can raise the overall ambient base brightness at night around some given radius by a defined density. Only one such section per track config is supported atm.

```ini
[LIGHT_POLLUTION]
RELATIVE_POSITION = 0, 0, 0  ; all values in KM except density/color of course
RADIUS_KM = 0.5
DENSITY = 0.35               ; percent/100
COLOR = 0.95, 0.8, 0.7       ; r,g,b
```

### Aligning trees with underlying surface

<a href="https://acstuff.ru/u/comparison/7Nl" title="Click to see the comparison"><img src="https://files.acstuff.ru/shared/MuXY/20220611-185902-la_canyons-ks_bmw_m4.jpg" width=380></a>

If your track has a lot of hills with vegetation on them, it might look out of place if trees and bushes would be evenly lit on both sunny and shadowy side of a hill. Use this to connect lighting of vegetation with lighting of a surface below it:

```ini
[ALIGN_TREES_...]
SURFACE_MATERIALS = terrain_01
TREE_MATERIALS = shader:ksTree
```

It would slightly increase initial loading time, but after that the computed data would be cached.

### Fix for tree triangles aligning with view direction

<a href="https://acstuff.ru/u/comparison/1FA" title="Click to see the comparison"><img src="https://files.acstuff.ru/shared/wozy/20220611-191114.png" width=380></a>

While new trees are still in development, here is a cheap and easy fix hiding tree triangles aligned with camera view and looking as thin lines because of that:

```ini
[SHADER_REPLACEMENT_...]
MATERIALS = shader:ksTree?
MATERIAL_FLAG_0 = 1
```

### Double-biased shadows

If you see shadows on your track getting detached from objects that cast them, an easy way to fix the issue would be to use double-sided biased shadows:

```ini
[SHADER_REPLACEMENT_...]
MATERIALS = building?, box?
DOUBLE_FACE_SHADOW_BIASED = 1
```

You can just use “?” for materials to apply it to everything, but it might work out better to only apply it to objects that need it and avoid setting it for large horizontal surfaces or objects containing of two planes back to back with no space between them (shadows for those might look worse with that option).

### Tiling fix

<a href="https://acstuff.ru/u/comparison/UjP" title="Click to see the comparison"><img src="https://files.acstuff.ru/shared/ZvJr/20220611-191813-ks_silverstone1967-ks_bmw_m4.jpg" width=380></a>

Tired of textures with obvious tiling? Here is a fix that’s been in CSP since very first builds (that’s why it’s so unconventionally looking):

```ini
[SHADER_REPLACEMENT_...]
MATERIALS = grass-shad
PROP_... = ksAlphaRef, -193
```

Works for:
- ksMultilayer;
- ksMultilayer_fresnel_nm;
- ksPerPixelMultiMap_NMDetail;
- ksPerPixelMultiMap_AT_NMDetail;
- nePerPixelMultiMap_parallax;
- nePerPixelMultiMap_tessellation.

Also, `ksMultilayer_fresnel_nm4` and `ksMultilayer_objsp_nm4` have a separate option for it. And if you’re just using `ksPerPixel` and want to fix tiling, just switch it to a shader with a fix:

```ini
[SHADER_REPLACEMENT_...]
MATERIALS = my_material
SHADER = ksPerPixel_tilingfix
```

### Per-pixel fog for large low-poly meshes

Currently by default most of shaders calculate fog in vertex shader, resulting in fog looking weird if meshes are too lowpoly. Usually those lowpoly meshes use `ksPerPixel` shader, so you can simply switch to a shader with per-pixel fog:

```ini
[SHADER_REPLACEMENT_...]
MATERIALS = my_material
SHADER = ksPerPixel_ppfog
```

Other shaders using per-pixel fog:

- ksPerPixel_horizon (used by `[Material_Horizon]`, material meant for those tube-like meshes encircling tracks);
- ksPerPixel_tilingfix;
- smWaterSurface.

### Spotlights

If you have a simple light emitter mesh used for spotlight, there is an option to boost its emissiveness if camera is right in front of it:

```ini
[SHADER_REPLACEMENT_...]
MATERIALS = spotlight_emissive
PROP_... = ksAlphaRef, -193
```

Available for:

- ksPerPixel;
- ksPerPixelAlpha;
- ksPerPixelAT.

### Flammable materials

Some materials can be set on fire:

https://github.com/ac-custom-shaders-patch/acc-extension-config/assets/3996502/4d9fe189-7c5c-4784-ab51-4ed6256f0a35

To activate, add to your `[SHADER_REPLACEMENT_...]`:

```ini
ATTRIBUTE_0 = ParticlesFX.Flammable, 1
```

Or simply use `[Material_Bale]` from “materials_track.ini”. Currently only hay material gets darker as it burns, let me know if any other shaders need that behavior. And preferably consider keeping flammable meshes relatively simply, it does a bit of raycasting for flames spreading and what not.
