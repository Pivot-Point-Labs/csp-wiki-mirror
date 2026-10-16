# Shader Replacements

Originally shader replacements were meant, well, for replacing shaders for existing models, but it grew further and further into much more than that, allowing to change material parameters and properties, textures, object parameters and sometimes even a bit of behaviour.

Main difference from things like `[MATERIAL_ADJUSTMENT_...]` for tracks or `[EMISSIVE_...]` for cars, shader replacements are completely static, applied once either during loading or after config change. This way, they themselves do not affect performance or waste any RAM (while dynamic `[MATERIAL_ADJUSTMENT_...]` is being updated each frame, for example). So for static changes, I’d highly recommend to use shader replacements.

One consequence of that difference though is that, if you change config and remove a `[SHADER_REPLACEMENT_...]` section, it wouldn’t restore original values.

### Syntax

```ini
[SHADER_REPLACEMENT_...]
ACTIVE = 1    ; set to 0 to disable the whole section (default value is 1)
SKINS = red?  ; list of skins to use replacement with (only for cars)

; First, targets, either materials or meshes (one thing to consider:
; for altering material properties, each mesh in MESHES would get its own material, thus
; increasing number of GPU calls, so it’s better to use MATERIALS where possible):
MATERIALS = tree?, texture:grass?.dds
MESHES = mesh_bush_?

; Optionally, a new shader:
SHADER = ksTree_ppshadows

; Shader can be set differently for different original shaders:
SHADER_OVERRIDE_0 = ksTree, ksGrass  ; if original is ksTree, use ksGrass instead
SHADER_OVERRIDE_... = ksPerPixelAT?, ksTree ; if original starts with "ksPerPixelAT", use ksTree

LEAVE_FUNCTIONAL_SHADERS = 1  ; keeps CSP-specific functional shaders unchanged when
                              ; replacing shader for everything else

; Material properties:
PROP_0 = ksAmbient, 0.4
PROP_1 = ksDiffuse, 0.5
PROP_... = ksEmissive, 1, 0, 0 ; as usual, you can use "..." to fill indices automatically

; Alternative KEY/VALUE way to set material properties:
KEY_0 = ksAmbient
VALUE_0 = 0.4
KEY_... = ksDiffuse   ; supports up to KEY_99/VALUE_99
VALUE_... = 0.5

; Textures, set with one of this ways (here, it’s better not to use "..." to make sure key
; would be paired with its value):
RESOURCE_0 = txDiffuse
RESOURCE_TEXTURE_0 = name_of_texture_in_kn5.dds ; TEXTURE refers to texture in original model

RESOURCE_1 = txNormal
RESOURCE_REF_1 = txDetailNM  ; REF refers to original texture in certain slot

RESOURCE_2 = txMaps
RESOURCE_COLOR_2 = 1, 1, 1 ; COLOR creates new 1×1 solid color texture

RESOURCE_3 = txDetail
RESOURCE_FILE_3 = custom.dds ; FILE refers to a texture on a disk, next to the config

FILL_MISSING_TEXTURES = 1 ; this option would automatically create missing textures, such
                          ; as txNormal (flat) or txMaps (white), to ensure non-broken look
FORCE_POINT_SAMPLER = 1       ; forces pixel texture sampler, if you have tiny texture and you
                              ; want to make it sharp and pixelated, not blurry
FORCE_MINUS_TWO_LOD_BIAS = 1  ; forces texture sampler with -2 LOD bias for sharper textures

; Material parameters (for details, scroll to "Different modes" section):
BLEND_MODE = ALPHA_BLEND   ; OPAQUE, ALPHA_TEST, ALPHA_BLEND, TRANSPARENT_AS_BLACK, ADD or ALPHA_ADD, MULTIPLY or ALPHA_MULTIPLY
CULL_MODE = OFF            ; DOUBLESIDED, FRONT_NO_MS, WIREFRAME, WIREFRAME_AA, FRONT_BIASED, SHADOWS_DOUBLE, SHADOWS_FRONT
DEPTH_MODE = NORMAL_FORCED ; NOWRITE, OFF, LESSEQUAL, LESSEQUAL_NOWRITE, NORMAL_FORCED
LINEAR_ALPHA_FIX = 1       ; fixes alpha blending in linear colorspace, values 0–3 (use only if things are bad)

; Shadow parameters:
CAST_SHADOWS = 1  ;* sets if mesh should cast shadows, either 0, 1 or TERRAIN:
                  ; 1 enables them constantly, TERRAIN only when the sun is low, to speed it up

CAST_DYNAMIC_SHADOWS = 1  ;* sets if mesh should cast dynamic shadows

DISTANT_SHADOWS = 1       ;* sets if mesh should cast distant (fourth cascade) shadows,
                          ; either 0, 1 or TERRAIN

SEMITRANSPARENT_SHADOWS = 1  ; for semi-transparent shadows, either 0, 1, TEXTURE or NORMALS:
                             ; 1 for solid semi-transparency, TEXTURE would consider texture,
                             ; NORMALS uses normals-based semi-transparency (with optional
                             ; extra parameters, e.g. "NORMALS, 1, 0")

; Double face shadows (although it might make shadows rendering a bit slower,
; I recommend to try it, it seems to improve shadows quite a lot by getting rid of lots of
; holes or peter-panning effect, especially for dashboards or with distance):
DOUBLE_FACE_SHADOW = 1         ; this one might — and, most likely, will — cause a lot of self-shadowing
DOUBLE_FACE_SHADOW_BIASED = 1  ; but this one is biased, so it would work nicely

; Masking pass (with it, mesh is rendered twice, first, with multiply blending mode and
; a custom type of shader to extract solid texture color, thus colorizing stuff behind it
; for proper colored glass look). Instead of setting values directly, consider using “materials_glass.ini”:
EXTRA_MASK_PASS = 1              ;* enables masking pass
EXTRA_MASK_PASS_COLOR = 0, 0, 0  ;* optional color offset, RGB, can be either positive or negative values
EXTRA_MASK_PASS_OPACITY = 2      ;* optional opacity adjustment for that colored glass pass
EXTRA_MASK_PASS_COLOR_MULT = 1, 1, 1  ;* optional color multiplier for masking pass
EXTRA_MASK_PASS_OPACITY_CLIP = 0      ;* optional opacity cutout threshold for masking pass

; Colorful shadowing (creates colored shadow for semitransparent surfaces, like stained glass). Works for car
; interior geometry. Instead of setting values directly, consider using banner material from “materials_glass.ini”:
COLORFUL_SHADOWING = 1                   ;* enables colorful shadowing, value sets intensity
COLORFUL_SHADOWING_COLOR = 0, 0, 0       ;* optional color offset
COLORFUL_SHADOWING_COLOR_MULT = 1, 1, 1  ;* optional color multiplier
COLORFUL_SHADOWING_OPACITY_CLIP = 0      ;* optional opacity cutout threshold

; Other parameters:
FIXED_EMISSIVE = 1  ; Weather FX can alter emissiveness to better simulate eye adaptation; use this
                    ; flag to disable that behaviour for given mesh (use only in very special cases
                    ; like with BLEND_MODE=MULTIPLY or mirrors; although mirrors get this flag automatically)
IS_TRANSPARENT = 1  ;* for that IsTransparent flag, to make sure mesh would be rendered last
IS_VISIBLE = 1      ;* sets mesh visibility, set to 0 to hide mesh
IS_EXTRA_PASS_TRANSPARENT = 1  ;* marks mesh as transparent in extra rendering pass
RENDER_LAST = 1     ;* renders mesh after other meshes in the same group
LAYER = 0           ;* mesh layer, which is also a minimum detail level mesh would be rendered at
LOD_IN = 0          ;* LOD in distance (mesh will be hidden if distance is lower), in meters
LOD_OUT = 500       ;* LOD out distance (mesh will be hidden if distance is bigger), in meters

DISABLE_FAR_PLANE_CLIPPING = 1  ;* when checking visibility against camera frustum, skip far plane, required
                                ; for distant geometry (with its custom shader) to work
INCLUDE_IN_CUBEMAP = 0          ;* set to 0 to exclude mesh from cubemap rendering
INCLUDE_IN_SECONDARY_VIEWS = 0  ;* set to 0 to exclude mesh from secondary views (mirrors, etc.)
FUR_LAYERS = 4      ;* number of fur layers, from 0 to 32

; Extra FX parameters (for Extra FX post-processing, require v0.3.0-preview356 or newer):
EFX_SKIP_GBUFFER = 0    ;* controls gbuffer rendering pass
EFX_MASK_GBUFFER = 0    ;* controls gbuffer masking
EFX_BLEND_GBUFFER = 0   ;* controls gbuffer blending
EFX_DELAYED_RENDER = 0  ;* controls delayed rendering

; Moving meshes in rendering order relative to other meshes:
MOVE_MESH_IN_FRONT_OF = some_mesh  ;* places mesh before specified target in rendering order
MOVE_MESH_BEHIND = other_mesh      ;* places mesh after specified target in rendering order

; Material sharing behaviour:
SHARED_MATERIALS = 0  ; set to 1 to apply to all meshes sharing the same material,
                      ; or FORCE to apply even for non-unique materials

; Material flags:
MATERIAL_FLAG_0 = 1          ; custom material shader flag 0
MATERIAL_FLAG_1 = 1          ; custom material shader flag 1
MATERIAL_FLAG_2 = 1          ; custom material shader flag 2
VRS_FIX = 1                  ; applies Variable Rate Shading fix
DIM_EMISSIVE_IN_CUBEMAP = 1  ; dims emissive in cubemap rendering
LINK_KS_VALUES = 1           ; links ks values

; Z-buffer tweaks:
DISTANT_FIX = 1    ; reduce Z-fighting for for distant geometry
STICKERS_FIX = 1   ; shift geometry a bit closer to camera, great for stickers and such

; Alternative emissive modes (only one can be used at a time):
ADAPTIVE_EMISSIVE = 1              ; adaptive emissive mode (distant for tracks, nearby for cars)
ADAPTIVE_DISTANT_EMISSIVE = 1      ; adaptive distant emissive mode
ADAPTIVE_NEARBY_EMISSIVE = 1       ; adaptive nearby emissive mode
WHITE_REFERENCE_POINT_EMISSIVE = 1 ; emissive based on white reference point

; * — per-object tweaks, those will not create new materials if you’re using MESHES and nothing but them.
```

