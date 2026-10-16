# New "COSMIC" (Comprehensive Suspension with Modular Input of Configurations) suspension type allows for custom definition of suspension not otherwise available in AC [CSP v0.1.79+]

Fully supported in CSP v0.20+

COSMIC allows explicit creation of joints and bodies to produce desired suspension types, versus the preset types in vanilla AC (DWB, STRUT, AXLE, ML), while also avoiding the type-specific bugs in AC's presets (STRUT has many issues, ML hardly works, etc).

Note: only recommended for adept physics developers - cosmic removes many development boundaries, but this means it is quite easy to overstep them (and e.g. cause the game to crash). Additionally, Assetto Corsa's (relatively low) default physics rate means that certain suspension types will not function well. The more complicated and stiff the linkage, the more difficulty the Open Dynamics Engine physics solver will have. Visit the CSP Discord for development support or to make documentation suggestions.

Damage works the same as in vanilla AC (for now), and ARBs can use vanilla or cphys code (see general Suspension docs).

***Scroll to the bottom for helpful general tips.***

> **Known Bugs:**
>
>**0.1.79**
> * Slider joint is broken. Fixed for 0.2.
> * "Simple" damper values do not work on coilovers. Fixed for 0.2.
> * Coilovers require DAMPER_LUTS and dampers.ini. Fixed for 0.2 via allowing above option.
> * FLIP_PRELOAD accidentally defaults to 1. Set FLIP_PRELOAD=0 for normal behavior. Will default to 0 for 0.2.
> * Damper luts potentially broken. Good on 0.2.
> * "Strut" steer axis issue. Fixed for 0.2
> * Rim offset not working. Working in 0.2, see docs for functionality (different to KS).
> * Whole world of a mess with damper/spring setup options. All sorted on 0.2.
>
>**0.2.0**
> * Preload broken on coilovers using spring luts. Fixed for 0.2.1
> * ENGINE_TORQUE_BODY not working 100% correctly when using TORQUE_MODE_EX=2 (one function still applying torque to the wrong body). Fixed with 0.2.1
>
>**Current**
> * Preload broken on torsion bars, use PRELOAD_TORQUE instead. Will be fixed for 0.2.5

## Make sure to read through the entirety of each of the following examples, as they have critical information spread throughout.

---

*suspensions.ini*

