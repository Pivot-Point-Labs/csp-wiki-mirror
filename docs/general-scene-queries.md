# Scene Queries

A lot of CSP configs, as well as `ac.SceneReference()` in Lua, expect a reference to nodes or meshes in the scene. For most cases a simple mesh name would do, but there are times when something more advanced would work better, so here are some details on they work.

First of all, all those queries unless stated otherwise support a wildcard “?” meaning any amount of any symbols. Other than that, matching tries to grab the whole string, so if you want to search for a substring, use “?keyword?” pattern.

### Properties

Apart from using name, queries can refer to properties. The syntax for those is “property:value”, so instead of using “MESH_NAME”, you can use “material:MATERIAL_NAME”, for example.

##### Specific nodes

- `carRoot:N`: a car root node of Nth car;
- `driverRoot:N`: a driver root node of Nth car;
- `driverNeck:N`: a driver neck node of Nth car;
- `sceneRoot:yes`/`:no`¹: the root node;
- `carsRoot:yes`/`:no`¹: the node containing cars;
- `trackRoot:yes`/`:no`¹: track root node;
- `staticRoot:yes`/`:no`¹: static geometry root (known as “BLURRED”);
- `dynamicRoot:yes`/`:no`¹: dynamic geometry root (known as “UNBLURRED”).

Using most of those from car or track config won’t work at all, they are limited in their queires to their corresponding nodes. Same goes for car and track Lua scripts, but other types of Lua scripts can go a bit wild.

##### Common properties

There properies work with objects of any type.

- `class`: object type (known: `node`, `model`, `carNodeSorter`, `nodeBoundingSphere`, `parent`, `nodeEvent`, `idealLine`, `particleSystem`, `staticParticleSystem`, `displayNode`, `textNode`, `cspNode`, `renderable`, `mesh`, `skinnedMesh`, `skidmarkBuffer`);
- `active:yes`/`:no`: active status;
- `first:yes`/`:no`¹: first child of its parent;
- `last:yes`/`:no`¹: last child of its parent;
- `lod:N`/`:A`/`:B`/…: an objects is from a certain LOD (for car models);
- `modelRoot:yes`/`:no`: root node of a KN5 file;
- `driverPiece:yes`/`:no`: objects in driver models;
- `insideInterior:yes`/`:no`: objects in car cockpits;
- `insideSteeringWheel:yes`/`:no`: objects in car steering wheels;
- `insideWheel:yes`/`:no`: objects in car wheel nodes;
- `insideSuspension:yes`/`:no`: objects in car suspension nodes;
- `insideNthWheel:N`: objects in Nth cars wheels;
- `insideNthSuspension:N`: objects in Nth cars suspensions;
- `parent:X`: if parent matches X (which might also be a property query);
- `child:X`: if node has a child matching X. More expensive than others, so use carefully.

##### Material-related properties

There properies work with objects with materials (meshes and skinned meshes). They can also be used in `MATERIALS = …` parameters of, for example, [shader replacements](general-shader-replacements.md) sections.

- `material:X`: material name;
- `shader:X`: shader name;
- `vegetation:yes`/`:no`: trees and grass;
- `dynamic:yes`/`:no`: entities that move on their own (trees, grass, flags);
- `supportsDamage:yes`/`:no`: materials supporting damage (such as “ksPerPixelMultiMap_damage_dirt”);
- `alphaBlend:yes`/`:no`: material uses alpha blending;
- `alphaTest:yes`/`:no`: material uses alpha testing;
- `isTextureDefault:X`²: if texture X is the default one and not from a skin;
- `isTextureSlotDefault:X`²: if texture in a slot X is the default one and not from a skin;
- `texture:X`: name of any texture;
- `materialProperty:X`²: if material has a property X;
- `materialResource:X`²: if material has a texture slot X;.

##### Mesh properties

These ones only match with meshes.

- `renderable:yes`/`:no`: non-renderable meshes are used for physics;
- `transparent:yes`/`:no`: transparent flag;
- `static:yes`/`:no`: static flag (usually assigned to track meshes);
- `largerThan:N`: if diameter of mesh bounding sphere is larger than N meters (does not account for parent scaling);
- `castsShadows:yes`/`:no`: shadow casting option;
- `lodIn:N`: if LOD in distance is within 0.5 of N meters;
- `lodOut`: if LOD out distance is within 0.5 of N meters;
- `hasLodDistance:yes`/`:no`: if mesh has defined LOD distances;
- `wet:yes`/`:no`: mesh getting wet during the rain (some of car meshes inside remain completely dry);
- `mirror:yes`/`:no`: car rear view mirror meshes;
- `windscreenGeneratedUV:yes`/`:no`: RainFX generated alternative UV for windscreens and mirrors;
- `layer:N`: mesh layer (aka its level detail, meshes on layer 5 only drawn with high world detail);
- `actsAsHeadlights:yes`/`:no`: based on car emissive configuration;
- `actsAsBrakeLights:yes`/`:no`: based on car emissive configuration.

##### Skinned mesh properties

- `transparent:yes`/`:no`: transparent flag;
- `castsShadows:yes`/`:no`: shadow casting option;
- `hasLodDistance:yes`/`:no`: if mesh has defined LOD distances;
- `layer:N`: mesh layer (aka its level detail, meshes on layer 5 only drawn with high world detail).

All indices are zero-based.

¹ With CSP builds before 0.1.80-preview400, `:no` option is not supported, use cancellation (`!first:yes`).
² Has to be an exact match, “?” is not supported.

### Complex queries

To use multiple properies at once it’s possible to combine queries into complex expressions. First thing is to add “{” and “}” to expression ends, and write the complex thing in them. Supported operators:

- `^`: logical **not**;
- `&`: logical **and**;
- `|` (or `,`): logical **or**.

Brackets can be used to assign explicit order (without them “!” takes precedence, then goes “&”). Few examples:

- `{ RT_DRIVER_Face & ( isTextureDefault:DRIVER_Face.dds | isTextureDefault:DRIVER_Face_NM.dds ) }`;
- `{ transparent:yes & alphaBlend:yes & ( shader:ksPerPixelReflection | shader:smGlass? ) }`.

### Few more things

Please note: the reason CSP allows to list nodes in configs just by doing something like `MESHES = A, B, C` is simply due to the fact config parser in CSP always deals with lists, so in that example it read three queries. On another hand, Lua API working with scenes only expects a single query, so you would need to use `ac.findMeshes('{ A, B, C }')` there.

Also, if you’re working with shader replacements, consider using `MATERIALS` instead of `MESHES = material:…` where possible. While there are certain optimizations in place, sometimes CSP still has to make a copy of material for each individual mesh if your shader replacement alters something like material property on per-mesh basic.
