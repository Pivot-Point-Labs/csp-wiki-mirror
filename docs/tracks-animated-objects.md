# Animated Objects

With this CSP feature, you can animate objects in various ways. Move clock needles, get trains to move along tracks, spin weather vanes and windmills, link position, rotation or scale to [conditions](tracks-conditions.md) or use keyframe animations with “.ksanim“. And if you would need other behaviours, please let me know.

First of all, important note: if you’re making a new track and want to animate something, it would be much easier to export things you want to animate in a separate KN5 and save it using “Save KN5/Car” option. Saving KN5 as track means its whole hierarchy would get collapsed into a single list of meshes. Faster to render and with working physics, but meshes can’t be moved unless they are within their own nodes. Otherwise, you would have to wrap meshes in nodes with a config, in some cases it might get a bit too complicated (especially if “.ksanim“ files are involved). I described the process farther.

Here is an example of an animated track, the one used in [this video](https://youtu.be/XOIRDhoIm6c): [track link](https://drive.google.com/uc?id=1UywohUEgZcfv0u9-MVw49TrB-50mMfqi). Thanks to Soyo for preparing it!

### Syntax

Whole thing starts with this:

```ini
[ANIMATED_...]
ACTIVE = 1        ; (optional) set to 0 to disable
NODE = root_node  ; name of a node to move (for keyframe animation, set a node
                  ; encloding the whole thing)
```

But after that, each behaviour has its own parameters. How to specify the behaviour? It’s chosen based on what parameters are there! Not sure why I went this route when I was adding it, but I feel like it’s going to come back and bite me later.

Before we move further, just a couple of things to note:

- A lot of those animations rely on lags. You can think of them as mass. 0 for instant reaction, 1 for not reacting at all. Really, most of CSP features use those, but I thought I’d mention it here just in case.

- For some of those behaviours, you can use value from condition instead of a number. I marked those values with `*`. Just put a condition name instead of a number there and it’ll work.

### Windmill

```ini
[ANIMATED_...]
NODE = windmill_rotating_part
WINDMILL_DIR = 1, 0, 0       ; direction of wind to which windmill would react
WINDMILL_DIR_EXP = 1         ; increase to decrease spinning from almost-sideways wind¹
WINDMILL_DIR_BOTH_SIDES = 1  ; set to 0 to make wind blowing from the back to have no affect
SPIN_AXIS = 0, 0, 1          ; spinning axis
WIND_SPEED_KMH_MIN = 0.5     ; wind speed at which windmill starts to spin
WIND_SPEED_KMH_MAX = 20      ; wind speed at which windmill spins at its highest speed
WIND_SPEED_KMH_STOP = 0      ; wind speed at which windmill forcefully stops²
LAG_UP = 0.999               ; lag for speeding up
LAG_DOWN = 0.999             ; lag for spinning down
LAG_BRAKING = 0.98           ; lag for forceful stop
SPEED_MULT = 1               ; spinning speed multiplier*
```

¹ By default wind blowing 60° from `WINDMILL_DIR` would result in half the spinning, but if value of `WINDMILL_DIR_EXP` is 2, it would only be a quarter.

² Meant for those modern windmills generating electricity. They don’t speed if wind is too strong, to make sure they wouldn’t spin to pieces.

### Weather vane

```ini
[ANIMATED_...]
NODE = weather_vane
WEATHERVANE_DIR = 1, 0, 0  ; direction of wind to which vane would react
WEATHERVANE_DIR_EXP = 0    ; increase to decrease spinning from almost-sideways wind¹
SPIN_AXIS = 0, 1, 0        ; spinning axis
SPEED_MULT = 1             ; spinning speed multiplier
WIND_SPEED_KMH_MIN = 0.5   ; wind speed at which vane starts to spin
INERTIA = 0.99             ; vane inertia
ANGLE_OFFSET = 0           ; angle offset just in case
```

¹ It’s all very similar to according windmill params, but since weather vanes usually react to anything, default value here is 0.

### Clock needle

```ini
[ANIMATED_...]
NODE = needle_hours
CLOCK_NEEDLE = HOUR  ; role, valid values: SECONDS, MINUTE, HOUR or HOUR24
OFFSET_DEG = 0       ; offset in degress
DEBUG_VALUE = 0      ; set to non-zero value to debug things, it would force needle to that value
SPIN_AXIS = 0, 0, 1  ; spinning axis
LAG = 0.67           ; lag for smoother movement
```

### Keyframe animation

```ini
[ANIMATED_...]
NODE = animated_node
ANIMATION = animation.ksanim  ; animation filename, must be located next to config
TICK_TOCK_MODE = 0            ; set to 1 to make animation go forwards and backwards
DURATION = 10                 ; animation duration in seconds*
; PROGRESS =                  ; animation progress¹*
```

¹ `PROGRESS` is meant to link animation to a certain condition instead of just looping it with a given interval. This way, you can tie animation to things like time of day, sun angle and more.

### Train

```ini
[ANIMATED_...]
NODE = train_node
MOVE_ALONG = train_loop             ; name of a mesh along which train is going to move¹
NODES_FOLLOWING = train_1, train_2  ; names of carriages attached to the train

CLUSTER_THRESHOLD = 3      ; might have to adjust to help trajectory detection
STARTING_POINT = X, Y, Z   ; for unlooped paths, start here and move to another end
INVERT_DIRECTION = 0       ; for looped paths
TICK_TOCK_MODE = 0         ; set to 1 to go forwards and backwards
CUBIC_INTERPOLATION = 0    ; set to 1 for smoother movement (recommended)
SPEED_KMH = 40             ; basic train speed*
; PROGRESS =               ; travel progress²*
PIECE_LENGTH = 5           ; length of attached carriages
LAG_UP = 0.9               ; acceleration lag
LAG_DOWN = 0.9             ; deceleration lag
DELAY_BETWEEN_RUNS = 0, 0  ; min and max boundaries for a random delay between runs, in seconds
DEBUG_PATH = 0             ; set to 1 to highlight resulting path

; Path can also contain local speed adjustment areas:
SPEED_ADJUSTMENT_0 = 50             ; target speed for a train within that area*
SPEED_ADJUSTMENT_0_POINT = X, Y, Z  ; coordinates
SPEED_ADJUSTMENT_0_RADIUS = 20, 60  ; radius of full effect and of adjustment start, in meters

; Train can also create new inputs for other conditions, great for attaching audio or lights:
SPEED_CONDITION_INPUT = MyNewInput_TrainSpeed
PROGRESS_CONDITION_INPUT = MyNewCondition_TrainProgress
```

¹ That mesh is used to generate the path, should be something like a long narrow strip (possibly hidden). It could be either closed or open, and train would tilt depending on where its normals are facing (if you look [at the example](https://youtu.be/XOIRDhoIm6c), train makes some sort of a barrel roll there).

² `PROGRESS` is meant to link travel to a certain condition. This way, you can link it to things like time of day, sun angle and more. Not sure if it would be helpful for trains, but there could be other things traveling along certain path, right?

#### Few tips on using trains from @John514

- Align trains on the Y axis;
- Train car No. 1 must be on the bottom (towards Y');
- The moving objects need to be rotated by 90d on the X axis.

### Conditional animation

This one would be chosen if either `POSITION`, `ROTATION` or `SCALE` is set. Here, position, scale and rotation angle all can be set using track condition or expression.

```ini
[ANIMATED_...]
NODE = something_moving
POSITION = X, Y, Z
SCALE = X, Y, Z
ROTATION = X
SPIN_AXIS = 0, 1, 0
```
