# Emissive Objects

Originally, AC has `lights.ini` allowing you to make things glow depending on conditions (two conditions, in fact, headlights and brake lights). But if you’d like to set things in more details, now patch has more options.

### Syntax

```ini
[EMISSIVE_REVERSE_0]
NAME = _ext_REVERSE_LIGHTS  ; name (or names) of a mesh to glow (MESHES also works as an alternative key)
COLOR = 25, 25, 25          ; glowing color if condition is met
OFF_COLOR = 0, 0, 0         ; glowing color otherwise, default value is 0
LAG = 0.8                   ; with zero, turns on and off immediately
SIMULATE_HEATING = 0.3      ; adds heating effect, going through orange tint while turning on and off
LOCATION = REAR             ; light location used for damage and light guessing, default value depends on type
ACT_AS_HEADLIGHTS = 0       ; if set to 1, emissiveness is raised when camera is caught in car’s headlights
```

### Supported types

- `EMISSIVE_LIGHT_N`: headlights, default location is FRONT;
- `EMISSIVE_BRAKE_N`: brake lights, default location is REAR;
- `EMISSIVE_REVERSE_N`: reverse lights (for reverse gear), default location is REAR;
- `EMISSIVE_TURNSIGNAL_LEFT_N`: turning signal, left (don’t forget to split into front and rear so guessing would work);
- `EMISSIVE_TURNSIGNAL_RIGHT_N`: turning signal, right;
- `EMISSIVE_CORNERINGLAMP_LEFT_N`: cornering lamp, left, with `STEER_THRESHOLD` parameter in degress;
- `EMISSIVE_CORNERINGLAMP_RIGHT_N`: cornering lamp, right, with `STEER_THRESHOLD` parameter;
- `EMISSIVE_LOWBEAM_N`: active only with lights in low beam state;
- `EMISSIVE_HIGHBEAM_N`: active only with lights in low beam state (either of them added would automatically disable patch trying to tweak emissiveness of `lights.ini` lights for low/high beams);
- `EMISSIVE_EXTRA_A_N`, `EMISSIVE_EXTRA_B_N`, `EMISSIVE_EXTRA_C_N`, `EMISSIVE_EXTRA_D_N`: four extra emissive objects for any custom need, each with its own shortcut to switch on an off, with replay and online support.

### Supported types for interior indicators (default location is `NONE`)

- `EMISSIVE_HAZARD_N`: hazards (like that red button on dashboard);
- `EMISSIVE_HANDBRAKE_N`: handbrake indicator;
- `EMISSIVE_BATTERY_N`: battery indicator;
- `EMISSIVE_TYRES_N`: indicator for flatten tyres, with `PRESSURE_THRESHOLD` parameter;
- `EMISSIVE_ABS_N`: indicator for ABS, on if ABS is on;
- `EMISSIVE_ABS_INACTION_N`: looks like you wouldn’t need it? if any car has it, please let me know;
- `EMISSIVE_TRACTIONCONTROL_N`: indicator for traction control, on if TC is on (usually, it’s a warning signal for when TC is off, so, use `COLOR = 0, 0, 0` and `OFF_COLOR = 25, 0, 0`);
- `EMISSIVE_TRACTIONCONTROL_INACTION_N`: triggered when TC is active and working;
- `EMISSIVE_TURNSIGNAL_N`: joined turning lights indicator for dashboard, like the one in Ferrari F40;
- `EMISSIVE_ENGINE_DAMAGE_N`: check engine lamp, with `ENGINE_LIFE_THRESHOLD` parameter;
- `EMISSIVE_ENGINE_TEMP_N`: engine temperature, with `TEMP_MIN`, `TEMP_MAX` and `TEMP_EXP` parameters to turn on gradually;
- `EMISSIVE_GEAR_R_N`: triggered with reverse gear;
- `EMISSIVE_GEAR_N_N`: triggered with neutral gear;
- `EMISSIVE_GEAR_D_N`: triggered with “drive” gear;
- `EMISSIVE_GEAR_…_N`: triggered with a specific 1…9 gear;
- `EMISSIVE_OPENDOORS_N`: triggered if doors are opened.

