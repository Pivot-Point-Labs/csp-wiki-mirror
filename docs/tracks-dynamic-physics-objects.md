# Dynamic Physics Objects

CSP 0.1.78 adds an option for tracks with extended physics to configure in detail behaviour of dynamic physics objects (“AC_POBJECT_…” ones). Now it’s possible to redefine their mass, change collision parameters, use geometric colliders and enable collisions between those objects.

<a href="https://gfycat.com/ThreadbareWildDwarfmongoose"><img src="https://thumbs.gfycat.com/ThreadbareWildDwarfmongoose-size_restricted.gif"></a>

### Syntax

```ini
; data/surfaces.ini:

[DYNAMIC_OBJECTS_...]
MESHES = AC_POBJECT_1?    ; Filter for object names
DETECT_BOX_COLLIDER = 0   ; If set to 1, CSP would try to automatically detect if collider mesh is
                          ; a box and if so, replace it with a fitting box collider with correct
                          ; center of gravity
MASS = 1                  ; Mass in kg (default mass of those objects in AC is 1 kg)
LINEAR_DAMPING = 0.9      ; Damping for linear motion (increase to make objects stop sooner)
ANGULAR_DAMPING = 0.9     ; Damping for angular motion
INTERCOLLISION = 1        ; If set to 1, objects can collide with other objects with the same flag
COLLIDER_DEBUG = 1, 0, 0  ; If set, objects would get an outline for their geometric colliders
COG_OFFSET = X, Y, Z      ; Optional offset for the center of gravity

; Collision parameters
BOUNCE = 0.5             ; Bounce coefficient
FRICTION = 0.9           ; Contact friction
INTENSITY = 0.1          ; Collision intensity (affects damage, audio and visual effects)
                         ; Other collision parameters are also applicable here

; Geometric colliders
NO_MESH_COLLIDER = 1     ; If you’re using geometric colliders, add this option to disable mesh
                         ; colliders

; These descriptions can contain multiple collider definitions (for example, a cone can be roughly
; approximated with a box and a capsule)
; Geometric collider: sphere
COLLIDER_SPHERE_0 = R                   ; Adds new spherical collider with given radius in meters
COLLIDER_SPHERE_0_OFFSET = X, Y, Z      ; Optional offset

; Geometric collider: box
COLLIDER_BOX_1 = W, H, L                ; Adds new box collider with given width, height and length
COLLIDER_BOX_1_OFFSET = X, Y, Z         ; Optional offset
COLLIDER_BOX_1_DIRECTION = 0, 0, 1      ; Optional direction for orienting box
COLLIDER_BOX_1_UP = 0, 1, 0             ; Optional up vector for orienting box

; Geometric collider: capsule (like a cylinder with hemispheric caps, faster than cylinder)
COLLIDER_CAPSULE_2 = R                  ; Adds new capsule collider with given radius in meters
COLLIDER_CAPSULE_2_OFFSET = X, Y, Z     ; Optional offset
COLLIDER_CAPSULE_2_DIRECTION = 0, 0, 1  ; Direction for capsule
COLLIDER_CAPSULE_2_LENGTH = L           ; Length in meters

; Alternatively, instead of offset, direction and length starting and ending points can be set
COLLIDER_CAPSULE_3 = R
COLLIDER_CAPSULE_3_FROM = X, Y, Z       ; Starting point
COLLIDER_CAPSULE_3_TO = X, Y, Z         ; Ending point

; Geometric collider: cylinder (like a capsule with flat caps, a bit slower)
COLLIDER_CYLINDER_4 = R                 ; Adds new cylinder collider with given radius in meters
                                        ; Other parameters are the same as with capsule
```

If two different sections match the same object, both would apply, subsequent sections overwriting values set by earlier defined sections (ordered numerically). Also, please note: if your track uses extended physics and there are no `[DYNAMIC_OBJECTS_...]` sections, `DETECT_BOX_COLLIDER` would apply automatically. To disable it (just in case), add something like:

```ini
[DYNAMIC_OBJECTS_...]
MESHES = ?
DETECT_BOX_COLLIDER = 0
```
