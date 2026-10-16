# Smart Mirror

Smart Mirror extension adds a few useful things for rear view mirrors. Main is, of course, Real Mirrors by henter, amazing feature replacing single reflection for all mirrors with separate, adding visible car in those reflections and even accurately correcting for camera position.

### Syntax

There are a few tweaks for cars available:

```ini
[SMART_MIRROR]
DISALLOW_REFLECTION_TILTING = 1     ; disable that simple tilting effect (for cars with monitors)
DISALLOW_MAPPING_NORMALIZATION = 1  ; by default since 0.1.49 Custom Shaders Patch automatically remaps UV
  ; for mirrors to make sure aspect ratio is correct. Set this value to 1 to disable it for a particular car.
  ; Requires AC reload if changed.

; Options for real mirrors:
[REAL_MIRROR_N]  ; where N is mirror index
ROTATION = 0, 0  ; rotation
FOV = 10         ; field of view in degress
ASPECT_MULT = 1  ; multiplier for aspect ratio
IS_MONITOR = 0   ; set to 1 to make mirror act as a monitor
FLIP = 0         ; set to 1 to flip mirror

USE_MONITOR_SHADER = 0           ; set to 1 to use monitor shader with pixels visible if camera is too close
MONITOR_SHADER_SCALE = 400, 100  ; adjust pixel density of monitor shader
MONITOR_SHADER_TYPE = 0          ; set to 1 to use IPS matrix for monitor, without skewing colors
```

Players can later readjust real mirrors the way they like it.

### Guessing

- If any of real mirrors have `IS_MONITOR = 1`, simple tilting effect will be disabled by default;
- IPS matrix is set as default for any car manufactured after 2015.
