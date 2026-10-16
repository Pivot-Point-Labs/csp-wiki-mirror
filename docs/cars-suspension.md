# Suspension

## Additional Suspension values as part of Extended Physics
Remember to [enable Extended Physics](cars-enabling-extended-physics.md)

### Alternative ways of applying torque to suspension
This is a fix for a Kunos bug that caused inaccuracies with anti-effects geometry.

*suspensions.ini*

```ini
[_EXTENSION]				; Since 0.2.3p211 it is now disabled entirely for axle suspension types
TORQUE_MODE_EX = 0 			; Options:
					; 0 is default/vanilla and has incorrect application of forces to hub. Accelerative torques are passed through the hub when in reality that is not the case.
					; 1 is broken
					; 2 recommended and should be physically accurate. There have been updates that have changed its behavior over CSP versions, but only in attempts to reduce bugs and improve edge-case behavior.
```

---

### Fix for progressive spring rates
Fix for another Kunos bug

*suspensions.ini*

```ini
[_EXTENSION]
FIX_PROGRESSIVE_RATE = 1
```

---

### New double-wishbone suspension extension
Including input for motion ratio lookup tables, bumpstop lookup tables, progressive rate fix, with more to come
Example implementation:

*suspensions.ini*

```ini
[_EXTENSION]
USE_DWB2 = 1

[FRONT]
MOTION_RATIO = motion_ratio_f.lut	; Motion ratio lookup table (deflection from zero-point|motion ratio)
BUMP_STOP_LUT = bsf.lut    		; Deflection|Force - must start with 0|0
					; Legacy implementation. See further down the page for the current implementation.
[HEAVE_FRONT]
MOTION_RATIO = motion_ratio_hf.lut
BUMP_STOP_LUT = bshf.lut

[REAR]
MOTION_RATIO = motion_ratio_r.lut
BUMP_STOP_LUT = bsr.lut

[HEAVE_REAR]
MOTION_RATIO = motion_ratio_hr.lut
BUMP_STOP_LUT = bshr.lut
```

---

### New labelled spring adjustments for cars using DWB2
Example implementation:
note: *suspensions.ini* format does not change.
*setup.ini*

```ini
[SPRING_LF] 				; LF, RF, RR, LR - replaces old SPRING_RATE_LF entry
SHOW_CLICKS = 0
TAB = SUSPENSIONS
NAME = Spring Rate LF
LUT = suspension_springs.lut 		; Format: name|rate
POS_X = 0
POS_Y = 1
HELP = HELP_LF_WHEELRATE 		; Same as vanilla AC options, for now..
DISPLAY_VALUE_IN_BRACKETS = 1 		; 1 - displays value in brackets next to name in setup window.
```

---

### Added anti-roll bar motion ratios

---

### New labeled anti-roll bar adjustments for extended cars
Example implementation:

*suspensions.ini*

```ini
[ARB]
EXTEND = 1 				; Required to enable extended ARBs
FRONT_MOTION_RATIO = 1.0
FRONT = 100000 				; Front anti-roll bar stiffness in N/m
REAR_MOTION_RATIO = 1.0
REAR = 10000 				; Rear anti-roll bar stiffness in N/m
```

**note:** setup.ini entries not required for motion ratios to function, but the EXTEND line under [ARB] is.

*setup.ini*

```ini
[ARB_F] 				; F, R - replaces old vanilla AC entry
SHOW_CLICKS = 0
TAB = SUSPENSIONS
NAME = ARB Front
LUT = suspension_arb_front.lut 		; Format: name|rate
POS_X = 0.5
POS_Y = 0
HELP = HELP_FRONT_ARB 			; Same as vanilla AC options, for now...
DISPLAY_VALUE_IN_BRACKETS = 0 		; 1 - displays value in brackets next to name in setup window.
```

---

### Steering ratio setup adjustments (note breaks AI and animations, so not recommended)
#### Broken/unsupported as of May 2022
Example implementation:
*setup.ini*

```ini
[STEERING_RATIO]
SHOW_CLICKS = 0
TAB = SUSPENSIONS 			; Desired tab
NAME = Steering Ratio
LUT = suspension_steer.lut 		; Format: display_name|ratio
POS_X = 0.5
POS_Y = 4
HELP = NULL 				; No suitable option at the moment
DISPLAY_VALUE_IN_BRACKETS = 1 		; 1 - displays value in brackets next to name in setup window.
```

---

### Adjustable double wishbone suspension geometry (requires DWB2)
Example implementation:

*setup.ini*

```ini
[FRONT_GEOMETRY]
SHOW_CLICKS = 0
TAB = SUSPENSIONS
NAME = Front Geometry
LUT = setup_front_geometry.lut		; name|index
GEO_0 = suspensions_front_1.ini		; INI file with the changed items (options: hub_mass and all pickup points)
GEO_1 = suspensions_front_2.ini		; same format as suspensions.ini - only modified items are required
					; (if values are not present, it will load from the suspensions.ini)
DEFAULT = 0				; Default GEO_ index to load
POS_X = 0.5
POS_Y = 3
HELP = NULL 				; No suitable option at the moment

[REAR_GEOMETRY]
SHOW_CLICKS = 0
TAB = SUSPENSIONS
NAME = Rear Geometry
LUT = suspensions_setup_rear_geometry.lut
GEO_0 = suspensions_rear_1.ini
GEO_1 = suspensions_rear_2.ini
DEFAULT = 0;
POS_X = 0.5
POS_Y = 4
HELP = NULL
```

---

### Damper Lookup tables for cars using DWB2 suspension (Note motion ratio will be applied to dampers)
Example implementation:

