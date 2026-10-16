# Deforming Walls

Visually deforming walls can be a good thing to set if you’re using [soft wall colliders](tracks-collision-parameters.md) on your track. Note that for them to work you need to enable [extended track physics](tracks-enabling-extended-physics.md).

### Syntax

```ini
[DEFORMING_WALLS_...]
MESHES = mesh0, …                ; List of meshes to deform
MAX_DEPTH = 1.0                  ; Maximum deformation depth
RESTORATION_LAG = 0.8            ; Lag for wall to get back into its normal shape
DEPTH_MULT = 1.0                 ; Multiplier for depth
RADIUS_MULT = 1.0                ; Multiplier for deforming radius
TESSELLATION = 1                 ; Set to 1 to use tessellation (usually those walls should not
                                 ; have enough triangles otherwise)
TESSELLATION_DISTANCE = 20, 100  ; Tessellation distances from camera; first value for maximum
                                 ; tessellation, second for minimum
TESSELLATION_FACTOR = 10, 3      ; Maximum and minimum tessellation factor
ALPHA_MODE = OPAQUE              ; ...
```

When collision occurs, CSP would check for any deforming meshes in the vicinity, and if anything is found would activate temporary deformation with optional tessellation. Once deformation is faded out (based on `RESTORATION_LAG`), it’ll switch back to normal shader. You can use `[SHADER_REPLACEMENT_...] CULL_MODE = WIREFRAME` to see tessellation in action.
