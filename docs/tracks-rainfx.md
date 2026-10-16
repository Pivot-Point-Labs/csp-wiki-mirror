# Rain FX

**Generic Definition**

* PUDDLES_MATERIALS - the key part for physics for generating puddles.
* SOAKING_MATERIALS - by default, all materials will get 35% darker when wet, SOAKING_MATERIALS will get 70% darker (adds 35% darkening again).
* SMOOTH_MATERIALS - the ones which wouldn’t get darker at all and would get rain drops on top of them, such as bits of glass, cars, smooth clean metals and so on. If something is mentioned in both SMOOTH_… and SOAKING_…, it’d get rain drops, but would still get 35% darker.
* ROUGH_MATERIALS - won’t get any reflections and wouldn’t even get noticeably shinier, just darker as they get wet. Pretty much a requirement for any grass surfaces, because otherwise procedural grass wouldn’t be able to get nice reflections to match and with Extra FX especially whole thing looks pretty broken.
* LINES_MATERIALS - allow to mark paint lines on track surface. It wouldn’t have any visual effect, but it would affect physics a bit later (much slippier).
* LINES_FILTER_MATERIALS - similar to LINES_MATERIALS, but instead of just using whole thing as a surface paint mask, it would filter out only brighter areas, for tracks like Silverstone where track lines are not overlaying meshes, but instead a part of texture.
* RELIEF_MATERIALS - broken at the moment, and not sure if there would ever be a need to actually change it. The idea was to have more puddles in lower areas, for that, CSP uses track height map. That parameter specifies what goes into it, and by default it just uses everything. That means that around high buildings there could be more puddles, as area around would be perceived as a local minimum. Don’t know if that is similar to how it works IRL or not, but if not, well, this parameter allows to exclude buildings quickly.
* For each of the above XXX_MATERIALS, you can use XXX_MESHES version too.

**More Specific Cases**

* The main track asphalt surfaces should be defined as both PUDDLES_MATERIALS and SOAKING_MATERIALS.
* It's not necessary to define curbs as SOAKING_MATERIALS since they usually don't get much darker when wet, but curbs as PUDDLES_MATERIALS, sure.
* For now it is recommended to keep PUDDLES_MATERIALS for roads only, as they do some things assuming it would be a road. For puddles in other places, such as grand stands, it might even be worth preparing separate shaders set for materials with smaller non-road puddles which wouldn’t depend on large scale relief, wouldn’t read racing line offset and so on.
* An example of SOAKING_MATERIALS can be cloth roofs.
* There is no need to define grooves as any of the Rain FX materials/meshes. Now there is a new shader for grooves and it wouldn’t have puddles at all. Whole thing with puddles is to add real-time reflections, but all grooves are doing now is simply masking reflections for SSLR. The following link shows the list of shaders supporting puddles (more will be added soon, please let Ilya know if he needs to add one urgently): gitlab.com/ac-custom-shaders-patch/public/acc-shaders/-/blob/master/.build/lists.txt
* About sand surface, it can be defined as either ROUGH_MATERIALS or SOAKING_SURFACES, as it sort of looks good with both, a bit of reflections or just dark sand trap. A suggestion can be defining it based on how smooth it would be. Like, if it’s on some beach, fine and smooth sand, it can definitely get more reflective, while regular sand pits are usually quite roughened up, so maybe they would look better without any reflections. Also, performance plays a role too, might help a bit to have fewer materials reflective.
* Bystanders can be defined as ROUGH_MATERIALS too, as sometimes it seems strange to see them getting reflective.
* The amount of SMOOTH_MATERIALS defined wouldn’t really affect performance. You can define as many as possible, or just the ones you'd see when driving. The shaders are more complex, but if they’re not taking much screen space currently, it doesn’t really matter.

**Tutorial for Making Configs**

1. Copy the example codes below to the end of the *.ini config file inside extension\config\tracks\loaded folder. If you are working on a track whose config file is not in GitHub repo, create an 'extension' folder inside content\tracks\your_track folder and an 'ext_config.ini' file inside of it.
2. Load into the game, use F7 freer camera to navigate around the track. Windowed mode is recommended so that you can work on the config file at the same time.
3. Open the Objects Inspector app and Alt-click on the objects you'd like to work on.
4. Click on the material/mesh name in Object Inspector so it copies to clipboard, then paste into the config file under the XXX_MATERIALS/MESHES you'd like.
5. Save the config file, and you can see the in-game effect immediately.
6. Repeat step 3 - 5 for other track objects. For personal use, work on however many you'd like. For sharing with public, please try to be as thorough as possible.
7. Good examples can be ks_nordschleife, spa, and ks_highlands if you want some reference.


```ini
[RAIN_FX]
PUDDLES_MATERIALS = some_material  ; wildcard "?" possible as usual
SOAKING_MATERIALS = ...
SMOOTH_MATERIALS = ...
ROUGH_MATERIALS = ...
LINES_MATERIALS = ...
LINES_FILTER_MATERIALS = ...

; you can use ..._MESHES = counter-part too!

; define edges or points from where rain should drip down...
STREAM_EDGE_... = -1207, 39, -1750, -1173.6, 39.5, -1750.2  ; x1,y1,z1 , x2,y2,z2
STREAM_POINT_... = -1232.69, 38.48, -1411.69                ; x,y,z

; RELIEF_MATERIALS = '{ dynamic:no & !Bx? }'  ; broken atm
```
**For bridges/tunnels**
- you can define areas where rain should not fall
```ini
[TRACK_OCCLUDER_BOX_0]
DESCRIPTION=upper plane of a box, underneath no rain
POINT_0=726.001, 15.7748, 586.403
POINT_1=730.039, 15.7748, 600.85
POINT_2=723.472, 15.7748, 602.709
POINT_3=719.433, 15.7748, 588.262

[TRACK_OCCLUDER_WALL_0]
DESCRIPTION=for a wall only 2 points needed
POINT_0=678.85, 11.4539, 574.043
POINT_1=734.493, 11.4539, 759.929
```