### Different modes

#### Blend modes (`BLEND_MODE = …`)

- `OPAQUE`: regular opaque mode;
- `ALPHA_TEST`: regular alpha test;
- `ALPHA_BLEND`: regular alpha blend;
- `ADD`: additive mode, might work well for glowing areas (just make sure to set `ksDiffuse` and `ksAmbient` to zero and rely only on `ksEmissive`);
- `MULTIPLY`: multiply mode just in case (again, use only `ksEmissive`, and also don’t forget to set `FIXED_EMISSIVE` to 1 to make sure surface would have constant color);
- `TRANSPARENT_AS_BLACK`: works similar to alpha blend, but transparent surfaces instead of being transparent are black (used by extended config for Ruf Yellowbird to fix its grid at the back which doesn’t have stuff modelled behind it, maybe would be useful somewhere else);

Keep in mind, opaque and alpha test ones are the fastest, others slow things down. All but `OPAQUE`, `ALPHA_TEST` and `TRANSPARENT_AS_BLACK` might need transparency flag for the mesh (but only if you can’t move all the meshes that could be behind it above it in rendering queue, otherwise, please, avoid using transparency flag to both save performance and improve visual quality, as usual).

#### Cull modes (`CULL_MODE = …`)

- `FRONT`: regular mode, culling back side;
- `BACK`: show back side and hide front side;
- `WIREFRAME`: show wireframe;
- `WIREFRAME_AA`: show antialiased wireframe (very slow);
- `DOUBLESIDED`, `NONE` or `OFF`: show both sides.

