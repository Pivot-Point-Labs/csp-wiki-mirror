# Wheels

Some settings related to wheels.

### Base tyre dimensions

By default CSP uses physics dimensions to estimate tyre size, but those don’t always match visuals. With these settings it’s possible to override those. Dimensions will be used, for example, by Skidmarks FX and Particles FX, so it’s a good idea to make sure they match.

All the parameters are optional, if not set, CSP would revert to guessed values.

```ini
[WHEEL_LF, WHEEL_RF, WHEEL_LR, WHEEL_RR]  ; use whatever tyres you need to configure
IS_OPEN = 0           ; Set to 1 if this wheel is not covered by something, very important for tyres smoke
TYRE_WIDTH = 0.3      ; Tyre width
TYRE_OFFSET = 0.035   ; Tyre offset
RIM_WIDTH = 0.24      ; Rim width
RIM_OFFSET = 0.05     ; Rim offset
; DEBUG = 1           ; Uncomment to show debug outlines, helps with calibrating dimensions
```

### Skidmarks FX

```ini
[SKIDMARKS_FX]
ALPHA = 0.6, 0.9        ; Minimum and maximum alpha
COLOR_BASE = '#131419'  ; Base color
COLOR = '#131419'       ; Accent color

; Optionally, settings can be redefined for certain wheels:
[SKIDMARKS_FX_TYRES_...]
TYRES = ST              ; If set, only applies to certain compounds (use short names here)
TYRES_FRONT = 1         ; If set, only applies to front wheels
TYRES_REAR = 1          ; If set, only applies to rear wheels
TYRES_LEFT = 1          ; If set, only applies to left wheels
TYRES_RIGHT = 1         ; If set, only applies to right wheels
ALPHA = 0.6, 0.9        ; Minimum and maximum alpha
COLOR_BASE = '#131419'  ; Base color
COLOR = '#131419'       ; Accent color
```

### Particles FX

##### Smoke

Both smoke appearance and behaviour can be adjusted. Default values are listed here. If two values X/Y are provided, X is the default value for regular cars and Y is the value for open wheelers.

```ini
[PARTICLES_FX]
SMOKE_COLOR = 0.8, 0.9, 1.0, 1.0  ; Adjust smoke color (can be used for colored smoke), fourth value
                                  ; acts like opacity multiplier and has a range from 0 to 2
SMOKE_COLOR_CONSISTENCY = 0.5     ; Increase to make smoke keep its color for longer as it expands
SMOKE_FLYOFF_START = 0            ; Start of the area in which smoke can detach from the wheel
SMOKE_FLYOFF_END = 0.15/0.5       ; End of the detachable smoke area (in radians)
SMOKE_FLYOFF_DELAY = 2.0/0.5      ; Delay for smoke flying off a wheel
SMOKE_STUCK_OFFSET = 1.0/0.0      ; Initial offset for smoke stuck to a wheel (0 for the middle, 1 for
                                  ; inside direction)
SMOKE_STUCK_MAX_SPEED = 20        ; Maximum angular speed for stuck-to-wheel smoke
SMOKE_BLOCK_START = -1            ; If above zero, sets the start of a region where smoke can’t detach
                                  ; (for example, for overhanging wheel arch)
SMOKE_BLOCK_END = -1              ; End of a region where smoke can’t detach (in radians)
SMOKE_INITIAL_SIZE_A = 0.08/N1    ; Minimum size of a smoke particle
SMOKE_INITIAL_SIZE_B = 0.1/N2     ; Maximum size of a smoke particle

; Where:
; • N1 = tyre width / 2.2
; • N2 = tyre width / 2.0
```

All the settings can be redefined for a certain axis, car side or set of tyres:

```ini
[PARTICLES_FX_SMOKE_...]
TYRES = SM          ; Change smoke color for tyres with SM for a short name
COLOR = 1, 0, 0, 1  ; Note that “SMOKE_” prefix is no longer needed here

[PARTICLES_FX_SMOKE_...]
TYRES_FRONT = 1     ; Only affect front tyres
BLOCK_START = 0.4   ; Add blocking area for the front axis
BLOCK_END = 0.6

[PARTICLES_FX_SMOKE_...]
TYRES_LEFT = 1      ; Only affect left tyres
FLYOFF_DELAY = 4    ; Increase flyoff delay for whatever reason

[PARTICLES_FX_SMOKE_...]
TYRES_REAR = 1      ; Only affect rear right tyre with semislick tyres set
TYRES_RIGHT = 1
TYRES = SM
COLOR = 1, 1, 0, 1  ; Color defined in further sections would override anything set before
```

