# Examples

Some examples of bits of track configs.

### Pit doors opening if cars are present

<img src="https://files.acstuff.ru/shared/DSpT/20220611-180514-g333_sachsenring-ks_bmw_m4.jpg" width=380>

Given: a single mesh for all track doors that uses `stPerPixelNM_UVflow` shader to open and close.

```ini
; First, mesh needs to be split into separate meshes, one for each door:
[SPLIT_MESHES_...]
MESHES = PitwallSpotLightsGlass
NAME_FORMAT = PitwallSpotLightsGlass_{NearestPitStop}

; Then, instead of creating a light and material adjustment for each door let’s speed things up with INIpp, defining three templates:
[TEMPLATE: Pits_LightCondition]
@OUTPUT = CONDITION_... ; first template will produce [CONDITION_...] section
@GENERATOR_STARTING_INDEX = 0 ; we’re going to use it in @GENERATOR run, so it will be initiated a given amount of times automatically
NAME = Pits_Condition_$1 ; $1 will be replaced by generator iteration index, starting with 0 (because of parameter above)
INPUT = " CAR_ACTIVE_$1 * condition:LIGHTS_ON " ; there are now all these CAR_ACTIVE_0, CAR_ACTIVE_1, CAR_ACTIVE_2, … inputs, but nobody would just go and add them hand by hand
LAG = 0.97 ; all regular [CONDITION_...] parameters can go here as usual

[TEMPLATE: Pits_Light]
@OUTPUT = LIGHT_SERIES_... ; second template will produce [LIGHT_SERIES_...] section
@GENERATOR_STARTING_INDEX = 0
CONDITION = Pits_Condition_$1
MESHES = PitwallSpotLightsGlass_$1
COLOR = '#ffeeaa', 10
CLUSTER_THRESHOLD = 1
DIRECTION = NORMAL
DIRECTION_OFFSET = 0, 0.2, 0
RANGE_GRADIENT_OFFSET = 0
OFFSET = 0, 0, 0
SPOT = 160
SPOT_SHARPNESS = 0.9
RANGE = 20
SHADOWS = 1
SHADOWS_HALF_RESOLUTION = 1
SHADOWS_STATIC = 1
SHADOWS_EXP_FACTOR = 1
SHADOWS_BOOST = 4
SHADOWS_OFFSET = 0.03, -0.05, 0.03
SHADOWS_CLIP_PLANE = 0.001
SHADOWS_CLIP_SPHERE = 0.001
SPECULAR_MULT = 1

[TEMPLATE: Pits_Emissive]
@OUTPUT = MATERIAL_ADJUSTMENT_... ; and third — [MATERIAL_ADJUSTMENT_...] section
@GENERATOR_STARTING_INDEX = 0
CONDITION = Pits_Condition_$1
MESHES = PitwallSpotLightsGlass_$1
KEY_0 = ksEmissive
VALUE_0 = '#ffeeaa', 20
VALUE_0_OFF = 0, 0, 0
KEY_1 = ksAlphaRef
VALUE_1 = -193
VALUE_1_OFF = 0

; And generating them 32 times each:
[] ; non-existent section: adds nothing on its own, simply launches generators
@GENERATOR = Pits_LightCondition, 32 ; running them 32 times each
@GENERATOR = Pits_Light, 32
@GENERATOR = Pits_Emissive, 32
```
