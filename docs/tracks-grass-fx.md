# Grass FX

Grass FX replaces original AC grass with the one spawned procedurally around the camera, with higher density and a few other features like deformation. For the whole thing to work, list meshes which should spawn the grass.

### Spawn syntax

For any `…_MATERIALS`, there is also `…MESHES`, like `GRASS_MESHES`; both could be used at the same time.

```ini
[GRASS_FX]
; Spawning areas
GRASS_MATERIALS =            ; list of materials to spawn grass on top of
GRASS_MESHES =               ; same for meshes
OCCLUDING_MATERIALS =        ; list of occluding materials: for example, road mesh covering grass mesh, adding road material here would stop grass from showing through the road
OCCLUDING_MESHES =           ; same for meshes
OCCLUDING_MATERIALS_ALPHA =  ; list of smoothly occluding materials: imagine a piece of grass and a piece of sand on top, smoothly blending out showing grass, add sand material here for transition to work nicely
OCCLUDING_MESHES_ALPHA =     ; same for meshes
ORIGINAL_GRASS_MATERIALS =   ; list original grass materials to hide them if Grass FX is active
; NOTE: if you want to keep original 3dgrass (using ksGrass shader), then use an
; EMPTY line above with NO NAME after the "=" !!!
```

By default, grass would only spawn if surface color is right. It expects green-ish color, not too bright, not too dark. If needed, you can readjust it. Raise thresholds to make grass more patchy and uneven, lower thresholds for grass of all sorts of colors.

```ini
[GRASS_FX]
; Spawn mask settings
MASK_MAIN_THRESHOLD = 0.5  ; how saturated (with green) should the surface be (not real saturation, could be more than 1)
MASK_RED_THRESHOLD = 0.05  ; offsets target color from green to yellow and red, if set high enough
MASK_MIN_LUMINANCE = 0.02  ; minimum luminance to spawn grass on
MASK_MAX_LUMINANCE = 0.35  ; maximum luminance
```

Here is an example of settings for grass to spawn everywhere:

```ini
[GRASS_FX]
MASK_MAIN_THRESHOLD = -1
MASK_RED_THRESHOLD = 0
MASK_MIN_LUMINANCE = -1
MASK_MAX_LUMINANCE = 1
```

### Shape settings and trimming

Basic shape settings are simple to use:

```ini
[GRASS_FX]
SHAPE_SIZE = 1.0   ; general size
SHAPE_TIDY = 0.0   ; how tidy grass is (untidy grass in uneven, tilted more)
SHAPE_CUT = 0.0    ; how cut grass is
SHAPE_WIDTH = 1.0  ; grass width relative to its height
```

Higher size value lowers density. Default value, 1.0, corresponds to pretty low track grass.

To make grass change with time, you can set trim period and double values. First would be a value at the beginning of trim period, second value is for the end of trim period. Trim period could either be day of the week at which trimming occurs, or duration in days (with optional offset).

Here is one example, grass getting cut and then getting untidy:

```ini
[GRASS_FX]
TRIM_PERIOD = THURSDAY  ; grass will be cut each Thursday
SHAPE_SIZE = 0.5, 1.0   ; 0.5 at Thursday, 1 at Wednesday
SHAPE_CUT = 1.0, 0.5    ; very cut at Thursday, then less so
SHAPE_TIDY = 1.0, 0.5   ; very tidy at Thursday
```

Or, another example, grass growing over the course of the year:

```ini
[GRASS_FX]
TRIM_PERIOD = 365
SHAPE_SIZE = 4, 8
SHAPE_TIDY = 0
```

Also, each `SHAPE_…` number in there could be a track condition instead, so you can bind grass height to time of day or something. Although more sensible example could be to bind it to year progress with some custom LUT.

### Local adjustments

To alter the way grass looks in different areas, you can define up to four extra configurations, and then assign those configurations to different meshes. If you wonder, why only four, this way four configurations map perfectly on a local adjustments texture (with four channels) for more optimized processing. And it allows you to hand-paint adjustment map as well. Another approach could be to assing parameters to channels, but then, it would either need at least three massive textures, or we would only have four parameters.

Grass configurations have the same parameters as `[GRASS_FX]`: shape and color mask. Here is how I set grass on Brands Hatch:

```ini
; Configuration A for tidy weekly cut grass
[GRASS_FX_CONFIGURATION_A]
TRIM_PERIOD = THURSDAY ; grass will be cut each thursday
SHAPE_SIZE = 0.5, 1
SHAPE_CUT = 1, 0.5
SHAPE_TIDY = 1, 0.5

; Configuration B for trampled grass under spectators
[GRASS_FX_CONFIGURATION_B]
MASK_MAIN_THRESHOLD = 1.1 ; higher threshold means grass would spawn more rare, in patches
SHAPE_SIZE = 2
SHAPE_TIDY = 0

; Configuration C for wild grass
[GRASS_FX_CONFIGURATION_C]
MASK_MAIN_THRESHOLD = 0.3 ; slightly lower threshold for grass to grow more
TRIM_PERIOD = 365 ; grass slowly grows during the year
SHAPE_SIZE = 4, 8
SHAPE_TIDY = 0

; only up to a D config is possible atm
[GRASS_FX_CONFIGURATION_D]
...
```

And then, this is how it could be assigned to different meshes:

```ini
[GRASS_FX_ADJUSTMENT_...]
MATERIALS =  ; list of materials for configuration to be used for
MESHES =     ; list of meshes for configuration to be used for
MAP = A, 1   ; name of configuration and its intensity. with 0 intensity, basic [GRASS_FX] configuration will be used. anything in-between will blend values

; Adjustment can also use several configurations at once, with a custom blending
MAP = 0.8, 0.5, 0.2, 0.0  ; 80% of configuration A, then 50% of B, then 20% of C
```

With custom blend value, there is another possibility: if for some reason you would need 10 different grass heights, just make a configuration of grass that would be very high, and then assign 10% of it to one mesh, 20% of it to another and so on.

Adjustments will be blurred according to this parameter:

```ini
[GRASS_FX]
MASK_BLUR = 1  ; value values from 0 to 3, 0 disables blurring
```

`GRASS_FX_ADJUSTMENT` section can also have up to 8 local areas in a shape of circle or ellipse, allowing to fine-tune grass in a more localized area, or create gradients. Use Grass FX debug app to view adjustment app, it would help massively to set it up.

```ini
[GRASS_FX_ADJUSTMENT_...]
MESHES = …
MAP = A ; weight defaults to 1 if not set

EXTRA_0 = B, 0.5          ; same rules as for adjustment’s MAP value
EXTRA_0_CENTER = X, Z     ; X and Z are world coordinates (in meters); could also use X, Y and Z, in that case, Y would be skipped
EXTRA_0_RANGE = FROM, TO  ; FROM and TO are distances, in meters; FROM for inner (most intense) radius and TO for outer (not intense at all) radius. if FROM is higher than TO, area will be inverted, covering everything but inside of that circle
EXTRA_0_ASPECT_RATIO = 1  ; change from 1 to turn circle into ellipsis
EXTRA_0_ANGLE = 0         ; angle in degress to rotate ellipsis
EXTRA_0_OPACITY = 1       ; opacity of local area
```

Easier way to use it is to include “common/grass_fx.ini” and use `GrassFX_ExtraArea` mixin from it. Main advantage: no need to worry about indexes (“_0” part), plus instead of FROM and TO for range, that mixin provides a nice Fade variable. Here is an example from Brands Hatch, where I used it to switch grass from wild to trampled under spectators and around parking lot:

```ini
[INCLUDE: common/grass_fx.ini] ; for GrassFX_ExtraArea mixin

[GRASS_FX_ADJUSTMENT_...]
MATERIALS = grass_ext
MAP = C, 0.5 ; half wild grass

; areas of trampled grass, up to 8 per GRASS_FX_ADJUSTMENT section
@ = GrassFX_ExtraArea, Map = B, Center = "-350, 0, -300", Range = 140, Fade = 20, Aspect = 3.5, Angle = 40 ; spectators and parking along starting positions
@ = GrassFX_ExtraArea, Map = B, Center = "-459.04, 4.57, -192.12", Range = 30, Fade = 10 ; around helicopter
@ = GrassFX_ExtraArea, Map = B, Center = "-76.31, 12.47, -441.7", Range = 100, Fade = 20, Aspect = 2.5, Angle = 20 ; main spectator stands
@ = GrassFX_ExtraArea, Map = B, Center = "-171.61, 1.86, -461.88", Range = 60, Fade = 20, Aspect = 2, Angle = 20 ; parking in the back
```

You can also use `GRASS_FX_ADJUSTMENT` without any meshes, drawing rectangles defined by center, size and angle in degrees, like so:

```ini
[GRASS_FX_ADJUSTMENT_...]
CENTER = X, Y, Z  ; or just X and Z, world coordinates in meters
SIZE = X, Y, Z    ; or just X and Z, in meters
ANGLE = 0
MAP = A
```

It could make sense to set its `MAP` to something like all zeroes and then cover it with extra areas, for example. Or, you can attach a custom adjustments texture to it:

```ini
[GRASS_FX_ADJUSTMENT_...]
CENTER = X, Y, Z
SIZE = X, Y, Z
ANGLE = 0
TEXTURE = texture_name.dds  ; located next to config file
TEXTURE_OFFSET = 0, 0       ; texture offset in UV coordinates
TEXTURE_SCALE = 1, 1        ; texture scale
```

