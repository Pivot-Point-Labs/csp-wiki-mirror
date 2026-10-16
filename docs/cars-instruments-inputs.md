# Inputs

With **v0.1.25-preview183**, a better way of setting up instruments was created. The idea is to have a single list of inputs available for digital and analog instruments (including conditional text), animations and even emissives (with optional threshold for toggling and possibility to switch to analog mode).

Existing code for old extended instruments was rewritten to avoid having three separate systems running, but I tried to keep things compatible. Still, if you would notice anything breaking, please let me know.

### Syntax

In order to keep things compatible, the way to pick an input might vary for different cases. For example:

Note: "..." stands for INPUT type
```ini
; ANALOG INSTRUMENTS
; New approach:
[ANALOG_INDICATOR_...]
INPUT = AMBIENT_TEMP

; Old-style approach (only works for hours, minutes and seconds to keep clocks working):
[HOUR_INDICATOR]
...

; DIGITAL INSTRUMENTS
; The way to set it via digital_instruments.ini
[ITEM_0]
TYPE_EXT = DRIFT_POINTS

; Old-style approach (works with any input):
[DI_DRIFT_POINTS]
DIGITAL_ITEM = 0

; DIGITAL INSTRUMENTS (CONDITION)
; The way to set it via digital_instruments.ini
[ITEM_0]
TYPE_EXT = CONDITION_TEXT
INPUT = TURBO_WASTEGATE

; CUSTOM ANIMATIONS
; New approach
[ANIMATION_...]
INPUT = LOWBEAM

; Old-style approach (works with any input):
[ANIMATION_...]
BIND_TO_EXTRA_A = 1

; EMISSIVES
; New approach
[EMISSIVE_...]
INPUT = BODY_DAMAGE

; Old-style approach (works with any input):
[EMISSIVE_LIGHT]
...

...
```

### Input parameters

With all those types of inputs, as you can see, you have a section defining the thing. That’s where you can configure input in almost any way you might need.

```ini
[ANIMATION_...]
INPUT = TYRE_PRESSURE
INPUT_SELECTOR = THIRD

INPUT_ADD = 0.0
INPUT_MULT = 1.0
INPUT_MIN = 10.0
INPUT_MAX = 40.0
INPUT_MOD = 5.0
INPUT_LUT = (| 0=0 | 10=20 |)

INPUT_LAG_UP = 0.9
INPUT_LAG_DOWN = 0.95

INPUT_ROUND = 2.0
INPUT_ROUND_MODE = FLOORING

INPUT_STALLED_VALUE = 7.5
INPUT_STALLED_LAG = 0.85

[EMISSIVE_...]
INPUT = BODY_DAMAGE
INPUT_THRESHOLD = 20
INPUT_THRESHOLD_INVERSE = 1
INPUT_DEBUG = 30
```

- `INPUT`: defines type of input, but in some cases, the way to define type might be different. Look at “Syntax” section for mode details.
- `INPUT_SELECTOR`: sets how to deal with several values (for example, both tyre pressure and body damage have four values, for each wheel and for each side). Possible values:
  - `MIN` (alias: `MINIMUM`): pick minimum value;
  - `MAX` (alias: `MAXIMUM`): pick maximum value;
  - `SUM` (alias: `TOTAL`): add up values together;
  - `MULT` (alias: `MULTIPLIED`): multiply values;
  - `AVG` (alias: `AVERAGE`): sum values and divide them by number of values;
  - `LEN` (alias: `LENGTH`): calculate square root of sum of squares (for example, for finding total G-force);
  - `X` (alias: `FIRST`): get first value from the series;
  - `Y` (alias: `SECOND`): get second value from the series;
  - `Z` (alias: `THIRD`): get third value from the series;
  - `W` (alias: `FOURTH`): get fourth value from the series;
  - any number `N`: get Nth value.