Example implementation (note: may not load in-game if copy and pasted directly, as the geometry coordinates were blindly altered, it is simply to show the parameters):
```ini
[_EXTENSION]
TORQUE_MODE_EX=2                ;highly recommended
DAMPER_LUTS=1                   ;required for coilovers as of v0.1.79, not required as for v0.2+

;[ODE]                          ;optional - tuning these parameters can help with stability. See Open Dynamics Engine Manual (http://ode.org/wiki/index.php/Manual#Joint_error_and_the_Error_Reduction_Parameter_.28ERP.29) for more information.
;ERP=0.9                        ;this is the AC default for certain joint types, others (and global value) are 0.3
;CFM=1                          ;*10^-7 - just did this to keep numbers more reasonable

[REAR] ;or front
TYPE=COSMIC
RIM_OFFSET=0.00                 ;same as KS
BASEY=0.0	                ;Distance of CG from the center of the wheel in meters. Rear Wheel Radius+BASEY=Rear CoG Actual CG height =(FWR+FBasey)+(RWR+Rbasey))/CG_LOCATION%      ;same as KS
TRACK=1.5                       ;track width @ rim offset corresponding to coordinates (if coords are measured from wheel center, this number is the track at wheel center. If using rim offset at all, it's recommended to measure coords/track from hub face and input real rim offset).
HUB_MASS=50                     ;same as KS *but see notes about bodies below
TOE_OUT=0.0004, 0.0004          ;same as KS, but as of 0.3.0, most values can have different defaults for left and right. Use comma separated values to indicate L, R
STATIC_CAMBER=-2, -1.5          ;same as above

BODY_0_NAME=ROCKER              ;rigid bodies can be defined starting from #0. Pre-existing bodies include HUB_L, HUB_R, and CHASSIS.
BODY_0_MASS=0.2                 ;mass of body in kg
BODY_0_INERTIA=0.1, 0.05, 0.1   ;inertia box of body - not particularly necessary for most applications, default 0,0,0
BODY_0_POS=0.6, 0.1, 0.1        ;typically best to put this at the body's center of mass. Coordinates are relative to the wheel.
BODY_0_MIRROR=1                 ;0 to disable mirroring to the other side of the car laterally, default 0

BODY_1_NAME=T_BAR
BODY_1_MASS=0.1                 ;mass doesn't necessarily have to match real component, sometimes it's better to have lighter/heavier parts for solver stability. If the part is unsprung, it is good practice to remove it from HUB_MASS in the proportion that makes sense (e.g. a wishbone would have approximately 50% of its mass removed from HUB_MASS. This is done to ensure that the unsprung mass of the car stays accurate to the desired value)
BODY_1_INERTIA=0.0, 0.0, 0.0
BODY_1_POS=0.8, 0.2, 0.4

;BODY_2_NAME=CHASSIS2
;BODY_2_MASS=500                ;all masses automatically adjust CHASSIS mass to ensure car.ini mass is obeyed
;BODY_2_INERTIA=1,1,1
;BODY_2_CARPOS=0,0.0,0          ;carpos is in the car reference frame, in this case, the body is being placed at the car's origin (sprung CoG)
;ENGINE_TORQUE_BODY=CHASSIS2    ; this line tells the solver which body that reaction torque from the engine/wheels should get applied to. Useful and necessary for live axle designs, etc.

HJ0=ROCKER_HINGE                ;hinge joints can be used for many different things, in this case, as a rocker arm hinge
HJ0_BODY_B=ROCKER               ;if BODY_A is not listed, it is assumed to be CHASSIS, and if BODY_B is not listed, it is assumed to be HUB_L. This is true for all joint types. HUB_R also available, L is default.
HJ0_POS_A=0.6, 0, 1              ;POS0 and POS1 were standard in v0.1.79. POS_A and POS_B will alternatively work in CSP v0.2 and later and will be standard. POS0 and POS1 still usable for backwards compatibility. Position relative to wheel (same as KS)
HJ0_POS_B=0.6, 0.1, 1
HJ0_PARITY=-1                       ;-1 means mirrored left and right, 0 means left only, 1 means right only, default -1

;important note about body assignment:
;if you list the same name for Body A and Body B, the code will assume you are connecting the left and right side's mirrored bodies (if available). If, for example, you have a heave spring that connects to the rocker arm on each side, you simply put _BODY_A=ROCKER and _BODY_B=ROCKER, and it will make the connection without further intervention. This applies to joints/springs/dampers/coilovers/etc.

;HJ1=CHASSIS_HINGE              ;you can use hinges to create a rudimentary version of chassis flex by connecting the main chassis and sub chassis bodies with a torsion bar (shown later)
;HJ1_BODY_B=CHASSIS2
;HJ1_CARPOS_A=0, 0, 1.5         ;carpos for joints is in the reference frame of BODY_A. A bit poorly named, may add alias in future.
;HJ1_CARPOS_B=0, 0, -1.5

DJ0=WB_BOTTOM_FRONT             ;distance joints are what is used by e.g. DWB suspension in AC
;DJ0_BODY_A=CHASSIS2
DJ0_POS_A=0.6, -0.1, 0.4
DJ0_POS_A_1=0.6, -0.11, 0.4      ;suspension geometry adjustment available in v0.2+, see setup.ini docs below
DJ0_POS_B=0.05, -0.1, 0.0        ;if creating a 3-point wishbone (as shown here), make sure that its hub coordinates are shared or the solver will have issues
DJ1=WB_BOTTOM_REAR
;DJ1_BODY_A=CHASSIS2
DJ1_POS_A=0.6, -0.1, -0.1
DJ1_POS_B=0.05, -0.1, 0.0
DJ1_KP=0                        ;indicate that this joint is kingpin bottom (also works for ball joints) - used for steering axis - POS1+BODY_B is the designated coordinate/body combination

DJ2=WB_TOP_FRONT
;DJ2_BODY_A=CHASSIS2
DJ2_POS_A=0.5, 0.0, 0.3
DJ2_POS_B=0.1, 0.05, 0.1
DJ3=WB_TOP_REAR
;DJ3_BODY_A=CHASSIS2
DJ3_POS_A=0.6, 0.0, 0.1
DJ3_POS_B=0.1, 0.05, 0.1
DJ3_KP=1                        ;indicate that this joint is kingpin top

STEER_JOINT_0=STEER_LINK        ;tie rods - only difference to distance joints is toe setup + they're steered
;STEER_JOINT_0_BODY_A=CHASSIS2
STEER_JOINT_0_POS_A=0.7, 0.0, -0.2 ;car side (body A is chassis in this case). POS_A & POS_B work in 0.2
STEER_JOINT_0_POS_A_1=0.7, 0.0, -0.22
STEER_JOINT_0_POS_B=0.05, 0.0, -0.2 ;tire side (body B is the hub)

DJ4=PUSHROD                     ;distance joint being used as a pushrod from the hub to the rocker
DJ4_BODY_A=ROCKER
DJ4_POS_A=0.6, 0.1, 0.05         ;rocker side
DJ4_POS_B=0.1, -0.2, 0.1         ;wheel side
DJ4_LENGTH_OFFSET = 0.0         ; default length adjustment - in this case, the pushrod will be used to adjust ride height, so this is somewhat analogous to "rod_length" in vanilla suspension types. Most suspension, however, will use spring preload for this instead.

DJ5=T_BAR_ROD
DJ5_BODY_A=ROCKER
DJ5_BODY_B=T_BAR
DJ5_POS_A=0.7, 0.1, 0.1          ;rocker side
DJ5_POS_B=0.7, 0.2, 0.4          ;t-bar side

DJ6=ARB_CONSTRAINT1             ;these distance joints are recreating a relatively complicated ARB/3rd spring linkage
;DJ6_BODY_A=CHASSIS2
DJ6_BODY_B=T_BAR
DJ6_POS_A=0.5, 0.0, 0.4          ;chassis side
DJ6_POS_B=0.8, 0.2, 0.4          ;t-bar side
DJ6_PARITY=-1

J0=T_BAR_BJ                     ;ball joints can be used to connect rigid bodies together to only allow for rotational degrees of freedom
;J0_BODY_A=CHASSIS2
J0_BODY_B=T_BAR
J0_POS=0.8, 0.0, 0.4
J0_PARITY=0                     ;intentionally not mirrored as there is only one of these parts on the car

;SLIDER_0=TOOLBOX_PATH          ;slider locks 2 rigidbodies into moving along a single axis.
;SLIDER_0_BODY_B=TOOLBOX        ;can either directly define AXIS or use POS_A, POS_B to calculate it
;SLIDER_0_AXIS=0.0,0.0,1.0
;SLIDER_0_POS_A=0,0,0            ;generated axis takes precedence over AXIS, either are fine to use
;SLIDER_0_POS_B=0,0,1

;[REAR_TORSION_0]               ;torsion bars can be used for chassis flex - make sure you don't make an undamped spring!
;RATE=30000                     ;Nm/deg
;PRELOAD_TORQUE=0                      ;Nm of preload to apply to hinge
;PRELOAD=0                      ;degrees of preload to apply to hinge (additive with torque)
;HINGE=CHASSIS_HINGE            ;hinge that torsion bar is attached to
;PARITY=0

[REAR_COILOVER_0]               ;a coilover being used as a corner damper. Coilovers combine springs and dampers (with some other features). dampers.ini is required for use as of v1.79.
PULL_FORCE=0			;1 for pull spring/damper, default 0 (normally-compressed spring/damper)
INSTALL_RATE=4000000		;optional - installation stiffness of the coilover assembly, N/m
RATE=200000			;N/m
;HELPER_RATE=2000		;N/m of helper spring - new for 0.2.2 - does not work with spring lut at this time (spring lut acts in parallel with linear springs, not in series)
;HELPER_TRAVEL=0.02		;m of deflection at which helper compresses fully - new for 0.2.2
;BODY_A=CHASSIS2                ;CHASSIS by default
BODY_B=ROCKER                   ;HUB_L by default
PRELOAD=0.0			;meters
PRELOAD_FORCE=2400		;N - this can be used in cases where spring length is desired to always be the same at static ride height, regardless of the spring used. In this case, the car is using a pushrod for ride height and it is desired that the dampers stay at "design" length, so preload force is used.
POS_A=0.5, 0.1, 0.5	        ;POS_A and POS_B in 0.2+
POS_B=0.7, 0.1, 0.1
MIN_LENGTH=0.3		        ;minimum length of the damper (where it hits the hard stops and limits suspension travel)
MAX_LENGTH=0.5		        ;maximum length of the damper
END_RATE=1000000		;spring rate of hard stops
END_VTAPER=0.02			;velocity at which rate tapers off in rebound
END_VMAX=0.10			;velocity where end limit adds 0 force in rebound (these parameters help with energy loss to avoid bouncing after crash landings)
BUMPSTOP_GAP=0.035              ;the gap to the bumpstop (when suspension is at the design length of the damper - ie sqrt((pos0-pos1)^2)). Alt: travel above 0 design where bumpstop begins
ELECT_LOG=CORNER                ;CORNER or HEAVE ; only use this once per axle, it designates that the coilover travel should be logged to certain channels as the designated corner/heave damper travel for the axle

[REAR_COILOVER_1] ;heave damper
PULL_FORCE=1			;pull spring/damper
INSTALL_RATE=5000000		;N/m
RATE=0				;N/m - no spring in this case, only bump stops
;BODY_A=CHASSIS2
BODY_B=T_BAR
PRELOAD=0.0			;meters
PRELOAD_FORCE=0			;N - no preload of any kind shown here as the rest of the suspension is taking care of that (it also wouldn't work as there's no spring on this coilover)
POS_A=0.8, 0.1, 0.1 	        ;chassis (body A)
POS_B=0.8, 0.2, 0.4	        ;t-bar
MIN_LENGTH=0.2
MAX_LENGTH=0.4
END_RATE=1000000
END_VTAPER=0.02
END_VMAX=0.10
BUMPSTOP_GAP=0.020
PARITY=0                        ;not mirrored as there's only one heave spring
ELECT_LOG=HEAVE
FLIP_PRELOAD=1                  ;this can flip the sign of the preload in the setup menu, see setup.ini entry below for explanation
;DAMP_BUMP=5000                 ;N sec/m
;DAMP_FAST_BUMP=1000            ;Note: v0.2+. For setup functionality, dampers.ini is still required. Only use "simple" rates for non-adjustable dampers.
;DAMP_FAST_BUMPTHRESHOLD=0.05
;DAMP_REBOUND=10000
;DAMP_FAST_REBOUND=2000
;DAMP_FAST_REBOUNDTHRESHOLD=0.10

;[REAR_SPRING_0]                ;simple springs can also be added
;PULL_FORCE=1                   ;default 0, this works differently to how coilovers work. It pulls from both negative and positive deflection. On coilovers, the sign is simply flipped
;POS_A=0.7, 0.1, 0.1 	        ;chassis (body A)
;POS_B=0.7, 0.2, 0.4	        ;t-bar
;BODY_A=ROCKER
;BODY_B=T_BAR
;RATE=1                         ;N/m
;INSTALL_RATE=4000000		;optional - installation stiffness of the spring, N/m
;SPRING_LUT=(0.2=0|0.3=1230|0.4=2500)    ;Optional, m|N
;BUMPSTOP_LUT=(0=0|0.03=5000|0.06=20000) ;Optional, deflection(m)=force(N) lut for rubber bumpstops
;BUMPSTOP_GAP=0.25

;[REAR_DAMPER_0]                ;as well as simple dampers
;DAMP_BUMP=5000                 ;N sec/m
;DAMP_FAST_BUMP=1000
;DAMP_FAST_BUMPTHRESHOLD=0.05
;DAMP_REBOUND=10000
;DAMP_FAST_REBOUND=2000
;DAMP_FAST_REBOUNDTHRESHOLD=0.10
;BODY_A=CHASSIS
;BODY_B=HUB_L
;POS_A=0.3,0.5,0
;POS_B=0.3,0.0,0
;MIN_LENGTH=0.355
;MAX_LENGTH=0.575
;END_RATE=1000000
;END_VTAPER=0.02
;END_VMAX=0.10
```