Double sided mode will affect performance negatively by increasing surface to shade.

#### Depth modes (`DEPTH_MODE = …`)

- `NORMAL_FORCED`: by default any transparent meshes (with transparent flag) ignore depth mode, which can lead to artifacts in some cases, and this value might help with it, but use it carefully, it’s not a perfect solution and has its own issues (helps with windows on Brands Hatch though);
- `OFF`: or 'DEPTH_OFF' - mesh can’t be occluded or wouldn’t occlude anything, if it’s rendered last, it would show on top, if it’s rendered first, everything would be drawn over it;
- `NOWRITE`: or 'DEPTH_NOWRITE' or 'READONLY' or 'READ_ONLY' mesh can be occluded by others, but it itself wouldn’t occlude anything;
- `LESSEQUAL`: or 'DEPTH_LESSEQUAL' mesh can occlude other meshes if they’re in exactly the same spot (replacing regular `<` in "new distance to camera < old distance to camera" by `≤`);
- `LESSEQUAL_NOWRITE`: or 'DEPTH_LESSEQUAL_NOWRITE' or 'LESSEQUAL_READONLY' or 'LESSEQUAL_READ_ONLY'
- `NORMAL`: default; normal distance-to-camera-based occlusion mode

I suspect `LESSEQUAL` might be perfect for stickers on cars added with a second layer, as it wouldn’t require any offset for them to work properly.


### Colors for filling missing textures

