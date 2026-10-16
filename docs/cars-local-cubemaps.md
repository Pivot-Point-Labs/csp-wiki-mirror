# Local Cubemaps

Local cubemaps is a trick allowing to improve reflections on spherical-looking objects by taking a snapshot of the whole car around them and using it as a mask for reflections on that object. Here is the whole thing in action:

[![YouTube video](https://img.youtube.com/vi/9ez4cXidH6A/0.jpg)](https://www.youtube.com/watch?v=9ez4cXidH6A)

Those Caterham headlights are a great example. Even SSLR can’t handle them properly, and without car reflected in those headlights, they look like some distant floating blobs.

### Important notes

- It’s only meant for spherical-like objects of relatively small size, like those headlights. Since it takes a spherical shot around some point and uses it to mask reflections, it’s not going to help with anything else, like chrome bumpers or bonnet.

- Meshes with local cubemap reflections should originally have “ksPerPixelMultiMap” shader, or shading will get messed up. If you need some features of other shaders, please let me know.

- Due to heavy caching, rare updates and overly simplified rendering of that mask, the whole thing doesn’t affect FPS that much. And with disabled dynamic local cubemaps in Reflections FX settings, the whole thing is pretty much zero FPS cost.

### Syntax

There are a couple of ways to use this feature. If it’s case with headlights, there is a template file “oldschool_lights_reflections.ini” designed to simplify the whole setup process (setting up two local cubemaps for left and right headlights):

```ini
[INCLUDE: common/oldschool_lights_reflections.ini]  ; including template which will do most of the work
MeshesLeft = headlightL   ; list of meshes on the left side, optional
MeshesRight = headlightR  ; list of meshes on the right side, optional
MeshesToCut = headlights  ; list of meshes to be cut (in case there is a single mesh for both
                          ; left and right headlights)
SplitAxis = 1, 0, 0       ; needed only if MeshesToCut is used, axis for splitting (in case mesh
                          ; is rotated strangely)
SplitThreshold = 0        ; needed only if MeshesToCut is used, point on axis to split meshes around
Offset = 0, 0, 0          ; offset for cubemaps’ pivots in meters (X for left cubemap will be inverted)
HigherResolution = 0      ; set to 1 in rare cases you would want to use higher resolution
DynamicReflections = 0    ; set to 1 to enable dynamic update, for example, if movement and
                          ; steering of frong wheels should be shown in reflections
DebugMode = 0             ; set to 1 to enable debug mode to check updating areas
Reflectivity = 0.5        ; how reflective should material be (0.5 is a good value for chrome)
ExcludeNodes = COCKPIT_HR, HUB_LR, HUB_RR  ; list of nodes to exclude from reflections to speed things up (usually
                          ; there is no sense to waste time rendering rear parts, rear wheels and interior)
```

For some more general cases, use more direct syntax (that template unwraps to it), only setting one cubemap per section:

```ini
[LOCAL_CUBEMAP_...]
MESHES = Spotlight_SUB0     ; list of meshes to change material and add local cubemaps for
POSITION = 0, 0, 0          ; optional, set position manually (otherwise center of meshes will be used)
OFFSET = 0.08, 0, 0.13      ; offset for cubemap pivot in meters
HIGH_RESOLUTION = 1         ; set to 1 in rare cases you would want to use higher resolution
IS_DYNAMIC = 1              ; set to 1 to enable dynamic update
DEBUG = 0                   ; set to 1 to enable debug mode to check updating areas
STATIC_FACES = TOP, BOTTOM, FRONT, LEFT  ; list of faces to stop from being updated dynamically (helps
                            ; a lot with performance, so enable debug mode and add as many faces as possible)
EXCLUDE_NODES = COCKPIT_HR  ; list of nodes to exclude from reflections to speed things up
```

If you would want to split mesh in two more manually, [here are some docs for it as well](cars-meshes-splitting.md).

### Features to add later

- Similar thing for tracks.