- `INPUT_MULT`: multiply value by X;
- `INPUT_ADD`: add X to value;
- `INPUT_MIN`, `INPUT_MAX`: if any of those values are set, original number will be clamped within those bounds, default values are —∞/+∞;
- `INPUT_MOD`: if greater than zero, module from division by that value will be taken instead, before going through look-up table (but after going through min/max check);
- `INPUT_LUT`: optional look-up table allowing to set things like scale or offset as well as something more complex, uses linear interpolation;
- `INPUT_LAG_UP`, `INPUT_LAG_DOWN`: optional smoothment for changing value, applied after LUT. First one is used if actual number is higher than smoothed one, second is for moments when original number is smaller than smoothed one;
- `INPUT_ROUND`: optional rounding to that number (for example, if you want one digit after dot, use `INPUT_ROUND = 0.1`);
- `INPUT_ROUND_MODE`: mode for rounding, could be either:
  - `FLOOR` (alias: `FLOORING`): drop rounded part;
  - `ROUND` (alias: `ROUNDING`): regular rules, go to next step if rounded part is equal or higher than half of `INPUT_ROUND`;
  - `CEIL` (alias: `CEILING`): always go to the next step if any part to be rounded is present;
- `INPUT_STALLED_VALUE`: optional replacement for original number for stalled engine, runs after min/max check, but before optional module division and LUT;
- `INPUT_STALLED_LAG`: if forced stalled value is set, this number would define how smooth is transition;
- `INPUT_THRESHOLD`: emissives in their default mode can be either on or off, this option sets threshold for that switch;
  If you need to specify the range instead, use:
  - `INPUT_THRESHOLD_LOWER` and `INPUT_THRESHOLD_UPPER`: work as A < x < B, excluding A and B;
  - `INPUT_THRESHOLD_LOWER_INC` and `INPUT_THRESHOLD_UPPER_INC`: work as A ≤ x ≤ B, including A and B;
- `INPUT_THRESHOLD_INVERSE`: if set to `0` (for false), emissive would turn on if value is below threshold;
- `INPUT_DEBUG`: easy way to test things, especially for analog instruments — it replaces original value with something else (basically by overriding min/max values as the ones applied first anyway).

In most cases, you don’t need to set those values, patch has some defaults, but it might be useful for some cases.

### Available inputs

Mark “flag” labels inputs which return 1.0 or 0.0 depending on condition (which could be smoothed with lag settings).

- `SPEED`: current speed relative to world, km/h;
- `SPEED_WHEELS`: current speed based on angular speed of powered wheels, km/h;
- `VELOCITY`: current velocity relative to world, 3D vector, m/s;
- `VELOCITY_LOCAL`: current velocity relative to car (X for left/right, Y for up/down), 3D vector, m/s;
- `RPM`: engine RPM;
- `STEER`: rotation of steering wheel, degress;
- `HANDBRAKE`: handbrake status, from 0 to 1;
- `GAS`: throttle pedal status, from 0 to 1;
- `BRAKE`: brake pedal status, from 0 to 1;
- `CLUTCH`: clutch pedal status, from 0 to 1;
- `FUEL`: remaining fuel, in liters;
- `WATER_TEMPERATURE` (alias: `WATER_TEMP`): water temperature, in °C;
- `TURBO`: turbo boost;
- `GEAR`: current gear, with —1 for reverse and 0 for neutral (doesn’t go through neutral when shifting on sequential gearbox), default format is `GEAR` (see “Format” section below);
- `PERF_METER`: performance meter comparing this lap with best, seconds;
- `PERF_METER_DIFF`: in AC performance app, there is that red/green bar, it shows this value;
- `TYRE_WEAR`: tyres wear, four values, from 0 to 1:
  - Front left: `INPUT_SELECTOR = 0`, `X` or `FIRST`;
  - Front right: `INPUT_SELECTOR = 1`, `Y` or `SECOND`;
  - Rear left: `INPUT_SELECTOR = 2`, `Z` or `THIRD`;
  - Rear right: `INPUT_SELECTOR = 3`, `W` or `FOURTH`;
- `TYRE_VIRTUAL_KM`: tyres driven distance, four values, from 0 to 1:
  - Front left: `INPUT_SELECTOR = 0`, `X` or `FIRST`;
  - Front right: `INPUT_SELECTOR = 1`, `Y` or `SECOND`;
  - Rear left: `INPUT_SELECTOR = 2`, `Z` or `THIRD`;
  - Rear right: `INPUT_SELECTOR = 3`, `W` or `FOURTH`;
