# Lights

There are two ways to add a light source to a track: simply specify `[LIGHT_...]` with position and direction for a single light source or use `[LIGHT_SERIES_...]` to automatically generate a bunch of lights based on geometry (for example, one for each lamp post).

### Syntax for single light

There are three ways of setting a single light. Firstly, with position and direction (you can use Object Inspector to quickly find out position, just click anywhere and copy coordinates):

```ini
[LIGHT_...]
POSITION = X, Y, Z
```

Second way is to use a mesh with an optional offset in meters. Mesh will be split into groups, largest group will be a position of a light:

```ini
[LIGHT_...]
MESH = mesh_name
OFFSET = X, Y, Z  ; optional offset in meters
```

And third way is to set a line light. It requires both starting and finishing point. Optionally, you can also set two colors for gradient:

```ini
[LIGHT_...]
LINE_FROM = X, Y, Z
LINE_TO = X, Y, Z
COLOR_FROM = '#ff0000', 2
COLOR_TO = '#00ff00', 3
```

Just to clarify, those line lights, especially with different colors, don’t have a lot to do with how accurate area light would behave. Please set them wisely.

With all three ways, default direction is down:

```ini
DIRECTION = 0, -1, 0
```

### Syntax for light series

With lights series approach, lights can be generated from meshes, or you can list a bunch of them at once. Here is the second way. In this example, all lights will be pointing downwards:

```ini
[LIGHT_SERIES_...]
POSITION_0 = X, Y, Z
POSITION_1 = X, Y, Z
POSITION_2 = X, Y, Z
; and so on
```

And here is a version with custom directions:

```ini
[LIGHT_SERIES_...]
POSITION_0 = X, Y, Z
DIRECTION_0 = 1, 0, 0
POSITION_1 = X, Y, Z
DIRECTION_1 = 1, 0, 0
POSITION_2 = X, Y, Z
DIRECTION_2 = 1, 0, 0
; and so on
```

To generate lights from meshes, list either their names or materials. All meshes will be split into groups, and a light will be created for each of those groups. Optional offset here is also available. Here, as usual, all lights are pointing downwards:

```ini
[LIGHT_SERIES_...]
MESHES = lamppost?, glowing_window?
MATERIALS = glowing_material?  ; or, you could use "MESHES = material:glowing_material?"
OFFSET = X, Y, Z  ; optional offset in meters
```

And, as usual, with `DIRECTION` you can set a custom value. However, this combination of `[LIGHT_SERIES_...]` and meshes has an alternative, where lights would point out along with sum of normals of an associated chunk of mesh:

```ini
DIRECTION = NORMAL
```

For example, imagine you have a bunch of flood lights, with a single mesh containing all of brightly glowing areas (which would just be flat squares). Using `DIRECTION = NORMAL` all lights generated from that mesh would automatically align with the direction each square is facing. This is how those flood lights on Brands Hatch are set:

<a href="https://i.imgur.com/21aE7zP.jpg"><img src="https://i.imgur.com/21aE7zP.jpg" width="400" ></a>

There are also a couple of parameters to tweak that alignment (and these are the default values):

```ini
DIRECTION_ALTER = 0, 0, 1
DIRECTION_OFFSET = 0, -0.4, 0
```

Value of `DIRECTION_OFFSET` would simply be added to the resulting direction, skewing it slightly. `DIRECTION_ALTER`, on the other hand, sort of re-orients the whole thing. With `DIRECTION_ALTER = 0, 0, -1` lights would be turned 180° and work backwards, with `DIRECTION_ALTER = 1, 0, 0` lights would turn 90° along vertical axis, with `DIRECTION_ALTER = 0, 1, 0` 90° along horizontal axis.

### Syntax for both light series and regular lights with their default values

