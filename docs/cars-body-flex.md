# Body Flex

Body flex is a new feature added in v0.1.80-preview428 (it was added some time before, but needed a revision) allowing to simulate torsional stiffness of a car (and show it visually). To use it, add to `suspensions.ini`:

```ini
[_EXTENSION_FLEX]
TORSIONAL_STIFFNESS=10000  ; Nm/deg
TORSIONAL_DAMPING=100      ; Nm/(deg/s)
```

With this method, you get rotational bending along Z axis, which is sufficient for most cases. Actual stiffness values can be found online. For damping, it’s a bit trickier, but something should be possible to estimate.

If for some reason you do need car to flex in other axises or have a positional flex, you can do it by setting explicit CFM and ERP values, but I haven’t figured out a good way to split CFM across axis, so it’s pretty rough at the moment.