There are also settings related to heating estimation, but these can be a subject to change in the future with alteratons to the heating estimation model:

```ini
[PARTICLES_FX]
FORCE_THICKNESS = -1        ; If set (in 0…1 range), overrides smoke thickness
HEAT_K = 0                  ; If set, overridees heating multiplier from smoke settings in Particles FX section (0…2 range)
COOL_AIR_K = 0.0001         ; Air cooling coefficient
COOL_GROUND_K = 0.001       ; Ground cooling coefficient
COOL_CARCASS_K = 0.1        ; Tyre carcass cooling coefficient
CARCASS_MULT = 0.5          ; Multiplier for tyre carcass cooling
REL_VELOCITY_THRESHOLD = 3  ; Minimum speed difference between tyre and ground to start heating up the tyre
```

#### Sparks

Use tyre dimensions to alter the placement of spark emitters.

### Tyres FX

Adds a bunch of visual effects for tyres: visual flexing, wear and damage, new dirt and grass effects, custom textures for different types of tyres, procedural tyre normals and especially custom look for blown tyres. Effects are only active for tyres nearby to keep things slightly faster.

(Would be cool if configs logic would be similar to Particles FX configs, but because all of it was written in different time periods simultaneously with me trying to learn how to code… Oh well. At least things are backwards compatible.)

```ini
[TYRES_FX]
ENABLED = 0                  ; Set to 0 to fully disable Tyres FX for a given car (or axis)
NOFX_DISTANCE_SWITCH = 16    ; Distance to disable Tyres FX at (48 for open wheelers, 16 for regular cars)
VISIBLE_IN_INTERIOR_CAM = 0  ; If effects are active with interior cameras (1 by default for open wheelers)

; Visual damage:
WEAR_MAX_VIRTUAL_VM = 25     ; Virtual kilometers for a tyre to show up as fully worn (defaults: 10 for
                             ; open wheelers, 15 for racing cars, 25 for regular cars)
DAMAGE_FLAT_SPOT_GAIN = 5    ; Intensity of flat spot damage
DAMAGE_FLAT_SPOT_FADE = 0.1  ; Fading speed for flat spot damage
DAMAGE_GRAIN_GAIN = 5        ; Intensity of grain damage
DAMAGE_GRAIN_MAX = 0.8       ; Maximum amount of grain damage
DAMAGE_WIDTH_K = 1.2         ; Width of visual damage area
DAMAGE_OFFSET_K = 0          ; Horizontal offset of visual damage area
DAMAGE_FLAT_SPOT_DEBUG = 0   ; If set, overrides flat spot damage around the entire wheel for debugging
DAMAGE_GRAIN_DEBUG = 0       ; If set, overrides grain damage around the entire wheel for debugging

; Material parameters for visual damage:
DAMAGE_SPEC_MULT = 0.6       ; Multiplier for ksSpecular of damaged areas
DAMAGE_SPEC_EXP_MULT = 0.2   ; Multiplier for ksSpecularEXP of damaged areas
DAMAGE_REFL_MULT = 0.8       ; Multiplier for fresnelMaxLevel of damaged areas
DAMAGE_OCCLUSION_MULT = 0.2  ; AO multiplier for damaged areas
DAMAGE_NORMALS_MULT = 2      ; Normal map boost value

; Visual dirt:
DIRT_ACCUMULATION = 600      ; How fast dirt or grass adds up to a wheel
DIRT_FADE = 20               ; How fast dirt fades (also, clamped from above by physics dirty level)
DIRT_OFFSET_K = 0.0          ; Offset for dirt map on a wheel along X axis relative to car
DIRT_WIDTH_K = 1.0           ; Dirt width on a wheel (set it in a way that it barely touches sides)
DIRT_GRASS_DEBUG = 0         ; If set, override grass dirt for debugging
DIRT_DIRT_DEBUG = 0          ; If set, override non-grass dirt for debugging

; Shape deformation:
FLEX_MULT = 1.0              ; Multiplier for sideways flexing (based on physics, but sometimes tyres might
                             ; have a strange configuration: this parameter can help)
FLEX_PROFILE_MULT = 0.45     ; Bending part of a tyre profile, from 0.1 to 2
FLEX_SQUASH_SMOOTHING = 0.1  ; Temporal filtering for squashing, from 0 to 1 (decrease for smoother changes)
FLEX_SKEW_RANGE_MULT = 3     ; Skew range
FLEX_SKEW_SMOOTHING = 0.1    ; Temporal filtering for skewing (decrease for smoother changes)
FLEX_MAX_SKEW_MULT = 0.8     ; Multiplier for maximum skewing

; Positioning of custom normals (more on that a bit further down):
CUSTOM_NORMALS_POS = -0.15, 0.15  ; Align custom normals from side to side with this parameter
CUSTOM_NORMALS_SCALE = 12         ; How much custom normals repeat along the circumference

; Blown tyres:
BROKEN_TYRES_DYNAMIC = 1       ; Change to 0 to disable procedural look for blown tyres
BROKEN_TYRES_BASE_NUDGE = 0.0  ; Optional nugde in the middle for blown tyres (make sure it doesn’t intersect
                               ; with tyre geometry unless you want to use a custom shape for interior part
                               ; of a blown tyre)
BROKEN_TYRES_BASE_BRIGHTNESS = 1.0 ; Brightness of the interior part of blown tyre
BROKEN_TYRES_NORMAL_LF =       ; If set, meshes in this query are shown when tyres are not broken (replace _LF
                               ;  with _RF, _LR, _RR)
BROKEN_TYRES_BROKEN_LF =       ; If set, meshes in this query are shown when tyres are broken
```

