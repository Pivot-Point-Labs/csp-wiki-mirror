# Tyre Physics

## Extended Raytracing for Tire Collision Detection and Contact Patch Movement

**Enable in `tyres.ini`:**

```ini
[_EXTENSION]
LATERAL_RAYS=0            ;per side, 0 means 1 in middle
LONGITUDINAL_RAYS=4       ;per side, 0 means 1 in middle
MAX_RAY_ANGLE=60          ;degrees swept per side
DISABLE_RAY_DOUBLING=0    ;set to 1 to disable low speed ray doubling (good for performance)
```

---

## Maxwell Hysteresis Damping (new in 0.3.0)
```ini
[FRONT]
SIDEWALL_LOSS_FACTOR_Z=0.1  ; is additive to Kunos viscous damping, recommend using 0 for KS damping to start.
```

---

## Load Sensitivity Smoothing
```ini
[_EXTENSION]
SMOOTH_LOAD_SENS = 1    ;setting to 0 gets rid of cubic interpolation on load sensitivity luts, which can help avoid issues with certain lut shapes.
```

---

## Deterministic Sidewall Deflection
Adds vertical (pre 0.3.0) deflection from lateral and longitudinal contact patch deflections (post 0.3.0). Note that solution is deterministic (deflection directly derived from forces), as proper simulation cannot be done at AC's 333Hz.

### Example (`tyres.ini`)

```ini
[FRONT]
SIDEWALL_K_MULT=1.0   ; multiplier of vertical rate for lateral stiffness
SIDEWALL_K_MULT_X=2.0 ; multiplier of vertical rate for longitudinal stiffness
```

---


## Temperature-Dependent Slip Dropoff Curves
Lookup tables for falloff vs. temperature.
⚠ **Note:** Does *not* display correctly in the Tire Tester App.

### Example (`tyres.ini`)

```ini
[FRONT] ; or any compound
FALLOFF_LEVEL=0.7
FALLOFF_LEVEL_CURVE=tyres_fall_level.lut ; temp | falloff_level
FALLOFF_SPEED=1.5
FALLOFF_SPEED_CURVE=tyres_fall_speed.lut ; temp | falloff_speed
```

---

## Practical Temperature Ratio
Controls weighting between surface and carcass/core temperature when calculating grip.

### Example (`tyres.ini`)

```ini
[_EXTENSION]
PRACTICAL_TEMP_RATIO = 0.25 ; 0 = core/carcass only, 1 = surface only (AC default = 0.25)
```

---

## Spring Rate Change With Camber
Applies a multiplier based on a lookup table.

### Example (`tyres.ini`)

```ini
[FRONT]
CAMBER_SPRING_MULT = camber_sr.lut ; degrees | spring_rate_multiplier
```

---

## Rolling Radius Change With Load
Kunos treats rolling radius as constant; this corrects that behavior.

### Example (`tyres.ini`)

```ini
[FRONT]
ROLLING_RADIUS_MULT=0.1 ; proportion of deflection applied to rolling radius (0–1)
```

---

## Quadratic Radial Growth With Wheel Speed
Adds a quadratic term for tire growth at high angular velocity.

### Example (`tyres.ini`)

```ini
[FRONT]
RADIUS_ANGULAR_K_2=0.05
; radius_add = (K2/1e6)*ω² + (RADIUS_ANGULAR_K/1000)*ω
```

---

## Longitudinal Grip Adjustment With Camber
Quadratic camber → DX scaling.

### Example (`tyres.ini`)

```ini
[FRONT]
DX_CAMBER_REF=3   ; reference camber angle (deg) — must not be 0
DX_CAMBER_MULT=0.98 ; multiplier at reference angle
```

---

## Additional Slip Parameters
Used for shaping slip-dropoff behavior.

### Example (`tyres.ini`)

```ini
[FRONT]
DROPOFF_FACTOR_0=60 ; visualize at https://www.desmos.com/calculator/dtlzovroom
DROPOFF_FACTOR_1=1
```

---
