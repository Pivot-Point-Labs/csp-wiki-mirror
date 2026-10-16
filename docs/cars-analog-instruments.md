# Analog Instruments

You can set new analog instruments with extended config, unlimited amount, with various customizations. Any input from [this list](cars-instruments-inputs.md) is supported.

### Syntax

```ini
[ANALOG_INDICATOR_...]
INPUT = TIME_HOURS               ; any of supported inputs
NAME = ARROW_TIME_HOURS          ; name of mesh to move
UPPER_BOUND = 24                 ; maximum input value for arrow to move with
LOWER_BOUND = 0                  ; minimum input value
START = -180                     ; offset for starting point, degress
RANGE = 360                      ; full range of arrow to move to at the upper bound, degress
POS_OFFSET_START = 0, -0.1, 0.1  ; position offset for the minimum value
POS_OFFSET_END = 0, -0.1, 0.1    ; position offset for the upper bound
SCALE_START = 0, 1, 1            ; scale for the minimum value
SCALE_END = 1, 1, 1              ; scale for the upper bound (allows to create progress bars and such)
SPEED_LAG = 0.2                  ; lag for speed, adding inertia of movement
G_FACTOR = 0.1, 0, 0             ; adds a bit of needle offset bound to G-forces for those axis
LUT = (| 60=-1| 90=-62 |)        ; optionally maps input values to degrees
```

If needed, you can use original style parameters too (available only if `UPPER_BOUND` is not set):

```ini
[ANALOG_INDICATOR_...]
INPUT = RPM
INPUT_MAX = 8200
NAME = ARROW_RPM
ZERO = 1
STEP = 0.033375
```

LUT, as with original AC style, also works as intended, allowing to set degrees:

```ini
[ANALOG_INDICATOR_...]
INPUT = WATER_TEMP ; temperature: here, angles are set with LUT, as in original
NAME = ARROW_WATER
MIN_VALUE = 60
```

Keep in mind that new inputs system has a lot of other options like `INPUT_MIN`, `INPUT_MAX`, `INPUT_MOD` and `INPUT_STALLED_VALUE` allowing to make that needle move more accurately.

### Tips

- Use `INPUT_DEBUG` to make sure input values map to dials properly;
- With `POS_OFFSET_START` and `POS_OFFSET_END`, you can fix positioning of needle, or add movement. Or even replace rotation with movement alone;
- If you want needle to stop going through 360° back to 0°, set `RANGE` to 359.99;
- With new system, you could recreate [vintage tachometers](cars-vintage-tachometers.md) without actually using that feature at all.