Red channel would set the share of A configuration, green — the share of B configuration and so on.

### Multilayer local adjustments (new)

For multilayer shaders with their txMask texture, you can bind different Grass FX adjustments to different channels of that mask, like so:

```ini
[GRASS_FX_ADJUSTMENT_...]
MATERIALS = grass, top2
USE_MULTILAYER_MASK = 1 ; use multilayer mask for adjustment
MASK_R = A, 3  ; red channel for wilder grass
MASK_G = -10   ; forcing base configuration for green channel
MASK_B = B, 3  ; blue channel for wildest grass
MASK_A = C     ; alpha channel for rare grass
```

This piece is taken from [Silverstone](https://github.com/ac-custom-shaders-patch/acc-extension-config/blob/master/config/tracks/ks_silverstone.ini#L1345) config. In short, instead of single `MASK` value, you can set `MASK_BASE` for areas with mask being fully black, MASK_R for red channel and so on.

Oh, and also, there is `USE_MULTIMAP_DETAIL_MASK` option to bind it to alpha of txDiffuse instead, for ksMultiMap… shaders. Same values too, although I think you would only need `MASK_BASE` and `MASK_A`.

### Custom textures

Grass FX uses a single texture atlas for the whole race track. The way it works, texture is sort of split into grid, default size: 16 columns and 1 row. Then, during generation, first row is used for regular basic and everywhere spawning grass. You can generate its textures using [this tool](https://github.com/ac-custom-shaders-patch/ac-grass-gen). And other rows could be mapped to other different grass pieces.

![img](https://i.imgur.com/vFkd1m8.png)

As you can see, one grass piece could take more than a single cell. Here is how config can load a new texture:

```ini
[GRASS_FX]
TEXTURE =  grass_fx/highlands.dds  ; located next to config file; if not found there, patch would look in its textures folder
TEXTURE_GRID = 8, 3      ; columns and rows
```

Note how some grass blades are bright green. This is how your texture can ask CSP to use surface color: set red and blue channels to black, and it’ll use surface color and green channel as brightness/AO value. If you don’t want grass to take its color from surface, just use a regular color, not bright green one. And also, make sure your color channels don’t stop where it’s fully transparent: separate alpha into its own channel, switch to RGB channels and make sure colors continue, or MIP layers are going to be messed up.

After loading a custom texture, you can define up to four custom texture groups. Each group can contain up to eight custom grass pieces, and those A/B/C/D grass configurations mentioned before, as well as base `[GRASS_FX]` configuration, all can set their own spawning chances for different grass groups.

Here is an example of a group:

```ini
[GRASS_FX_TEXTURE_GROUP_0]
; columns index start at 1, but rows index start at 0!
PIECE_0 = 1, 1 ; first piece stars with cell at (1, 1), that piece with a single yellow flower

PIECE_1 = 2, 1 ; second piece, takes a single cell as well

PIECE_2 = 1, 2, 2, 1 ; third piece, with yellow and white flower, taking 2×1 slots
PIECE_2_CHANCE = 0.1 ; would appear 10 times less often then first two pieces

PIECE_3 = 3, 1, 1, 2 ; piece taking 1×2 slots, the one with purple flowers
PIECE_3_CHANCE = 0.01 ; would appear 100 times less often
PIECE_3_SIZE_MULT = 1.2, 2 ; default size multiplier is based on size in cells, overriding
PIECE_3_WIND = 0.5 ; less affected by wind (default value is 1)
```

And to assign a texture group to a configuration, use this:

```ini
[GRASS_FX_CONFIGURATION_A]
TEXTURE_BASE_CHANCE = 1       ; chance of regular grass to spawn
TEXTURE_GROUP_0_CHANCE = 0.2  ; chance of first group to spawn
TEXTURE_GROUP_1_CHANCE = 0.1  ; chance of second group to spawn

; And now use it:
[GRASS_FX_ADJUSTMENT_...]
MATERIALS = grass, top2
MAP=A
```

Important note: custom types of grass only affect third generation pass onwards, so user would still see a lot of regular grass nearby. This way, some complex high grass or bushes won’t disappear after a few meters.

### About semi-transparent grass

By default procedural grass from Grass FX is not being rendered in G-buffer, thus cutting time almost in half. On most tracks with low grass and matte surfaces, it’s perfectly fine, however on some with either high grass or reflective surface behind it (like water), grass seems glitch and transparent. To fix that, use:

```ini
[EXTRA_FX]
FORCE_GRASSFX_GBUFFER_PASS = 1
```

There is also an option in Extra FX settings enabling that pass for all tracks.
