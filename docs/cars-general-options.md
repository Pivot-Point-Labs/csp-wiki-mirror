# General Options

There are some general options for cars, allowing to tweak some things of how patch works with them.

```ini
[BASIC]
RACING_CAR = 0                 ; By default CSP uses car class to determine if car is a race car,
                               ; and it uses this value a lot to determine default parameters (for
                               ; example, racing cars don’t have low beams by default)
OPEN_WHEELER = 0               ; CSP uses this flag for guessing some parameters if not set
                               ; explicitly (for example, for how sparks or tyres would look, or
                               ; even how car is rendered in rendering queue); by default it tries
                               ; to detect this value from tags in “ui_car.json”
RALLY_CAR = 0                  ; Similar case, although rally check is only used for switching
                               ; headlights to rally mode if it’s a single car race
DIESEL_ENGINE = 0              ; If engine is diesel or not (used for exhaust smoke color)
BRAKES_THRESHOLD = 0.01        ; How much brake pedal should be pressed for brake lights to turn on
LIGHT_DAMAGE_SPEED_MIN = 80    ; Collision speed for lights to start breaking
LIGHT_DAMAGE_SPEED_MAX = 120   ; Collision speed for lights to fully break
IS_LOW_BEAM_AVAILABLE = 1      ; Are low beams available (by default available on street cars only)
HEADLIGHTS_ARE_HEADLIGHTS = 1  ; Are headlights what they are (few modded cars use headlights
                               ; as a way to animate dashboard or things like that instead)
STOP_LODS_ADJUSTMENT = 0       ; Prevents patch from adjusting LODs even if user prefers LODs to
                               ; work differently (like, forcing LOD B for other cars)
IGNORE_OTHER_CONFIGS = 0       ; Set to 1 to ignore other configs that may be available in other places
NO_NEED_FOR_LIGHTS_FIX=1       ; For cars that were made on broken CSP versions; set to 0 if extra
                               ; lights are extremely bright (auto-guessed by default)
SPARKS_UPWARDS_FORCE = 300     ; Multiplier for force acting on sparks as fly from below the car
                               ; (by default 500 for open wheelers, 300 for racing cars, 100 for
                               ; the rest)

[DATA]
DISABLE_ANALOGINSTRUMENTSINI = 1  ; Disables “analog_instruments.ini” completely, so you could
                                  ; recreate it with custom analog instruments
DISABLE_LIGHTSINI = 1             ; Disables “lights.ini” completely, so you could recreate it
                                  ; with custom emissives
LIGHT_ANIMATION_TIME = 1          ; Alter duration of headlights animation

; These options allow to alter the way lights from “lights.ini” work
LIGHT_SWITCH_LAG_mesh_name = 0.9  ; Replace lag for “mesh_name” from “lights.ini”
LIGHT_HEATING_K_mesh_name = 0.9   ; Replace heating coefficient for “mesh_name” from “lights.ini”

; Temporary and might be removed later
FAKE_HIGHBEAMS_INDICATOR_mesh_name = 0.9  ; Change behavior of some green “mesh_name” dashboard
                                  ; indicator from “lights.ini”, to change its color to blue
                                  ; for high beams

[KN5]
; Prevent patch from optimizing certain meshes in case it causes issues
DISALLOW_MESH_OPTIMIZATIONS = mesh1, mesh2
DISALLOW_MESH_MORE_OPTIMIZATIONS = mesh1, mesh2

[LOADING_SCREEN_DETAILS]
; Prevent patch from optimizing certain meshes in case it causes issues
COMMENT = Additional comment

[EXTRA_GUESSING]
FIX_WINDSCREENS = 1  ; By default CSP would try to automatically find and apply ksWindscreen
                     ; shader for windscreen materials, set this to 0 to disable

[VAO]
OPACITY = 0.9     ; override opacity of VAO patch if set
MULTIPLIER = 1.0  ; override brightness multiplier of VAO patch if set
```

### Lighting tweaks

```ini
[LIGHTING]
; Parameters for fake shadow in the bottom half of the interior, for headlights of cars behind
INTERIOR_FAKE_SHADOW_OPACITY = 0.9  ; Opacity
INTERIOR_FAKE_SHADOW_HEIGHT = 0.1   ; Height, or Y coordinate of shadow’s boundary
INTERIOR_FAKE_SHADOW_FADE = 0.2     ; How smooth is the transition

; Parameters for fake shadow up top, to stop track lights from lighting up things close to the ceiling
INTERIOR_FAKE_UPPER_SHADOW_HEIGHT = -0.1  ; Height, or Y coordinate of shadow’s boundary
INTERIOR_FAKE_UPPER_SHADOW_FADE = 0.1     ; How smooth is the transition

; Multipliers for emissive values in “lights.ini”, a way to fix for older cars with dimmer lights
EMISSIVE_MULT = 1                ; General multiplier
EMISSIVE_HEADLIGHTS_MULT = 1     ; Multiplier for headlights
EMISSIVE_BRAKELIGHTS_MULT = 1    ; Multiplier for brake lights
EMISSIVE_PARKINGLIGHTS_MULT = 1  ; Multiplier for parking lights

; Other lighting parameters
LIT_MULT = 1                 ; How much car reacts to dynamic lights
SPECULAR_MULT = 1            ; How bright are speculars on the car
FULLY_SHADOWED_INTERIOR = 1  ; If shadows are not available, render interior fully shadowed
```
