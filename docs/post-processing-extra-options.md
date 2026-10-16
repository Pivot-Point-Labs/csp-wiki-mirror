# Extra Options

Assetto Corsa uses YEBIS for post-processing, and although post-processing filters can access a lot of its options, still, a few were left untouched. Maybe you would find a good use for them?

*Note: new post-processing selector app has a built-it editor, you can access it via context menu like so:*

<a href="https://gfycat.com/MerryGrandGuineafowl"><img src="https://thumbs.gfycat.com/MerryGrandGuineafowl-size_restricted.gif" width="400" ></a>

### Adjust size of metering area for auto-exposure

```ini
[EXT_AUTO_EXPOSURE]
METERING_AREA_SIZE = 0.2, 0.2    ; size of metering area (X and Y), where 1 is either full width or height
METERING_AREA_OFFSET = 0.0, 0.1  ; offset from center, same units
METERING_AREA_DEBUG = 0          ; set to 1 to see that area highlighted
```

### Color grading (aka color look up tables)

```ini
[EXT_COLOR_GRADING]
ENABLED = 1
STRENGTH = 1.0  ; from 0 to 1
FILE = 'data:image/png;base64,iVBORw0KGgoAAAAN…'
```

For `FILE`, you can either use file name of a PNG image located in “system/cfg/ppfilters”, or you can encode it in [base64](http://b64.io/) and use that base64 PNG URL. Image can be either in common CM-compatible format, [like so](http://api.unrealengine.com/udk/Three/rsrc/Three/ColorGrading/RGBTable16x1.png), or it could be a HaldCLUT image. If it doesn’t load, try saving it in more regular PNG format, like 24 bpp (48 bpp is supported with 0.1.41).

### Extra color transformations

Unlike color grading, which is applied to LDR image (after tonemapping, where brightest area is regular white), these transformations are applied before tonemapping, to HDR image. Order matters, set by section indices.

```ini
[EXT_COLOR_CORRECTION_0]
TYPE = BIAS_RGB
RGB = -0.05

[EXT_COLOR_CORRECTION_1]
TYPE = MODULATION_RGB
RGB = 1.2

[EXT_COLOR_CORRECTION_2]
TYPE = FADE_RGB
RGB = 0.2, 0.1, 0.2
EFFECT_RATIO = 0.2

[EXT_COLOR_CORRECTION_3]
TYPE = MONOTONE_RGB_SAT_MOD
RGB = 1.2, 1, 1
SATURATION = 1.2
MODULATION = 0.2
```

Supported color transformation types:

- Without parameters: `GRAYSCALE`, `NEGATIVE`;
- With single number `VALUE` parameter: `SATURATION`, `BRIGHTNESS`, `CONTRAST`, `BIAS`, `SEPIA_TONE`;
- With three numbers `RGB` parameter: `SATURATION_RGB`, `MODULATION_RGB`, `CONTRAST_RGB`, `BIAS_RGB`;
- With various parameters:
  - `TEMPERATURE` (parameters: `TEMPERATURE_K`, value; `LUMINANCE`, number);
  - `WHITE_BALANCE` (parameters: `TEMPERATURE_K`, value; `LUMINANCE`, number);
  - `MONOTONE_RGB` (parameters: `RGB`; `EFFECT_RATIO`, number);
  - `MONOTONE_RGB_SAT_MOD` (parameters: `RGB`; `SATURATION`, number; `MODULATION`, number);
  - `FADE_RGB` (parameters: `RGB`; `EFFECT_RATIO`, number);
  - `HUE` (parameters: `HUE`, number; `KEEP_LUMINANCE`, flag);
  - `HSB` (parameters: `HUE`, number; `SATURATION`, number; `BRIGHTNESS`, number; `KEEP_LUMINANCE`, flag).