Settings for different axis can be redefined with:

```ini
[TYRES_FX_FRONT]
DIRT_WIDTH_K = 10

[TYRES_FX_REAR]
DIRT_OFFSET_K = 0.2
```

Custom tyre textures can be used to override textures for different tyre sets:

```ini
[TYRES_FX_CUSTOMTEXTURE_SM]  ; Overriding textures for texture set with short name “SM”
TXDIFFUSE =     ; Replacement for txDiffuse
TXBLUR =        ; Replacement for txBlur
TXNORMAL =      ; Replacement for txNormal
TXNORMALBLUR =  ; Replacement for txNormalBlur
```

All keys are optional, if any are not set default textures will be used. If tyres have more than a single material, use a postifix “_1”, “_2”, etc.:

```ini
[TYRES_FX_CUSTOMTEXTURE_SM]
MATERIAL = first_material
TXDIFFUSE = tex1.dds

[TYRES_FX_CUSTOMTEXTURE_SM_1]
MATERIAL = another_material
TXDIFFUSE = tex2.dds
```

Textures will be looked for next to “ext_config.ini” first. Optionally, you can put them in a ZIP file and use “file.zip::path/in/zip/entry_name.dds” format. And if you only need to replace textures on a certain axis, use a corresponding suffix:

```ini
[TYRES_FX_CUSTOMTEXTURE_SM_FRONT]
[TYRES_FX_CUSTOMTEXTURE_SM_REAR]
[TYRES_FX_CUSTOMTEXTURE_SM_FRONT_1]
[TYRES_FX_CUSTOMTEXTURE_SM_REAR_1]
```

One more tip: if you have two sets that need to share a texture, you can use INIpp feature to save on copy-pasting:

```ini
[TYRES_FX_CUSTOMTEXTURE_SM, TYRES_FX_CUSTOMTEXTURE_S]  ; Replace textures for both SM and S at once
TXDIFFUSE = tex1.dds
```

Custom tyre meshes. With these, certain meshes can be shown only if certain tyre sets are selected:

```ini
[TYRES_FX_CUSTOM_MESHES_...]
TYRES_0 = …         ; List of short tyre names; if currently selected tyres are in this list, …
TYRES_0_MESHES = …  ; … show meshes listed here
TYRES_1 = …         ; Another list of tyre names; if selected tyres are here, …
TYRES_1_MESHES = …  ; … show these meshes
DEFAULT_MESHES = …  ; If selected tyres are not TYRES_0, TYRES_1, etc. (within this section), show these meshes
```

### Procedural normal textures

```ini
[TYRES_FX_PATTERN]
TYRES_REAR =
TYRES_FRONT =
TYRES_LEFT =
TYRES_RIGHT =
TYRES =
PATTERN_TRIM =
```

### Shadowed wheels

TODO
