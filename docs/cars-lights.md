# Lights

CSP creates dynamic light sources for cars based on emissive meshes defined in `lights.ini` and custom emissives. Most parameters are automatically guessed from the model, but you can override everything manually. All of these settings go in the car's extended config.

### Section naming

For each light type there is a shared section name (used as a fallback) and a per-index section name. Parameters in the per-index section take priority. For index 0, the shared section is used as a fallback. For index 1 and above, the shared section is ignored.

| Light type | Shared (index 0 fallback) | Per-index |
|---|---|---|
| Headlights | `LIGHT_HEADLIGHTS` | `LIGHT_HEADLIGHT_0`, `LIGHT_HEADLIGHT_1`, … |
| Brake lights | `LIGHT_BRAKES` | `LIGHT_BRAKE_0`, `LIGHT_BRAKE_1`, … |
| Reverse lights | `LIGHT_REVERSE` | `LIGHT_REVERSE_0`, `LIGHT_REVERSE_1`, … |
| KERS lights | `LIGHT_KERS` | `LIGHT_KERS_0`, `LIGHT_KERS_1`, … |
| Open door lights | `LIGHT_OPENDOORS` | `LIGHT_OPENDOORS_0`, `LIGHT_OPENDOORS_1`, … |
| LED panel lights | `LIGHT_LED_PANEL` | `LIGHT_LED_PANEL_0`, `LIGHT_LED_PANEL_1`, … |
| Turn signals (left) | `LIGHT_TURNSIGNALS_LEFT` | `LIGHT_TURNSIGNAL_LEFT_0`, … |
| Turn signals (right) | `LIGHT_TURNSIGNALS_RIGHT` | `LIGHT_TURNSIGNAL_RIGHT_0`, … |
| Cornering lamps (left) | `LIGHT_CORNERINGLAMP_LEFT` | `LIGHT_CORNERINGLAMP_LEFT_0`, … |
| Cornering lamps (right) | `LIGHT_CORNERINGLAMP_RIGHT` | `LIGHT_CORNERINGLAMP_RIGHT_0`, … |

Up to 4 lights are supported per type (indices 0–3). Extra lights and license plate lights use a different naming scheme (see below).

### Common parameters

These parameters are available across all light types listed above:

