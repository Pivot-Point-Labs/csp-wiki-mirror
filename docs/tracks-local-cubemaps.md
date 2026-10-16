# Local Cubemaps

Usually all the things in AC use one global cubemap (like a 360° picture) shot around camera position for reflections. Because of that, if you have a glossy building, for example, when camera moves, reflections start to move too, often too much:

<a href="https://gfycat.com/glassslowbarasingha"><img src="https://thumbs.gfycat.com/GlassSlowBarasingha-size_restricted.gif" width="400" ></a>

*Notice how reflection changes even though the angle between look direction and building surface doesn’t change.*

And this is how this glass looks with local cubemap:

<a href="https://gfycat.com/CooperativeDelectableGrunion"><img src="https://thumbs.gfycat.com/CooperativeDelectableGrunion-size_restricted.gif" width="400" ></a>

### Syntax

```ini
[LOCAL_CUBEMAP_...]
MESHES = base_vetri    ; list of track meshes to have their own cubemap
POSITION = 100, 1, 10  ; (optional) cubemap position, if not set, center of meshes will be used
OFFSET = 0, 0, 0       ; (optiona) offset for position guessed from meshes
EXCLUDE = base_vetri   ; list of meshes to exclude from cubemap (speeds things up as well)
CLIP_PLANE_NEAR = 2    ; near clipping plane, meters (might help to remove reflections from close things)
HIGH_RESOLUTION = 0    ; set to 1 to use high resolution cubemap (for large flat surfaces)
LOW_RESOLUTION = 0     ; set to 1 to use low resolution cubemap (for dynamic cubemaps)
IS_DYNAMIC = 0         ; set to 1 to switch to dynamic mode
DYNAMIC_FAST = 0       ; (not recommended!) set to 1 to update one face per frame
STATIC_FACES = TOP, LEFT, REAR, BOTTOM  ; static faces to exclude from dynamic updates (see tips)
INCLUDE_SKY = 1        ; set to 0 to exclude sky and speed things up a tiny bit (if not needed)
INCLUDE_CARS = 0       ; set to 1 to include cars
DYNAMIC_LIGHTING = 0   ; set to 1 to include lights in reflection
DEBUG = 0              ; set to 1 to see the center of cubemap and static faces highlighted red
DEBUG_CLEAR = 0        ; disable sky and set to 1 to test refresh rate
```

With dynamic cubemap and shown cars, you can make those mirrors more lively:

[![Example](https://thumbs.gfycat.com/LateOfficialChihuahua-size_restricted.gif)](https://gfycat.com/lateofficialchihuahua)

But please be careful, that stuff is pretty expensive. If you have several mirrors on a track, you can use the single moving local cubemap to cover all of them:

```ini
[LOCAL_CUBEMAP_...]
POSITION_0 = 10, 1, 100  ; position of first mirror
POSITION_1 = 10, 1, 200  ; position of second mirror
POSITION_2 = 10, 1, 300  ; position of third mirror
...
```

And cubemap will move to the position which is closer to viewer.

### Important tips

- Don’t worry about static cubemaps with changing time of day: even static ones will update from time to time to follow changing lighting conditions.
- Please remember about performance. Avoid using high resolution, dynamic, lighting or cars unless needed.
- One cubemap with low resolution takes 2.6 MB of VRAM, with normal resolution — 12.5 MB, with high resolution — 50.3 MB. Keep that in mind as well, please.
- Do not use `DYNAMIC_FAST` unless there is a real need for it.
- Without `DYNAMIC_FAST`, local cubemap updates a face once every couple of frames or so. Usually though, only a couple of faces needs to be updated frequently. Mark other ones in `STATIC_FACES` (using `DEBUG = 1` to check which ones are which) and one face per couple of frames would be more than enough (as in that GIF).
- I suggest to position cubemaps manually. Keep in mind, cubemap reflections are 100% perfect for a surface point at the center of the cubemap, and the further points are from the center, the less accurate reflections become. If you have a big building with glass windows, position cubemap closer to the side facing the track, and maybe a bit lower, so mainly visible area would look more accurate at expense of other sides.
- Another way to use this thing is to have one static cubemap for a lot of objects all over the track where you don’t need good reflections, just need to stop them from moving and be in a certain theme. For example, windows of houses in Highlands. With something as simple like that:

  ```ini
  [LOCAL_CUBEMAP_...]
  MESHES = material:House_02, material:house?
  POSITION = 842.36, 6.79, 612.28  ; position somehere in that town, so houses would reflect some other houses
  LOW_RESOLUTION = 1
  ```

  Those windows will get a nice stable reflections and since it’s not dynamic and in lower resolution, it might actually render faster than original (considering user would use cubemaps with resolution higher than 256×256).
- Or, even set position somewhere from above, so it would be mainly sky.