- `TYRE_DIRT`: dirt levels for tyres, four values, from 0 to 1;
- `TYRE_SLIP`: tyres slip values, four values;
- `TYRE_SLIP_ANGLE`: tyres slip angles, four values;
- `TYRE_SLIP_RATIO`: tyres slip ratio, four values;
- `ENGINE_LIFE` (alias: `ENGINE_DAMAGE`): remaining engine life points, from 0.0 to 1000.0 (alias has inversed threshold by default);
- `SUSP_DAMAGE`: suspension damage, four values, from 0 to 1;
- `GEARBOX_DAMAGE`: gearbox damage, from 0 to 1;
- `BODY_DAMAGE`: maximum speed of collision for given side, four values, in km/h:
  - Front: `INPUT_SELECTOR = 0`, `X` or `FIRST`;
  - Rear: `INPUT_SELECTOR = 1`, `Y` or `SECOND`;
  - Left: `INPUT_SELECTOR = 2`, `Z` or `THIRD`;
  - Right: `INPUT_SELECTOR = 3`, `W` or `FOURTH`;
- `SUSP_TRAVEL`: suspension travel, four values, meters;
- `RIDE_HEIGHT`: ride height, four values, meters;
- `BLIND_SPOT`: blind spot detection, four values;
- `SLIP_RATIO`: slip ratio for wheels, four values;
- `G_FORCE`: current G-force, 3D vector, G;
  - LATERAL: `INPUT_SELECTOR = 0`, `X` or `FIRST`;
  - VERTICAL: `INPUT_SELECTOR = 1`, `Y` or `SECOND`;
  - LONGITUDAL: `INPUT_SELECTOR = 2`, `Z` or `THIRD`;
- `GEAR_GRINDING` (flag): are gears grinding?
- `LAP_TIME`: lap time, seconds;
- `LAP_TIME_BEST`: best lap time, seconds;
- `LAP_TIME_LAST`: last lap time, seconds;
- `LAP_COUNT`: number of laps finished;
- `HORN` (flag): is horn active?
- `POSITION`: car leaderboard position

##### From emissives set

- `LIGHT` (alias: `HEADLIGHTS`, flag): are headlights on?
- `LIGHT_SUGGESTION`: AI headlights suggestion value;
- `BRAKE` (alias: `BRAKE_LIGHTS`, flag): are brake lights on?
- `REVERSE` (alias: `REVERSE_LIGHTS`, flag): are reverse lights on?
- `HAZARD` (flag): are hazards on (with blinking for emissives by default)?
- `LOWBEAM` (flag): are low beams on?
- `HIGHBEAM` (flag): are high beams on?
- `EXTRA_A` (flag): is Extra A thing on?
- `EXTRA_B` (flag): is Extra B thing on?
- `EXTRA_C` (flag): is Extra C thing on?
- `EXTRA_D` (flag): is Extra D thing on?
- `EXTRA_E` (flag): is Extra E thing on?
- `EXTRA_F` (flag): is Extra F thing on?
- `EXTRA_G` (flag): is Extra G thing on?
- `EXTRA_H` (flag): is Extra H thing on?
- `EXTRA_I` (flag): is Extra I thing on?
- `EXTRA_J` (flag): is Extra J thing on?
- `EXTRA_K` (flag): is Extra K thing on?
- `EXTRA_L` (flag): is Extra L thing on?
- `EXTRA_M` (flag): is Extra M thing on?
- `EXTRA_N` (flag): is Extra N thing on?
- `EXTRA_O` (flag): is Extra O thing on?
- `EXTRA_P` (flag): is Extra P thing on?
- `EXTRA_Q` (flag): is Extra Q thing on?
- `EXTRA_R` (flag): is Extra R thing on?
- `EXTRA_S` (flag): is Extra S thing on?
- `EXTRA_T` (flag): is Extra T thing on?
- `DRL` (flag): are daytime running lights on?
- `TURNSIGNAL_LEFT` (flag): are left turning signals on?
- `TURNSIGNAL_RIGHT` (flag): are right turning signals on?
- `TURNSIGNAL_NOHAZARD_LEFT` (flag): are left turning signals on (but not because of hazards)?
- `TURNSIGNAL_NOHAZARD_RIGHT` (flag): are right turning signals on (but not because of hazards)?
- `TURNSIGNAL` (flag): are any turning signals on?
- `TURNSIGNAL_NOHAZARD` (flag): are any turning signals on (but not because of hazards)?
- `CORNERINGLAMP_LEFT` (flag): is left cornering lamp on?
- `CORNERINGLAMP_RIGHT` (flag): is right cornering lamp on?
- `OPENDOORS` (flag): are doors opened?
- `SEATBELT` (flag): is seatbelt set?