```ini
[LIGHT_HEADLIGHTS]
; Position and shape
POSITION = 0, 0.7, 1.8           ; light position in car space, guessed from mesh if not set
OFF_POSITION = 0, 0.7, 1.8       ; position used in "off" state, guessed from mesh if not set
MIRROR = 0.7                      ; mirroring offset on X axis for symmetric pair, 0 to disable
OFF_MIRROR = 0.7                  ; mirroring offset for "off" state
OFFSET = 0, 0, 0                 ; added to both on and off positions
OFF_OFFSET = 0, 0, 0             ; added only to the off position
DIRECTION = 0, -0.2, 1           ; light direction
SPOT = 48                        ; spot angle in degrees, 0 for point light
SPOT_SHARPNESS = 0               ; 0 for soft falloff from center, 1 for sharp edge
SPOT_EDGE = 0.12, 0.12, 0.12     ; RGB edge color offset for colored edges
SPOT_EDGE_SHARPNESS = 10         ; how quickly color transitions to edge

; Color
COLOR = 1, 1, 1, 10              ; RGBM color (fourth value is multiplier)
BASE_COLOR = 1, 1, 1, 1          ; multiplied with COLOR
OFF_COLOR = 0.5, 0.5, 0.4, 1    ; color when light is in "off" state
OFF_MULT = 0.1                   ; if OFF_COLOR is not set, it's computed as COLOR × OFF_MULT

; Range and fading
RANGE = 240                      ; how far light reaches in meters
RAW_RANGE = 0                    ; set to 1 to use RANGE directly without internal adjustments
RANGE_GRADIENT_OFFSET = 0        ; at what point of light travel it starts to fade
FADE_AT = 450                    ; distance at which the light source starts fading away
FADE_SMOOTH = 50                 ; smoothness of fading, clamped to [0, FADE_AT]
OFF_RANGE_MULT = 0.5             ; range multiplier for "off" state
OFF_FADE_MULT = 0.3              ; fade multiplier for "off" state

; Rendering
SPECULAR_MULT = 1                ; specular highlight intensity
DIFFUSE_CONCENTRATION = 0.88     ; 0: surfaces facing away are fully lit; 1: only direct surfaces
SINGLE_FREQUENCY = 0             ; 0 for regular light, 1 for something like sodium lamps
VOLUMETRIC_LIGHT = 1             ; enables volumetric light effect (expensive)
LONG_SPECULAR = 1                ; enables long speculars for wet roads with Rain FX

; Binding
BOUND_TO = mesh1, mesh2          ; override guessed emissive mesh names to bind brightness to
BOUND_VERSION = 0                ; bound computation version; set to 1 for newer behavior
BOUND_EMISSIVE_MAX = 500         ; max emissive value (default 500 for BOUND_VERSION=0, 0 for 1)
BOUND_EXP = 1                   ; exponent applied to bound emissive value
RELATIVE_TO = NODE_NAME          ; attach light position to a specific node (useful for animated parts)
ONESIDED = RIGHT                 ; disables mirroring; set to RIGHT to flip to right side only
PREFER_FRONT = -1                ; 0 to force rear meshes, 1 to force front meshes, -1 for auto
EMISSIVE_INDEX = 0               ; which emissive instance to use when there are multiple matches

; Visibility
SELF_LIGHTNING = 0               ; controls whether this light illuminates its own car (see below)
INTERIOR_ONLY = 0                ; only active when camera is inside the car
EXTERIOR_ONLY = 0                ; only active when camera is outside the car
AFFECTS_TRACK = 1                ; whether this light affects the track surface; can also be
                                 ; "INTERIOR_ONLY" to skip car exterior rendering specifically
DISTANT_GLARE = 1                ; show a glare effect when seen from a distance
NO_SELF_SPECULAR = 0             ; skip specular highlight on the car itself
AMBIENT_INFLUENCE = 1            ; how much day/night ambient affects the light

; Fake shadow reduction
FADE_FAKE_SHADOW = 0             ; reduces interior fake shadow when this light is active (0–1)

; Interaction with other systems
DISABLE_WITH_BOUNCED_LIGHT = 0   ; disable when screen-space bounced light from Extra FX is active
DISABLE_WITH_EMISSIVE_LIGHT = 0  ; disable when emissive light from Extra FX is active
SKIP_LIGHT_MAP = 0               ; skip contributing to Extra FX light map
MIRROR_DIRECTION = 0             ; mirror light direction for the symmetric pair

; Wings
AFFECTED_BY_WING = -1            ; index of wing controller affecting this light, -1 for none
AFFECTED_BY_WING_LUT =           ; LUT file for wing effect

; Blinking pattern
BLINKING_PATTERN = (|0=1|0.5=0.8|1=1)  ; LUT for blinking pattern, input is time
BLINKING_DURATION = 2            ; pattern duration in seconds (normalizes the LUT)
```

### About `SELF_LIGHTNING`

