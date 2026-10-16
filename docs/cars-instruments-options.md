# General Options

Some miscellaneous instruments options, not really deserving their own page.

```ini
[INSTRUMENTS]
HAZARDS_G_THRESHOLD = -1  ; set G-force for hazards to turn on automatically on sudden braking
SPEED_FIX = 1             ; use speed of powered wheels for speedometer
SPEED_LAG = 0.85          ; speed lag for SPEED_FIX option
SPEED_LIMIT = 0           ; if more than zero, used as upper bound for speed for SPEED_FIX option

[STATUS_BATTERY]
; parameters for overly simplified battery voltage estimation for instruments
; battery voltage reacts to RPM
BASE_VOLTAGE = 12.4  ; base battery voltage
MAX_VOLTAGE = 13.6   ; maximum battery voltage
RPM_LAG = 0.98       ; RPM lag

[STATUS_OIL]
; similar thing, overly simplified estimation for instruments
PRESSURE_BASE = 1.0         ; base oil pressure for idling engine
PRESSURE_STEP = 1.0         ; oil pressure increase for each 1000 RPM
PRESSURE_LAG_UP = 0.998     ; oil pressure increase lag
PRESSURE_LAG_DOWN = 0.9985  ; oil pressure decrease lag

TEMPERATURE_MULT = 1.0         ; relation of oil temperature to water temperature
TEMPERATURE_RPM_FACTOR = 0.03  ; extra increase of oil temperature for each 1000 RPM
TEMPERATURE_LAG_UP = 0.995     ; oil temperature increase lag
TEMPERATURE_LAG_DOWN = 0.995   ; oil temperature decrease lag
```
