# Aerodynamics

### New `HEADLIGHTS` input for aero controller
Example:

```ini
[DYNAMIC_CONTROLLER_0]
WING=1
COMBINATOR=ADD ; or MULT, same as any other controller
INPUT=HEADLIGHTS
LUT=controller.lut ; 0 is off, 1 is on
FILTER=0.5
UP_LIMIT=90
DOWN_LIMIT=0
```

**New option to use inline LUTs in aero.ini**

### Full aero map implementation (2D lookup table and many features)
Example implementation:

_aero.ini_
- **note: at least one [WING] element is still required for AC to load**
```ini
[MAP_0]
NAME = name
MAP_CL_RH = filename.2Dlut    ;cl*area versus meters (ride heights at each axle)
MAP_CD_RH = filename.2Dlut    ;cd*area versus meters (ride heights at each axle)
MAP_BALANCE_RH = filename.2Dlut    ;ratio of front:rear cl*area versus meters (ride heights at each axle)
MAP_YAW_CL = filename.lut    ;degrees|multiplier
MAP_YAW_CD = filename.lut    ;degrees|multiplier
MAP_YAW_BALANCE = filename.lut    ;degrees|addition
MAP_ROLL_CL = filename.lut    ;degrees|multiplier
MAP_ROLL_CD = filename.lut    ;degrees|multiplier
MAP_ROLL_BALANCE = filename.lut    ;degrees|addition
MAP_STEER_CL = filename.lut    ;degrees (average at wheels)|multiplier
MAP_STEER_CD = filename.lut    ;degrees (average at wheels)|multiplier
MAP_STEER_BALANCE = filename.lut    ;degrees (average at wheels)|addition
MAP_SPEED_CL = filename.lut    ;kph|multiplier
MAP_SPEED_CD = filename.lut    ;kph|multiplier
MAP_SPEED_BALANCE = filename.lut    ;kph|addition
FRONT_RH_OFFSET = 0.00 ;meters (static ride height offset - it adds to the ride height input that's sent to the 2D-LUT lookup)
REAR_RH_OFFSET = 0.00 ;same as above
CL_MULT = 1.00
CD_MULT = 1.00
BALANCE_OFFSET = 0.00    ;%/100
INTERPOLATION = LINEAR          ; LINEAR, CUBIC
DRAG_OFFSET = 0.00, 0.00    ;meters, meters - left/right, up/down
FRONT_FORCE_DELAY=0.05    ;delay for forces at the front of the car - higher numbers mean less lag
REAR_FORCE_DELAY=0.04    ;delay for forces at the rear of the car - higher numbers mean less lag
DRAG_FORCE_DELAY=0.045    ;delay for drag forces - higher numbers mean less lag
```

2D LUT example (x-axis is front ride height, y-axis is rear - axis values must ascend as you move right and down):
```
    0.015    0.020    0.025
0.020    1    1    1
0.025    1    1    1
0.030    1    1    1
0.035    1    1    1
0.040    1    1    1
```

Tab/space-separated for ease of import from spreadsheet software (e.g. MS Excel). It is recommended that you build the table in Excel and copy and paste it into your 2DLUT file.

### Aero fan implementation (e.g. Chaparral 2J)
Example implementation:

_aero.ini_

```ini
[FAN_0]
NAME=Name
MAP_FORCE_RH=filename.2Dlut          ; meters (ride heights at each axle) vs. force produced
MAP_BALANCE_RH=filename.2Dlut         ; meters (ride heights at each axle) vs. front balance (%/100)
MAP_SPEED_FORCE=filename.lut         ; kph|force_multiplier
MAP_SPEED_BALANCE=filename.lut          ; kph|balance_offset
FRONT_RH_OFFSET=0.000          ; meters (static ride height offset)
REAR_RH_OFFSET=0.000        ; meters (static ride height offset)
FORCE_MULT=1.00
BALANCE_OFFSET=0.00         ; %/100
INTERPOLATION=LINEAR          ; LINEAR, CUBIC
```

### Aero map setup adjustments
Example implementation:

_setup.ini_

```ini
[AEROMAP]
SHOW_CLICKS=0
TAB=AERO
NAME=Aero Configuration ; the setup option's title
LUT=aero_map_setup.lut ; format: display_name|aeromap_index
DEFAULT=0 ; the default index of map (others contained in the LUT will be switched off unless selected in the setup window)
POS_X=0.5
POS_Y=9
HELP=NULL ; vanilla AC options only, for now.
```
