# Collision Parameters

Tracks now can override collision parameters for different meshes. Apart from obvious uses like making low-friction wall or super-bouncy ground mesh, more importantly this also can be useful for adjusting collision softness. Softer collision can be a better approximation of, for example, a tyre wall, but harded collision in a different case can help with cars falling through objects if colliding at high speeds.

### Syntax

All the parameters are optional (but if you’re using `MAX_DEPTH`, add at least one other parameter, at least `INTENSITY = 1`):

```ini
; data/surfaces.ini:

[COLLISION_PARAMS_...]
MESHES = ?WALL?        ; Names of meshes to get new parameters
COLLIDERS = CAPSULE_?  ; Names of geometric colliders
SOFT_ERP = 0.8         ; Error reduction parameter
SOFT_CFM = 0.0001      ; Constrain force mixing, the higher it is, the softer is the collision
BOUNCE = 0.5           ; Bounce parameter
FRICTION = 0.25        ; Contact friction
INTENSITY = 1          ; Collision intensity (affects damage, audio and visual effects)
MAX_DEPTH = 0.2        ; If set and collision depth is above that parameter, collision becomes
                       ; hard: might help with performance and avoid objects passing through
                       ; walls
RIGID_WITH_BODIES = 0  ; If set to 1, collisions with 3D colliders would be fully rigid
RIGID_WITH_BOXES = 0   ; If set to 1, collisions with boxes (usually used for car bottoms)
                       ; would be fully rigid
```

Same logic applies to `[CUSTOM_COLLISIONS]` of [extra server options](misc-server-extra-options.md), or to geometric colliders and dynamic objects configuration. More information about geometric colliders is available [here](tracks-geometric-colliders.md).

Note: if you’re making a soft tyre wall or something like that, you can also [get deformation to apply visually](tracks-deforming-walls.md).
