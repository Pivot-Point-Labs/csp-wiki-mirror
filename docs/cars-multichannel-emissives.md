This might be a particularly long explanation, sorry. I’m not good at writing those, so I’ll explain it step-by-step, hopefully then it would be somewhat helpful.

# Part 1, what is it?

First of all, what is it for? Originally, if we wanted to make emissive mesh for a light, a dashboard indicator, braking signals and so on, we would have to make a separate glowing bit into a separate mesh. It was all right when we only used headlights, braking lights and a couple of dashboard lights, but now with Custom Shaders Patch, there are turning indicators, reverse lights, tens of new dashboard indicators and so on. Separating all those meshes is getting boring, plus it’s expensive to render, since each new mesh is a new draw call.

And that’s where multi-channel emissives come to help. Instead of separating, now a single mesh can have up to four different light-emitting areas, or up to seven for symmetrical case (allowing to bind rear, braking, reverse and both turning lights to a single mesh, for example). Or up to 25 different areas for a special case with dashboard mesh, for all those icons.

<img src="https://i.imgur.com/J06vRnH.jpg" width="240" />
<img src="https://i.imgur.com/NaoctH4.jpg" width="240" />
<img src="https://i.imgur.com/HRcDvEp.jpg" width="240" />
<img src="https://i.imgur.com/tEjn7lA.jpg" width="240" />

*All these lights are set without any mesh splitting, with a simple config, with those multi-channel emissives.*

# Part 2, new `…_emissive` shaders:

That’s where it all started: Stereo had an idea to add new `ksPerPixelMultiMap_emissive` shader, similar to `ksPerPixelMultiMap`, but with a separate `txEmissive` texture slot, used as colored mask for emissive colors. Originally, emissive color would be color of emissive parameter `ksEmissive` multiplied by diffuse color in given point. Now, there is also an extra color layer from `txEmissive`, allowing to create neat things like making only windows of buildings glow without separating them.

# Part 3, new `emChannelsMode` parameter for that shader:

This new parameter is the main part of the whole multi-channel emissive thing. Now, shader `ksPerPixelMultiMap_emissive` (and others) has got additional `ksEmissive1`, `ksEmissive2` and `ksEmissive3` channels now. They won’t change anything by default, but set `emChannelsMode` to 1 and then:

- Red channel of `txEmissive` will be used as mask for `ksEmissive`;
- Green channel will be used as mask for `ksEmissive1`;
- Blue channel will be used as mask for `ksEmissive2`;
- Alpha channel will be used as mask for `ksEmissive3`.

So if you’re working on let’s say a new car, instead of separating the mesh in pieces, you now can just draw a custom `txEmissive` and make a mask brake lights in red channel, rear lights in green, reverse in blue and turning lights in alpha, and that’s it! And you can also, of course, make it blurry or something like that, to add some nice falloff towards boundaries.

### How to use it

There are two general ways to use it.