```ini
[LIGHT_..., LIGHT_SERIES_...]
ACTIVE = 1
DESCRIPTION = my light

; Shape
SPOT = 120  ; or 0 by default for line lights
SPOT_SHARPNESS = 0.3
RANGE = 40
RANGE_GRADIENT_OFFSET = 0.2

; Light
COLOR = 1, 1, 1, 40
SPECULAR_MULT = 0
SINGLE_FREQUENCY = 0
DIFFUSE_CONCENTRATION = 0.88
CONDITION = NightLights
CONDITION_OFFSET =  ; by default is not set

; How light source fades with distance (for performance reasons)
FADE_AT = 400
FADE_SMOOTH = 50

; Extra options
VOLUMETRIC_LIGHT = 0
LONG_SPECULAR = 0
SKIP_LIGHT_MAP = 0
DISABLE_WITH_BOUNCED_LIGHT = 0

; Shadows:
SHADOWS =  ; by default is not set
SHADOWS_STATIC =
SHADOWS_HALF_RESOLUTION =
SHADOWS_SPOT =
SHADOWS_RANGE =
SHADOWS_DIR =
SHADOWS_OFFSET =
SHADOWS_BOOST =
SHADOWS_CLIP_PLANE = 0.5
SHADOWS_CLIP_SPHERE = 0.5
SHADOWS_EXP_FACTOR = 20
SHADOWS_EXTRA_BLUR =
```

- Main params:
  - `ACTIVE`: set to 0 to disable a light;
  - `DESCRIPTION`: just a name of the light, shown with light outlines in debug mode;
- Shape:
  - `SPOT`: spot angle, set to 0 for point lights;
  - `SPOT_SHARPNESS`: how sharp is spot edge, with 0 brightest point is in the middle, with 1 it’s 100% bright right until the edge;
  - `RANGE`: how far light would reach, in meters;
  - `RANGE_GRADIENT_OFFSET`: at what point of light travel it would start to fade (for better look, keep it lower and instead boost light brightness);
