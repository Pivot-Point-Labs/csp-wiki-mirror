# Meshes Manipulation

Ideally these things would be done in 3D editor instead, but sometimes it might not be possible, like when making a track for an existing track.

### Smoothing normals

Helps to fix an issue with some of surfaces of a track not being smooth. It becomes especially noticeable with Rain FX where reflections in puddles break apart. Now there is a quick and easy way to fix it with a config.

```ini
[SMOOTH_NORMALS_...]
MESHES = mesh0, …         ; List of affected meshes
MATERIALS = material0, …  ; List of affected materials (use of these, or both)
PRECISION = 0.0001        ; Smoothing threshold
NORMAL_CONTRIBUTION = 0   ; How much normals would be taken into consideration to detect edges
```

The way it works, it would take all found meshes, find all vertices that are closer to each other than `PRECISION` and average their normals. If `NORMAL_CONTRIBUTION` is non-zero, it would be added to vertex position during grouping stage, thus allowing to keep some edges. Usually though, using it on something like a piece of asphalt, there is no need to use that parameter.

Example:

```ini
[SMOOTH_NORMALS_...]
MATERIALS = asph
PRECISION = 0.01
NORMAL_CONTRIBUTION = 0
```

### Normals alteration

This one, for example, can be used to reorient normals of tree leaves so they would face upwards.

```ini
[ALTER_NORMALS_...]
MESHES = mesh0, …         ; List of affected meshes
MATERIALS = material0, …  ; List of affected materials (use of these, or both)
ALTER = 0, 1, 0           ; Optional reorientation of a normal vector (turns vector along provided vector)
; OFFSET = 0, -0.01, 0          ; Optional offset
```

Example:

```ini
[ALTER_NORMALS_...]
MESHES = flat.trees.?
OFFSET = 0, 1e9, 0
```

### Meshes splitting

Splits meshes into separate elements. Use with extreme caution: it would increase number of draw calls, which isn’t always a good idea.

```ini
[SPLIT_MESHES_...]
MESHES = mesh0, …               ; List of affected meshes
MATERIALS = material0, …        ; List of affected materials (use of these, or both)
NAME_FORMAT = '{Name}.{Index}'  ; Names for new meshes
ORDER_PIVOT = X, Z, Y           ; Ordering of detached nodes would start from this position (closest
                                ; detached mesh would get an index 0)
```

Available substitutions for name format:

- `Name`: original mesh name;
- `Index`: index of an element (based on its distance to `ORDER_PIVOT`);
- `Position`: position of the center of its AABB in world coordinates;
- `NearestPitStop`: index of nearest pit stop;
- `NearestStart`: index of nearest starting position.

Example:

```ini
[SPLIT_MESHES_...]
MESHES = PitwallSpotLightsGlass
NAME_FORMAT = PitwallSpotLightsGlass_{NearestPitStop}
```

### Meshes subdivision

With distant geometry some huge low-poly meshes acting both as distant geometry and underlying ground can cause issues, like on Shuto. This thing can help.

```ini
[SUBDIVIDE_MESHES_...]
MESHES = mesh0, …         ; List of affected meshes
MATERIALS = material0, …  ; List of affected materials (use of these, or both)
ITERATIONS = 2            ; Number of iterations, default value is 1
```

Example:

```ini
[SUBDIVIDE_MESHES_...]
MESHES = material:mat_main_background
ITERATIONS = 2
```

### Wrapping meshes

For animating objects their meshes have to be wrapped in nodes, but if track KN5 was saved as track everything will be flatten. In general I would recommend to save dynamic objects in separate KN5 saved as car, but if that’s not an option you can instead wrap existing flattened meshes into a node:

```ini
[WRAP_MESHES_...]
NAME = node          ; Name of a new node
MESHES = mesh0, …    ; List of meshes to add
PIVOT_POS = X, Z, Y  ; Pivot position of the created node

; Optionally, node orientation can be set with vectors:
PIVOT_DIR = X, Z, Y  ; Direction of its Z axis (or use PIVOT_DIR_POINT with world coordinates for node to look at)
PIVOT_UP = X, Z, Y   ; Direction of its Y axis (or use PIVOT_UP_POINT with world coordinates)

; Or, with angles (in radians):
PIVOT_HEADING = …
PIVOT_PITCH = …
PIVOT_ROLL = …
```

Example:

```ini
[WRAP_MESHES_...]
NAME = windmill_spin
MESHES = windmill_spin
PIVOT_POS = -5.47, 9.178, -27.592
```
