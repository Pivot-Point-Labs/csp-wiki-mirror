# Thermal Model V4 (W.I.P, new in 0.3.0)
A completely new, physically-based thermal model featuring rim temp, sidewall temps, and multilayer tread/carcass temps. It also includes physical tire wear. Much more computationally expensive than V1/2 models.

Please find debug/visualization page in Car Debug app.

Strongly recommended to use maxwell hysteretic damping (see code in Tyre Physics) in conjunction with this model.

This model is designed to be fairly plug and play, and as such should function without explicitly including most of its parameters (as they are set to reasonable defaults). If you cannot tell what a parameter means based on its description, it is recommended to not change it.

NOTE: This model is very much still a work in progress and **will** change, please keep that in mind if using it in your projects.

### Example Implementation (`tyres.ini`)

```ini
[_EXTENSION]
PRACTICAL_TEMP_RATIO=1              ; currently deprecated.
USE_TREAD_COVER=1                   ; possible this is deprecated now, but good to include regardless.
LATERAL_RAYS=3                      ; per side, some amount required for thermal distribution calculations
LONGITUDINAL_RAYS=4                 ; per side, some amount required for thermal distribution calculations

[THERMAL_MODEL]
VERSION=4
DEBUG=0                             ; adds thermal powers to CSP Logger. Large number of channels, do not leave enabled.

[ADDITIONAL1]
CAMBER_TEMP_SPREAD_K=1              ; controls lateral spread of tire temperature. Formula is subject to change.

[FRONT]
WIDTH=0.300                         ; tread width of tire, used for volume/mass calculations in thermal model
RADIUS=0.350                        ; unloaded radius of tire, used for volume/mass calculations in thermal model
TREAD_DEPTH=0.01                    ; tread section depth in meters, do not include line for slick tires
TREAD_COVER=0.3                     ; ratio (%/100) of valleys in tread, now used for surface convection calculations, do not include line for slick tires
WEAR_RATE=0.03                      ; physical wear rate (mainly based on work energy), necessary for temperature loss due to material removal
SIDEWALL_K_MULT=1.0                 ; lateral sidewall stiffness as a ratio of vertical stiffness
SIDEWALL_K_MULT_X=2.0               ; longitudinal sidewall stiffness as a ratio of vertical stiffness
ROLLING_RESISTANCE_0=12             ; now more important than ever, rolling resistance directly controls energy generation within the tire
ROLLING_RESISTANCE_1=0.0001         ; speed proportional component influences net RR and thus net energy input
ROLLING_RESISTANCE_SLIP=1000        ; "slip" proportional component influences additional RR (and thus internal heat generation) from cornering

[THERMAL_FRONT]
OPTIMAL_TEMP_OFFSET=0               ; can be used to quickly offset friction luts for different compounds
PERFORMANCE_CURVE=tcurve.lut        ; grip mult vs temperature lookup table
;PERFORMANCE_MAP=tmap.2dlut         ; grip mult vs temperature (degC, x) and sliding velocity (m/s, y) 2d lookup table. If you don't have data, not recommended.

BULK_THICKNESS=0.015                ; thickness of entire bulk section, meters
SIDEWALL_THICKNESS=0.005            ; thickness of entire sidewall section (per side), m

VOLUMETRIC_HEAT_CAPACITY=1700       ; kJ/(m^3K), baseline at 0C
SURFACE_TRANSFER=500                ; Baseline road heat transfer rate, W/(m^2K)
CONDUCTIVITY=0.25                   ; Tread/bulk thermal conductivity W/(mK)
EFFUSIVITY=0.50                     ; Effusivity controls tire:asphalt energy split (effusivity ratio), 1.0 is 100% of energy going to tire
WEAR_K=1.0                          ; Coefficient for energy taken up by physical wear
GRAIN_GAIN=0.0                      ; As vanilla
BLISTER_GAIN=0.0                    ; As vanilla
SURFACE_TO_AMBIENT=10               ; Overall gain for surface convection
SURFACE_TO_AMBIENT_SIDEWALL=5       ; Overall gain for sidewall convection
ENGINE_BAY_MIX=0, 0                 ; L, R. Controls how much of engine bay air mixes with airflow to tire/wheel. Fudge factor, use only as necessary.

RADIATION_CONSTANT=0.95             ; Emissivity (controls radiative cooling)

CARCASS_ROLLING_K=0.6               ; Controls the % of rolling resistance that's turned into heat inside the bulk of the tire
FLEX_SPEED_COEFF=0.5                ; Controls the % of vertical damping that's turned into heat inside the bulk of the tire

INTERNAL_CONVECTION_K=0.5           ; Controls internal convection for rim/core/carcass transfer

RIM_TO_AMBIENT=0.0005               ; to be redone, controls rim to ambient transfer (similar to v1/2 models)
BRAKE_TO_RIM=0.00010                ; to be redone, controls brake to rim transfer (similar to v1/2 models)
```


# Thermal Models V1 & V2
Revamp AC’s tire thermal model by adding carcass temperatures and improved heat-transfer modeling.
*Parameters become more realistic but more difficult to tune.*

### Example Implementation (`tyres.ini`)
*Only extension-relevant parameters shown. All Kunos parameters are still required.*

```ini
[THERMAL_MODEL]
VERSION = 1 ; version of thermal model. Current versions: 1, 2. V2 works with extended rays to dynamically calculate side to side temperature distribution, plus changes some calculations.


[THERMAL_FRONT] ; Kunos parameters (some repurposed)
SURFACE_TRANSFER=0.93          ; cooling rate from track to tire surface
PATCH_TRANSFER=0.002           ; lateral heat distribution on the tread
CORE_TRANSFER=0                ; obsolete
INTERNAL_CORE_TRANSFER=0       ; obsolete
FRICTION_K=0.0127              ; friction-generated heat
ROLLING_K=0                    ; obsolete
PERFORMANCE_CURVE=tcurve_1.lut ; celsius | grip_multiplier
COOL_FACTOR=8                  ; speed²-scaled multiplier for SURFACE_TO_AMBIENT
SURFACE_ROLLING_K=0.001        ; heat from internal tread resistance


[THERMAL2_FRONT] ; new CSP parameters
CARCASS_ROLLING_K=0.15         ; rolling resistance → carcass heat
BRAKE_TO_CORE=0.0006           ; brake heat → internal air
SURFACE_TO_AMBIENT=0.076       ; surface → air
SURFACE_TO_CARCASS=0.023       ; surface → carcass
CARCASS_TO_SURFACE=0.61        ; carcass → surface
CARCASS_TO_CORE=0.025          ; carcass → internal air
CORE_TO_CARCASS=0.0005         ; core → carcass
CORE_TO_AMBIENT=0.002          ; core → ambient (via rim)
```

---
