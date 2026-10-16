# Surface Tweaks

Along with regular surface properties, such as `FRICTION` or `DAMPING`, there are now some extra ones added by CSP.

- `_EXT_SURFACE_TYPE`: type of the surface (overrides guessing based on `WAV`).
  - `EXTRATURF`;
  - `GRASS`;
  - `GRAVEL`;
  - `KERB`;
  - `OLD`;
  - `SAND`;
  - `ICE` (added in 0.2.5);
  - `SNOW` (added in 0.2.5).
- `_EXT_SURFACE_TYPE_MODIFIER`: adjusts SurfacesFX behavior for sand, grass and gravel. Default value is `REGULAR`.
  - `LOOSE`;
  - `REGULAR`;
  - `FIRM`.
- `_EXT_PERLIN_NOISE`: set to 0 to make sure sine noise will be used despite CSP settings, or to 1 to replace sine noise with perlin noise (`SIN_HEIGHT` and `SIN_LENGTH` would still be used, but now for perlin instead).
- `_EXT_PERLIN_OCTAVES`: number of octaves for perlin noise, from 1 to 10.
- `_EXT_PERLIN_PERSISTENCE`: perlin noise persistence (amplitude multiplier for following octaves).

Note: if surface type is not set explicitly, SurfacesFX gravel (if SurfacesFX module is enabled, or there are any tyres with `TYPE_HINT=GRAVEL` present) will activate for surfaces with `DIRT_ADDITIVE ≥ 0.7`, or surfaces with `DIRT_ADDITIVE ≥ 0.3` and (`FRICTION < 0.9` or `WAV` set to “grass.wav”, “gravel.wav” or “sand.wav”).
