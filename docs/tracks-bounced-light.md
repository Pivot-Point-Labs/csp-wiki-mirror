*Whole thing might be a bit tricky, sorry if this post doesn’t make much sense. If you have any questions or suggestions on how to improve it, please let me know.*

# Basics

Bounced light is a part of Extra FX adding a bit of extra lighting from horizontal lit surfaces to any walls or ceilings nearby. Here it is in action:

<a href="https://i.imgur.com/6FEYdOf.jpg" target="_blank"><img src="https://i.imgur.com/6FEYdOf.jpg" title="Before" width="280"></a> <a href="https://i.imgur.com/Aha9f7r.jpg" target="_blank"><img src="https://i.imgur.com/Aha9f7r.jpg" title="After" width="280"></a>

Neat part is that it only takes about 0.3 ms for everything, it’s not a screen-space effect (so it would work even if lit up road wasn’t in the frame) and it doesn’t have any temporal lag, so it reacts to any change of lighting immediattely. However, there are a couple of drawbacks, because of which, it requires a track config to work.

### How does it work

It’s stupidly simple: just make a shot of the track around camera, from above, blur it and use it to add bounced light. A bit of complication is that, during application stage, it also compares distance from a point to the surface underneath. Greater difference means more blurring and less intensity:

<a href="https://i.imgur.com/5a6Q5hL.jpg" target="_blank"><img src="https://i.imgur.com/5a6Q5hL.jpg" title="Before" width=380></a>

So here is the first drawback: for tunnels and underpasses to work, light map should only contain surfaces you would expect to bounce light back. In the example with Black Cat County (on first two shots), rocks shouldn’t end up in light map, or the whole thing would look very wrong. Notice how light map doesn’t include it, but has shadow from those rocks:

<a href="https://i.imgur.com/2Bh4ydT.jpg" target="_blank"><img src="https://i.imgur.com/2Bh4ydT.jpg" width=380></a>

Second drawback is of similar nature: whole thing works primarily with a single layer tracks. I think that’s why no other game really used that trick, as long as you get, like, two stories building, whole thing falls apart. Thankfully in AC 98% of tracks are flat, so it works just fine. And there is a few extra options that might help to deal with some of more complicated cases, but it’s far from perfect, at least at the moment.

### Syntax

For any `…_MATERIALS`, there is also `…MESHES`, like `SURFACE_MESHES`; both could be used at the same time.

```ini
[BOUNCED_LIGHT]
SUPPORTED = 1 ; this one is simple, sets that track supports bounced lights
SURFACE_MATERIALS = ? ; list of materials bouncing light back, default value is 1
OBJECT_MATERIALS = ; list of objects: they are excluded from light map completely, add here things like billboards, signs, walls, rails, anything that is not a flat surface casting light back up
SPOT_MATERIALS = ; list of objects which would contribute to bounced light without altering surface height. for example, on Black Cat County, rocks are listed here, so they would bounce light back, but won’t affect ground height
OCCLUDING_MATERIALS = ; list of objects which will be drawn as black, thus casting shadow on the ground
CLIP_POINT_... = 192, 79, 494 ; list of clip points (more about it a bit later)
CLIP_POINT_... = -197, 3, -776 ; keep in mind, with CSP, you can use “...” for keys and indices will be set automatically
CLIP_POINT_... = ...
```

What are clip points? It’s an easy way to separate ceilings from everything else. Again, take a look at these rocks on Black Cat County. It’s all a single piece of mesh. While I might want for its lower part to contribute to bounced light, upper part should, of course, be excluded. And it happens more often than not: for example, you might want to get rid of a hill over a tunnel, which uses the same mesh name and material as a bunch of terrain somewhere nearby. That’s where clip points are coming in.

Imagine a plane at the height of 500 meters. Each clip point pulls it down in such a way that it would reach that point and then go back:

<a href="https://gfycat.com/AgonizingHonoredGuanaco"><img src="https://thumbs.gfycat.com/AgonizingHonoredGuanaco-size_restricted.gif" width=380 ></a>

*You can turn on that debug view in Extra FX Debug app, in Bounced Light options.*

It’s a bit of a strange system, but I found it to be working well with both simple passages and long tunnels, and it works great with shaders (keep it might shaders will only use 16 closest points, but it seems to be more than enough). Clip points can not only pull that plane down, but, of course, also move it up. Plus, each clip point can have its own weight modifying its “gravity”, if needed.