---

*dampers.ini* (please see base documentation in Cars - Suspension)

New headers (**1.79 only**):
```ini
[FRONT_0] ;increase index for every damper on the car (including both coilovers and simple dampers - all simple dampers come first, then coilovers)

[FRONT_0_BLOWOFF]
```
**v0.2+**:
```ini
[FRONT_0] ;for simple dampers

[FRONT_C0] ;for coilovers, same indices as in suspensions.ini

[FRONT_0_BLOWOFF]

[FRONT_C0_BLOWOFF]
```

---

*bumpstops.ini* (please see base documentation in Cars - Suspension)

New headers:
```ini
[FRONT_C0] ;FRONT_0 format for simple dampers, add the C for coilover, make sure index matches suspensions.ini index
DEFAULT=1 ;same as base docs
STACK=2 ;same as base docs

[FRONT_C0_0]
LUT=sameasbasedocs.lut
[FRONT_C0_1]
LUT=stillsameasbasedocs.lut
```

---

*setup.ini*

To go along with above suspensions.ini example:
```ini
[TORSION_RATE_LF_0] ;per corner, same indices as supension.ini
SHOW_CLICKS=0
TAB=SUSPENSION
NAME=Torsion Bar LF
LUT=suspension_bars_t.lut ;can use normal MIN/MAX/STEP or a lut
POS_X=0
POS_Y=0
HELP=HELP_LF_WHEELRATE

[SPRING_RATE_LR_C0] ;C0 for coilover 0
SHOW_CLICKS=0
TAB=SUSPENSION
NAME=Spring Rate LR
LUT=suspension_springs.lut
POS_X=0
POS_Y=8
HELP=Null

;[SPRING_RATE_LR_0] ;0 for simple spring 0
;SHOW_CLICKS=0
;TAB=SUSPENSION
;NAME=Spring Rate LR
;LUT=suspension_springs.lut
;POS_X=0
;POS_Y=8
;HELP=Null

[DJ4_LENGTH_OFFSET_LR] ;works for any distance joint. Adjust length via setup, 0 is design length.
SHOW_CLICKS=0
TAB=SUSPENSION
NAME=Pushrod Length Rear
MIN=-100 ;0.1mm
MAX=100  ;0.1mm
STEP=2   ;0.1mm
POS_X=0.5
POS_Y=7
HELP=NULL

[DJ0_POS_A_SETTING_LR]     ;change the coordinates used for a given joint, currently available for DJ and STEER_JOINT (v0.2+)
SHOW_CLICKS=0
TAB=SUSPENSION
NAME=Front Geometry
LUT=setup_front_susp.lut ;lut optional, it selects the indices as defined in the suspension.ini entry, so can use MIN/MAX/STEP as well.
DEFAULT=0                ;change the default loaded suspension geometry
POS_X=0.5
POS_Y=3
HELP=NULL

[STEER_JOINT_0_POS_A_SETTING_LR]
SHOW_CLICKS=0
TAB=SUSPENSION
NAME=Front Geometry
LUT=setup_front_susp.lut ;lut optional, it selects the indices as defined in the suspension.ini entry, so can use MIN/MAX/STEP as well.
DEFAULT=0                ;change the default loaded suspension geometry
POS_X=0.5
POS_Y=3
HELP=NULL

[STEER_JOINT_0_LENGTH_OFFSET_LR] ;v0.2+ works for any steer joint. Adjust length via setup, 0 is design length.
SHOW_CLICKS=0
TAB=SUSPENSION
NAME=Tie Rod Length Rear
MIN=-100 ;0.1mm
MAX=100  ;0.1mm
STEP=2   ;0.1mm
POS_X=0.5
POS_Y=7
HELP=NULL

[SPRING_PRELOAD_LR_C1] ; spring gap flipped sign 0.1mm - can use preload inversely to gap a spring, in this case, "preload" actually is being used for the spring gap, hence the flipped value in the suspensions.ini
SHOW_CLICKS=0
TAB=SUSPENSION HEAVE
NAME=Spring Gap
MIN=-200 ;0.1mm
MAX=700
STEP=1
POS_X=0
POS_Y=4
HELP=HELP_HF_TRAVEL_RANGE

[BUMPSTOP_LR_C1] ; rubber
SHOW_CLICKS=0
TAB=SUSPENSION HEAVE
NAME=Bump Rubber R
LUT=bs_setup.lut
POS_X=1
POS_Y=3
HELP=HELP_HR_WHEELRATE

[BUMPSTOP_GAP_LR_C1] ; rubber gap
SHOW_CLICKS=0
TAB=SUSPENSION HEAVE
NAME=Bump Rubber Gap
MIN=0  ;mm
MAX=70 ;mm
STEP=1 ;mm
POS_X=1
POS_Y=4
HELP=HELP_HF_TRAVEL_RANGE

[BUMPSTOP_NUM_LR_C1] ; rubber stack #
SHOW_CLICKS=0
TAB=SUSPENSION HEAVE
NAME=Bump Rubber Stack
MIN=1
MAX=4
STEP=1
POS_X=0.5
POS_Y=5
HELP=Null

[DAMPER_BUMP_LF_C0] ;v0.2+ the index now matches the suspensions ini index instead of the "true" index on the car. e.g. If there's a parity=0 damper at index 1 in the suspensions.ini, LF_1 will exist and RF_1 will not.
SHOW_CLICKS=2
TAB=DAMPERS
NAME=Bump
MIN=0
MAX=41
STEP=1
DEFAULT=13
POS_X=0
POS_Y=0
HELP=HELP_LF_DAMPER_BUMP

;[DAMPER_BUMP_LF_0] ;v0.2+
;SHOW_CLICKS=2
;TAB=DAMPERS
;NAME=Bump
;MIN=0
;MAX=41
;STEP=1
;DEFAULT=13
;POS_X=0
;POS_Y=0
;HELP=HELP_LF_DAMPER_BUMP
```