### Custom inputs

Emissives support custom inputs. You can find more information [here](cars-instruments-inputs.md).

**Important note:** although custom inputs usually give you a numerical value (with all those lags, LUTs and what not), custom emissives by default only turn on when that numerical value exceedes certain threshold. You can change that behaviour by using `USE_SMOOTH_TRANSITION = 1`.

```ini
[EMISSIVE_...]
INPUT = BODY_DAMAGE          ; BIND_TO also works as an alternative key
INPUT_THRESHOLD = 20
NAME = _ext_DAMAGE_LIGHT
COLOR = 25, 0, 0
```

You can also force an emissive off with a separate input:

```ini
FORCE_OFF_INPUT = HAZARD     ; FORCE_OFF_BIND_TO also works as an alternative key
```

With `FORCE_OFF_INPUT`, all `FORCE_OFF_`-prefixed input parameters apply (such as `FORCE_OFF_LUT`, etc.).

Although for exterior indicators, I would recommend to keep using `EMISSIVE_LIGHT_N` syntax for now, until I rewrite guesser to work with new emissive types. That part is such a mess at the moment.

### Other parameters

- `TOGGLE_VISIBILITY = 0`: set to 1 and mesh would disappear if inactive;
  - `TOGGLE_VISIBILITY_INVERSE = 0`: set to 1 to inverse behavior of `TOGGLE_VISIBILITY`;
- `USE_SMOOTH_TRANSITION = 0`: use numerical output of INPUT instead of a flag comparing it with `INPUT_THRESHOLD`;
- `ONLY_WITH_HEADLIGHTS = 0`: if set to 1, emissive only activates when headlights are on (default depends on type);
- `CAST_LIGHT = 1`: for specific types of lights, patch can try and guess dynamic lights, same as with `lights.ini` (set this parameter to 0 to disable it if needed);
- `CLUSTER_THRESHOLD = 0.5`: how to guess dynamic lights based on model;
- `BIND_AS = LICENSE_PLATE`: set this glowing mesh to control brightness of license plate dynamic light (which is guessed and set separately, that’s why it needs to be bound like that);
- `FALLBACK_HEADLIGHTS_COLOR = 10, 10, 10`: emissive color used if condition is not met and headlights are enabled, not used at all if parameter is not set;
- `FALLBACK_HIGHBEAM_COLOR = 20, 20, 20`: this one is used if condition is not met, after `FALLBACK_BRAKES_COLOR`, but before `FALLBACK_LOWBEAM_COLOR`;
- `FALLBACK_LOWBEAM_COLOR = 5, 5, 5`: and this one is after `FALLBACK_HEADLIGHTS_COLOR`, but before `FALLBACK_HEADLIGHTS_COLOR`;
- `FALLBACK_BRAKES_COLOR = 15, 0, 0`: emissive color used if condition is not met and brake lights are active, works before `FALLBACK_HEADLIGHTS_COLOR`;
- `FALLBACK_BRAKES_COLOR_HIGHER = 1`: with this parameter set to 1, `FALLBACK_BRAKES_COLOR` will be used before main `COLOR`.
- `FALLBACK_BASE_COLOR = 0, 0, 0 `: emissive color used when headlights are off, 0 by default
- `FALLBACK_IDLE_COLOR = 0, 0, 0 `: emissive color used engine is in idle, 0 by default
- `FALLBACK_DRL_COLOR = 0, 0, 0 `: emissive color with DRL lights


With `FALLBACK_HEADLIGHTS_COLOR` and `FALLBACK_BRAKES_COLOR`, you can bind a single mesh to act as turning signal, brakes light and parking (rear) light. Or, with `FALLBACK_BRAKES_COLOR` and `FALLBACK_BRAKES_COLOR_HIGHER`, you can set a mesh to act as reverse light, but once brake pedal is pressed, reverse light would turn red.

