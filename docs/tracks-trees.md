New CSP 0.1.79 feature: a way to add thousands of trees on tracks with a simple config. With LODs, billboards for distant trees and heavy use of instancing CSP should be able to handle hundreds of thousands of trees with no problem (and if it’s not, let me now and I’ll work on further speeding things up). Also, this system can be used for bushes — currently they won’t deform, but that is something that can always be added later.

<a href="https://gfycat.com/WindingWhiteArgusfish"><img src="https://thumbs.gfycat.com/WindingWhiteArgusfish-size_restricted.gif"></a>

# Tree models

First thing you would need is a model of a tree. In the future I’m hoping to try and be able to add procedural tree model generation, but it is what it is for now.

Model requirements:
- 10K triangles for LOD A, 6K triangles for LOD B, 3K triangles for LOD C (just suggestions, could be more than that or less though);
- Single mesh per LOD (use multi-material if you need one texture for trunk and another for branches and such);
- Pivot of each model should be right at the middle of its base (think of it as a tree positionining point on a surface);
- Materials should contain both diffuse (albedo) and normal texture (use bump texture in 3DS Max);
- Alpha of normal textures can be used for local ambient occlusion;
- Alpha of diffuse textures is used for transparency: make sure trunk texture is opaque.

Once you got a few LOD models fitting requirements (don’t have to be three LODs either, could be fewer if needed), simply combine them in a single scene and export as FBX.

<a href="https://files.acstuff.ru/shared/movf/20221025-093706.png"><img src="https://files.acstuff.ru/shared/movf/20221025-093706.png"></a>

