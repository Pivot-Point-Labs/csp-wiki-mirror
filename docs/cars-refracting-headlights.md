# Refracting Headlights

Refracting headlights replace the regular transparent cover material with a custom shader that simulates refraction through the lens, with the inner volume of the headlight (reflectors, bezels and bulbs) baked into a small set of textures and ray-marched at runtime. Compared to a normal transparent shader, this gives a much more believable depth, parallax and lit-up bulbs without any extra geometry or draw calls per frame. [A YouTube video showing the effect in action](https://www.youtube.com/watch?v=UlPzYAlPEy4).

Each headlight is defined as a set of outer cover meshes (the transparent lens) and a set of inner meshes hidden behind them. On first load CSP renders a few orthographic snapshots of those meshes (surface normals, inner color, depth, normals mask and an emissive map for bulbs) and uses them to fake refraction, internal reflections and glow at runtime. Maps are usually shared between left/right headlights of the same car and can be cached on disk between sessions.

### Requirements

- Outer cover meshes must originally use a transparent shader. Their material is replaced with `smRefractingCover` (or `smRefractingCover_taa` when forward TAA is available).
- At least one inner mesh must be specified, otherwise the headlight is skipped with a warning.
- A single mesh can only belong to one refracting headlight; if it is already used by another `[REFRACTING_HEADLIGHT_…]` section it is ignored.
- Please consider keeping resolution and number of sections low, and using mirroring as much as possible. Each entry takes a few MBs of RAM and VRAM, and with emissive channels, in most cases, a single entry for the front and another for the rear lights should be enough.

### Syntax

Define one section per headlight. Most numerical parameters can be tuned live from the in-game Reflections FX debug app (Refraction tab) and copied back into config with the “Copy settings to clipboard” button.

```ini
[REFRACTING_HEADLIGHT_0]
ACTIVE = 1                       ; set to 0 to disable this headlight
SURFACE = headlight_glass_L      ; outer transparent cover meshes (required)
INSIDE = headlight_inner_L       ; meshes behind the cover used to bake the inner maps (required)
INSIDE_BULBS = bulb_L            ; optional, meshes treated as bulbs (a brighter, separately blurred map)
OVERLAY = headlight_decals_L     ; optional, extra layer baked on top of the cover (for example, something like electric tape covering some of the glass)
SURFACE_LODS = headlight_glass_L?  ; optional, extra cover meshes from lower LODs to also receive the shader
BLEND_MODE = OPAQUE              ; blend mode of the refracting material; use ALPHA when REFRACTION_MASKING = 1

; Reference space (origin/direction/mirror are interpreted in this space)
RELATIVE_TO = CAR                ; one of CAR, SURFACE, PARENT, PARENTS_PARENT, or a node name; SURFACE/PARENT
                                 ; are useful for animated/openable headlight covers

; Placement (auto-guessed from the SURFACE meshes if not all five are given)
ORIGIN = 0.7, 0.7, 1.8           ; center of the headlight in the chosen reference space
RADIUS = 0.12                    ; half-size of the area covered by the lens, in meters
DIRECTION = 0, 0, 1              ; outward direction of the lens (will be normalized)
MIRROR_POS = 0, 0, 0             ; a point on the symmetry plane between left and right headlights
MIRROR_DIR = 1, 0, 0             ; normal of that symmetry plane

; Glass / refraction
IOR = 1.5                        ; index of refraction of the cover
F0 = 0.8                         ; base Fresnel reflectivity of the cover
ABSORPTION = 0.02                ; how much light is absorbed inside the volume (foggy glass)
NM_SHARE_EXT = 0                 ; how much the original normal map of the cover affects external refraction (0–1)
NM_SHARE_INT = 0.6               ; how much it affects the inner reflections (0–1)
NORMALS_BIAS = 0, 0, 0           ; bias added to baked inner normals
LOD_BIAS = -0.5                  ; mip LOD bias for sampling baked inner textures
SIDE_FALLOFF = 0                 ; softens the look near the edges of the cover
EXTRA_SIDE_THICKNESS = 0         ; extra simulated glass thickness towards the edges
GLASS_EXTRA_THICKNESS = 0.005    ; additional uniform glass thickness, in meters
IOR_FLYOUT_FLAT = 0              ; lerps IOR towards 1 (flat lens), 0 keeps it physical, 1 disables refraction;
                                 ; not physically correct, only meant for stylized flat lenses
RAYTRACE_STEP_START = 0.072      ; initial ray-march step (relative to RADIUS)
RAYTRACE_STEP_INCREASE = 1.05    ; geometric growth factor of subsequent ray-march steps

; Reflections inside the volume
REFLECTIVENESS_MULT = 10         ; boost for sharp reflections off the baked inner geometry
REFLECTIVENESS_DIFFUSE_MULT = 60 ; boost for the diffuse part of those reflections
REFLECTIVE_GAMMA = 1             ; gamma applied to reflective response curve
BOUNCED_BACK_MULT = 0.4          ; intensity of light bouncing back off the cover from inside
INNER_SPECULAR = 10              ; specular intensity of inner surfaces
INNER_SPECULAR_EXP = 800         ; specular sharpness (`ksSpecularEXP`-equivalent) of inner surfaces
AMBIENT_MULT = 0.25              ; how much ambient light reaches the inner volume

; Color
GLASS_COLOR = 0.5, 0.5, 0.5      ; tint applied by the cover, RGB
DIFFUSE_MAP_MULT = 1             ; multiplier for the baked inner diffuse map
DIFFUSE_MAP_FILTER_MULT = 1      ; multiplier for using the diffuse map as a color filter for emissives
EXTRA_GLASS_COLORIZATION = 1     ; extra glass tint pass; default is 1 only if DIFFUSE_MAP_FILTER_MULT is not set

; Emissive (bulbs glow inside the headlight)
BASE_EMISSIVE_K = 0.05           ; constant baseline emissive
EMISSIVE_MULT = 1                ; multiplier for the inner emissive contribution
GLASS_EMISSIVE_MULT = 0.25       ; how much the cover itself glows from inner emissives

; Bulbs (small bright dots picked up from the inner emissive map)
BULB_COLOR = 1, 1, 1             ; tint applied to detected bulbs
BULB_REFLECTION_K = 0.2          ; reflection adjustment for bulbs (negative values reduce them)
BULB_BLUR_K = 2                  ; blur multiplier for the bulbs map

; Surface masking (using the outer cover’s own textures)
USE_NORMAL_ALPHA = 0             ; take alpha for refraction shape from `txNormal` of the cover; defaults to 1
                                 ; if any cover material uses an alpha-from-normal shader
REFRACTION_MASKING = 0           ; use diffuse alpha as a refraction mask (transparent parts skip refraction);
                                 ; only works when USE_NORMAL_ALPHA = 1, also forces ALPHA blend mode at runtime

; Sharing and caching
SHARED = 1                       ; share computed maps between sections of the same car with identical settings;
                                 ; defaults to 0 if DYNAMIC_EMISSIVE_MAP = 1
DYNAMIC_EMISSIVE_MAP = 0         ; set to 1 to re-bake the inner emissive map when emissives inside change at
                                 ; runtime (more expensive, disables sharing by default)
RESOLUTION_MULT = 1              ; multiplier for baked map resolution, clamped to 0.25–4 (default base is 256 px)
```

### Custom bulbs

By default bulbs are detected automatically from the baked inner emissive map. To define them manually instead, use:

```ini
USE_CUSTOM_BULBS = 1             ; switch to manually defined bulbs
USE_COLORED_BULBS = 0            ; set to 1 to keep separate channels for differently-colored bulbs
MIRROR_3_AS_4 = 1                ; with multi-channel bulbs, right side uses channel 4 instead of 3 (similar to
                                 ; `emMirrorChannel3As4` in multi-channel emissives)
MIRROR_2_AS_5 = 0                ; same idea, channel 2 → channel 5 on the right side
CUSTOM_BULB_0 = 0.5, 0.5, 0, 0   ; (x, y, size, aspect): center in normalized 0–1 baked-map coordinates,
                                 ; size and aspect of the bulb shape; up to four bulbs are supported
CUSTOM_BULB_1 = …
CUSTOM_BULB_2 = …
CUSTOM_BULB_3 = …
```

### Linking inner emissives to the cover

The cover material has its own `ksEmissive`-style channels used by the shader to drive headlight glow and bulb intensity. To copy values from emissives on the inner meshes to those channels (so e.g. turning on the high beam inside lights up the cover too), define one or more `SYNC_EMISSIVE_…` blocks:

```ini
SYNC_EMISSIVE_0 = bulb_L                ; inner meshes whose emissive should drive the cover
SYNC_EMISSIVE_0_CHANNEL_IN = 0          ; channel(s) to read on the inner meshes (default 0 = ksEmissive)
SYNC_EMISSIVE_0_CHANNEL_OUT = 0         ; channel(s) to write on the cover meshes (default 0)
SYNC_EMISSIVE_0_MULT = 1                ; multiplier applied during the copy
```

`CHANNEL_IN` and `CHANNEL_OUT` accept either a single value or a list of equal length to remap multiple channels at once. If neither `SYNC_EMISSIVE_…` nor `SYNC_EMISSIVE_AUTO` is set, no copying happens.

```ini
SYNC_EMISSIVE_AUTO = 1           ; shortcut: automatically copy `ksEmissive` from all INSIDE meshes to the
                                 ; cover meshes with multiplier 1 (only used if no SYNC_EMISSIVE_… block is set)
```

When the synced inner meshes are tagged as `light_brakes` or `light_headlights` in their extra-FX flags, the same flags are propagated to the cover meshes automatically, so their glow reacts to the corresponding light state.

### Multiple headlights

Define one section per lamp (`[REFRACTING_HEADLIGHT_0]`, `[REFRACTING_HEADLIGHT_1]`, …). When two sections on the same car use identical settings (same hash), they share a single set of baked maps to save memory; this is enabled by default and can be turned off with `SHARED = 0`.

### Caching

Baking the maps takes a few frames on first load. With caching enabled in CSP settings (Reflections FX → refracting headlights cache), generated maps are stored on disk per car and reused on subsequent loads. The cache is invalidated automatically when section settings change.

### Tuning

The Reflections FX debug app exposes a Refraction tab with sliders for every parameter above, gizmos for `ORIGIN` / `DIRECTION` / `MIRROR_POS` / `MIRROR_DIR`, and previews of every baked map. Use it to dial in a headlight, then press “Copy settings to clipboard” to get a ready-to-paste `[REFRACTING_HEADLIGHT_0]` block.
