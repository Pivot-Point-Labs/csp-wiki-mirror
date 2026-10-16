# Filtering

For defining light series, material adjustments or, for example, emissive objects, config needs to specify an entity to work with. In most those cases, you can set a list of objects as well:

```ini
[EMISSIVE_LIGHT_0]
MESHES = mesh0, mesh1, mesh2
...
```

### Masking

To make things simpler, you can also use simple masking. Maybe you noticed how Windows uses “*” for “any symbols in any quantity”? Patch uses “?” for the same purpose (for compatibility reasons).

```ini
[EMISSIVE_LIGHT_0]
MESHES = mesh?  ; would also include any other meshes starting with “mesh”, like mesh_99
...
```

### Properties

Filtering by properties is supported as well, with masking if needed:

```ini
[SHADER_REPLACEMENT_0]
MESHES = texture:cobbles_?.dds
SHADER = nePerPixelMultiMap_parallax
...
```

Please don’t add spaces before or after “:”, it’s not as flexible as CM’s filtering.

##### Known properties & examples

- Meshes:
  - `material:Material #91`: material name;
  - `renderable:yes`: is mesh renderable at all;
  - `transparent:yes`: is mesh marked as transparent;
  - `hasLodDistance:yes`: for tracks, is any LOD distance set;
  - `mirror:yes`: is mesh assigned for mirror (added in 0.1.62).
- Nodes and meshes:
  - `parent:COCKPIT_?R`: name of parent’s node;
  - `child:some_mesh`: name of one of the children;
  - `lod:A`: for cars, specify LODs (for use with extended filtering; see examples);
  - `active:yes`: is node active or not (added in 0.1.62);
  - `insideInterior:yes`: node is inside interior (added in 0.1.62);
  - `insideSteeringWheel:yes`: node is inside steering wheel (added in 0.1.62);
  - `first:yes`: is mesh the first child (added in 0.1.62);
  - `last:yes`: is mesh the last child (added in 0.1.62).
  - `modelRoot:yes`: is mesh the last child (added in 0.1.62).
- Meshes and materials:
  - `shader:ksPerPixel?`: shader name;
  - `texture:NULL.dds`: true if at least any used texture matches that name (case-independant);
  - `materialProperty:dirtyLevel`: checks if shader has a certain property or not;
  - `materialResource:txBlur`: checks if shader has a certain resource or not;
  - `supportsDamage:yes`: checks if shader supports damages or not;
  - `alphaBlend:yes`: is alpha blending enabled for material (added in 0.1.62);
  - `alphaTest:yes`: is alpha testing enabled for material (added in 0.1.62);
  - `vegetation:yes`: vegetation shaders, such as tree or grass (added in 0.1.62);
  - `dynamic:yes`: “moving” shaders, such as tree, grass or flag (added in 0.1.62).

Since 0.1.62, for things like `parent:…` you can use properties inside too, not only names. For example, if you want to move a track mesh so it would be rendered last, here is a bit of Hong config:

```ini
[SHADER_REPLACEMENT_...]
MATERIALS = decal_01, decal_02, decal_solids
MOVE_MESH_BEHIND = parent:modelRoot:y
```

(Just to clarify, the way `MOVE_MESH_BEHIND` works, it finds all nodes and meshes with given filter and then moves original mesh so it would be rendered *after* the one found. Filter `parent:modelRoot:y` finds all the children in track root node, so `MOVE_MESH_BEHIND` moves decals after the last one of track meshes. Adding it more as a comment for myself because I just got confused by it.)

### Extended filtering

Since **v0.1.25-preview183**, now extended filtering is supported, with logical expressions, grouping and all that. For that to work, first, wrap query in curly brackets, to point out it’s an extended filter. Everything else is pretty similar to filtering in CM:

```ini
[REFLECTIONS_FX]
MASK_CUBEMAP_SKIP = MIRROR_GEO, { GEO_INT? & parent:COCKPIT_HR }  ; you can list regular queries in the same bit as before
```

I recommend to use quotes to separate extended query, and wrap separate keywords in different quotes inside if you would want to use any of special symbols:

```ini
[MESH_ADJUSTMENT_...]
MESHES = '{ "some mesh^4" & !shader:ksPerPixel }'  ; spaces are optional, but they help
...
```

Supported expressions from higher to lower priority (of course, you can use brackets “(” and “)” to change the order):

- `! A`: for NOT, matches if A doesn’t match;
- `A & B`: for AND, matches if both sides match;
- `A ^ B`: for NOR, matches if either A or B matches, but not both at once;
- `A | B`: for OR, matches if at least A or B matches, or both.

I think in more than 99% percent of cases, that thing won’t be needed, but sometimes it could really help. For example, let’s take Highlands config, adding glowing windows via 165 MB replacement KN5. Sometimes it might get broken or failed to load, and without it, changing “ksEmissive” makes glow whole buildings rather than just windows. But extended filtering allows to rewrite it:

```ini
[MATERIAL_ADJUSTMENT_2]
MATERIALS = '{ ( buildings_ext2, Gazebo_Tent ) & shader:ksPerPixelMultiMap_emissive }'
KEY_0 = ksEmissive
...
```

No more glowing buildings, as it’ll work only if shader is changed to “ksPerPixelMultiMap_emissive”.

### Examples

- Take mesh1 from LOD A and mesh2 from LOD B (in case there would be wrong mesh1 in LOD B and mesh2 in LOD A), for cars:

  ```ini
  MESHES = '{ lod:A & mesh1 }', '{ lod:B & mesh2 }'
  ```

### Features to add later

- More properties to filter by.
