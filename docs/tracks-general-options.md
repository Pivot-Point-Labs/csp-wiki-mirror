# General Options

There are some general options for tracks, allowing to tweak some things of how patch works with them. Most of those settings require race reload to apply.

```ini
[BASIC]
SUPPORTS_WIND = 1  ; set to 0 to disable all wind-based effects completely. might be good for interior tracks?
RALLY_TRACK = 0    ; single rally car on a rally track would get differently acting headlights. patch would try to guess rally track based on tags, but you can change it here
PITBOXES = 4       ; amount of pit boxes on a track, to fix if "ui_track.json" is messed up
IGNORE_OTHER_CONFIGS = 0  ; set to 1 to ignore other configs that may be available in other places

[LIGHTING]
ENABLE_TREES_LIGHTING = 0        ; if all your trees are not very close to a track, you can improve performance a lot by disabling trees lighting completely
TRACK_AMBIENT_GROUND_MULT = 0.5  ; only define it if needed! allows to redefine ambient multiplier for surfaces facing down
BOUNCED_LIGHT_MULT = 1, 1, 1, 1  ; multiplier for bouncing light (set to 0 if track is black, for example)
LIT_MULT = 1                     ; multiplier for dynamic lights affecting the track
SPECULAR_MULT = 1                ; multiplier for speculars
CAR_LIGHTS_LIT_MULT = 1          ; multiplier for dynamic lights affecting cars on the track
TERRAIN_SHADOWS_THRESHOLD = 0.0  ; ?

[PARTICLES_FX]
FIREWORKS_POS_... = 12.4, 100.5, 340.0   ; x,y,z position for fireworks
FIREWORKS_POS_... = 16.4, 101.0, 341.0   ; x,y,z another second position for fireworks

[WEATHER_FX]
SKY_BELOW_HORIZON = 1  ; how far should sky be rendered below the horizon (default value is 0.2115, set to 1 to have 360° sky)

[SPECTATORS]
; list of meshes used for custom spectators (not "camera_facing.ini" thing), to hide if user chose to hide spectators in certain modes
MESHES = mesh1, mesh2

[KN5]
; prevent patch from optimizing certain meshes in case it causes issues
DISALLOW_MESH_OPTIMIZATIONS = mesh1, mesh2
DISALLOW_MESH_MORE_OPTIMIZATIONS = mesh1, mesh2

[VAO]
OPACITY = 0.9     ; override opacity of VAO patch if set
MULTIPLIER = 1.0  ; override brightness multiplier of VAO patch if set

[WIND]
IGNORE = meshnames?           ; disable wind for certain meshes
DYNAMIC_FLAGS = AUTO          ; Valid values: NONE, AUTO, or regular mesh filter
TREES_NORMALIZATION = 0.8, 1  ; Stretch trees normalization area so original 0.9 would become 0
GRASS_NORMALIZATION = 0.8, 1  ; Stretch grass normalization area so original 0.9 would become 0
RANDOMIZED_OFFSET_BASE = 4.0            ; ? 4.f
RANDOMIZED_OFFSET_REL = 0.0             ; ? 0.5f
RANDOMIZED_OFFSET_CHANGE_SPEED = 5.0    ; ? 5.f
RANDOMIZED_OFFSET_CHANGE_MAX = 0.0      ; ? 0.8f

; not per track-cfg, but in "extension\config\track_adjustments.ini" :
; [AUDIO]
; DISPLAY_DUMMIES = 0           ; 1 to show position of audio objects created by config with [EVENT_...]
; VOLUME = 1.0                  ; 0..1 for patch-sounds like rain and such
```
