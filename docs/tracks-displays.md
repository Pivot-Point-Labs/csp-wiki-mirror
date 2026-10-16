# Displays

Displays allow to animate track textures. Well, at the moment, they only support camera feed, but later more options will be available (hopefully).

<a href="https://gfycat.com/horribledimhermitcrab"><img src="https://giant.gfycat.com/HorribleDimHermitcrab.gif" width="400" ></a>

Whole configuration consists of two parts, first is for general display setup (target meshes, position and size on texture, color adjustment) and second is for actual mode, which for now is just some cameras.

Hint: to light it up at night, use the material in a separate MATERIALS_ADJUSTMENT section with some emissive, use the mesh in DISPLAY section

### Syntax (general)

```ini
[DISPLAY_...]
; General settings:
MESHES = tvstaff_HI_?    ; list of track meshes to act as displays
REGION_START = 20, 320   ; display position on texture, in pixels
REGION_SIZE = 508, 290   ; display size on texture, in pixels

; Update and rendering options
HIGH_REFRESH_RATE = 1    ; high refresh rate (enabled by default; 30 FPS with this option on, 15 FPS without)
FLIP_X = 0               ; change to 1 to flip output on X axis (mainly for strange UV mapping)
FLIP_Y = 0               ; change to 1 to flip output on Y axis (mainly for strange UV mapping)

; Color corrections:
OUTPUT_ALPHA = 1         ; alpha channel value for display area
OUTPUT_GAMMA = 0.55      ; gamma correction, reduce to make darker areas even darker
OUTPUT_SATURATION = 1.0  ; saturation correction
OUTPUT_BRIGHTNESS = 1.0  ; brightness correction
OUTPUT_FISH_EYE = 0.0    ; increase to add lens distortion effect
OUTPUT_VIGNETTE = 0.0    ; increase to darken corners
OUTPUT_CHROMATIC_ABERRATION = 0.0 ; increase to add that nasty chromatic aberration

; Mode settings:
…
```

And then, for the whole thing to work, in the same section add mode settings.

### Syntax (camera mode)

```ini
[DISPLAY_...]
; General settings:
…

; Mode settings:
MODE = CAMERA

; First camera
CAMERA_0 = 176.03, 211.67, -189.67         ; camera position
CAMERA_0_TARGET = 171.65, 209.59, -185.13  ; point at which camera is looking
CAMERA_0_UP = 0, 1, 0                      ; camera’s upwards direction, defaults to 0, 1, 0
CAMERA_0_FOV = 50                          ; FOV angle in degress, defaults to 50
CAMERA_0_ASPECT_RATIO = 1.752              ; aspect ratio, defaults to REGION_SIZE.x/REGION_SIZE.y

; Second camera
CAMERA_1 = 451.95, 197.55, 103.46
CAMERA_1_TARGET = CLOSEST_CAR  ; instead of fixed point, uses closes car
CAMERA_1_TARGET_INERTIA = 0.9  ; camera inertia for smoother movement
CAMERA_1_TARGET_TARGET_REFERENCE_POINT = 431, 197, 103
                               ; point to which closest car is taken, defaults to camera position

CAMERA_2 = -44.02, 195.05, 284.45
CAMERA_2_TARGET = FOCUSED_CAR  ; another mode, focused car (usually the one camera is linked to)
CAMERA_2_TARGET_INERTIA = 0.9
CAMERA_2_FOV = 35
```

Currently, active camera is the nearest one. The way it works, let’s say, for example, you have a bunch of TVs all over the track. You can set them with a single `[DISPLAY_...]` and then add a camera next to each of those TVs. Having nearest camera active ensures driver would get a proper view for whatever TV they’re closest to currently, and yet at its core it’s a single entity, single rendering pass, single texture combination, so everything is clean and optimized.

### About processing distance

Cameras and displays only work if they’re not too far away from camera. You can’t have a camera showing things from 10 km away, that’s a pretty important limitation and is entirely intentional. Even now, AC has all those optimizations with LODs and what not, and those cameras need to consider that and not just make whole thing visible, otherwise it would be terrible for performance. Plus, CSP recently got that chunk optimization simply removing remote geometry from scene tree to save some time on processing, and I hope later I could add more things there, ideally unloading resources from VRAM or maybe even RAM too. Of course, having cameras showing stuff from 10 km away would break all that.

### Digital screen shader

As you can see on that introduction GIF, it’s not just showing an image, but also has that pixel pattern, messes up colors with grazing angles and what not. That is not because of `[DISPLAY_...]`, but because of custom material `[Material_DigitalScreen]` from `common/materials_track.ini`.

It can work in two different ways. If you have your screen separated into a separate mesh, then it’s easy, just use it for the whole thing:

```ini
[Material_DigitalScreen]
Materials = tv_staff
UseTextureCoordinates = 1  ; if mapping seems weird, change to 0
                           ; (although it shouldn’t, or else how would DISPLAY_… work?)
ScreenAspectRatio = 0.5    ; adjust if pixels look skewed
ScreenScale = 1024         ; adjust for target resolution, in general using texture size here might be a good idea
```

Another case is if you have your screen combined with regular mesh, then there is an option to use MultiMap version with different masking options. This is how I set it for Vallelunga, using `OUTPUT_ALPHA = 0` in `[DISPLAY_...]`, since rest of `txDiffuse` there had white alpha-channel:

```ini
[Material_DigitalScreen]
Materials = tv_staff
UseMultiMap = 1
UseDiffuseMask = INVERT  ; works with OUTPUT_ALPHA = 0 in DISPLAY
ScreenScale = 1024
```

Apart from `UseDiffuseMask`, there is also `UseMapsMask` and `UseNormalMask`, both taking either `0`, `1` or `INVERT`. And another option is to define area explicitly:

```ini
[Material_DigitalScreen]
Materials = tv_staff
UseMultiMap = 1
UseAreaMask = 1
AreaMaskCenter = 264, 464
AreaMaskSize = 508, 288
AreaMaskTotalSize = 2048, 2048
ScreenScale = 1024
```

### Features to add later

- More modes: something programmable, slideshow, ideally also would be great to be able to play a video;
- More camera modes and movements;
- Make 3D cameras follow cars? Although that is more for track animations;
- Allow to adjust for scaled and rotated mapping?
