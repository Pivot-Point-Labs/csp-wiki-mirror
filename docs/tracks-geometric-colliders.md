# Geometric colliders

Originally, only type of collider available for tracks in AC is mesh collider, which is good for things like track surface and walls, but with some other kinds of obstacles, like, for example, lamp poles, it might not work the best. Also, if you, for example, have a bunch of buildings or thin double-sided walls, replacing mesh containing all of their walls with box colliders might provide some performance and stability improvements.

### Syntax

```ini
; data/surfaces.ini:

[_EXTENSION]
COLLIDER_DEBUG = 1  ; If set to 1, outlines of colliders will be highlighted (also, if set, live
                    ; reload for colliders would be available as well)

; Capsure collider: like a cylinder, but with hemispheres on its ends, faster than cylinder; a good
; fit for lamp posts
[COLLIDER_CAPSULE_...]
RADIUS = 0.5         ; Capsule radius

; Position and orientation can be defined like this:
LENGTH = 10          ; Capsule length in meters
POSITION = X, Y, Z   ; Position of capsule center in world coordinates
DIRECTION = 0, 1, 0  ; Direction (here, vertical)

; Or, like this:
FROM = X, Y, Z       ; Starting point in world coordinates
TO = X, Y, Z         ; Ending point in world coordinates

; Cylinder collider: like a capsule, but with flat caps, slightly closer
[COLLIDER_CYLINDER_...]
... ; Parameters are the same as with capsule

; Sphere collider: fastest option (of normal colliders)
[COLLIDER_SPHERE_...]
POSITION = X, Y, Z   ; Position in world coordinates
RADIUS = 5           ; Radius in meters

; Box collider
[COLLIDER_BOX_...]
POSITION = X, Y, Z   ; Position in world coordinates
SIZE = 10, 1, 5      ; Size in meters: width, height and length
DIRECTION = 0, 0, 1  ; Orientation vector
UP = 0, 1, 0         ; Vector facing upwards (for tilted boxes)

; Plane collider: everything on the inner side of the plane will be pushed outside; might possibly
; work for underlying ground? Or to block out inaccessible areas?
[COLLIDER_PLANE_...]
POSITION = X, Y, Z   ; Plane position
NORMAL = 0, 1, 0     ; Plane normal
```

Also, each collider can have these properties:

```ini
[COLLIDER_SPHERE_...]
NAME = my_collider   ; Name; used by custom collision parameters collider filter
LAYER = 255          ; Collider layer
COLOR = R, G, B, A   ; Color for outline visible with debug mode
```

More information about collision params is available [here](tracks-collision-parameters.md). As for layers, colliders with the same layer will be grouped together and when checking intersection between a car and colliders CSP would first check for the intersection between a car and collider groups, so it might be a good idea to group nearby colliders into a separate layer. Don’t worry about it too much though: I’m hoping in future to add something so that CSP would group colliders into optimal groups automatically.

Note: you can use new Render Stats app with its “Other threads” button to see how much time it takes for physics to do its collision checking step.