##### Separate gears for compatibility and just in case

- `GEAR_R` (flag): is reverse gear on?
- `GEAR_N` (flag): is neutral gear on?
- `GEAR_D` (flag): is drive gear on?
- `GEAR_1` (flag): is first gear on?
- `GEAR_2` (flag): is second gear on?
- `GEAR_3` (flag): is third gear on?
- `GEAR_4` (flag): is fourth gear on?
- `GEAR_5` (flag): is fifth gear on?
- `GEAR_6` (flag): is sixth gear on?
- `GEAR_7` (flag): is seventh gear on?
- `GEAR_8` (flag): is eight gear on?
- `GEAR_9` (flag): is nineth gear on?

##### Extra physics stuff not working in replays for now

- `BRAKEBIAS`: brake bias, from  0.0 to 1.0;
- `ABS` (flag): is ABS on or off?
- `ABS_INACTION` (flag): is ABS currently active (with blinking for emissives by default)?
- `SPEEDLIMITER`: speed limiter, 0 for disabled, km/h;
- `SPEEDLIMITER_INACTION` (flag): is speed limiter currently stopping a car (with blinking for emissives by default)?
- `TYRE_COMPOUND_INDEX`: index of currently tyres set;
- `DIFF_PRELOAD`: differential preload value;
- `TRACTIONCONTROL` (alias: `TC`): traction control mode, integer;
- `TRACTIONCONTROL_INACTION` (alias: `TC_INACTION`, flag): is traction control working now (with blinking for emissives by default)?
- `AWD_FRONT_SHARE_PERC`: amount of torque applied to front axis right now, from 0 to 1;
- `AWD_FRONT_SHARE_NM`: amount of torque applied to front axis right now, N×m;
- `TYRE_PRESSURE` (alias: `TYRES`): tyre pressure, four values;
- `TYRE_TEMPERATURE`: tyre temperature, four values;
- `ENGINE_TORQUE`: current engine torque in Nm;
- `ENGINE_POWER`: current engine power in bhp;
- `KERS_CHARGE`: KERS charge;
- `KERS_CURRENT_KJ`: KERS current;
- `KERS_MAX_KJ`: maximum KERS current;
- `KERS_LOAD`: KERS load;
- `KERS_INPUT`: KERS input;
- `KERS_CHARGING` (flag): is KERS charging?
- `TURBO_BOOST`: turbo boost (could be negative for [extended turbos with `EXT_SPIN_DELAY`](Cars-–-Extra-turbo-options)), has value for each turbo (allowing to set needles bound to specific turbos);
- `TURBO_WASTEGATE`: current turbo wastegate, has value for each turbo (allowing to set needles bound to specific turbos);
- `AUTO_SHIFTING` (flag): is automatic shifting active?
- `MANUAL_SPEED_LIMITER` (flag): is manual speed limiter (externally forced) active?

##### Extended physics

