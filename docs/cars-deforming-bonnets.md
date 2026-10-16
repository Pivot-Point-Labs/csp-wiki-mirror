# Deforming Bonnets

Simple trick of moving vertices of bonnets and boot lids, giving them that damaged look. Works with all cars that already have bonnets slightly opening and wobbling on taking damage.

![In action](https://i.imgur.com/3nGbge1.png)

### Syntax

```ini
[DEFORMING_HOOD]
NAME = MOTORHOOD          ; name of parenting node containing all meshes to deform
MAX_DAMAGE = 40           ; km/h, 40 is default
OFFSET_Y_MIDDLE = 0.04    ; how high would it offset in the center at full damage
OFFSET_Y_END = 0.02       ; how high would it offset at the far end at full damage
OFFSET_Z_END = 0.06       ; how far would it offset at the far end
BULGING_EXTRA = 0.0       ; increase to make shape go less triangly and more trapezoid-like
BULGING_EXPONENT = 2.0    ; affects the curve of slopes around raised center
NOISE_Y_AMPLITUDE = -0.16 ; some simple vertical noise at the center
NOISE_Z_AMPLITUDE = 0.2   ; and horizontal noise at the far end
NOISE_Y_FREQUENCY = 7.0    ; which adds
NOISE_Z_FREQUENCY = 7.0    ; some randomization
Z_FACTOR = 2.5            ; how center is being found
Z_BIAS = 0.0              ; with, if needed, manual offset

[DEFORMING_REAR]
NAME = REARHOOD
; everything else is the same
```

All sizes are in meters. As usual with visual stuff, nothing physically accurate, but, on the other hand, it means greater range of possible configurations.

Be careful, noise gets offset from car to car to keep it more varied, so don’t rely on its specific arrangement too much.

### Guessing

Some cars don’t need it as they have wide front bumpers, for example. Safer to set it by hand, it doesn’t take a lot of time to do too. So, no guessing.

### Features to add later

- Doors?
- Bumpers?