*suspensions.ini*

```ini
[_EXTENSION]
DAMPER_LUTS = 1    			; Currently required
```

Create a new file:
*dampers.ini*

```ini
[HEADER]
ENABLE = 1 				; 0 to disable

[FRONT]
BUMP_SLOW_0 = damp_bump_slowf_0.lut	; Format: speed (m/s) | force (Newtons - sign does not matter).
BUMP_SLOW_4 = damp_bump_slowf_4.lut	; Note: SLOW entries do not extrapolate, only FAST do. If using SLOW only, ensure the velocities are high enough for intended use. At least up to 5 m/s is suggested as a baseline.
BUMP_SLOW_9 = damp_bump_slowf_9.lut	; You must at least have a LUT for your first and final adjustment
REBOUND_SLOW_0 = damp_reb_slowf_0.lut	; (if not adjustable, you only need the _0 entry).
REBOUND_SLOW_4 = damp_reb_slowf_4.lut	; Linear interpolation between surrounding entries will be done for entries that are not present
REBOUND_SLOW_9 = damp_reb_slowf_9.lut	; (1-3 and 5-8 in this example).
BUMP_FAST_0 = damp_bump_fastf_0.lut
REBOUND_FAST_0 = damp_reb_fastf_0.lut
```

*setup.ini*

```ini
[DAMPER_BUMP_LF]    			; The names are the same as Kunos entries, except DAMP has been replaced by DAMPER
SHOW_CLICKS = 2
TAB = DAMPERS
NAME = Bump
MIN = 0					; Minimum setting
MAX = 11				; Maximum setting
STEP = 1
DEFAULT = 7				; Default setting
POS_X = 0
POS_Y = 0
HELP = HELP_LF_DAMPER_BUMP
```

---

### Bump stop/rubber lookup tables for cars using DWB2 suspension (Available since v1.74)

For heave elements, extra functionality is added. You can use the old packer rate as a 3rd spring and the new bumpstop rate as a bump rubber, both with associated gaps. The gaps for each are at the ground (i.e. when the car is at static deflection). Packer range is used as the bumpstop gap for the corner springs, and it works the same as in vanilla AC.

Further note: Old implementation of bumpstop lookup tables still works.

Example implementation:

*suspensions.ini*
```ini
[_EXTENSION]
SEPARATE_BSH_GAPS = 1 			; If 0 or line not present, bumpstop_gap = packer_range

[HEAVE_FRONT]
BUMPSTOP_GAP = 0.1 			; Gap in meters to bumpstop under static loading

[HEAVE_REAR]
BUMPSTOP_GAP = 0.1 			; Gap in meters to bumpstop under static loading
```

Create a new file:
*bumpstops.ini*
```ini
[HEADER]
ENABLE = 1

[FRONT]
DEFAULT = 0 				; Default index/choice of bump rubber
STACK = 1 				; Number of rubbers stacked
[REAR]
DEFAULT = 0
STACK = 2

[FRONT_HEAVE]
DEFAULT = 0
STACK = 2
[REAR_HEAVE]
DEFAULT = 1
STACK = 3

[FRONT_0] 				; Can have as many as needed
LUT = filename.lut 			; Deflection in meters|force in newtons. Must begin with 0|0
[FRONT_1]				; (a "spring" should not produce force at 0 deflection in any case)
LUT = filename.lut

[REAR_0]
LUT = filename.lut
[REAR_1]
LUT = filename.lut

[FRONT_HEAVE_0]
LUT = filename.lut
[FRONT_HEAVE_1]
LUT = filename.lut

[REAR_HEAVE_0]
LUT = filename.lut
[REAR_HEAVE_1]
LUT = filename.lut
```

*setup.ini*

```ini
[BUMPSTOP_HF] 				; HF, HR
SHOW_CLICKS = 0
TAB = SUSPENSION HEAVE
NAME = Bump Rubber F
LUT = bs_setup.lut 			; can use this to assign names to each rubber. Format: Name|index
POS_X = 1
POS_Y = 0
HELP = HELP_HR_WHEELRATE

[BUMPSTOP_GAP_HF] 			; HF, HR
SHOW_CLICKS = 0
TAB = SUSPENSION HEAVE
NAME = Bump Rubber Gap
MIN = 0
MAX = 100
STEP = 1
POS_X = 1
POS_Y = 1
HELP = HELP_HF_TRAVEL_RANGE

[BUMPSTOP_NUM_HF] 			; HF, HR
SHOW_CLICKS = 0
TAB = SUSPENSION HEAVE
NAME = Bump Rubber Stack
MIN = 1
MAX = 3
STEP = 1
POS_X = 0.5
POS_Y = 2
HELP = Null

[BUMPSTOP_LF]				; LF, RF, LR, RR
SHOW_CLICKS = 0
TAB = SUSPENSION ADV.
NAME = Bump Rubber LF
LUT = bs_setup.lut
POS_X = 0
POS_Y = 0
HELP = HELP_LF_BUMP_STOP_RATE

[BUMPSTOP_NUM_LF]			; LF, RF, LR, RR
SHOW_CLICKS = 0
TAB = SUSPENSION ADV.
NAME = Rubber Stack LF
MIN = 1
MAX = 3
STEP = 1
POS_X = 0
POS_Y = 1
HELP = Null

[PACKER_RANGE_LF] 			; LF, RF, LR, RR - same as in vanilla
SHOW_CLICKS = 0
TAB = SUSPENSION ADV.
NAME = Bump Rubber Gap LF
MIN = 0
MAX = 50
STEP = 1
POS_X = 0
POS_Y = 2
HELP = HELP_LF_TRAVEL_RANGE
```