- `USER_SPEEDLIMITER` (flag): is user speed limiter (set with custom physics in electronics.ini) active?
- `ENGINE_MAP`: index of currently selected engine map;
- `CPHYS_SCRIPT_0`: value #0 set by custom physics Lua script;
- `CPHYS_SCRIPT_1`: value #1 set by custom physics Lua script;
- `CPHYS_SCRIPT_2`: value #2 set by custom physics Lua script;
- `CPHYS_SCRIPT_3`: value #3 set by custom physics Lua script;
- `CPHYS_SCRIPT_4`: value #4 set by custom physics Lua script;
- `CPHYS_SCRIPT_5`: value #5 set by custom physics Lua script;
- `CPHYS_SCRIPT_6`: value #6 set by custom physics Lua script;
- `CPHYS_SCRIPT_7`: value #7 set by custom physics Lua script;
- `TC2`;
- `FUELMAP`;

##### Extra numbers added by patch

- `DRIVEN_TOTAL`: total odometer, value in km (with initial value loaded from Odometer app or Sidekick, or being passed from CM);
- `DRIVEN_SESSION`: odometer within current session, value in km;
- `STALLED` (flag): is engine stalled (for now, that means very low RPM for some time)?
- `BATTERY`: estimated battery voltage;
- `OIL_PRESSURE` (alias: `OIL`): estimated oil pressure;
- `OIL_TEMPERATURE` (alias: `OIL_TEMP`): estimated oil temperature;
- `EXHAUST_TEMPERATURE` (alias: `EXHAUST_TEMP`): estimated exhaust temperature;

##### Wipers

- `WIPERS_MODE`: 0 when wipers are off, otherwise, their current mode;
- `WIPERS_PROGRESS`: progress of wipers animation;

##### Some extras for rare cases (maybe for some monitor?)

- `DRIFT_VALID` (flag): is current drifting valid (for example, not offroad)?
- `DRIFT_BONUS_ON` (flag): is drift combo bonus on?
- `DRIFT_COMBO`: drift combo counter, integer;
- `DRIFT_INSTANT`: current drift points, integer;
- `DRIFT_POINTS`: total drift points, integer;
- `TRACK_PROGRESS`: track progress from 0 to 1;
- `COMPASS`: car direction in degrees, 0° is for North, 90° for East, default format is `COMPASS`;

##### Fuel consumption stuff (WIP, formulas might be reworked)

- `FUEL_BURNT`: fuel burnt in liters, in this session;
- `FUEL_BURNT_TOTAL`: fuel burnt in liters, in total;
- `FUEL_CONSUMPTION_KPL`: fuel consumption in kilometers per liter, average from this session;
- `FUEL_CONSUMPTION_LP100K`: fuel consumption in liters per 100 km, average from this session;
- `FUEL_CONSUMPTION_MPG`: fuel consumption in miles per galon, average from this session;
- `FUEL_CONSUMPTION_LPL`: fuel consumption in liters per lap, average from this session;
- `FUEL_CONSUMPTION_KPL_TOTAL`: fuel consumption in kilometers per liter, average in total;
- `FUEL_CONSUMPTION_LP100K_TOTAL`: fuel consumption in liters per 100 km, average in total;
- `FUEL_CONSUMPTION_MPG_TOTAL`: fuel consumption in miles per galon, average in total;
- `FUEL_CONSUMPTION_LPL_TOTAL`: fuel consumption in liters per lap, average in total;
- `FUEL_ESTIMATE_DISTANCE`: estimate distance in meters, from session average consumption;
- `FUEL_ESTIMATE_DISTANCE_TOTAL`: estimate distance in meters, from total average consumption;
- `FUEL_ESTIMATE_TIME`: estimate time in seconds, from session average consumption;
- `FUEL_ESTIMATE_TIME_TOTAL`: estimate time in seconds, from total average consumption;
- `FUEL_ESTIMATE_LAPS`: estimate distance in laps, from session average consumption;
- `FUEL_ESTIMATE_LAPS_TOTAL`: estimate distance in laps, from total average consumption;

#### Racing things

- `POSITION`: position in the race, starting from 1;
- `LAP_TIME`: current lap time in seconds, default format for this and other times is “LAP_TIME”;
- `BEST_LAP_TIME`: best lap time in seconds;
- `LAST_LAP_TIME`: last lap time in seconds;
- `EXPECTED_LAP_TIME`: expected lap time in seconds (from best lap time and performance delta);
- `LAPS_COUNT`: amount of laps driven;
- `FLAG_TYPE`: type of currently shown racing flag (exactly the same as the one in track conditions);