To add a clip point, I recommend to simply move camera where it should be, copy its coordinates and paste to track config as a new line with `CLIP_POINT_...` key. That button copies camera position (from AccExtHelper app [here](https://github.com/ac-custom-shaders-patch/acc-extension-apps)):

<a href="https://i.imgur.com/Zn9XOOY.jpg" target="_blank"><img src="https://i.imgur.com/Zn9XOOY.jpg" title="Before" width="200"></a>

To alter weight of a clip point, simply add a fourth value to it. Default weight is 1. And remember when I mentioned 500 meters a bit earier? That could also be changed:

```ini
[BOUNCED_LIGHT]
CLIP_BASE_WEIGHT = 1 ; weight for clip plane to start with, increase to make it harder for clip points to pull it
CLIP_BASE_Y = 500
```

That’s all for basic setup! Hopefully any of that made sense. Oh, and one important tip: please make sure to add anything that is not contributing to bounced light to `OBJECT_MATERIALS`, that might save a lot of time when rendering light map.


### Features to add later

- Option for track light to keep it enabled only if bounced light is disabled, as a fix for tunnels.

# Extras

### Caustics

<img src="https://files.acstuff.ru/shared/SOUG/20220611-180033.png" width=380>

To activate caustics, use:

```ini
[BOUNCED_LIGHT]
CAUSTICS = 1
CAUSTICS_SCALE = 1  ; optionally, adjust caustics intensity
```

### Extra clip planes

As a strange solution for multi-level tracks, with bridges and what not, there is one possible solution at the moment: define a new clip plane with new clip points, limited in space. If camera would end up below that plane, extra clip points will be added. Here is an example, let’s say I want to make this tunnel on Nordschleife to have a nice bounced light on the ceiling while still not breaking bounced light for everything above it.

<a href="https://i.imgur.com/vn3mW5s.jpg" target="_blank"><img src="https://i.imgur.com/vn3mW5s.jpg" width=380></a>

For that, I can define a new clipping plane like this:

```ini
[BOUNCED_LIGHT_ADJUSTMENT_...]
CENTER = -441.05, -141.52, -1993.56 ; center of a new clipping plane
RADIUS = 200 ; its radius, to save performance by discarding it if camera is too far away, and to reduce unnecessary triggering
CLIP_BASE_Y = -200 ; base Y value
CLIP_POINT_... = -440.49, -145.23, -1996.67 ; points defining plane: one below the bridge
CLIP_POINT_... = -468.28, -136.91, -2005.69 ; one one the left, above, to get that bump
CLIP_POINT_... = -416.11, -135.55, -1975.77 ; one one the right, above, to get that bump
CLIP_POINT_... = -418.04, -149.52, -2037.85 ; one after the bridge, to push plane below the road
CLIP_POINT_... = -452.52, -142.24, -1974.21 ; one before the bridge, to push plane below the road
```

<a href="https://i.imgur.com/GnbzW1I.jpg" target="_blank"><img src="https://i.imgur.com/GnbzW1I.jpg" width=380></a>

And as soon as camera would move below that plane, its points would get applied to main clip plane, causing bounced light to change:

<a href="https://gfycat.com/DisguisedAdvancedFlycatcher"><img src="https://thumbs.gfycat.com/DisguisedAdvancedFlycatcher-size_restricted.gif" width=380 ></a>

This hack is far from ideal, but I believe in general it might work all right, for example, with camera bound to a car which would either move above or below the bridge. Also, that jump might be smoothed out later on.

### Height map

For the whole thing to look nicer, it needs to know distance to surface at any given point. Now, imagine there are holes in surface, or, for example, you forgot to mark some parked car as object mesh, and it’s being perceived like a major bump affecting bounced light. To try and combat this issue, Custom Shaders Patch expands depth map: basically, for each pixel, it would check all the neighbours in a certain radius and pick lower, but non-zero value (to deal with holes). But in some cases, it might reduce quality of bounced light on steep surfaces. This is how you can change that behaviour:

```ini
[BOUNCED_LIGHT]
DEPTH_EXPANSION_STEPS = 1 ; default value is 1
```

Increase amount of steps to increase radius of that check for some extra complicated cases (not recommended). Or, if you know your light map doesn’t have holes and steep jumps (there are options in Extra FX Debug app to check detected distance to surface), set it to 0 to improve performance and quality a bit.
