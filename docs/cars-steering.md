# Steering

## Real-Feel Steering
Enables CSP’s *Real-Feel* force-feedback module.
This normalizes steering torques to your sim wheel's steering torque (which is specified in CSP settings in CM) such that what you feel is 1:1 with what the simulation is producing.

This system also includes a power steering module for cars with power steering (most modern vehicles).

**Enable in `car.ini`:**

```ini
[CONTROLS]
ENABLE_REAL_FEEL=1 ; enables CSP's real steering forces. Required for power steering. Defaults to unassisted torque.
```

---

## Power Steering System
Adds simulation of **electric or hydraulic power steering assist**.
Real steering effort is computed via Real-Feel, then CSP performs a power steering system simulation to produce the net torque that is sent to your wheelbase.

### Maximum Assist Torque

```ini
ASSIST_TORQUE_MAX = 90 ; maximum assist torque of the system in Nm
```

Defines the **ceiling** for how much torque the power-steering system can apply.
Higher values = stronger assist, lighter steering feel.

---

### Steering Assist Maps
Lookup tables defining **how the power steering system responds to driver-applied torque**, outputting an assist factor from **0–1**.

```ini
ASSIST_MAP_0=car_steer_assist_map0.lut ; driver torque (Nm) | assist factor (0–1)
ASSIST_MAP_1=car_steer_assist_map1.lut ; additional assist maps allowed without limit
```

**Notes:**
- Values should map **driver input torque → ratio of ASSIST_TORQUE_MAX applied**.
- Desmos to help visualize how the system works: https://www.desmos.com/calculator/qjxnqdr4zx
- You can define any number of maps (`ASSIST_MAP_2`, `ASSIST_MAP_3`, etc.).

---

### Power Steering Setup Option

Defines an in-game setup slider for selecting the **power steering assist map** (or assist level).
Appears in the setup menu under the defined tab and naming.

**Example — `setup.ini`:**

```ini
[POWER_STEERING_SETTING]
SHOW_CLICKS=0
TAB=GENERAL
NAME=Power Steering
MIN=0    ;always 0, can also use LUT setup options
MAX=1    ;maximum index specified in car.ini
STEP=1
DEFAULT=0 ;default map
POS_X=0.5
POS_Y=6
HELP="Power Steering Assist - Note: Power steering requires real steering forces to be enabled in CSP settings!"
```

---

---

## Rack Travel Lookup Table
Defines the **steering rack displacement** as a function of **steering wheel rotation**.
This allows non-linear steering ratio behavior (common in real cars due to u-joint nonlinearity and variable speed rack systems).

**Example — `car.ini` (`[CONTROLS]` section):**

```ini
[CONTROLS]
RACK_TRAVEL_LUT=car_susp_rack_travel.lut ; steering wheel degrees | rack travel (m). Mirrored; no negative X values needed.
```

**Notes:**
- The LUT expects values only for positive steering angles — CSP mirrors the table automatically.
- Allows accurate simulation of variable-ratio steering racks or u-joint nonlinearities.
- For u-joints, can use this Desmos helper tool: https://www.desmos.com/calculator/hhtnwqoaxv (not for the faint of heart)

---
