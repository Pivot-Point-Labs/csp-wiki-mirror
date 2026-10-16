# Main settings

Tyres FX module adds a few things to tyres look, such as visual flex, damage and wear. CSP will try and guess settings automatically, but sometimes it might be helpful to adjust settings manually. Remember, you can check out [guessed config](cars-about-guessed-configs.md) to see the guessed values.

### Syntax

Please, adjust settings only if defaults are not working well, and only the ones you need to adjust. Don’t just copy the entire thing!

```ini
[TYRES_FX]  ; use [TYRES_FX_FRONT] or [TYRES_FX_REAR] to override settings for a certain axis
ENABLED = 1                  ; set to 0 to disable Tyres FX
NOFX_DISTANCE_SWITCH = 32    ; distance to pause Tyres FX at
VISIBLE_IN_INTERIOR_CAM = 0  ; set to 1 if tyres are visible from interior (will be set automatically for open wheelers)

; Visual flex
FLEX_MULT = 1                ; multiplier for visual flex (default value of 1 should reflect physics behavior, so it’s better not to change it)
FLEX_MAX_SKEW_MULT = 0.8
FLEX_PROFILE_MULT = 0.45
FLEX_SKEW_RANGE_MULT = 3
FLEX_SKEW_SMOOTHING = 0.1
FLEX_SQUASH_SMOOTHING = 0.1

; Dirt accumulation
DIRT_ACCUMULATION = 600  ; accumulation rate
DIRT_WIDTH_K = 1.1       ; width coefficient
DIRT_OFFSET_K = 0        ; horizontal offset coefficient
DIRT_FADE = 20           ; dirt fading rate
DIRT_DIRT_DEBUG = 0      ; set to 1 to see tyres fully dirty
DIRT_GRASS_DEBUG = 0     ; set to 1 to see tyres fully covered in grass

; Visual wear
WEAR_MAX_VIRTUAL_VM = 25  ; distance to drive until tyres will appear fully won (by default uses physics values)

; Visual damage
DAMAGE_WIDTH_K = 1.2         ; damage width coefficient
DAMAGE_OFFSET_K = 0          ; damage horizontal offset
DAMAGE_FLAT_SPOT_DEBUG = 0   ; set to 1 to see tyres covered in flat spot damage
DAMAGE_FLAT_SPOT_GAIN = 5    ; flat spot damage gain rate
DAMAGE_FLAT_SPOT_FADE = 0.1  ; flat spot damage fading rate
DAMAGE_GRAIN_DEBUG = 0       ; set to 1 to see max amount of grain damage
DAMAGE_GRAIN_GAIN = 5        ; grain damage gain rate
DAMAGE_GRAIN_MAX = 0.8       ; grain damage upper limit
DAMAGE_NORMALS_MULT = 2      ; multiplier for damage normals
DAMAGE_OCCLUSION_MULT = 0.2  ; intensity of ambient occlusion produced by damage
DAMAGE_REFL_MULT = 0.8       ; reflectivity fading in damaged areas
DAMAGE_SPEC_EXP_MULT = 0.2   ; shininess fading in damaged areas
DAMAGE_SPEC_MULT = 0.6       ; specularity fading in damaged areas

; Blown tyre look
BROKEN_TYRES_BASE_BRIGHTNESS = 1  ; adjust brightness of the interior part for blown tyres
BROKEN_TYRES_BASE_NUDGE = 0       ; adjust shape of the interior part for blown tyres

; Tweaks for aligning procedurally generated textures
CUSTOM_NORMALS_POS =       ; placement, left and right sides
CUSTOM_NORMALS_SCALE =     ; scale (repeats around the circumference), whole number

; Optional shine for very new tyres (goes away pretty much instantly)
NEW_SHINE_SPECULAR_MULT = 1      ; increase to make new tyres more shiny (for F1, something around 10 could work well)
NEW_SHINE_SPECULAR_EXP_MULT = 1  ; increase to make new tyres more glossy (for F1, something around 4 could work well)
```

# Shader tweaks

## `txMaps` alternative for ksTyres shader

Original AC uses alpha of `txDiffuse` (and its blurred version) as a multiplier for specularity and reflectivity, acting similar to red and blue channels of `txMaps`. So, it’s a good idea to at least make sure occluded parts of grooves are black there, so they wouldn’t reflect things (something like a local AO map).

With CSP, you can also use alpha of `txNormal` (and its blurred version) to set up a shininess/roughness map. To do so, simply add to car config:

```ini
[SHADER_REPLACEMENT_...]
MATERIALS=shader:ksTyre?
PROP_... = extTyresFlags, 4
PROP_... = extRoughnessExp, 10
```

With this setup CSP will alter `ksSpecularEXP` value based on alpha of `txNormal`, going from original `ksSpecularEXP` where the texture is black to `extRoughnessExp` where the texture is white. A couple of examples:

- Set `ksSpecularEXP` to 0 and `extRoughnessExp` to something like 50 and alpha of `txNormal` will act as shininess map, similar to green channel of `txMaps`: the brighter it is, the smaller speculars and sharper reflections will be.
- Set `ksSpecularEXP` to 50 and `extRoughnessExp` to 0 and alpha will act as roughness map, blurring reflections and increasing the size of speculars where it’s the brightest.

## Flipping normals

Use this piece of code to flip normals on X axis (can be useful sometimes to fix the look of tyres):

```ini
[SHADER_REPLACEMENT_...]
MATERIALS=shader:ksTyre?
PROP_... = extTyresFlags, 1
```

Use 2 to flip normals on Y flag. To combine several flags (for example, enable `extRoughnessExp` and flip normals at once), simply sum up all the flags you need.
