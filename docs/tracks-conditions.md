# Conditions

Track configs can define conditions and use them as inputs for intensity of dynamic lights, blending between different values of material variables, parameters for custom audio events and more.

### Syntax

```ini
[CONDITION_...]
NAME = CONDITION_NAME    ; Name for condition to refer to
INPUT = SUN              ; Key for condition input
LUT = (|0=0|90=1|)       ; LUT setting relation between input and output value
LAG = 0.8                ; Lag for smooth transition
LAG_DELAY_ON = 1800      ; How much time in seconds it takes to turn on; if missing, LAG will be used instead
LAG_DELAY_OFF = 0        ; Same but for turning off; with 0 set LAG would be used
LAG_DELAY_FUNC = SQRT    ; Interpolation for non-zero LAG_DELAY_…, available values: SQR, POW3, SQRT, LINEAR
SIMULATE_HEATING = 0.7   ; If above zero, transition would simulate heating by turning more red as it shuts down
BOUND_TO_SPECTATORS = 0  ; If set to 1, input would be multiplied by amount of spectators, I have no idea why
                         ; it’s there in such weird form, but there is a better way now anyway

; Flashing parameters:
FLASHING_FREQUENCY = 0             ; Flashing frequency
FLASHING_MIN_VALUE = 0             ; Flashing would apply multiplier from this min value to 1
FLASHING_SKIP_OFF_STATE = 0        ; Base flashing works as sine wave spending half of the time disabled, set
                                   ; this to 1 to skip those disabled phases
FLASHING_SKIP_DOWNHILL_STATE = 0   ; Set this 1 to skip phases where sine wave gets smaller
FLASHING_SMOOTHNESS = 1            ; Exponent for flashing value (or, set to LINEAR to turn sine wave into
                                   ; linear transition)
FLASHING_NOISE_AMPLITUDE = 0       ; Increase to add some random noise
FLASHING_NOISE_BOUND = 1           ; Maximum speed for randomized noise to change
FLASHING_NOISE_SPEED = 10          ; Rate of change for randomized noise speed to change
FLASHING_LUT = 0                   ; Optional LUT for the noise
FLASHING_SYNCED = 0                ; If set to 1, all things using this condition would have the noise synced
```

LUTs can be referring to a file instead of being inlined, with the same format original AC LUTs are using. Also, these LUTs can provide RGB values instead, allowing for colorful transitions.

For more examples check out “config/tracks/common/conditions.ini”.

### Complex expressions

When referring a condition, or setting INPUT value of a condition, it’s now possible to refer to other previously defined conditions in an expression form:

```ini
[CONDITION_...]
NAME = condition_my_1
INPUT = 'SUN * 2 + TIME'

[CONDITION_...]
NAME = condition_my_2
INPUT = 'condition_my_1 * 4 - 100'

[LIGHT_...]
CONDITION = 'saturate( condition_my_2 * 0.01 + condition_my_1 + TIME )'
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

### Available inputs

- `TIME`: time of day in seconds from 00:00 to 23:59, rounded.

- `TIME_SMOOTH`: time of day in seconds from 00:00 to 23:59, not rounded.

- `SUN`: sun angle in degress (0 for sun in zenith, 90 for sun at the horizon).

- `YEAR_PROGRESS`: year progress from 0 to 1.

- `YEAR_DAY`: day of the year from 1 to 365 (29 of Febuary is skipped, so you can bind certain dates after it without having to worry about it).

  If you need to bind a certain day, use lut:

  ```ini
  [CONDITION_...]
  INPUT = YEAR_DAY     ; 184th day is 4th of July
  LUT = (| 1=0 | 184=0 | 185=1 | 186=0 | 356=0 |)
  ```
  ```ini
  [CONDITION_...]
  INPUT = YEAR_DAY     ; hard winter cuts by day
  LUT = (|1=1|40=1|41=0|332=0|333=1|365=1|)
  ```
  ```ini
  [CONDITION_...]
  INPUT = YEAR_PROGRESS    ; kinda winter fading
  LUT = (| 0=0.5 | 0.1=1 | 0.2=0 | 0.8=0 | 0.9=0.35 | 1=0.5 |)
  ```

- `WEEK_DAY`: day of the week from 1 to 7.

- `AMBIENT`: ambient brightness multiplier, 1.0 at night, and very low (≈0.01) at noon with clear sky (Python function: `ac.ext_getAmbientMult()`).

- `FOG`: fog intensity.

- `FLAG_TYPE`: type of race flag.

  This input also has parameters INPUT_CHANGE_DELAY with a number of seconds for delaying changes for, and INPUT_STAY_FOR with a number of seconds to keep the change for.

  Possible values:

  - 0: no flag is shown, not a race;
  - 1: start of race, everything is all right;
  - 2: caution, yellow flag;
  - 3: slippery track surface¹²;
  - 4: pit lane closed¹²;
  - 5: black flag;
  - 6: slow vehicle on a track²;
  - 7: ambulance on course/final lap¹²;
  - 8: return to pits (drivethrough penalty);
  - 9: return to pits due to a mechanical problem¹²³;
  - 10: unsportsmanlike conduct¹²;
  - 11: ignoring black flag¹²;
  - 12: faster car approaching (blue flag);
  - 13: session finished;
  - 14: one lap left;
  - 15: session suspended²;
  - 16: code 60¹².

  ¹ requires a drawing of some sorts;

  ² won’t be triggered by AC by default, but a custom track or online script can set that flag;

  ³ requires a car number on a board.

- `CAR_ACTIVE_X`: returns 1 if car at pits #X (0-based index) is present, otherwise returns 0.

- `CAR_DAMAGE_X`: returns maximum level of damage of a car at pits #X (0-based index); damage value is the biggest impact speed.

- `CAR_DAMAGE`: return maximum level of damage of any car; damage value is the biggest impact speed.

- `SPECTATORS`: percentage of spectators on a track, from 0 to 1.

- `RAIN`: rain intensity, from 0 to 1.

- `RAIN_WETNESS`: returns track wetness (quickly raises to 1 as rain starts).

- `RAIN_WATER`: returns amount of water on a track (slowly rises to track intensity and stays, defines puddles).

- `ONLINE_RACE`: returns 1 if it’s an online race.

- `ONE`: always returns 1.

- `ZERO`: always returns 0.

- `HOLIDAY`: type of current holiday for fireworks and other festive effects.

  Could be of three main types:

  - Global: trigger by system time, work everywhere;
  - Regional: trigger by system time according to region in Windows settings, in some regions might not trigger at all;
  - Track-based: trigger by time in-game if track is set to be in a certain region.

  Currently supported holidays:

  - 0: None;
  - 1: New year (global);
  - 2: Christmas¹;
  - 3: Victory Day¹;
  - 4: Independence Day²;
  - 5: Halloween²;
  - 6: Japan Fireworks Festival²;
  - 7: Chinese New Year²;
  - 8: Eid Al Adha²;
  - 9: Guy Fawkes Night²;
  - 10: St. Istvan Celebration²;
  - 11: Canada Day²;
  - 12: Victoria Day²;

  ¹: regional (triggered based on system region set in Windows settings);

  ²: regional or track-based (triggered based on system region or if track is in a fitting region country).

  Japan Fireworks Festival takes time in August, by default from 1st to 3rd of August. To change dates according to track’s prefecture, use `[PARTICLES_FX] JAPAN_AUGUST_FESTIVALS_INTERVAL = 1, 3` (default values).

  Let me know if there are other holidays you would want to see.
