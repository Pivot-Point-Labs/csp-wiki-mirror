# Visually Adjustable Wings

This feature adds visual effect for different wing angles in car setups. Nothing too complex, just a bit of rotation. Very similar to the way analog needles work.

### Syntax

```ini
[ADJUSTABLE_WING_0]
NAME = WING_REAR  ; name of wing root node to rotate
WING = 2          ; index of section in aero.ini
ANGLE_BASE = 0    ; base offset for angle
ANGLE_MULT = 0.8  ; angle multiplier
DEBUG_MODE = 0    ; set to 1 to adjust PIVOT easier
ROTATION_PIVOT = 0, 0.0, -0.035  ; rotation pivot relative to wing root node, should be at the center of wing mesh
ROTATION_AXIS = -1, 0, 0         ; I’m pretty sure in most cases, this value wouldn’t be changed, but just in case
```

About angle multiplier, of course logically you might want to set it to 1, but I keep it a bit lower for existing cars where models weren’t made with this feature in mind. As for debug mode, with it enabled, wing would start oscillate back and forth instead of being linked to aero wing: great for adjusting rotation pivot.

### Guessing

Patch would try and find rear wing using those conditions:
- Node is called REAR_WING, WING_REAR, WING;
- Its pivot is above 1.0 meters and behind Z = -1.0;
- There is an aero wing called REAR.

If found, it would turn into visually adjustable wing, with some mild settings. And if you want to disable that behavior, add any adjustable wing manually. For example, like so, if you don’t need them at all:

```ini
[ADJUSTABLE_WING_0]
NAME = _non_existent_node_
```

### Features to add later

- LUT for angle, if it would be needed.
