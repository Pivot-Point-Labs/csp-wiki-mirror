# Mesh Splitting

Nothing to see here, really. The whole thing was added so a couple of cars could work with [local cubemaps](cars-local-cubemaps.md). Meant for some very rare cases of preparing a config to an already existing car where for some reason you would need to split a mesh in two bits.

Requires a game restart in order for changes to take effect. Must be placed above any other sections that act on the split meshes.

Splitting does not function recursively, you cannot split a split mesh for a second time.
### Syntax

```ini
[MESH_SPLIT_...]
ACTIVE = 1 			; Quickly enable or disable section
MESHES = mesh 	    		; List of meshes to cut
SPLIT_NAME = name 		; Specify exact mesh name of new split mesh
SPLIT_POSTFIX = 	   	; Postfix for the new split mesh, not used if name is set explicitly
SPLIT_MATERIAL = name 		; Specify exact material name of new split mesh
SPLIT_MATERIAL_POSTFIX = 	; Postfix for the material for the new split mesh, not used if name is set explicitly
INSERT_TO = node 		; Specify new parent for new mesh
INSERT_IN_FRONT = 0
MODE = 				; Available options:
				; PLANE = Split along a plane based on the SPLIT_AXIS
				; LOOK_AT = Split mesh triangles facing given direction
				; COPY_FLIPPED = Take mesh, duplicate, then invert direction. Useful to to fix missing interior windows

; if MODE = LOOK_AT
LOOK_AT = 0, 0, 0 		; Cut mesh triangles facing this point relative to the parent of the mesh
LOOK_AT_THRESHOLD = 0 		; Specify how precisely the faces must be facing the above point to be selected. 0 for all.

; if MODE = PLANE
SPLIT_AXIS = 1, 0, 0   		; axis to cut mesh by (cut will be perpendicular to it, where X is lateral, Y is Longitudinal, Z is vertical
SPLIT_THRESHOLD = 0.0  		; offset for cut along the line, in meters

MODEL_SPACE = 0 		; Convert the co-ordinates to use the car root node instead of mesh parent node
```

Just to clarify, it’s not actually *cutting*, no triangles will be split in two. Just regrouping existing triangles into two different meshes.

### Features to add later

- More separation? Maybe one day it could help with adding turn signals and such without extra KN5s.