### Fallback color evaluation order

For reference, the full fallback evaluation order (top to bottom, first match wins):

1. Main `COLOR` (if emissive is on and `FALLBACK_BRAKES_COLOR_HIGHER` is not set)
2. `FALLBACK_BRAKES_COLOR` (if brakes are on and emissive is off)
3. Main `COLOR` with `FALLBACK_BRAKES_COLOR_HIGHER = 1` (brakes override even when on)
4. `FALLBACK_HIGHBEAM_COLOR` (if high beams are on)
5. `FALLBACK_LOWBEAM_COLOR` (if low beams are on)
6. `FALLBACK_HEADLIGHTS_COLOR` (if headlights are on)
7. `FALLBACK_DRL_COLOR` (if daytime running lights are on)
8. `FALLBACK_IDLE_COLOR` (if engine is running / not stalled)
9. `FALLBACK_BASE_COLOR` (always, when headlights are off)
10. `OFF_COLOR` (final fallback)

### Blinking, option A

It so happened that now, there are two ways to make emissive blink. Should’ve named the second (B) option differently… First one is good to use with turn signals or indicators: unless some opposite input is triggered, it would finish blinking loop with given amount of times (in most cases, 1). Second option would just shut down emissive without finishing the sequence.

- `BLINK_REPEAT = 1                ; just make it blink`
- `BLINK_FREQENCY_HZ = 2.4         ; sets frequency for blinking`
- `BLINK_FREQENCY_HAZARDS_HZ = 2   ; if needed, different frequency for hazards`
- `;;; BLINK = 1   ; alternatively you can make it only blink once or this minimum amount of blinks`

(`REPEAT_FREQUENCY_HZ` and `REPEAT_FREQUENCY_HAZARDS_HZ` are wrong, patch accidentally divides their values by two, that behavior is kept for compatibility.)

### Blinking, option B

That option won’t finish a sequence once light is off, and with LUT support is meant for something more visual, like slowly fading in and out neon lights:

- `BLINKING_PATTERN = (|0=1|0.5=0.8|1=1|2=0.6|3=0.8|3.5=1)`: sets blinking pattern as LUT (could be a file name as well), input is blinking pattern time;
- `BLINKING_DURATION = 2`: optional time for blinking pattern in seconds (if set, then pattern will be normalized).

Here is an example on how to use blinking pattern: [config of BMW E30 Drift](https://github.com/ac-custom-shaders-patch/acc-extension-config/blob/master/config/cars/kunos/bmw_m3_e30_drift.ini#L21).

### Animated turn signals

For animated turn signals, you can set a range of meshes to work (similar to how RPM series instrument works, just split your turn signal mesh into pieces). To specify them, use either:

```ini
RANGE_START_INDEX = 0
RANGE_END_INDEX = 2
RANGE_PREFIX = _ext_turnsig_left_
```

Which would search for `_ext_turnsig_left_0`, `_ext_turnsig_left_1`, `_ext_turnsig_left_2`, or:

```ini
RANGE_NAMES = _ext_turnsig_left_0, _ext_turnsig_left_1, _ext_turnsig_left_2
```

Which would search for same three meshes, but with `RANGE_NAMES`, you can use different order or even non-sequentially named meshes. Other parameters for animated turn signals:

- `RANGE_DELAY = 0.1`: delay in seconds between pieces flashing up;
- `SMOOTH_IN = 1`: turn on in animated fashion;
- `SMOOTH_OUT = 0`: turn off in animated fashion (cars usually don’t do that).

### Couple of small hints

- Each time patch parses color value, it checks for fourth number and multiplies color by it, so, if you want to make it brighter, just add fourth value different from 1;
- Although you could use `BLINKING_PATTERN` for extra lights as well, it’s better to use `BOUND_TO` instead, as it would ensure lights are in sync with emissives;
- You can find a lot of examples [here](https://github.com/ac-custom-shaders-patch/acc-extension-config/tree/master/config/cars/kunos).