- `txDiffuse`: white;
- `txMaps`: white;
- `txDetail`: white;
- `txNormal`: flat normal (127, 127, 255);
- `txNormalBlur`: flat normal (127, 127, 255);
- `txNormalDetail`: flat normal (127, 127, 255);
- `txNormalR`: flat normal (127, 127, 255);
- `txNormalG`: flat normal (127, 127, 255);
- `txNormalB`: flat normal (127, 127, 255);
- `txNormalA`: flat normal (127, 127, 255).

### New parameters

Custom Shaders Patch adds a few more parameters for various shaders to tweak their behavior, and `[SHADER_REPLACEMENT_...]` is perfect for setting those.

#### extExtraSharpLocalReflections

Changes local reflections (SSLR). In some places, it’s preferrable to make reflections blurrier to hide the fact those are just simple cubemap reflections (by reducing ksSpecularEXP), and yet there is no reason to have local reflections that blurry too. To make them sharper, just set a non-zero value, it’s like a sharpness boost, from 0 to 1.

Another possibly more important function: if value is negative, local reflections would switch to forced mode, severely loosening quality checks for detected reflection. By default, those checks are pretty demanding: initially algorithm was designed for car paints, and for those, in most cases, it’s better to have a reflection of sky than buggy repeated reflection of side mirror. However, in other cases, like for car rims, it might be better to have any messy, but local reflection, instead of sky.

First part, sharpness boost, takes absolute value of `extExtraSharpLocalReflections`, so you can set `extExtraSharpLocalReflections` to -0.001 to switch to forced SSLR reflections without altering sharpness, or set it to -1 to make them forced and extra sharp (that weird combination saves on amount of data being passed from CPU to GPU).

Example, forced reflections for chrome for E30 by Kunos:

```ini
[SHADER_REPLACEMENT_...]
MATERIALS = Chrome
PROP_... = extExtraSharpLocalReflections, -0.001
```

#### seasonAutumn, seasonWinter

Available for almost all shaders, allows to tweak diffuse color. Autumn variable shifts it to yellow, and winter desaturates and boosts brightness. Both use greeness as a mask. Whole thing is meant as quick and cheap hack to get seasons, and hopefully in the future will be replaced with something more substantial. If you would want to use it, set it in `[MATERIAL_ADJUSTMENT_...]` bound to some season-based condition.

#### extColoredReflection, extColoredReflectionNorm, extColoredBaseReflection

Available for shaders with reflections, these parameters allow to make color of speculars and reflection being affected by color of the surface undernearth, for proper metallic look without all the expenses of PBR. It can also be very helpful to make car lights more reflective without losing color.

- `extColoredReflection`: from 0 to 1, how intense is colorization.

- `extColoredReflectionNorm`: from 0 to 1, how grey colors are colorized. With default value, 0, it works similar to getting hue and that’s it, so dark grey and white would affect reflections the same way. With 1, brightness would be taken into consideration as well, so dark grey surfaces would lose a lot of reflections.

- `extColoredBaseReflection`: only for MultiMap shaders with both regular and sun specular, reflections and sun specular would use `extColoredReflection` and base specular would use `extColoredBaseReflection`.

#### extBounceBack

Adds light bouncing back to light source, could be useful for road signs with that special paint or things next to car lights which light up when lit by other cars. Not sure what’s the correct term, but, it’s these things:

<img src="https://img-webike-370429.c.cdn77.org/catalogue/webike_images/0000/0000/0121/1057006_2.jpg" width="400" />

And [here is a great video on how they work](https://www.youtube.com/watch?v=z5cR6EA2jGY).

Supported by:

- `ksPerPixelMultiMap_AT_NMDetail_ps`;
- `ksPerPixelMultiMap_AT_ps`;
- `ksPerPixelMultiMap_NMDetail_emissive_ps`;
- `ksPerPixelMultiMap_NMDetail_ps`;
- `ksPerPixelMultiMap_emissive_ps`;
- `ksPerPixelMultiMap_ps`;
- `ksPerPixelNM_ps`;
- `ksPerPixelReflection_ps`;
- `smLicensePlate_ps`.

Variable sets the intensity of that bounced back light. An extra tip: there is this light maker app, it can help to quickly create a spot light at camera position directed forward, just increase the range and, possibly, intensity. Great for testing here.

### Comparison images

- [Regular shadows vs `DOUBLE_FACE_SHADOW_BIASED = 1`](https://acstuff.ru/u/comparison/Uab);
- [Regular tree shadows vs `SEMITRANSPARENT_SHADOWS = 1`](https://acstuff.ru/u/comparison/i27).
