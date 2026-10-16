# Mesh Adjustments

With these options you can adjust the object-properties of meshes.

```ini
[MESH_ADJUSTMENT_...]
MESHES = some_mesh
; MATERIALS = some_material  ; all objects using same mat would be affected
MOVE_TO = some_node
MOVE_IN_FRONT = meshfilter
LAYER = 0  ; layers for world-detail setting
IS_ACTIVE = 1
IS_TRANSPARENT = 0 ; transparent flag for object
IS_RENDERABLE = 0
CAST_SHADOWS = 1
```

For nodes:
```ini
[NODE_ADJUSTMENT_...]
NODES = some_node
MOVE_TO = some_other_node         ; this or
MOVE_IN_FRONT = some_other_node   ; that
IS_ACTIVE = 1
```