- Light:
  - `COLOR`: light color (more about format is further down);
  - `SPECULAR_MULT`: specular intensity;
  - `SINGLE_FREQUENCY`: set to 0 for regular lights, set to 1 for something like [sodium lights](https://www.youtube.com/watch?v=O7mEBpJVJbA);
  - `DIFFUSE_CONCENTRATION`: with 1 surfaces orthogonal to direction to light would be in shadow, with 0 even surfaces facing away would be fully lit;
  - `CONDITION`: name of a [condition](tracks-conditions.md) which would control brightness and color;
  - `CONDITION_OFFSET`: if set, it would offset condition flashing;
- How light source fades with distance (for performance reasons):
  - `FADE_AT`: distance in meters at which light is fading away and has 50% of its intensity;
  - `FADE_SMOOTH`: distance for which light is fading (increase to make fading smoother);
- Extra options:
  - `VOLUMETRIC_LIGHT`: set to 1 to enable volumetric light effect (careful though, it’s pretty expensive);
  - `LONG_SPECULAR`: set to 1 to enable long speculars for wet look with Rain FX (requires SSLR; please keep it mind it wouldn’t use dynamic shadow maps, so don’t use it for lights with shadows);
  - `SKIP_LIGHT_MAP`: set to 1 to stop light from contributing to bounced light of Extra FX;
  - `DISABLE_WITH_BOUNCED_LIGHT`: if you would have a light source meant to simulate light bounce, you can use this option to make sure it’s disabled when bounced light of Extra FX is active;
- Shadows:
  - `SHADOWS`: is shadows active or not (by default, would activate shadows for any none-line light affecting track with range above 15 meters);
  - `SHADOWS_STATIC`: set to 1 to mark shadows as static (much faster);
  - `SHADOWS_HALF_RESOLUTION`: set to 1 to use shadows of reduced resolution for smoother look and better performance;
  - `SHADOWS_SPOT`: optionally override shadows spot angle;
  - `SHADOWS_RANGE`: optionally override shadows range;
  - `SHADOWS_DIR`: optionally override shadows direction;
  - `SHADOWS_OFFSET`: optional offset for shadows origin (be careful, breaks shadows with anything but low values);
  - `SHADOWS_BOOST`: shadows intensity boost, if not set, calculated automatically;
  - `SHADOWS_CLIP_PLANE`: shadows clip plane nearby (for example, if your light source is within light bulb, you wouldn’t want it to shadow everything else);
  - `SHADOWS_CLIP_SPHERE`: same, but a sphere instead of a plane;
  - `SHADOWS_EXP_FACTOR`: exponential factor for shadows;
  - `SHADOWS_EXTRA_BLUR `: set to 1 to apply extra blur to shadows.

### About splitting into groups

Both `[LIGHT_...]` with mesh and `[LIGHT_SERIES_...]` with meshes split their meshes into groups. The basic principle is simple: starting with zero groups, for each vertex, find nearest group. If it’s closer than certain distance, add it to that group. Instead, create a new group. That threshold distance can be controlled:

```ini
CLUSTER_THRESHOLD = 10  ; distance in meters
```

Minimal value is 1 meter. Please check how many lights are actually being created: lower values might spawn too many lights, and all of them take time to render.

There is also an option to apply a UV-based filter to vertices that are taken into account:

```ini
UV_FILTER_0 = 0.2, 0.1, 0.4, 0.2
UV_FILTER_1 = 0.8, 0.81, 0.1, 0.1
```

First two values define coordinates of left top corner of an area, and second two are for the size of that area. Only vertices within that area will be taken into account.

### Light Maker

There is a small app which can help you set individual lights called Light Maker. It was originally added to showcase [bounced light capabilities](https://youtu.be/R9gsC5vB1Eg?t=44), but it could be useful for setting up lights in general as well. You can copy resulting light to clipboard and paste it to the config, or copy a light from config and paste it to Light Maker (simply focus its window and press Ctrl+V).

I’ll add a more advanced editor a bit later.

### About performance

Key thing about performance is that amount of lights is not an issue in itself, the main problem comes from how many pixels on a screen are affected by how many lights. 10 lights each affecting just a few percents of a screen area are better than a single light affecting whole screen. And by "affecting" I don’t mean only "lighting up" — think of [a box encoding a light source and aligned with world coordinates](https://www.shadertoy.com/view/WdjSRK). Any pixels within that box will be affected by the light. For that reason, please keep lights smaller, and especially avoid combining wide angles and long distances, those cause that box to grow fast.

A few other tips:

- More expensive part of line light is its specular component, set it to 0 to make things faster;
- Don’t forget about `FADE_AT` and `FADE_SMOOTH`: even though distant lights wouldn’t affect that many pixels, calculating and submitting them to shader might still waste some time;
- Volumetric lights and long speculars are expensive;
- Shadows are not only expensive, but also limited in number, so it’s better to disable them where possible or switch them to static and lower resolution.

### About shadows

Shadows are only available for spot lights with an angle below 180°. If you have a light with an angle above 180°, you can get shadows by using `SHADOWS_SPOT` to override and set a smaller angle only for shadows, although it’s only applicable in rare cases where there would be no shadows outside of that `SHADOWS_SPOT`. Here is example of a such light:

<a href="https://i.imgur.com/xIqgbwj.png"><img src="https://i.imgur.com/xIqgbwj.png" width="400" ></a>

Another thing is that the higher spot light is, lower shadow quality would be:

<a href="https://gfycat.com/excellentwarmheartedarawana"><img src="https://thumbs.gfycat.com/ExcellentWarmheartedArawana-size_restricted.gif" width="400" ></a>

Dynamic shadows used in Custom Shaders Patch use exponential shadow maps approach for better filtering. This technique allows to get smooth shadows with only a single texture read, cheaply increase shadows resolution with MSAA and can handle lights with wide angles much better ([comparison with common PCF approach](https://youtu.be/zw67CyByt38?t=45)), but they do have some flaws as well, and main one is that light can leak for some distance. To counteract that, we can increase exponent factor, but it can lead to shadows losing their smoothness and to a generally nasty look:

<a href="https://gfycat.com/HugePeskyEthiopianwolf"><img src="https://thumbs.gfycat.com/HugePeskyEthiopianwolf-size_restricted.gif" width="400" ></a>

So, as usual, it’s all about compromises and finding that middle ground that would look acceptable.

Keep in mind that there are only 15 slots for high resolution shadows and 16 slots for low resolution ones, so it might be a good idea to set some lights with low resolution shadows to make sure there’ll be a free slot. If there would be way too many lights with shadows, only closest to camera ones would get shadows.

### About moving lights

You can get light to move with [animated objects](tracks-animated-objects.md):

```ini
[LIGHT_...]
RELATIVE_TO = name of a moving node
```

Please avoid enabling shadows for lights that are constantly in motion, otherwise it would lead to Custom Shaders Patch rebuilding their track shadows maps each frame, and that is a pretty costly operation. For regular lights, it’s only done once.
