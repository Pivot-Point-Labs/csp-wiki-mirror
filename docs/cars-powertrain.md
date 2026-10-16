# General Engine

## Effects of altitude are modeled for engine power and aerodynamics (enabled by default for extended physics)

---

## Engine response delay (how long the engine takes to respond to an input)

*engine.ini*

```ini
[ENGINE_DATA]
RESPONSE_TIME=0.03 ; delay of response in seconds
```

---

## More accurate fuel consumption system. Fuel consumption parameter in car.ini now ignored (can be removed).
### Example implementation:

*engine.ini* — Note: only supplementary, Kunos parameters still required.

```ini
[ENGINE_DATA]    ; Kunos section
MECHANICAL_EFFICIENCY=0.85 ; %/100 - should match your "drivetrain losses" multiplier (note: only used for fuel calculations at the moment)
IDLE_THROTTLE=0.04    ; %/100 - how much throttle is used to achieve idle (note: only used for fuel calculations at the moment)
IDLE_CUTOFF=1800    ; rpm at which idle throttle ceases (note: only used for fuel calculations at the moment - suggested to use idle rpm + 100 for most cars - for some race cars, idle throttle never cuts out, so the cutoff should be greater than the rev limit)
```

Pick between one of the following options depending on your preference/the data you have available — option 1 is advised if you have no fuel-flow data (as its parameters are easier to source).
The LUT parameters do not need to be used — if they are commented out, the values default to the constants.
You must include a constant OR a LUT for each parameter.

- **Option 1 (thermal efficiency):**

```ini
[FUEL_CONSUMPTION]    ; new section
THERMAL_EFFICIENCY_LUT=therm_eff.lut    ; torque_ratio|engine thermal efficiency (%/100) — torque ratio = current engine torque / maximum engine torque
THERMAL_EFFICIENCY=0.35 ; %/100 — constant if LUT is not present
FUEL_LHV=43 ; fuel lower heating value — MJ/kg
TURBO_EFFICIENCY=0.8    ; optional — turbo efficiency at converting fuel into power
LOG_FUEL_FLOW=0    ; if 1, logs fuel flow — WARNING: large logs
```

- **Option 2 (fuel flow):**

```ini
[FUEL_CONSUMPTION]
MAX_FUEL_FLOW_LUT=max_flow.lut    ; rpm | maximum fuel flow (kg/hour)
MAX_FUEL_FLOW=100 ; kg/hr — constant if LUT is not present
LOG_FUEL_FLOW=0
```

---

## Engine Maps — multiplier for torque based on RPM per map
Example implementation:

*engine.ini*

```ini
[MAP]
DEFAULT=0    ; default map index
MAP_0=engine_map0.lut    ; rpm|torque_multiplier
MAP_1=engine_map1.lut    ; additional maps allowed
```

*setup.ini*

```ini
[ENGINE_MAPS]
SHOW_CLICKS=0
TAB=GENERIC
NAME=Engine Map
LUT=engine_map_setup.lut    ; format: name|index — can also use direct indexing, ensure indexes match MAP_ entries
POS_X=0.5
POS_Y=3
HELP=NULL
```

---

# Clutch
## Extended clutch damage

With 0.1.76 it’s now possible to get additional clutch damage from high torque. New options are set in `drivetrain.ini`, next to existing damage option:

```ini
[DAMAGE]
TORQUE_THRESHOLD =         ; uses torque produced by the engine
TORQUE_DAMAGE_K =          ; intensity multiplier, similar to existing DAMAGE_K
ENGINE_TORQUE_THRESHOLD =  ; uses total drivetrain torque
ENGINE_TORQUE_DAMAGE_K =
CLUTCH_TORQUE_THRESHOLD =  ; uses clutch torque
CLUTCH_TORQUE_DAMAGE_K =
```

---

# Turbos

## New for 0.2.8 (05/2025)
Extended turbo options.

engine.ini:
```ini
[HEADER]
TURBO_VERSION=1 ;0 is AC, 1 is v1 CSP

[TURBO_0]                   ; This can be used for any of the turbos
FLOW_ON_CUT=0.6             ; How much exhaust energy remains on an ignition cut (vs throttle cut). Linearly interpolated to based on cut amount (100% cut yields this flow rate).
```
An issue with the original KS code was how electronic throttle cuts were handled. AC treated fuel/ignition cuts in the same way as throttle body movement. That meant that on cuts for gears (and for TC), it would act as though the throttle was slammed closed, reducing exhaust flow to ~0, thus letting the the turbo unspool rapidly. In reality, the throttle stays open and there is still significant airflow on ignition cuts (or timing retardation etc, anything that cuts power and isn't the throttle), allowing the turbo to maintain RPM quite well. The net exhaust energy is of course lower, as fuel is not being burned, but the airflow does certainly not go to zero. CPHYS turbo was written to correct this behavior (in a simple, easy to use manner). In short, it stops the boost dropping large amounts on electronic gear shift cuts and TC cuts like in vanilla code, allowing for the use of more realistic lag down and up times.

## New in 2019
Patch adds new options for turbo, only available [with extended physics](cars-enabling-extended-physics.md): LUT for gas pedal and spin delay.

```ini
[TURBO_0]
LAG_DN=0.985
LAG_UP=0.9965
MAX_BOOST=1.0
WASTEGATE=0.58
DISPLAY_MAX_BOOST=0.58
REFERENCE_RPM=2500
GAMMA=4
COCKPIT_ADJUSTABLE=0
EXT_GAS_CURVE=(|0=0|0.3=0|1=1|)
EXT_SPIN_DELAY=0.2
```

Generally, gas pedal is used as a multiplier for turbo activation. With `EXT_GAS_CURVE` (which could also be a file name instead of inline LUT), you can remap that multiplier value, for example, stopping turbo from activating until pedal is pressed to at least 30% of its range. Somewhat similar effect could be achieved with controller with `INPUT=GAS`, but LUT allows to alter value before gamma is applied. Default value (for original physics) is `EXT_GAS_CURVE=(|0=0|1=1|)`.

As for `EXT_SPIN_DELAY`, it adds some sort of negative turbo pressure, extending boost range. Engine would act as naturally aspirated until turbo would spin beyond zero point. With `EXT_SPIN_DELAY=1`, if original turbo boost would equal 0.5, after altering, it’ll drop to 0, and would climb from there. With `EXT_SPIN_DELAY=0.5`, it would be 0.33. Default value (for original physics) is `EXT_SPIN_DELAY=0`.

Thanks to dj_amur for the suggestion of adding it.
