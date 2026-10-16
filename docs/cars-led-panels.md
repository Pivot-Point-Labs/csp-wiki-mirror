# LED panels

LED panels can help to set those things showing race position and driver name and occasionally flashing.

<a href="https://gfycat.com/colorfulfastivorybilledwoodpecker"><img src="https://thumbs.gfycat.com/ColorfulFastIvorybilledwoodpecker-size_restricted.gif" width="400" ></a>

Unlike original “digital_panels.ini”, this option would work in replays (also, it supports [any other input type](cars-instruments-inputs.md)). But the main difference is that it uses dynamic texture instead of floating digits, so it can fit bent surfaces better, and doesn’t require special parent nodes for digits placement.

### Important note

Before we move further, I would first like to go into a bit of depth on how it works and how to use it. The way it works, it’s a dynamic texture, background is transparent and digits or letters use a specified color. This means there are two ways you can get it to work:

- You can duplicate underlying mesh, move a new one a bit away, assign dynamic texture to its `txDiffuse` slot, make it emissive and set blending mode to alpha test. This is the simplest approach, but it adds a new draw call, would require to modify model and in general seems pretty whacky. There is another way though.

- Instead, you can use `ksPerPixelMultiMap_emissive` shader, and assign dynamic texture to `txEmissive` slot! You don’t need to change model to replace shader, simple `[SHADER_REPLACEMENT_...]` tweak would work nicely. This way, you wouldn’t need to edit any models. You might wander how it could work if `txDiffuse` would be applied to resulting emissive breaking LEDs shape — well, good news, there is a parameter to disable that `txDiffuse` interference!

### Syntax

```ini
[LED_PANEL_...]
MESHES = RSS_EXT_LED_Panel      ; target mesh
TEXTURE_SLOT = txEmissive       ; target texture slot
RESOLUTION = 1024, 512          ; resolution of newly generated texture
MASKS_PACK = lumirank_font.zip  ; name of a pack with LED masks
DIGIT_0 = 22, 47, 312, 455      ; X, Y, width and height of a first digit
DIGIT_1 = 353, 47, 312, 455     ; X, Y, width and height of a second digit
DIGIT_2 = 692, 47, 312, 455     ; X, Y, width and height of a third digit
                                ; you can set as many digits as you need

BASE_COLOR = '#ffffff', 0.5    ; base color (when it’s not flashing)
FLASHING_COLOR = '#ffffff', 1  ; color for flashing
FLASHING_APPLY_MASK = 1        ; should mask be applied to flashing

BLANCPAIN_FLASHING_PERIOD = 1       ; Blancpain flashing: period in seconds
BLANCPAIN_FLASHING_DURATION = 0.2   ; for how long it shuts off, in seconds
BLANCPAIN_FLASHING_RACE_CLASS = AM  ; race class (it would flash only for a leader in class)

N24_FLASHING_PERIOD = 3.5        ; N24 flashing: period in seconds
N24_FLASHING_TIME = 1.2          ; for how long it would flash in seconds
N24_FLASHING_FREQUENCY = 6       ; flashing frequency in Hz
N24_FLASHING_ACTIVE_SHARE = 0.7  ; how much time during flashing it spends in active stage

ROLE_0 = DRIVER_NAME  ; first role
ROLE_1 = POSITION     ; second role
                      ; you can set as many roles as you need

ROLE_DURATION = 3     ; how much time in seconds each role lasts
```

### About LED masks and `MASKS_PACK`

Masks are black and white textures marking with white areas to glow. They’re very similar to textures used in `texture\display_panel` (although they will be drawn on a dynamic texture instead of appearing in 3D space). However, because now letters can also be used, they have an extra feature added to save both space on disk and VRAM during the race. You can prepare a single high-resolution mask with all the LEDs and then make masks for letter and digits in much lower resolution, just roughly covering areas with target LEDs. It can save a lot of bytes without any sacrifice of quality, and might even make preparing masks easier. [Here is an example pack](https://drive.google.com/uc?id=1q2o7dgODEJGCIlz9i_2YZdid3DDmbSgS) from [RSS GT-M Bayro 6](https://racesimstudio.com/gtm-bayro-6) (thanks to Scott Shaw for the permission to use it as an example).

So, in other words, how it all works:

- To render a letter “A”, CSP will open a ZIP-archive mentioned in `MASKS_PACK` and look for “base/a.dds”;
- It would also look for “mask.dds”;
- If mask is found, it would render them both in multiply mode;
- Otherwise, only “base/a.dds” will be used.

For flashing stage, approach is similar:

- To render a letter “A”, CSP will look for “flashing/a.dds”;
- If nothing exists there, it would use “flashing_fallback.dds”;
- If `FLASHING_APPLY_MASK` is set to 1, it would use mask similar to non-flashing stage;
- Otherwise, it would just use a texture as if mask isn’t there.

### About roles

Currently, there are three types of roles:

- `DRIVER_NAME`: prints name of a driver (the same shown in a name tag, for example), shortened if necessary:

  ```ini
  ROLE_0 = DRIVER_NAME
  ```

- `TEXT`: prints a static text set in corresponding parameter:

  ```ini
  ROLE_0 = TEXT
  ROLE_0_TEXT = HELLO WORLD

- Anything else would be processed as [an input](cars-instruments-inputs.md), similar to [CSP digital instrument](cars-digital-instruments.md) and others:

  ```ini
  ROLE_0 = GAS
  ROLE_0_INPUT_MULT = 999
  ```

  Notice how regular “INPUT_…” params here have a corresponding “ROLE_N_” prefix. Apart from that, you can use it just as usual, with LUTs, lags and so on.

  Another important detail: by default, number format would have leading zeros, use this to change that:

  ```ini
  ROLE_0_NUMBER_FORMAT = 3.0
  ```

### About `ksPerPixelMultiMap_emissive` and shader replacement

Here is an example of how you can change a shader and set it to glow with a config:

```ini
[SHADER_REPLACEMENT_...]
MATERIALS = LED_Panel
SHADER = ksPerPixelMultiMap_emissive
FILL_MISSING_TEXTURES = 1
PROP_... = emSkipDiffuseMap, 1
PROP_... = ksEmissive, 100, 100, 100
```

For more information on the whole thing, [take a look at this](general-shader-replacements.md).

### Few tips

- If you want to make flashing color brighter, simply reduce brightness of base color and raise emissive;
- If there was some old texture in texture slot, digits would be drawn on top of it;
- If you’re using `txEmissive` approach, it might make sense to lower resolution comparing to txDiffuse resolution to save on VRAM and performance a bit.
