# New in 2019


## New optional traction control system. Allows for changes to slip target & cut amount.

### Example implementation:

electronics.ini

```ini
[TRACTION_CONTROL]            ; same as Kunos implementation; required and still functional
SLIP_RATIO_LIMIT=0.08         ; default slip ratio limit
CURVE=traction_control.lut    ; tc_setting | slip ratio limit
PRESENT=1 ; is available
ACTIVE=1 ; is on
RATE_HZ=80
MIN_SPEED_KMH=30

[TRACTION_CONTROL_2]
ACTIVE=1
TC2_SETTING=0                            ; required for TC2 setting adjustment, default setting for TC2

[TC_CONTROLLER_0]
2DLUT=file.2dlut       ; specifies 2D lookup table used by controller
2D_INPUT_X=SPEED       ; x-axis variable used for 2dlut - options: SPEED, GAS, GEAR, LATG, LONG, STEER, ENGINE_ACCEL, YAW_RATE
2D_INPUT_Y=GAS         ; same as above but for y-axis
MODIFY_SLIP_INPUT=1    ; If zero, controller modifies % cut, if 1, controller modifies goal slip value
COMBINATOR_2D=ADD      ; ADD or MULT - designates what the values in the lut do to the value they're modifying

[TC_CONTROLLER_1]
INPUT=LATG             ; variable used for lookup - options: SPEED, GAS, GEAR, LATG, LONG, STEER, ENGINE_ACCEL, YAW_RATE
COMBINATOR=MULT        ; ADD or MULT - designates what the values in the lut do to the value they're modifying
LUT=file2.lut          ; specifies lookup table used by controller
MODIFY_SLIP_INPUT=1

[TC_CONTROLLER_2]      ; note: one dimensional LUT math operations are completed before two dimensional operations
MODIFY_SLIP_INPUT=0
2DLUT=file3.2dlut
2D_INPUT_X=SETTING_2   ; this is the TC2 setting, not necessary to use.
2D_INPUT_Y=LONG
COMBINATOR_2D=MULT
LUT=file4.lut          ; specifies one dimensional lookup table used by controller
INPUT=GEAR
COMBINATOR=ADD
```

setup.ini
```ini
[TRACTION_CONTROL_2]
SHOW_CLICKS=0
TAB=ELECTRONICS
NAME=Traction Control 2
MIN=0 ;minimum # setting
MAX=10 ;maximum # setting
STEP=1
POS_X=0.5
POS_Y=1
HELP=NULL
```
