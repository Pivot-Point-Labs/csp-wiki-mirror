# Neck FX

With these options, you can alter how head of the driver moves in first person view, with Neck FX enabled.

### Syntax

```ini
[NECK]
HELMET_OFFSET = 0, 0, 0             ; add this option to set custom helmet offset if it’s enabled
BOUNDS_HORIZONAL = -130, 130        ; angles in which head is allowed to rotate on Y axis
BOUNDS_VERTICAL = -50, 50           ; angles in which head is allowed to rotate on X axis
LOOK_BACK_OFFSET = 0.24, 0.0, 0.15  ; head offset for looking back (to reduce overlay by a car: for example, in F1 cars, you might want to increase Y value)
PAN_LIMIT = 0.15, 0.1               ; boundary for panning, in X and Y directions, in meters
```

You can change those settings during the race or replay to adjust them more nicely.

### Guessing

Y value of `LOOK_BACK_OFFSET` for open wheelers is 0.07 by default. Also, `PAN_LIMIT` is 0.08, 0.06. Everything else is how it shows in **Syntax** section.
