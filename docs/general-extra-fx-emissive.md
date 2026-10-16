# Extra FX Emissive

With 0.1.79 and Extra FX enabled both cars and tracks now can set emissive meshes to cast actual light on geometry around them. Pretty much all the shaders supported, even skinned meshes:

<a href="https://gfycat.com/PartialLastingBovine"><img src="https://thumbs.gfycat.com/PartialLastingBovine-size_restricted.gif"></a>

### Syntax

```ini
[EXTRA_FX_EMISSIVE_...]
MESHES = …               ; list of meshes
MATERIALS = …            ; list of materials
DIGITAL_INSTRUMENTS = ?  ; filters for digital instruments (for most of them,
    ; names of sections in “digital_instruments.ini”), only for cars
RANGE = 0.1              ; range in meters (by default 0.08 for cars and 5 for tracks)
COLOR = 1                ; optional brightness multiplier (could be an RGBA value)
DIRECTED = …             ; set for 0 for point light and 1 for directed light, or to
    ; something in-between (by default guessed based on mesh shape)

; Optional optimization flags for cars:
INTERIOR_ONLY = 1        ; show up for interior views only
EXTERIOR_ONLY = 0        ; show up for exterior views only

; Optional advanced tweaks for more complex cases
EMISSIVE_TWEAK = 1       ; extra tonemapping for emissive color to balance things out
    ; (set to 0 to disable, set above 1 to further reduce effect or large emissive value)
MIP_BIAS = 0             ; MIP bias for texture (increase for smoother light)
IGNORE_TEXTURE_COLOR = 0 ; set to 1 to use COLOR and emissive color only

; Optional distribution settings (can affect performance):
COVERAGE = 3             ; samples density, by default 3 for cars and 2 for tracks (actual
    ; number of samples is controlled by mesh area, light range and coverage)
SAMPLES_LIMIT = 100      ; upper limit for number of samples to make sure generation won’t
    ; take huge amount of time, by default 400 for tracks
SPLIT_ELEMENTS = 0       ; split meshes into elements before generating samples,
    ; by default 1 for tracks
SPLIT_THRESHOLD = …      ; set to something above 0 to weld vertices within that distance
    ; before splitting elements
NORMAL_SHIFT = 0         ; increase to move light producing samples away from surface alogn
    ; normals (use it if surroundings are too dark)
COVERED_BY = …           ; stop emissive if a mesh with given name is visible
```

### Important notes

![Screenshot](https://files.acstuff.ru/shared/2hKr/20220919-164050-spa-pagani_huayra.jpg)

- For almost all cases, simple `[EXTRA_FX_EMISSIVE_...] MESHES = …` would work, but some options can help with cases more complex. The effect should work well with multichannel emissives, braking disks, glowing meshes (by default “gt3_exhaust_glow.ini” already switched to using glowing emissive when available).

- If you have a light source emulating glowing emissive, add `DISABLE_WITH_EMISSIVE_LIGHT = 1` to it so it would only work when Extra FX glowing emissives effect is disabled, avoiding double glow.

- You can attach this effect to rear view mirrors, but please don’t do this for now, this part will be auto-guessed with the next CSP update.

- Distributing glowing samples on a mesh can take some time, but it only happens once per mesh and then the result should be cached in “assettocorsa/cache”.

- When working on tracks, don’t use the effect for large lights illuminating most of the screen, instead consider using it for something like windows glowing at night or colorful advertising signs. When camera is covered by such light, some visual glitches might occus, and performance might get worse. Here are some possible use cases on Spa: [1](https://acstuff.ru/u/comparison/9d8), [2](https://acstuff.ru/u/comparison/fr2).

- If you’re setting up glow from car LEDs, you might run into problem with LEDs covering each other (for example, the case with 488 GT3). Use `COVERED_BY = …` (like `COVERED_BY = RPM_LED_LIMITER_1`) to stop underlying LED from illuminating things up when covered.

- To get headlight meshes to cast light within a headlight, you can set its surface to mask G-buffer without blocking it with `[EXTRA_FX] MASK_GBUFFER = headlight_glass_mesh_name` (it should get SSLR to work). [More on that here](general-extra-fx-flags.md).