---

*suspensions.ini working examples*

MacPherson Strut:
```ini
[FRONT]
TYPE=COSMIC
RIM_OFFSET=0.047	; OEM Spec
BASEY=-0.222
TRACK=1.565 ; offset added to track with COSMIC (essentially measuring hub to hub), vanilla TRACK=1.471
HUB_MASS=52.2		; Front unsprung mass, excluding any unsprung mass added below

BODY_0_NAME=STRUT_HELPER
BODY_0_MASS=10
BODY_0_POS=0.215,0.45,-0.0306 ; should be at strut top, this body allows the slider to mount to the chassis with a ball joint
BODY_0_MIRROR=1
; steer link
STEER_JOINT_0=STEER_LINK
STEER_JOINT_0_POS_A=0.385, -0.078, 0.07
STEER_JOINT_0_POS_B=0.039, -0.100, 0.129
DJ0=LCA_REAR
DJ0_POS_A=0.42,-0.091, -0.34
DJ0_POS_B=0.0525, -0.122, 0.01
DJ0_KP=0
DJ1=LCA_FRONT
DJ1_POS_A=0.42,-0.091 ,-0.04
DJ1_POS_B=0.0525, -0.122, 0.01
; attach strut to the car
J0=STRUT_TOP
J0_BODY_B=STRUT_HELPER
J0_POS=0.215,0.45,-0.0306
J0_KP=1
; slider lets the hub move relative to the helper
SLIDER_0=STRUT_MOTION
SLIDER_0_BODY_A=STRUT_HELPER
SLIDER_0_AXIS=-0.108, -0.45, 0.0306 ; axis or positions should both work
SLIDER_0_POS_A=0.215,0.45,-0.0306    ; positions used if present
SLIDER_0_POS_B=0.107,0.0,0.0

TOE_OUT=0.00000			 					; Toe-out expressed as the lateral offset of the chassis-side tie rod mount in meters
STATIC_CAMBER=-0.7							; Static Camber in degrees. Actual camber relative to suspension geometry and movement, check values in game

[FRONT_COILOVER_0]
RATE=21000
PRELOAD=0.138
POS_A=0.215,0.45,-0.0306 ; strut top
POS_B=0.107,0.0,0.0 ; same as the slider
MIN_LENGTH=0.40
MAX_LENGTH=0.54
BUMPSTOP_GAP=0.033

[FRONT_DAMPER_0] ;uses simple damping rates
DAMP_BUMP=2750
DAMP_FAST_BUMP=1040
DAMP_FAST_BUMPTHRESHOLD=0.053
DAMP_REBOUND=5850
DAMP_FAST_REBOUND=2700
DAMP_FAST_REBOUNDTHRESHOLD=0.053
POS_A=0.215,0.45,-0.0306 ; same coordinates as the coilover
POS_B=0.107,0.0,0.0
```

