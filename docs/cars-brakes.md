# New for 0.2.8 (05/2025)


## CSP Anti-Lock Braking System

As of 0.2.8, there is now the ability to add controllers for ABS, similar to CSP traction control. These controllers are, by necessity, quite complex, so please read the below documentation carefully to understand the functionality.

To start, each controller can use the following inputs:
* GAS (0 to 1 pedal input)
* THROTTLE (0 to 1 engine output)
* BRAKE (0 to 1 pedal input)
* BRAKE_PRESSURE (input psi per wheel)
* LATG (G)
* LONG (G)
* SPEEDKMH (car speed in kmh)
* GEAR
* STEER (deg at handwheel)
* WHEEL_ACCEL (angular in rad/s/s)
* ABS_SETTING
* SLIP_RATIO (actual slip ratio., not recommended as not possible to know in real life)
* ABS_SLIP_RATIO (slip ratio calculated by ABS system, not necessarily same as true SR)
* ABS_TARGET_SLIP (net target SR of ABS system)
* ABS_SLIP_DIFF_TARGET (SR minus target SR)
* ABS_SLIP_DIFF_LAT (SR minus other side's SR, 2 wheels)
* ABS_SLIP_DIFF_LONG (SR minus other axle side's SR, 2 wheels)
* ABS_SLIP_DIFF_SIDE (SR minus other side's SR, 4 wheels)
* ABS_SLIP_DIFF_AXLE (SR minus other axle side's SR, 4 wheels)
* ABS_SLIP_DIFF_RATIO (SR divided by target SR)
* YAW_RATE (deg/s)
* YAW_RATE_ACCEL (deg/s/s)
* RPM (engine rpm)


The basic system is a variable-gain PID controller with an additional constant controller (separate controller that is not dependent on the control parameter of the PID controller). It is recommended to research PID tuning before experimenting with the system.

All programming is done in the electronics ini. **The controller format is the same as for traction control, so please see the docs for that (currently on Trello) for 2dlut etc use.** Every parameter shown in the controllers below can be used for any of the other controllers (target, gain, p gain, i gain, d gain), they all run the same code internally.

electronics.ini
```ini
[ABS]
SLIP_RATIO_LIMIT=0.08
CURVE=abs_settings.lut
PRESENT=1
ACTIVE=1
RATE_HZ=333  ; this is deprecated for now, but for the moment, you should use 333 for backwards compatibility once we update it to be functional again.

[ABS_EXT]
ENABLE=1
DEBUG=1                        ; NOTE: DO NOT ENABLE FOR RELEASES. Logs many channels at max log rate in CSP Logger for debugging purposes. Useful to see what your controllers are doing.
USE_WHEEL_SPEED_SLIP=0         ; not implemented yet. 1 to use ECU wheel speeds for slip ratio calculation, default 0 (true SR)
RESPONSE_TIME=0.01             ; seconds, 95% response time of first order fxn. Very important parameter for control of system overall. Do not cheat this by making it too low unless you want unrealistic ABS.
INTEGRAL_ERROR_LIM=-0.01,10000 ; this clamps the integral controller's integral calculation. Without it, you can run into undershoot situations. You can monitor the integral calculation in the debug channels in CSP Logger.


[ABS_TARGET_CONTROLLER_0] ;these controllers modify the slip target of the ABS system. The number set by [ABS] CURVE/SLIP_RATIO_LIMIT is the baseline, these modulate on top of that. This specific controller is reducing the allowed longitudinal slip as lateral load is added (as the tire can't do two things at once).
LUT=(-1.2=0.5|-0.6=0.8|0=1|0.6=0.8|1.2=0.5)
INPUT=LATG
COMBINATOR=MULT

[ABS_TARGET_CONTROLLER_1] ;this is a bit of an experimental controller that is trying to do some anti-yaw correction under braking (adding stability). This is not really a good way to do it, but it shows the FLIP_RHS feature.
LUT=(-20=1|0=1|20=0.7)
INPUT=YAW_RATE
COMBINATOR=MULT
FLIP_RHS=1                ;this will flip the value of the input for the opposite side of the car, meaning you can run opposite effects (e.g. braking one side harder and releasing the other).

[ABS_TARGET_CONTROLLER_2] ; this controller is reducing the slip target a bit for the rear wheels under hard braking, this adds a bit of stability
LUT=(-1.2=0.9|0=1)
INPUT=LONG
COMBINATOR=MULT
FILTER_TIME_CONSTANT=0.1  ; this filter is applied to the output of the controller. It's a first order transfer function, value is time constant in seconds. Shown here, it is filtering away some of the noise you'd get from using a G force signal directly.
ENABLED_WHEELS=0,0,1,1    ; this parameter tells the ABS system which wheels the controller is active on (FL, FR, RL, RR). Here it is only enabled for the rear wheels.


[ABS_GAIN_CONTROLLER_0] ; "Constant" gain controllers are similar to the TC controllers, they take in inputs and spit out an intervention amount (0 is no ABS intervention, 1 is full release of brakes). They are likely the most intuitive of the gain controllers to use, but also one of the least stable. They are separate from the PID controllers as they do not necessarily take in ABS_SLIP_DIFF as the main control parameter (this one does, however). This can enable some specific effects that may be desired beyond those relating to slip error. This specific controller is using the slip difference to target to decide how much to cut the brakes. At 15% SR over the target, it will try to release the brake fully. It was used in lieu of a proportional controller as the net effects are quite similar with this setup but more intuitive.
LUT=(0=0|0.03=0.5|0.06=0.7|0.15=1)
INPUT=ABS_SLIP_DIFF
COMBINATOR=ADD          ;for every gain controller, the first will need to add, as they all default to 0

[ABS_GAIN_CONTROLLER_1] ; this controller is just disabling ABS when brake input is lower than 1% or so.
LUT=(0=0.0|0.01=0|0.015=1)
INPUT=BRAKE
COMBINATOR=MULT

[ABS_GAIN_CONTROLLER_2] ; this controller adds some system stability as car speed decreases, lowering the constant controller gain and relying more on the proportional, integral, and derivative controllers instead.
LUT=(0=0.0|50=0.2|100=1)
INPUT=SPEEDKMH
COMBINATOR=MULT


[ABS_PROPORTIONAL_GAIN_CONTROLLER_0] ; this kind of controller is not used in this system but is essentially quite similar to the result of the constant controllers above. It is a proportional controller with ABS_SLIP_DIFF as its input (meaning output is gain*ABS_SLIP_DIFF)
LUT=(0=0|1=0)
INPUT=NONE
COMBINATOR=ADD


[ABS_INTEGRAL_GAIN_CONTROLLER_0] ; these are the integral gain controllers. The implementation shown here is extremely simple. Net output for integral controllers is gain*clampedIntegral(ABS_SLIP_DIFF). Integral controllers can get rid of the steady state error caused by the other controller types. Generally, the higher the gain, the more overshoot.
LUT=(0=150|1=150)
INPUT=NONE
COMBINATOR=ADD

[ABS_INTEGRAL_GAIN_CONTROLLER_1] ; disabling controller gain at & below 1% brake input.
LUT=(0=0.0|0.01=0|0.015=1)
INPUT=BRAKE
COMBINATOR=MULT


[ABS_DERIVATIVE_GAIN_CONTROLLER_0] ; these are the derivative gain controllers. The implementation shown here is extremely simple. Net output for integral controllers is gain*derivative(ABS_SLIP_DIFF). Derivative controllers can dampen the response of the system, reducing oscillation. Too high of a gain can cause vibrations and instabilities.
LUT=(0=0.05|1=0.05)
INPUT=NONE
COMBINATOR=ADD
FILTER_TIME_CONSTANT=0.03 ; a filter is added here to model the filtering that would need to be done to a derivative signal in real life, as such signals are subject to noise.

[ABS_DERIVATIVE_GAIN_CONTROLLER_1] ; disabling controller gain at & below 1% brake input.
LUT=(0=0.0|0.01=0|0.015=1)
INPUT=BRAKE
COMBINATOR=MULT
```


## New "Real Feel" options via master cylinder implementation

For cars with dual master cylinders + balance bars in real life, there is now the option to use the below parameters instead of MAX_PRESSURE_SUM and PEDAL_FORCE_REF, which do the required force math for you, provided you have the requisite measurements.

brakes.ini
```ini
[DATA2]
PEDAL_FORCE_REF = 100       ; kgf. Fallback value for MC calculations if realfeel not enabled or clamp forces disabled and sim pedal max force is lower than this
MASTER_CYL_F_DEFAULT=1      ; default index of front MC
MASTER_CYL_R_DEFAULT=3      ; default index of rear MC
PEDAL_RATIO=4.04

[FRONT]
DISC_EFFECTIVE_RADIUS=0.1634 ; effective brake disc radius in meters, same as before
PISTON_DIAMETER_0=0.0270     ; piston diameter in meters, same as before
PISTON_DIAMETER_1=0.0270
PISTON_DIAMETER_2=0.03175
PISTON_DIAMETER_3=0.03175
PISTON_DIAMETER_4=0.0381
PISTON_DIAMETER_5=0.0381
MASTER_CYL_DIA_0=0.0168      ; master cylinder diameter in meters. No limit to number of options you can add.
MASTER_CYL_DIA_1=0.0178
MASTER_CYL_DIA_2=0.0191
MASTER_CYL_DIA_3=0.0206
MASTER_CYL_DIA_4=0.0222

[REAR]
DISC_EFFECTIVE_RADIUS=0.1509
PISTON_DIAMETER_0=0.0270
PISTON_DIAMETER_1=0.0270
PISTON_DIAMETER_2=0.03175
PISTON_DIAMETER_3=0.03175
PISTON_DIAMETER_4=0.0381
PISTON_DIAMETER_5=0.0381
MASTER_CYL_DIA_0=0.0168
MASTER_CYL_DIA_1=0.0178
MASTER_CYL_DIA_2=0.0191
MASTER_CYL_DIA_3=0.0206
MASTER_CYL_DIA_4=0.0222
```

setup.ini
```ini
[BRAKE_MC_F]
SHOW_CLICKS=0
TAB=GENERAL
NAME=MC Dia. F
LUT=setup_brake_mc_f.lut  ; label | index (not size!)
POS_X=0
POS_Y=4
HELP="Higher master cylinder sizes mean more pedal effort for the same line pressure."

[BRAKE_MC_R]
SHOW_CLICKS=0
TAB=GENERAL
NAME=MC Dia. R
LUT=setup_brake_mc_r.lut  ; label | index (not size!)
POS_X=1
POS_Y=4
HELP="Higher master cylinder sizes mean more pedal effort for the same line pressure."
```


# New in 2023


## "Real Feel" brake calibration

Via the FFB Tweaks settings page for CSP, users can set their pedal forces to match that of the real car via the below parameter. Note: only functional for advanced brakes.
```ini
[DATA2]
PEDAL_FORCE_REF = 100        ; kgf @ pedal face @ MAX_PRESSURE_SUM
```


# New in 2019


## New optional brake system (reworked heating with core temperatures, brake duct setup adjustments, support for brakes calipers with up to 12 pistons)

### Example advanced implementation:

brakes.ini

Note: only supplementary - Kunos parameters also required

```ini
[_EXTENSION]
ENABLE=1
USE_ADVANCED_SYSTEM=1

[DATA]
MAX_TORQUE=3000              ;Try to use similar values to calculated brake torque as it will still be used by the AI

[DATA2]
MAX_PRESSURE_SUM = 1400      ; sum of maximum expected front and rear brake pressures (pressure at front + pressure at rear) - PSI

[FRONT]
DISC_EFFECTIVE_RADIUS=0.16   ; effective brake disc radius in meters (if you don't have data, it's usually close to: (disc outer radius + disc inner radius)/2
PISTON_DIAMETER_0=0.03 ; piston #1 diameter in meters
PISTON_DIAMETER_1=0.03 ; piston #2 diameter in meters
PISTON_DIAMETER_2=0.03 ; piston #3 diameter in meters
PISTON_DIAMETER_3=0.03 ; piston #4 diameter in meters
PISTON_DIAMETER_4=0.03 ; piston #5 diameter in meters
PISTON_DIAMETER_5=0.03 ; piston #6 diameter in meters

[REAR]
DISC_EFFECTIVE_RADIUS=0.15
PISTON_DIAMETER_0=0.03
PISTON_DIAMETER_1=0.03
PISTON_DIAMETER_2=0.03
PISTON_DIAMETER_3=0.03
PISTON_DIAMETER_4=0.03
PISTON_DIAMETER_5=0.03

[TEMPS_FRONT]
COOL_TRANSFER=0.002    ;how fast heat transfers from the surface to the air (independent of speed)
TORQUE_K=0.60
PERF_CURVE=brake_temp_mu.lut    ;now functions as a celsius|friction coefficient lookup table
COOL_SPEED_FACTOR=0.03    ;speed-based air cooling contributed by ducting
COOL_SPEED_FACTOR_0=0.03    ;speed-based air cooling constant (independent of ducting)
CORE_TRANSFER_IN=0.08    ;how fast heat from the surface transfers to the core
CORE_TRANSFER_OUT=0.55    ;how fast heat from the core transfers to the surface
CORE_TRANSFER_AIR=0.0005    ;how fast heat from the core transfers to the air

[TEMPS_REAR]
COOL_TRANSFER=0.002
TORQUE_K=0.60
PERF_CURVE=brake_temp_mu.lut
COOL_SPEED_FACTOR=0.03
COOL_SPEED_FACTOR_0=0.03
CORE_TRANSFER_IN=0.08
CORE_TRANSFER_OUT=0.55
CORE_TRANSFER_AIR=0.0005
```

### Example simple implementation:

brakes.ini

Note: only supplementary - Kunos parameters also required

```ini
[_EXTENSION]
ENABLE=1
USE_ADVANCED_SYSTEM=0

[DATA]
MAX_TORQUE=3000    ; Desired maximum torque possible per side of the car (total system torque = MAX_TORQUE*2)

[TEMPS_FRONT]
COOL_TRANSFER=0.002    ;how fast heat transfers from the surface to the air (independent of speed)
TORQUE_K=0.60
PERF_CURVE=brake_temp.lut    ;now functions as a celsius|friction coefficient lookup table - for the simple system, it gets normalized (so that MAX_TORQUE is always the absolute max torque the brake system can produce), so it's fine to treat it as a multiplier for MAX_TORQUE in that sense.
COOL_SPEED_FACTOR=0.03    ;speed-based air cooling contributed by ducting
COOL_SPEED_FACTOR_0=0.03    ;speed-based air cooling constant (independent of ducting)
CORE_TRANSFER_IN=0.08    ;how fast heat from the surface transfers to the core
CORE_TRANSFER_OUT=0.55    ;how fast heat from the core transfers to the surface
CORE_TRANSFER_AIR=0.0005    ;how fast heat from the core transfers to the air

[TEMPS_REAR]
COOL_TRANSFER=0.002
TORQUE_K=0.60
PERF_CURVE=brake_temp.lut
COOL_SPEED_FACTOR=0.03
COOL_SPEED_FACTOR_0=0.03
CORE_TRANSFER_IN=0.08
CORE_TRANSFER_OUT=0.55
CORE_TRANSFER_AIR=0.0005
```

Effective radius visualization:
[picture to be added]

## Brake blanking adjustments

setup.ini

Note: only supplementary - Kunos parameters also required

```ini
[BRAKE_DUCT_F]
SHOW_CLICKS=0
TAB=BRAKES ;assigned setup tab
NAME=Front Brake Blanking
MIN=0      ;minimum % of brake blanking, higher means more blanking (less airflow)
MAX=100    ;maximum % of brake blanking
STEP=10
POS_X=0.5
POS_Y=2
HELP=NULL

[BRAKE_DUCT_R]
SHOW_CLICKS=0
TAB=BRAKES ;assigned setup tab
NAME=Rear Brake Blanking
MIN=0      ;minimum % of brake blanking
MAX=100    ;maximum % of brake blanking
STEP=10
POS_X=0.5
POS_Y=2
HELP=NULL
```
