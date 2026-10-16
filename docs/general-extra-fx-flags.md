Extra FX is another extension for Custom Shaders Patch adding a lot of screen-space effects based on depth and normals information of the scene, such as local reflections, SSAO, bounced light, volumetric headlights or temporal anti-aliasing. For the whole thing to function, it needs to render the scene second time (before main rendering pass), to prepare normal buffer and extra data like motion buffer for motion blur, or reflections info for SSLR.

# About non-transparent transparency and windows

The way those effects implemented here, to deal with car windows and similar surfaces, almost all of those transparent surfaces are being rendered in those Extra FX buffers, so they appear opaque. One exception is car windows from the inside, by default they won’t be rendered in Extra FX buffers and they even will be excluded from main rendering pass, and drawn only after Extra FX effects are applied. This way, as you can imagine, they’ll cover all the effects, but it’s generally a preferred behaviour for interior shots.

As an example, here is the scene:

[![Original shot](https://i.imgur.com/XT3669h.jpg)](https://i.imgur.com/XT3669h.jpg)

And here is how it looks in Extra FX buffers:

[![AO and bounced light](https://i.imgur.com/Hv9Olci.jpg)](https://i.imgur.com/Hv9Olci.jpg)
[![Local reflections](https://i.imgur.com/Kh9H7R8.jpg)](https://i.imgur.com/Kh9H7R8.jpg)

Because of that, Extra FX doesn’t affect anything behind the glass, and reflection of windows might look strange, but notice how side mirror is being reflected in side window, and at the same time, side window is being reflected in side mirror. Compare it with reflections in Mafia 3:

[![Screenshot from https://mafiagame.com/](https://i.imgur.com/QmyW1rs.jpg)](https://i.imgur.com/QmyW1rs.jpg)

Now, to the point. Sometimes you might like to override that behaviour. Some popup instruments over the windscreen getting motion blurred wrongly, or some headlights glass which would really need some local reflections underneath it, what not. And you can do that with extension config, as usual:

```ini
[EXTRA_FX]
DELAYED_RENDER = ...  ; all parameters are lists of meshes
SKIP_GBUFFER = ...
MASK_GBUFFER = ...
BLEND_GBUFFER = ...
AUTOFIX = 1   ; 1 is a default value
```

One thing though is that you have to be very careful with these ones. As the most things in that area, everything here is a bunch of hacky compomises. Different cases might need different solutions.

- `DELAYED_RENDER`: simply skip mesh from Extra FX and draw it after Extra FX was applied. Good for things like popup instruments in cars, the ones over dashboard over windscreen.

  Please keep in mind that as those meshes are rendered separately, they won’t get similar lighting tweaks as car would do. Masking for interior reflections won’t work on them either. And with TAA enabled, they won’t get MSAA even if it’s enabled in settings. So, really, not a great option for most cases.

- `SKIP_GBUFFER`: skip mesh from Extra FX while still rendering it in main render pass as usual. Might work well for something so transparent it’s almost invisible in most cases, like glass over dashboard instruments (and that glass would still get interior reflections masked properly).

  But, if skipped mesh is not quite as transparent, it might look pretty bad:
  [![Porsche 911 4.0 by Singer, made by Ben O'Bro, Arch](https://i.imgur.com/s82OVvN.png)](https://i.imgur.com/NpPaIOJ.jpg)

  Notice how reflection of something behind the glass appears as if it’s in front of it.

- `MASK_GBUFFER`: newly added and still somewhat experimental option, but I believe it should work for most cases where `SKIP_GBUFFER` fails.

  Instead of skipping mesh completely, it’s still being rendered in Extra FX buffers, but in a completely different way, dimming down reflections for SSLR to take that into account. It would still produce artifacts with things like SSAO, but in general those are much less noticeable comparing to SSLR when talking about things like headlights glass. Compare it yourself:
  [![Click to see full screenshots](https://i.imgur.com/L1B3mmh.png)](https://i.imgur.com/LfX4osB.jpg)

- `BLEND_GBUFFER`: option for overlays which should only slightly change some properties like reflection strength while not chanding shape of underlying surface at all. Useful for stickers if those need to blend with some smooth gradient.

- `AUTOFIX`: adds some auto-guessing for these flags, like marking grooves for tracks.

# About motion blur and TAA

There are a few problems with those ones too, with options to tweak the behaviour.

```ini
[EXTRA_FX]
ROTATING_FILTER = ...  ; all parameters are lists of meshes too
MOVING_FILTER = ...
GLASS_FILTER = ...
```

- `ROTATING_FILTER`: mark node as rotating, so rotation would get ignored when doing motion blur and TAA. No need to add it to things like needles, but if you have something like fast spinning fan looking all glitchy, this is the solution. Wheels are being added in here by default.

  <details><summary>Why is that?</summary>

  To do motion blur, shader needs to know a direction (and speed) at which pixel has moved since the last frame. Imagine an area of the spinning wheel:

  [![Oh my](https://i.imgur.com/FFObVa6.png)](https://i.imgur.com/FFObVa6.png)

  It was in point A last frame, it’s in point B now, but simple subtraction gives shader a completely wrong movement direction! So if it would to blur stuff like that, wheel would look very unfortunate, somehow leaking in and out at the same time. I couldn’t find out how big guys deal with it yet (one way could be to keep second to last frame and do some clever curve interpolation, but motion blur shader is crazy expensive as it is), and at least ignoring rotation completely stops it from looking insane.

  </details>

- `MOVING_FILTER`: one recently added improvement for TAA is that now it would compare the objects to reduce ghosting. By default Custom Shaders Patch marks whole car as moving entity, but if, for example, you want to reduce ghosting for analog instruments, list them here, and they would marked as something moving separately. For cars, default value is `ARROW_?, STEER_?, SHIFT_?`.

- `GLASS_FILTER`: another option for TAA, for switching surface to fast response mode. TAA would pay less attention to previous frames thus increasing reaction speed, at the cost of possible increase in aliasing. Great for things like digital instruments (glass on top or surface behind), navigator screens or some windows, if camera moving pass produces too much ghosting for stuff behind windows.

You can use debug stencil view in Extra FX debug app to check what mesh is marked like what. Bright purple areas are fast response ones.

# About semi-transparent Grass FX

By default procedural grass from Grass FX is not being rendered in G-buffer, thus cutting time almost in half. On most tracks with low grass and matte surfaces, it’s perfectly fine, however on some with either high grass or reflective surface behind it (like water), grass seems glitch and transparent. To fix that, use:

```ini
[EXTRA_FX]
FORCE_GRASSFX_GBUFFER_PASS = 1
```

There is also an option in Extra FX settings enabling that pass for all tracks.