##### Not related to car

- `ONE`: constant value of 1.0;
- `ZERO`: constant value of 0.0;
- `FPS`: current frames per second;
- `FRAME_TIME_MS`: current frame time, milliseconds;
- `AMBIENT_TEMPERATURE` (alias: `AMBIENT_TEMP`): ambient (air) temperature, °C;
- `ROAD_TEMPERATURE` (alias: `ROAD_TEMP`): road temperature, °C;
- `WIND_SPEED`: wind speed, km/h;
- `WIND_VELOCITY`: wind vector in world space, 3D vector, m/s;
- `WIND_DIR`: wind direction in degress, default format is `COMPASS`;
- `TIME`: number of seconds from 00:00, default format is `TIME`;
- `DATE`: current date as timestamp, default format is `DATE`;
- `TIME_HOURS`: numbers of hours, with `INPUT_MOD = 24` by default;
- `TIME_MINUTES`: numbers of minutes, with `INPUT_MOD = 60` by default;
- `TIME_SECONDS`: numbers of seconds, with `INPUT_MOD = 60` by default.

### Format

To use certain types of inputs, like the ones returning lap times, properly for digital displays, some formatting is necessary. Such types usually have it set by default, but you can override that behaviour, or make regular input formatted. More information is available [here](cars-digital-instruments.md).

### More complex expressions

With CSP 0.1.77 it is now possible to have inputs referring to other inputs and using expressions. First of all, to refer to another input you can create new shared inputs:

```ini
[SHARED_INPUT_...]
NAME = my_input  ; name to refer to it with
INPUT = GAS
; all of regular INPUT parameters are available here
```

And to use it later, or just use a complex expression:

```ini
[EMISSIVE_...]
INPUT = 'calc:max(my_input * GAS, BRAKE)'
```

Of course, shared inputs can refer to other shared inputs as well:

```ini
[SHARED_INPUT_...]
NAME = my_other_input
INPUT = 'calc:pow(my_input, 20) + WIND_SPEED'
```

Available functions:

- No arguments (constants):
  - `e`: euler number;
  - `pi`: pi.
- One argument:
  - `abs(x)`: returns absolute value of `x`;
  - `acos(x)`: returns angle in radians;
  - `asin(x)`: returns angle in radians;
  - `atan(x)`: returns angle in radians;
  - `ceil(x)`: rounds up;
  - `cos(x)`: takes angle in radians;
  - `cosh(x)`: takes angle in radians;
  - `exp(x)`: returns `e^x`;
  - `floor(x)`: rounds down;
  - `ln(x)`: natural log;
  - `log(x)`: log of 10;
  - `log10(x)`: log of 10;
  - `saturate(x)`: returns `x` if it’s between 0 and 1, otherwise returns 0 or 1, whatever is closer;
  - `sign(x)`: returns sign of `x` unless it’s 0, otherwise returns 0;
  - `sin(x)`: takes angle in radians;
  - `sinh(x)`: takes angle in radians;
  - `smoothstep(x)`: smoothstep is good for gradients;
  - `smootherstep(x)`: like smoothstep, but even smoother;
  - `sqrt(x)`: returns square root;
  - `tan(x)`: takes angle in radians;
  - `tanh(x)`: takes angle in radians.
- Two arguments:
  - `atan2(x, y)`: turns `x` and `y` into an angle in radians;
  - `max(x, y)`: returns biggest of `x` and `y`;
  - `min(x, y)`: returns smallest of `x` and `y`;
  - `pow(x, y)`: raises `x` in `y` power;
  - `step(x, y)`: if `y` is greater or equal to `x`, returns 1, otherwise returns 0.
- More arguments:
  - `clamp(x, min, max)`: returns `x` if it’s between `min` and `max`, otherwise returns `min` or `max`, whatever is closer;
  - `remap(x, a, b, c, d)`: if `x` equals `a`, returns `c`, if it’s `b`, returns `d`, otherwise linearly interpolates between `c` and `d` (without clamping).