This parameter (yes, it's a typo for "self lighting" kept for compatibility) controls whether a light illuminates its own car:

- `0`: light never illuminates the car it belongs to; this is the default for headlights since you don't want to see the headlight beam lighting up the car body from the front;
- `1`: light illuminates the car from both interior and exterior views; commonly used for interior dashboard lights, open door lights and other lights that should be visible on the car itself;
- `EXTERIORONLY`: light only illuminates the car when viewed from outside (e.g. chase cam, free cam), but not from the interior; this is the default for brake lights and reverse lights, so the red glow is visible on the bumper from third person but doesn't bleed through the dashboard in cockpit view.

### Line lights

Any section supporting the common parameters can be turned into a line light by specifying both endpoints:

```ini
[LIGHT_HEADLIGHTS]
LINE_FROM = 0.422, 0.1, -0.9
LINE_TO = 0.422, 0.1, 0.9
COLOR_FROM = 1, 0, 0, 5         ; color at the start point
COLOR_TO = 0, 1, 0, 5           ; color at the end point (if different from COLOR_FROM)
```

When `LINE_FROM` and `LINE_TO` are set, the light becomes a line light and the `RANGE_GRADIENT_OFFSET` is automatically set to 0.

---

## Headlights

Headlights have the most extensive parameters. Defaults depend on the car's year — older cars get wider, softer beams and more ancient-looking defaults.

```ini
[LIGHT_HEADLIGHTS]
; Spot shape
SPOT = 48                        ; spot angle in degrees, default depends on car year
SPOT_SHARPNESS = 0
SPOT_UP = 0.1, 1, 0             ; normalized up vector for asymmetric beam pattern;
                                 ; slightly angled for LHD/RHD by default on non-racing cars

; Second spot (wider ambient glow around main beam)
SECOND_SPOT = 144                ; angle for the wider ambient cone
SECOND_SPOT_SHARPNESS = 0.7
SECOND_SPOT_SKIP = 0.3           ; gap between main and second spot
SECOND_SPOT_RANGE = 20           ; range of second spot in meters
SECOND_SPOT_INTENSITY = 0.27     ; brightness multiplier for second spot

; Popup headlights animation
POPUP_ENABLED = 1                ; whether popup headlight animation is active
POPUP_START = 0.05               ; animation progress at which light starts appearing
POPUP_END = 0.7                  ; animation progress at which light is fully active
POPUP_SECOND_SPOT_INITIAL_VALUE = 0.4
POPUP_SECOND_SPOT_EXP = 0.6
POPUP_EDGE_OFFSET = 0.5
POPUP_EDGE_EXP = 0.3

; Shadows
SHADOWS_CULL_MODE =              ; shadow culling mode override

; Low beam behavior
LOWBEAM_MULT = 0.5               ; brightness multiplier when in low beam mode
LOWBEAM_RANGE_MAX = 70           ; maximum range in meters for low beams
LOWBEAM_RANGE_MULT = 0.8         ; range multiplier for low beams
LOWBEAM_RANGE_ONCOMING_MULT = 0.4  ; range multiplier for oncoming traffic in low beam mode;
                                    ; default depends on how modern the car is
```

Default values:
- `RANGE` defaults to about 240 m (adjusted by car year);
- `FADE_AT` defaults to 450 m;
- `SELF_LIGHTNING` defaults to `0` (headlights don't light up the car itself);
- `VOLUMETRIC_LIGHT` defaults to `1`;
- `AFFECTS_TRACK` defaults to `1`.

---

## Brake lights

```ini
[LIGHT_BRAKES]
DIRECTION = 0, 0, -1
SPOT = 175                       ; default depends on how modern the car is
SPOT_SHARPNESS = 0.3
SPOT_EDGE = 0.12, 0.12, 0.12
SPOT_EDGE_SHARPNESS = 10
```

Default values:
- `RANGE` defaults to 5 m;
- `FADE_AT` defaults to 120 m;
- `SELF_LIGHTNING` defaults to `EXTERIORONLY`;
- `EXTERIOR_ONLY` defaults to `1`.

---

## KERS lights

Used for the KERS harvesting indicator on racing cars. Same parameter set as brake lights.

```ini
[LIGHT_KERS]
DIRECTION = 0, 0, -1
SPOT = 175
SPOT_SHARPNESS = 0.3
SPOT_EDGE = 0.12, 0.12, 0.12
SPOT_EDGE_SHARPNESS = 10
```

Default values:
- `RANGE` defaults to 3 m;
- `FADE_AT` defaults to 120 m;
- `SELF_LIGHTNING` defaults to `EXTERIORONLY`;
- `EXTERIOR_ONLY` defaults to `1`.

---

## Reverse lights

```ini
[LIGHT_REVERSE]
DIRECTION = 0, 0, -1
SPOT = 175
SPOT_SHARPNESS = 0.3
SPOT_EDGE = 1, 1, 1
SPOT_EDGE_SHARPNESS = 0
```

Default values:
- `RANGE` defaults to 3 m;
- `FADE_AT` defaults to 120 m;
- `SELF_LIGHTNING` defaults to `EXTERIORONLY`;
- `EXTERIOR_ONLY` defaults to `1`.

---

## Turn signals

Turn signals use separate sections for left and right. Direction is guessed from mesh normals.

```ini
[LIGHT_TURNSIGNALS_LEFT]
DIRECTION = -1, 0, 0            ; guessed from mesh normals
SPOT = 175
SPOT_SHARPNESS = 0.6
SPOT_EDGE = 0.12, 0.12, 0.12
SPOT_EDGE_SHARPNESS = 0
```

Default values:
- `RANGE` defaults to 2.4 m;
- `FADE_AT` defaults to 60 m;
- `SELF_LIGHTNING` defaults to `EXTERIORONLY`;
- `EXTERIOR_ONLY` defaults to `1`.

---

## Cornering lamps

Same structure as turn signals, but with a wider range. Activated by steering input.

```ini
[LIGHT_CORNERINGLAMP_LEFT]
DIRECTION = -1, 0, 0
SPOT = 175
SPOT_SHARPNESS = 0.6
```

Default values:
- `RANGE` defaults to 4.8 m;
- `FADE_AT` defaults to 90 m.

---

## Open door lights

Lights that activate when doors are opened (puddle lights and similar).

```ini
[LIGHT_OPENDOORS]
DIRECTION = 0, -1, -0.15        ; points downward by default
SPOT = 160
SPOT_SHARPNESS = 0.8
```

Default values:
- `RANGE` defaults to 2 m;
- `FADE_AT` defaults to 40 m;
- `SELF_LIGHTNING` defaults to `1` (these lights illuminate the car itself);
- Shadows are enabled by default.

---

## LED panel lights

For cars with LED number panels (lumirank).

```ini
[LIGHT_LED_PANEL]
POSITION = 0, 0, 0              ; defaults to position from the lumirank definition
DIRECTION = 0, 0, -1            ; defaults to direction from the lumirank definition
SPOT = 180
SPOT_SHARPNESS = 0.6
MIRROR = 0
COLOR = 1, 1, 1, 8
```

Default values:
- `RANGE` defaults to 5 m;
- `FADE_AT` defaults to 80 m;
- `SELF_LIGHTNING` defaults to `1`.

---

## License plate lights

License plate lights are guessed from meshes with `Plate_D.dds` and `Plate_NM.dds` textures. They use a single non-indexed section.

```ini
[LIGHT_LICENSEPLATE]
ACTIVE = 1
MESHES = plate_mesh              ; override auto-detection based on plate textures
MESH_FILTER_DIRECTION = 0, 0, -1  ; used to filter vertices facing a certain direction
MESH_FILTER_OFFSET = 0
COLOR = 1, 0.9, 0.8, 2
LAYOUT = TWO_ON_TOP              ; light placement around the plate

; Layout-specific defaults (can be overridden)
SPOT = 170
SPOT_SHARPNESS = 0.9
RANGE = 0.3
RANGE_GRADIENT_OFFSET = 0.5
OFFSET = 0, 0.03, -0.05         ; offset from computed position
FALLBACK_EMISSIVE = 1, 1, 1, 0.3  ; emissive value for the plate mesh when lit

FADE_AT = 12
FADE_SMOOTH = 8
AFFECTS_TRACK = 0
```

Supported `LAYOUT` values:
- `AT_SIDES`: two lights on the sides of the plate;
- `TWO_ON_TOP`: two lights along the top edge (default);
- `ONE_ON_TOP`: single light centered on the top edge;
- `TWO_ON_BOTTOM`: two lights along the bottom edge;
- `ONE_ON_BOTTOM`: single light centered on the bottom edge;
- `NONE`: disables license plate lights.

---

## Extra lights

Extra lights are custom light sources, useful for underglow, neons, interior dashboard light and similar effects. The first extra light (index 0, `[LIGHT_EXTRA]`) is the automatically guessed dashboard light. Additional ones can be added with `[LIGHT_EXTRA_...]` (using the settings iterator syntax, e.g. `[LIGHT_EXTRA_UNDERGLOW]`, `[LIGHT_EXTRA_1]`, etc.).

For a quick reference on extra lights syntax, see [Extra Lights](extra-lights.md).

```ini
[LIGHT_EXTRA_...]
; Either use a point light:
POSITION = 1, 0, 1
COLOR = 10

; Or a line light:
LINE_FROM = 0.422, 0.1, -0.9
LINE_TO = 0.422, 0.1, 0.9
COLOR = 10
; optional per-endpoint colors:
COLOR_FROM = 0, 1, 0
COLOR_TO = 1, 0, 0

DIRECTION = 0, -1, 0
SPOT = 210
SPOT_SHARPNESS = 0.75
SPOT_EDGE = 0
SPOT_EDGE_SHARPNESS = 0
MIRROR = 0

; Binding to car state
BIND_TO_HEADLIGHTS = 1           ; follow headlights; can be EXCLUDING_HIGHBEAMS_FLASH or
                                 ; INCLUDING_HIGHBEAMS_FLASH as a second value for fine control
BIND_TO_HIGHBEAM = 0             ; only active with high beams
BIND_TO_LOWBEAM = 0              ; only active with low beams
BIND_TO_BRAKELIGHTS = 0          ; follow brake lights
BIND_TO_EXTRA_A = 0              ; bind to extra switch A (also B, C, D)
NOT_WITH_HEADLIGHTS = 0          ; turn off when headlights are on

; Emissive binding
BOUND_TO = mesh_name             ; bind brightness to emissive of a specific mesh
BOUND_EMISSIVE_MAX = 0.5

; Turn on/off lag
LAG = 0                          ; lag for both on and off (overridden by LAG_ON/LAG_OFF)
LAG_ON = 0                       ; lag when turning on
LAG_OFF = 0                      ; lag when turning off

; Other common parameters also apply (SELF_LIGHTNING, EXTERIOR_ONLY, etc.)
SELF_LIGHTNING = 1
EXTERIOR_ONLY = 0
INTERIOR_ONLY = 0
SKIP_LIGHT_MAP = 1
VOLUMETRIC_LIGHT = 0
FADE_AT = 7
FADE_SMOOTH = 2
FADE_FAKE_SHADOW = 0.8
RANGE = 0.25
RANGE_GRADIENT_OFFSET = 0.75
DIFFUSE_CONCENTRATION = 0.88
SPECULAR_MULT = 0
```

Default values for extra lights:
- `RANGE` defaults to 0.25 m;
- `FADE_AT` defaults to 7 m;
- `SELF_LIGHTNING` defaults to `1`;
- `INTERIOR_ONLY` defaults to `1` (for the auto-guessed dashboard light at index 0);
- `SKIP_LIGHT_MAP` defaults to `1`.

---

## Brake disc glow lights

Dynamic lights from glowing brake discs, based on brake temperature data.

```ini
[LIGHT_BRAKEDISCS_FRONT]
ACTIVE = 1

[LIGHT_BRAKEDISCS_REAR]
ACTIVE = 0

; Shared parameters (both sections fall back to [LIGHT_BRAKEDISCS])
[LIGHT_BRAKEDISCS]
COLOR = 1, 0.5, 0, 1.2          ; glow color
GLOW_BOUNDARY_FROM = 1           ; temperature boundary where glow starts
GLOW_BOUNDARY_TO = 10            ; temperature boundary where glow is at full brightness
POSITION = 0, 0, 0               ; position offset (mirrored automatically for left/right)
DIRECTION = 1, 0, 0              ; light direction (mirrored automatically for left/right)
SPOT = 130
SPOT_SHARPNESS = 0.8
```

Default values:
- Front brake discs are active by default, rear are not;
- `RANGE` defaults to 0.65 m;
- `FADE_AT` defaults to 30 m.

---

## Bounced light

When headlights or brake lights affect the track, CSP can create a fake bounced light that reflects back onto the car. This section controls that behavior.

```ini
; For headlights:
[BOUNCED_HEADLIGHTS]
ACTIVE = 1
MULT = 1, 1, 1, 1               ; RGBM multiplier for bounced light
OFFSET = 7                       ; radius of the bounced light
FALLOFF = 0.7
GRADIENT_OFFSET = 0.8
FADE_AT = 200
FADE_SMOOTH = 50

; For brake lights (same parameters):
[BOUNCED_BRAKE_LIGHTS]
ACTIVE = 1
MULT = 1, 1, 1, 1
; ...same parameters as above

; Shared fallback for both:
[BOUNCED]
ACTIVE = 1
; ...same parameters
```

Bounced lights are automatically disabled when screen-space bounced light from Extra FX is active.

---

## Bounced interior light

Light from headlights bouncing onto the interior ceiling.

```ini
[BOUNCED_INTERIOR_LIGHT]
ACTIVE = 1
MULT = 1, 1, 1, 1
OFFSET = 0, -1, 3               ; position offset from driver eyes
DIRECTION = 0, 1, -2
SPOT = 20
SPOT_SHARPNESS = 0.9
RANGE = 3.2
RANGE_GRADIENT_OFFSET = 0.9
```

Unlike the exterior bounced light, this is kept active by default even when screen-space bounced lighting is enabled, since it's too precise for screen-space to recreate accurately.

---

## Bounced mirror light

Light reflected from interior mirrors. Automatically detected from mirrors inside the car interior.

```ini
[BOUNCED_MIRROR_LIGHT]
ACTIVE = 1
DISABLE_WITH_BOUNCED_LIGHT = 0
DISABLE_WITH_EMISSIVE_LIGHT = 0
```

---

### Emissive compatibility fix

If CSP detects that many extra lights have abnormally high emissive values (a sign of configs made on broken CSP versions), it automatically applies an emissive compatibility fix. You can control this with:

```ini
[BASIC]
NO_NEED_FOR_LIGHTS_FIX = 1       ; set to 1 to skip the fix if lights look correct
NEEDS_LIGHTS_FIX = 0             ; set to 1 to force the fix
```

### Guessing

Most of these parameters are automatically guessed from the car model, its `lights.ini`, custom emissives, car class and production year. Parameters that are not set in the config are computed based on:
- Mesh positions and emissive colors from `lights.ini` and custom emissive definitions;
- The car's production year (older cars get wider, softer headlight beams);
- Whether the car is a racing car, open wheeler or road car;
- Whether it's left-hand or right-hand drive (affects headlight beam asymmetry).
