# Animations

With extra animations for cars, now you no longer have to create extra wings to add new animations. They could be bound to a lot of different inputs, allowing, for example, to create complex dashboard instruments.

Animations can work in two different modes:

- Using `INPUT` as trigger:

  Start animation as soon as it goes over a set threshold (similar to how emissives use inputs). Apart from [other parameters](cars-instruments-inputs.md), `INPUT_THRESHOLD` and `INPUT_THRESHOLD_INVERSE` could be used to adjust behavior.

- Using `INPUT` as animation progress value, directly:

  If bound to gas pedal, for example, for half-pressed pedal animation progress would be set to 50%. [LUTs and other `INPUT` options](cars-instruments-inputs.md) are available to scale behavior and add things like snapping to certain points of the animation).

### Syntax

```ini
[ANIMATION_...]
INPUT = REVERSE             ; bind to reverse gear
; BIND_TO = REVERSE           ; or this
FILE = animation.ksanim     ; file name of new animation in “animations” folder
TIME = 0.5                  ; animation time
INPUT_AS_PROGRESS = 0       ; set to 1 to switch to that second input-as-progress mode
LOOP_WHILE_ACTIVE = 0       ; if set to 0, animation would go to 0% if not triggered, and
                            ; to 100% otherwise; if set to 1, animation would play in
                            ; a loop if triggered and stop otherwise
LOOP_KEEP_UNTIL_DONE = 1    ; only for “LOOP_WHILE_ACTIVE”: set to 1 to make animation
                            ; go to 0% if stopped (like wipers would do, for example)
TICK_TOCK_MODE = 0          ; only for “LOOP_WHILE_ACTIVE”: loop as 0% → 100% → 0% instead
                            ; of jumping from 100% to 0%
AFFECTS_INTERIOR_SHAPE = 0  ; force to update interior reflections mask if animation is
                            ; playing (slower)
HOLD_STATE = 1              ; for hoods and such
BLEND_STATE = 0.3           ; smth for HOLD_STATE?
LUT = ...                   ; yes you can do here too
```

Default values are as listed above, so for minimum, you would only need `INPUT` and `FILE`. With `INPUT_AS_PROGRESS`, loop options won’t have any effect.

### Features to add later

- Blending between animations (?).