Now you can use [AC Content Manager](https://acstuff.ru/app/#get) to quickly convert that FBX to ready-to-use tree model. Go to “Content/Tools/Creator tools” and choose tree converter.

<a href="https://files.acstuff.ru/shared/H7Kq/20221025-093900.png"><img src="https://files.acstuff.ru/shared/H7Kq/20221025-093900.png"></a>

In it, simply choose your FBX file, output BIN file for the tree (could be somewhere in “content/tracks/&lt;yourtrack&gt;/extension/trees”) and the tool will do the rest. If needed, there will be a few parameters you can tweak (for example, coniferous trees would definitely need less subscattering and reflectivity). Tool should also track changes in FBX file while running so you could tweak model and get tree model refreshed automatically.

# Tree lists

Now that your tree model is ready you can finally add it to the track. Here is how the simplest config for them looks like:

```ini
[TREES]
LIST_0 = trees/trees.txt
```

Written like this, it will point CSP to a tree list in “content/tracks/&lt;yourtrack&gt;/extension/trees/trees.txt”. Inside it can simply list trees with their coordinates (“my_tree.bin” is a file next to “trees.txt“ exported by Tree Model Converter earlier):

```
tree: my_tree.bin; 208.4, -1, -53
tree: my_tree.bin; 207.9, -1, -29
tree: my_tree.bin; 207.1, -1, -19
tree: my_tree.bin; 138.5, -1, -12
```

<details><summary>More information about the tree list format</summary>
First of all, of course, setting trees like this is not the best method. A tool to arrange trees live in AC is currenly in development. But also, you might be interested in creating custom export scripts: if so, you might be interested in more details on the format.

Each line of a list is either a comment, a tree or a configuration line. Configuration lines consist of key and value and override parameter with the said key until the next configuration line with the same key. Two simple configuration lines:

```
configure: size variance = 0.8, 1.2  ; size multiplier will be chosen randomly in 80…120% range
configure: angle variance = 0, 360   ; angle will be chosen randomly in 0…360° range
```

All parameters:
- `size variance`: sets range for random size;
- `width variance`: sets range for random width multiplier;
- `angle variance`: sets range for random angles;
- `color variance`: sets range for random RGB color shifts;
- `brightness variance`: sets range for random brightness shifts;
- `fake shadow`: needs a single value which will be used as fake shadow opacity for all following trees;
- `seed`: replaces random seed for all subsequent trees with a new single value.

*Note: all random values are predetermined with a fixed seed even if no explicit seed is set.*

Each tree line can also override any of those values for one specific tree:

```
tree: tree0.bin; pos=-83.3, -0.99, -74.14; angle = 180; size = 1; width = 1; color = 2, 2, 2
```
</details>

For simpler editing multiple lists can be used in a same config. This way updating a list wouldn’t require to reload all lists.

# Other parameters

### Surface alignment

To automatically snap trees on underlying surface and align trees lighting with it (greatly helps on tilted surfaces) use `SURFACE_MESHES` and `SURFACE_MATERIALS` parameters like so:

```ini
[TREES]
LIST_0 = trees.txt
SURFACE_MATERIALS = tarmac, Concrete2Mat
```

### Seasonal conditions

You can tie season look to conditions making trees turn yellow in autumns and white in winters. Also, it’s possible to redefine those seasonal adjustmnents for different types of trees (stopping coniferous trees from getting yellow in autumn, for example):

```ini
[CONDITION_...]
NAME = SEASON_WINTER
INPUT = YEAR_PROGRESS
LUT = (|-1=0|0=0.25|0.05=0.35|0.075=2|0.12=0.3|0.2=0|0.45=0|0.6=0.00|0.7=0|0.85=0|0.95=0.2|1=0.25|)

[CONDITION_...]
NAME = SEASON_AUTUMN
INPUT = YEAR_PROGRESS
LUT = (|-1=0|0=0.75|0.2=0|0.45=0|0.6=0.05|0.7=0|0.75=0|0.8=0.75|1=0.75|)

[TREES]
LIST_0 = trees.txt
SEASON_AUTUMN_0 = SEASON_AUTUMN
SEASON_WINTER_0 = SEASON_WINTER
SEASON_AUTUMN_1 = tree_pine?, tree_big_pine.bin, 0
```

*Note: currently trees won’t lose leaves in winter. Add “[BASIC] LEAFLESS_WINTER=1” parameter in “tree.ini” of a generated tree (those bin-files are just archives that can be opened with something like 7Zip or WinRAR) so that in the future CSP would know to remove leaves from your tree once I figure out how to do it efficiently.*

# Baking and compiling

After everything else is ready you can use [vertex ambient occlusion bakery](https://github.com/ac-custom-shaders-patch/acc-bakeryoptix) to compile tree lists into a single binary file which should help noticeably speed up loading. It also adds ambient shadows from trees to the track and computes directional ambient shadows on trees, helping to add depth to dense forests. To set it up simply bake your track with new VAO bakery ([v17+](https://github.com/ac-custom-shaders-patch/acc-bakeryoptix/releases)). Make sure your track folder is in AC root folder and CSP 0.1.79 is installed: bakery will run Assetto Corsa in headless mode a few times to help with data processing.

After compiling, a new file “compiled_trees.bin” will be created in the track directory. Simply move it to wherever you’d prefer it to be located (for example, in “content/tracks/&lt;yourtrack&gt;/extension” folder) and change config to:

```ini
[TREES]
COMPILED_LIST = compiled_trees.bin
```

With that value, AC would automatically load compiled list instead of “LIST_…” values specified, speeding up reading and initial setup. List files after that can be removed from a published version.

A few more details:
- If “COMPILED_LIST” value is set, AC will ignore all “LIST_…” values, but only during its regular runs, not during the baking process. This way, you don’t have to remove “LIST…” to force CSP to use compiled data, or remove “COMPILED_LIST” line to revert CSP back to using text lists for updating baking data;
- Surface alignment (configurable with “SURFACE_…” values) is also stored in a compiled list. Make sure to recompile it if landscape geometry or normal map changes;
- VAO bakery doesn’t always have to compile binary list. Check out “baked_shadow_params.ini”: values “EXT_PROCEDURAL_TREES_…” set how trees will be processed, and if “EXT_PROCEDURAL_TREES_FINALIZE” is not set to 1 trees occlusion info instead will be stored in track’s “.vao-patch” file.