- If you’re making new car and creating new `txEmissive` to it, easiest way might be to just install those new shaders for ksEditor and even vanilla AC as well. You can get them [here](https://github.com/ac-custom-shaders-patch/sdk-shaders) (look at `X releases` link at the top to download);
- Or, you can use config to define areas procedurally. No need for extra textures, and including `common/custom_emissive.ini` template can make it much easier to work with. But I think if you’re making a new car, creating a small `txEmissive` texture could be easier, more flexible and, possibly, produce better results.

### Mirroring

Left and right turning signals should be independant, how to fit all that in four channels? Well, those meshes are usually symmetrical, so what we can do here, we can highlight both turning lights on texture in alpha-channel (for `ksEmissive3`) and then enable a special parameter `emMirrorChannel3As4`, setting it to 1. Then, shader will use `ksEmissive4` instead of `ksEmissive3` for those pieces of mesh which are located on the right side of a car.

Another thing to consider here though: it might have a problem locating that right side of a car. It would use relative mesh coordinates, so if your mesh is aligned nicely, with X axis pointing as it should, and pivot being in the middle, it’ll work with no problems. Otherwise, you’ll have to adjust mirroring parameters. There are two of them:

- `emMirrorDir`: direction to which mirroring should occur. Set to `(1, 0, 0)` for default right-left mirroring. But again, that direction is relative to mesh orientation (first value is for X, second for Y and third for Z);
- `emMirrorOffset`: offset for mirroring. For example, that piece of dashboard with left/right turning lights might need a value like 0.5 here, so mirroring plane would go in-between the indicators.

### Other parameters

- `emSkipDiffuseMap`: set to 1 to not take diffuse color into account when calculating emissive color. With it, you can make black surfaces glow! And, of course, you can use it with `emChannelsMode` set to 0 as well, so `txEmissive` will set color.
- `emAlphaFromDiffuse`: by default shader will take alpha from `txNormal`, acting similar to `ksPerPixelNM`. With this parameter set to 1, it will instead take alpha from `txDiffuse`.

### How to use those channels in config

For tracks, as you might imagine, it’s as straightforward as it can be. Just use a different variable name in your `MATERIAL_ADJUSTMENT` section:

```ini
[MATERIAL_ADJUSTMENT_...]
MESHES = windows
CONDITION = WINDOWS_GLOW_1
KEY_0 = ksEmissive1
VALUE_0 = 10, 10, 5, 1

[MATERIAL_ADJUSTMENT_...]
MESHES = windows
CONDITION = WINDOWS_GLOW_2
KEY_0 = ksEmissive2
VALUE_0 = 10, 10, 5, 1

; if conditions are different, various windows will turn on at different times
```

Cars usually use `[EMISSIVE_...]` sections, those now have a new parameter for this thing:

```ini
[EMISSIVE_HIGHBEAM_...]
NAME = GEO_Frontlight_Inner_Glass
COLOR = 400, 330, 280, 0.2
CHANNEL = 1  ; default value is 0 for ksEmissive; here 1 is used for ksEmissive1
LAG = 0.8
LOCATION = FRONT
```

As for `BOUND_TO` value for cars, linking lights to emissives, you can link to a certain channel like so:

```ini
[LIGHT_EXTRA_...]
BOUND_TO = GEO_Frontlight_Inner_Glass:1
```

### Intermission

This is it! If you’re making your own car, you can stop here, just draw `txEmissive` with masks in different channels and set it in ksEditor, and it’ll work just fine. Nice and easy.

There is more to it though, that’s why I’m splitting in in parts. For those of us who don’t want to draw textures and would like to set it all with a few lines of config, like me. There is also a bonus of being able to set things like turning lights much faster, or to use that up-to-25-emissives-per-mesh thing.

# Part 4, `custom_emissive.ini` for masking:

Sometimes it’s not really suitable to draw `txEmissive`. For example, if it’s a config for already existing car. For that, shader has a bunch of options to operate without that texture, using various types of areas as masks instead. But to work faster, shader expects those options to arrive in a certain precomputed form, and it would be wasteful to precompute them by hand. That’s where [INIpp](https://github.com/ac-custom-shaders-patch/inipp) comes to the rescue, with a bunch of templates ready to do most of the work.

To use those templates, start by including the file with them:

```ini
[INCLUDE: common/custom_emissive.ini]
```

*This file is available for both cars and tracks, although from now, I’m going to mainly describe cars. Tracks are the same, but simpler.*

And then, you can use it like so:

```ini
[CustomEmissive]
Meshes = turning_lights
Resolution = 1024, 1024
@ = CustomEmissive_Rect, Channel = 3, Mirror, Start = "10, 865", Size = "480, 165"
@ = TurningLightsFront, Channel = 3
```

This particular section is all it takes to set front turning lights on Peugeot 504 (not quite, it’s simplified here for an example), both emissive part and light sources. Now, let’s go line by line:

- `[CustomEmissive]`: this is how with INIpp, templates are used. This thing will unwrap itself to a new `[SHADER_REPLACEMENT_...]` section, replacing shader, filling missing textures and setting all basic parameters like, for example, setting `emMirrorDir` to default `(1, 0, 0)`.

- `Meshes = turning_lights`: sets list of meshes to replace shader of. You can use several meshes if needed. Here is one trick: set it for differently named meshes across different LODs:

  ```ini
  Meshes = '{ lod:A & turning_lights_lodA, lod:B & turning_lights_lodB }
  ```

- `Resolution = 1024, 1024`: texture resolution in pixels, width and height. Optional parameter. Without it, any sizes, coordinates and dimensions should be set in relative coordinates, from 0 to 1.

- `@ = CustomEmissive_Rect, …`: by default with `[CustomEmissive]`, nothing will glow, as if `txEmissive` is fully black. That line defines a new area for third channel, going from (10, 865) px, with the size of 480×165 px. Area is also set as mirrored, so everything on the right side of the car in that area will actually be fourth channel.

  If you wonder about strange syntax, this is how mixins can be used with INIpp (`@` is a short form for `@MIXIN`). Mixings are just a bunch of extra values for a section, so they can be declared once and then used again and again. In this case, mixin is called “CustomEmissive_Rect”: you can open “custom_emissive.ini” and find it there.

- `@ = TurningLightsFront, …`: and this is a short form for all the `[EMISSIVE_...]` and `[LIGHT_...]` for turning lights! Saves so much time writing it like that. It will automatically set color, light source and everything else. And `Channel = 3` tells it to bind those turning lights to third and fourth channel (turning lights mixin is aware it would only make sense with mirrored channels, so by default it takes both, main and mirrored). Behavious like that are described in more detail in part 5.

Two more things before we dive in:

- You can [search through this repo for already prepared configs](https://github.com/ac-custom-shaders-patch/acc-extension-config/search?q=custom_emissive&unscoped_q=custom_emissive) and use them as an example as well. Also, of course, feel free to load them in AC and mess around with parameters.

- I recommend to use something more advanced for editing configs than regular notepad. My personal favourite at the moment is [Visual Studio Code](https://code.visualstudio.com/), free and with a lot of extensions. Install [this one](https://marketplace.visualstudio.com/items?itemName=acarreiro.calculate), bind it to some hotkey and you’ll be able to calculate selected text right here without needing to copy it to some calculator. Not that it’s needed often, but when it is needed, saves quite a lot of time.

### Basic `[CustomEmissive]` parameters

- `Debug` (default value is 0.0): increase to add different colored emissive values to different channels, to see what’s what;
- `MirrorDir` (default value is `(1, 0, 0)`): sets direction for mirroring;
- `MirrorOffset` (default value is 0.0): sets offset for mirroring;
- `CompatibleWithPBRGlass` (default value is 0): set to 1 to make the whole thing compatible with `[Material_Glass]`;

### Extra helpful mixins for `[CustomEmissive]`

- `@ = CustomEmissive_SkipDiffuseMap`: skips diffuse map, setting `SkipDiffuseMap` to 1.

- `@ = CustomEmissive_UseDiffuseLuminocity`: particularly helpful mixin, allows to apply diffuse texture not as color mask, but as black-and-white mask, and with different logic, more like a threshold. For example, it could allow to stop any emissive at all if texture is darker than 10%.

  Parameters:
  - `SkipDiffuseMap` (default value is 1): if 1, regular colorized contribution from diffuse map will be disabled;
  - `From` (default value is 0.0): minimum diffuse brightness, anything below that won’t be emissive at all, from 0 to 1;
  - `To` (default value is 1.0): maximum brightness, everything above that would be 100% bright, from 0 to 1;
  - `Exponent` (default value is 1.0): gamma to adjust how gradient works between `From` and `To`, goes from 0 to ∞;
  - `Opacity` (default value is 1.0): contribution of this particular stage, with 0 it’s as if mixin is not here, goes from 0 to 1;
  - `Mask` (default value is `(1, 1, 1, 1)`): which channels should it affect;

  If needed, `From`, of course, can be bigger than `To`, so it would be as if diffuse texture is inverted. Also, `From`, `To`, `Exponent` and `Opacity` could use not a single, but four numbers, for different parameters to different channels.

  Used almost everywhere, example from Pagani Huayra config, where it’s used for dashboard indicators:

  ```ini
  @ = CustomEmissive_UseDiffuseLuminocity, Mask = "0, 1, 1, 1", Exponent = 4, From = 0.1, To = 0.3
  ```

- `@ = CustomEmissive_UseDiffuseAlpha`: absolutely the same as `CustomEmissive_UseDiffuseLuminocity`, but for diffuse alpha instead of luminocity.

- `@ = CustomEmissive_MirrorUV`: mirror UV, flipping it across a symmetry line if it’s on the wrong side (could be helpful in some very tricky cases).

  Parameters:
  - `Direction` (default value is `(1, 0)`): direction of mirroring, orthogonal to symmetry line;
  - `Offset`: offset either in pixels or coordinates, depending on if `Resolution` is set or not.

  Used in Pagani Huayra config:

  ```ini
  @ = CustomEmissive_MirrorUV, Offset = 612, Direction = "-1, 0" ; this trick allows to set six dashboard indicators
  ```

- `@ = AlphaFromTxDiffuse`: sets `emAlphaFromDiffuse` to 1, to use alpha-channel from txDiffuse.


### Procedural masks

There are three main types of masks. You can define one area of each type for each channel. Channels go from 0 to 3, all channels except 0 could be marked as mirrored.

Types are:

- Color masks.

  Those are easiest to use, if texture allows for that. For example, most masks for turning lights can be set like that:

  ```ini
  @ = CustomEmissive_Color, Channel = 3, Mirror, Color = "1, 0.5, 0"
  ```

  Where `(1, 0.5, 0)`, of course, means orange color: 100% red, 50% green, 0% blue. As you can imagine, `Color` parameter is required. Other parameters available:

  - `ThresholdLevel` (default value is 0.95): higher parameter is, more closely texture color would have to match `Color` set in this mask. Goes from 0 to 1.

  - `ThresholdSharpness` (default value is 20.0): reduce to make mask smoother, increase to make it sharper. Goes from 0 to ∞, although, I think, sane values would be somewhere from 1 to 50.

  - `Threshold`: simple alias for both `ThresholdLevel` and `ThresholdSharpness`, takes two values, first is `ThresholdLevel`.

  - `Normalization` (default value is 1.0): if this value is 1, brightness is not taken into account, only hue and saturation are compared. With 0, on contrary, color should match perfectly, all hue, saturation and brightness. And you can set a value somewhere in-between two. While it works well for turning lights — sometimes orange might get darker, but it’s still turning lights orange — for things like reverse lights, it’s better to reduce this value, so only white would match, but not dark gray areas.

    Here is how reverse lights for Peugeot 504 are set with it:

    ```ini
    @ = CustomEmissive_Color, Channel = 0, Color = "1, 1, 1", Normalization = 0.5, Threshold = "0.8, 1"
    ```

  - `Opacity`: this value goes from 0 to 1, altering intensity multiplier of resulting area.

  There is also global parameter `ColorInputBlur` (default value is 0.0) for `[CustomEmissive]`, allowing to blur diffuse texture before passing it through color masks. It won’t affect anything else.

- Rectangular areas with possibly rounded corners and blurred edges.

  Custom Shaders Patch adds a new app in AC, called Object Inspector. In its textures tab, it has those small checkboxes on the right side of textures list. Click one to see the texture, and then use mouse button to quickly highlight the area. This is the simplest way to get those coordinates and size. Or, you can use things like Photoshop or [XnView (free image viewer)](https://www.xnview.com/en/xnviewmp/) to get those coordinates. And in some other cases, when mapping is extra bad, it’s easier to simply guess proper coordinates by dividing values in half and then in half and so on, switching to other half if are gets lost. This trick helps to narrow it down much faster.

  **Please note:** if you’re using coordinates in pixels, set `Resolution`. If you’re using 0…1 coordinates, do not set `Resolution`. You can use `Resolution` as a parameter for `CustomEmissive_Rect` too, to localize its effect.

  Here are rear turning lights for Abarth 595:

  ```ini
  @ = CustomEmissive_Rect, Channel = 1, Mirror, Start = "0, 264", Size = "206, 142", CornerRadius = "0.25, 0.5"
  ```

  `Start` and `Size` are required, although you can use `Center` instead of `Start` to set coordinates of center point instead of top left corner (makes it easier to tweak size). Other parameters available:

  - `CornerRadius` (default value is 0.0): one or two parameters, if two, first is for horizontal part, second is for vertical. Set it to 1.0 and rectangle will turn into a circle. If you have a rectangle with dimensions like `(400, 100)`, then for rounded corners to be properly rounded, not stretched, horizontal value would have to be four times smaller, like `CornerRadius = "0.1, 0.4"`. This value also allows to set blurry edges: only way to get blurry edges here is to use rounded corners.

  - `Exponent` (default value is 1.0): simple way to tweak sharpness/blurryness for blurry edges and rounded corners. Goes from 0 to ∞, sane values would be from 0.1 to, maybe, 10. Smaller value is, sharper is the edge.

  - `Opacity`: this value goes from 0 to 1, altering intensity multiplier of resulting area.

  There are also some aliases available, with predefined parameters:

  - `CustomEmissive_Area`: exactly the same thing, kept for backwards compatibility;
  - `CustomEmissive_Circle`: circle, same, but has `CornerRadius = 1` and `Exponent = 0.1` as default values, `Exponent` can be redefined;
  - `CustomEmissive_CoverAll`: area covering the whole texture, for some special cases.

- Quadrilateral areas defined by four corner points.

  Similar to rectangular areas, to quickly set them up, you can use Object Inspector. Hold Ctrl and click four times to mark an area. And, same note about resolution also applies here.

  Those are more expensive to calculate, so I think it’s better to use them if nothing else helps.

  Here are rear turning lights for Peugeot 504:

  ```ini
  @ = CustomEmissive_Poly, Channel = 3, P1 = "390, 500", P2 = "350, 840", P3 = "-20, 840", P4 = "-20, 500", Exponent = 3, Sharpness = 50
  ```

  All four points, `P1`…`P4`, are required. Other parameters available:

  - `Sharpness` (default value is 1000.0): how sharp is the edge, goes from 0 to ∞.

  - `Exponent` (default value is 1.0): simple way to tweak gradient for non-sharp edge. Goes from 0 to ∞, sane values would be from 0.1 to, maybe, 10. Smaller value is, sharper is the edge.

  - `Offset` (default value is 0.0): sort of glows (or shinks) area, allowing to add round corners. You would have to reduce size for round corners to work though. Goes from -1.0 to 1.0.

  - `Opacity`: this value goes from 0 to 1, altering intensity multiplier of resulting area.

### Additional vertex masks

For some extra mind bending cases, there is a fourth option, vertex masks. Sometimes, rarely, there might be a particularly nasty mesh with no unique UV mapping. Can’t really do much with those, but with `CustomEmissive_VertexMask`, it’s possible to define up to a four points, one for each channel. The way it would work, shader will find a point given piece of mesh is closer to and use corresponding channel in there. You would need to use something like `StartWithWhite = 1` or `@ = CustomEmissive_CoverAll` on top of that for both channels, so it would cover everything and then get limited by `CustomEmissive_VertexMask`. If point for channel is not defined in `CustomEmissive_VertexMask` parameters, that channel won’t be affected. Example for rear turning lights of Mustang 2015:

```ini
@ = CustomEmissive_VertexMask, Point2 = "0.52, 0, 0", Point3 = "0.8, 0, 0"
```

Points are set in mesh coordinates, I find it quickest to just try and guess those values.

### How masks are applied step by step, and how it could be changed

How much trouble instead of just making a texture, heh. And there is more. Different types of masks can combine in different ways. To visualize it, keep it mind how the whole thing is calculated, step by step:

- First, shader takes base value, by default 0: nothing would glow.

  - It can be changed to 1 with `StartWithWhite = 1`: then, everything would glow.

- Then, it calculates those rectangular areas. By default it would add those to the result, meaning `StartWithWhite = 1` would make color masks useless.

  - Add `AreasSubtractive = 1` and it would instead subtract areas from base value. I used this trick for dials of BMW E30, to give them this nice glow fading to middle: those are just four blurry circles which are inverted with this option:

    <a href="https://i.imgur.com/I6QzTGZ.jpg" target="_blank"><img src="https://i.imgur.com/I6QzTGZ.jpg" width="240" /></a>
    <a href="https://i.imgur.com/K978ZQK.jpg" target="_blank"><img src="https://i.imgur.com/K978ZQK.jpg" width="240" /></a>

- After that, it calculates color masks. Again, it would add those by default.

  - Add `ColorMasksSubtractive = 1` for subtracing color masks;
  - Or, add `ColorMasksAsMultiplier = 1` and color masks will be applied as multiplier — that one I use often, for setting general shape with rectangular area and then using color mask on top to make it less solid colored:

    <a href="https://i.imgur.com/eqGnTaT.jpg" target="_blank"><img src="https://i.imgur.com/eqGnTaT.jpg" width="240" /></a>
    <a href="https://i.imgur.com/LJIP2gk.jpg" target="_blank"><img src="https://i.imgur.com/LJIP2gk.jpg" width="240" /></a>

- Next step, it calculates quadrilateral masks. Similar thing.

  - Add `PolysSubtractive = 1` for subtracing;
  - Or, add `PolysMasksAsMultiplier = 1` for it to act as multiplier. This is how this part set, it uses color, rectangular and quadrilateral masks, since those lights are not common “here is a piece of texture for reverse lights” type (original AC look is on the left side):

    <a href="https://i.imgur.com/FpMZ4uc.jpg" target="_blank"><img src="https://i.imgur.com/FpMZ4uc.jpg" width="240" /></a>
    <a href="https://i.imgur.com/J06vRnH.jpg" target="_blank"><img src="https://i.imgur.com/J06vRnH.jpg" width="240" /></a>

- After, vertex masks. They are multiplicative by default, other options are available:

  - Add `VertexMaskAdditive = 1` to set them in additive mode;
  - Or, add `VertexMaskSubtractive = 1` to set them in subtractive mode;

- And, for last step, it would apply masks based on diffuse luminocity or alpha, set by `@ = CustomEmissive_UseDiffuseLuminocity` or `@ = CustomEmissive_UseDiffuseAlpha`.

### Overlapping or not overlapping masks

Another thing, you can change how masks interact with each other. By default, all masks are acting separately, meaning they can overlap, and one area can act as both, let’s say, turning light and reverse light. In some specific cases though, it’s handy to be able to change this behaviour with those settings:

- `AreasSubtractNext = 1`;
- `ColorSubtractNext = 1`;
- `PolySubtractNext = 1`.

They do pretty much what they say: for example, with `AreasSubtractNext = 1`, area covered by rectangular mask in second channel won’t be affected by rectangular mask in first channel even if it’s covering the entire texture. For example, I used it for rear turning lights of Peugeot 504:

```ini
[CustomEmissive]
PolySubtractNext = 1
@ = CustomEmissive_Poly, Channel = 0, P1 = "0, 0", P2 = "1024, 0", P3 = "1024, 1024", P4 = "0, 1024" ; reverse lights covering everything
@ = CustomEmissive_Poly, Channel = 1, P1 = "133, -10", P2 = "178, 328", P3 = "600, 328", P4 = "600, -10" ; apart from an area with turning lights
```

### Rectangular areas as one general mask

You saw that E30 dashboard, right? With that smooth circular backlit, [a few paragraphs ago](https://i.imgur.com/I6QzTGZ.jpg)? It wouldn’t really work like that: if those areas would be set in subtractive mode, they would only subtract area for a certain channel. Well, there is another option to change that: `UseAreasAsMask = 1`. With it, rectangular areas will be used as a simple mask for the whole thing. And there is another mixin to make using it even simpler, `@ = CustomEmissive_AreaMask`. You don’t even need to set channels with it, just use it up to four times to mask whole emissive thing. And it sets `StartWithWhite` and `UseAreasAsMask` automatically. So here is actual E30 config:

```ini
[CustomEmissive]
Meshes = INT_DIALS_SUB0
AreasSubtractive = 1
@ = CustomEmissive_AreaMask, Center = "0.723, 0.273", Size = 0.55, CornerRadius = 1, Exponent = 0.3
@ = CustomEmissive_AreaMask, Center = "0.275, 0.6", Size = 0.55, CornerRadius = 1, Exponent = 0.3
@ = CustomEmissive_AreaMask, Center = "0.116, 0.117", Size = 0.23, CornerRadius = 1, Exponent = 0.3
@ = CustomEmissive_AreaMask, Center = "0.361, 0.117", Size = 0.23, CornerRadius = 1, Exponent = 0.3
```

Depths I’m willing to goto to avoid opening an image editor and draw a simple texture… 😅

# Part 5, `custom_emissive.ini` for behaviour:

I’d like to start by saying, what I would really like to see more of is some standardization. Let’s keep things similar, and here I’m talking about things like parameters of light sources for turning lights, or emissive intensity for reverse lights. If you don’t think they look right, let me know, and let’s discuss it and change default settings Custom Shaders Patch uses. Or, maybe it’s your post processing filter not having enough bloom (like Sol filter) — I think sometimes it might happen, and in that case, without standardization, you might accidentally set it too bright.

So here is where `custom_emissive.ini` comes in for that. It basically has a bunch of shortcuts for setting up those things easier, with ready-to-use values. You can still adjust it, of course, including intensity, but I hope you would consider keeping as many things by default as possible.

All behavious are defined in mixins. You can attach them to `[CustomEmissive]` or not, we’ll come to that a bit later. All of them have these parameters, and, as I said before, I hope you don’t really need to change most of them:

- `Color`: color for emissive, brightest value about 25 for exterior and 20 for interior lights;
- `Channel` (default value is 0): channel to attach behaviour to;
- `Intensity` (default value is 1.0): brightness multiplier;
- `Lag`: smooth switching on and off;
- `Location`: light location for damages to work, guessed properly in almost all cases;

For behavious that could cast light, such as turning or reverse lights, or open door light:
- `NotCastingLight` (default value is 0): set to 1 for emissives which shouldn’t cast light (mainly for cases where you would have things like secondary set of turning lights in front);
- `Direction`: light direction, three numbers for a vector;
- `Offset`: offset in meters for guessed position of light source;

### Turning lights

As trickiest, there are quite a few ways to set them:

- `@ = TurningLightsFront`: front turning lights;
- `@ = TurningLightsFrontCorner`: front turning lights located on corners, shining more sideways;
- `@ = TurningLightsRear`: rear turning lights;
- `@ = TurningLightsRearCorner`: rear turning lights located on corners, shining more sideways;
- `@ = TurningLightsRearCombined`: front and rear turning lights for those cases where it’s a single mesh for all (not recommended since damages won’t work properly, in most cases you could still split it with different channels anyway);
- `@ = TurningLightsRearCornerCombined`: front and rear turning lights located on corners, shining more sideways;
- `@ = DashTurningLights`: dashboard indicators for turning lights, of course, not casting light.

Turning lights have some special parameters too:

- `ChannelAlt`: channel for right side, by default is guessed from `Channel`, but could be set manually;
- `AnimatedDoors`: for turning lights on door mirrors, set left and right door names in here;
- `HeadlightsIntensity`: emissive intensity with turning lights off, but headlights on;
- `BrakingLightsIntensity`: emissive intensity with turning lights off, but brakes on.

### Other lights

- `@ = Headlights`;
- `@ = ParkingLights`: the ones at the back active with headlights;
- `@ = BrakingLights`;
- `@ = ReverseLights`;
- `@ = FogLights`: front lights bound to Extra A button;
- `@ = OpenDoorLight`: light for when doors are open;
- `@ = LicensePlateLights`: don’t produce any light, for those glowing bits next to license place (license plate light works separately anyway);

More types and options will be added soon.

### Dashboard lights

All dashboard lights mixins are based on `@ = DashIndicator` mixin, with these parameters:

- `Input`: input [from this list](cars-instruments-inputs.md);
- `InputThreshold`: if input is a number, that’s the threshold after which, indicator will glow;
- `InputInverse`: set to 1 to inverse threshold logic;
- `InputSelector`: alias for `INPUT_SELECTOR`;
- `OffColor`: color for disabled indicator;
- `Invert`: swaps on and off states;
- `DashHighlight`: use `DashHighlightColor` (defined as parameter for main `[INCLUDE]`) for inactive indicator, but turned on lights.

Here is how you can use it:

```ini
[CustomEmissive]
Meshes = polymsh118_SUB17
Resolution = 1024, 512
@ = CustomEmissive_Circle, Channel = 2, Mirror, Center = "811, 446.5", Size = 30, Exponent = 0.3
@ = DashIndicator, Input = HANDBRAKE, Channel = 2
```

By default, color will be guessed automatically based on input. Other dashboard lights mixins to speed up setting it up:

- `@ = DashHighlight`: simple dashboard highligh;
- `@ = DashWarningABS`: warning for disabled ABS;
- `@ = DashWarningTC`: warning for disabled traction control;
- `@ = DashWarningCollision`: warning for damaged car;
- `@ = DashWarningAirbag`: warning for used airbag (triggered by major collision);
- `@ = DashWarningEngine`: warning for damaged engine;
- `@ = DashWarningTemperature`: temperature warning;
- `@ = DashWarningTyrePressure`: tyre pressure warning (with `Pressure` parameter for threshold, default is 20);
- `@ = DashWarningSeatbelt`: seatbelt warning (triggered by open door and hidden driver);
- `@ = DashInteriorLight`: indicator for interior lights (triggered by open door);
- `@ = DashEmissiveDisplay`: always on no matter what;
- `@ = DashFogLights`: fog lights indicator, triggered by Extra A button;
- `@ = DashWarningSteering`: damaged steering warning, not doing anything for now, will be changed in the future.

# Part 6, `custom_emissive.ini` for 25 dashboard indicators in a single mesh:

An alternative to `[CustomEmissive]`, `[CustomEmissiveMulti]`. It uses a different shader with fewer options. Of all things, it only has rectangle areas, but it has 25 of them! Very useful for dashboards.

Here is an example of how it could be used:

```ini
[CustomEmissiveMulti]
Meshes = LIGHT_DASH         ; target mesh
Resolution = 1024, 512      ; texture resolution for coordinates to work
UseEmissive0AsFallback = 1  ; use ksEmissive (aka emissive channel #0) for glow everywhere untouched by other areas
@ = DashHighlight           ; bind dashboard highlight to emissive channel #0
@ = MultiItem, Role = TURNSIGNAL_LEFT, Center = "508, 246", Size = 30
@ = MultiItem, Role = TURNSIGNAL_RIGHT, Center = "1004, 246", Size = 30
@ = MultiItem, Role = LIGHT, Center = "504, 279", Size = 30
@ = MultiItem, Role = HIGHBEAM, Center = "508, 310", Size = 30
@ = MultiItem, Role = HANDBRAKE, Center = "1002, 313", Size = 30
@ = MultiItem, Role = ABS_INACTION, Center = "1006, 281", Size = 30
@ = MultiItem, Role = STALLED, Center = "582, 97", Size = 30
@ = MultiItem, Role = DashWarningABS, Center = "983, 377", Size = 30
@ = MultiItem, Role = DashWarningSeatbelt, Center = "559, 120", Size = 30
@ = MultiItem, Role = DashWarningTemperature, Center = "997, 208", Size = 30
@ = MultiItem, Role = DashWarningEngine, Center = "970, 150", Size = 32
@ = MultiItem, Role = DashWarningCollision, Center = "524, 178", Size = 32
```

Notice how now there is no need to first define an area and then attach a behaviour to it, it’s all done in a single line. Plus, notice `Role`: it could either be an input from [the list](cars-instruments-inputs.md), or a dashboard light mixin from part 5.

Also, there is no need to track emissive channels: mixin “MultiItem” automatically counts everything and sets it. You can use up to 24 of those “MultiItem” mixins, and then, if needed, set a shape for channel #0 instead of using `UseEmissive0AsFallback`.

Just as a reminder, you can use Object Inspector to quickly find out coordinates for those areas. Saves massive amount of time.

### Other options

- `UseEmissive0AsFallback` (default is 0): set to 1 to use everything untouched by other items as mask for channel #0, or set to `COVER_ALL` for channel #0 to affect everything;
- `SkipEmissiveMap` (default is 1): skip emissive map completely;
- `Debug`: highlight different areas with different colors.

And one last tip: you can use `@ = CustomEmissive_UseDiffuseLuminocity` and `@ = CustomEmissive_UseDiffuseAlpha` here as well, but unlike with `[CustomEmissive]`, where it could use up to four values for different channels, here it’s limited to two values. First is applied to last 24 channels used for indicators, and second value is applied to channel #0, usually used as backlit. For example, here is a dashboard for Abarth 500:

```ini
[CustomEmissiveMulti]
Meshes = LIGHT_DASH
UseEmissive0AsFallback = 1
Resolution = 1024, 512
@ = CustomEmissive_UseDiffuseLuminocity, From = "0.0, 0.2", To = "0.1, 0.3", SkipDiffuseMap = 0
@ = DashHighlight
@ = MultiItem, Role = TURNSIGNAL_LEFT, Center = "508, 246", Size = 30
@ = MultiItem, Role = TURNSIGNAL_RIGHT, Center = "1004, 246", Size = 30
@ = MultiItem, Role = LIGHT, Center = "504, 279", Size = 30
@ = MultiItem, Role = HIGHBEAM, Center = "508, 310", Size = 30
@ = MultiItem, Role = HANDBRAKE, Center = "1002, 313", Size = 30
@ = MultiItem, Role = ABS_INACTION, Center = "1006, 281", Size = 30
@ = MultiItem, Role = STALLED, Center = "582, 97", Size = 30
@ = MultiItem, Role = DashWarningABS, Center = "983, 377", Size = 30
@ = MultiItem, Role = DashWarningSeatbelt, Center = "559, 120", Size = 30
@ = MultiItem, Role = DashWarningTemperature, Center = "997, 208", Size = 30
@ = MultiItem, Role = DashWarningEngine, Center = "970, 150", Size = 32
@ = MultiItem, Role = DashWarningCollision, Center = "524, 178", Size = 32
```

There was a problem with some indicators on texture which are not being used (some are unknown to me, some are not yet supported), which were annoying glowing out of nowhere. By using 0.2/0.3 as thresholds for dashboard highlight, I could stop them from glowing on their own in disabled state:

  <a href="https://i.imgur.com/Gi7wOIa.png" target="_blank"><img src="https://i.imgur.com/Gi7wOIa.png" width="240" /></a>
  <a href="https://i.imgur.com/kNvWvbI.png" target="_blank"><img src="https://i.imgur.com/kNvWvbI.png" width="240" /></a>

### Conclusion

If you read all the way through here, I’m surprised and impressed, and if not, I completely understand. Considering how bad I am at writing things in English (writing this took me at least four hours), I hope at least 1/3 of it made any sense… If you have any suggestions on how to rewrite it to make it easier to understand, please let me know.