---

### General Tips

* Take advantage of the default values! Cosmic suspension files can get very long very quickly, but many of the parameters are fine left to their defaults, which can shorten the file significantly.

* All rates, forces, et cetera are at the component level. Meaning no more wheel rates, spring rates are the rates of the springs themselves, same for dampers and their crossover velocities.

* Be mindful of movement constraints when "designing" a cosmic suspension. Ball joints only constrain translation, so rotation must be controlled by something else (another ball joint limits the rotation to only 1 axis, and another limits relative movement entirely). Distance joints are just two ball joints that are connected, so the same principles apply. Hinges are essentially just two ball joints as well (but with a memory framework that stores the axis and angle, etc).

* If doing geometry that has the spring/damper connecting to one of the control arms (e.g. most DWB designs), the correct approach is to create a rigid body at the CoG of the control arm (a fair approximation is the weighted average of the 3 corner coordinates - weight the hub point as 2 and the chassis points as 1) and then connect that body to the chassis and hub via ball joints. This is only needed if something needs to be attached to the control arm. If not, it can just be made from distance joints.

* Strut suspension can be made with a slider joint, a rigid body, and a ball joint. The ball joint attaches the strut top (body) to the chassis, and the slider joint attaches the hub to the strut top.

#### Joint types

- `BALL`: connection via freely spinning socket ensuring constant distance between objects:

  <img src="https://files.acstuff.ru/shared/hcP7/20221025-145018.png" width="200">

- `SLIDER`: basic slider connection:

  <img src="https://ode.org/wiki/images/8/89/Slider.jpeg" width="200">

- `DISTANCE`: connection ensuring distance between points:

  <img src="https://files.acstuff.ru/shared/PbU1/20221025-145918.png" width="200">

- `HINGE`: connection ensuring only 1DoF around provided axis:

  <img src="https://ode.org/pix/hinge.jpg" width="200">
