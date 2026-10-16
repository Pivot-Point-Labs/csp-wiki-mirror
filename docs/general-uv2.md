# UV2

For some extra details you can now add an secondary UV mapping to some of your meshes and use it for an overlaying texture. As an example, let’s say you’re working on an F1 car and have its body mesh unwrapped for a nice AO baking with evenly distributed details and everything. You’d also want to add some stickers on it, but with 2K resolution for AO texture stickers look sad, and 4K might look a bit much. With UV2 you can have a separate unwrap focused entirely on stickers, so their separate texture could use the space much more efficiently.

### How to add UV2 to KN5

Currently, with existing KN5 format there is no good way to add UV2 to models directly, but, similar to VAO patch, you can generate an additional binary file for CSP to read and load UV2 from. Just use Content Manager: there is a tool on Content/Tools/Creator which can take an FBX file, filter out meshes with two unique UV sets and generate a new ”.uv2” file that you can save next to KN5 file (naming it the same).

### How to use UV2 in a material

For now the simplest way is to use a shader replacement and load the texture from there (and if you don’t want “extension” folder to end up with hundreds of textures, keep in mind you can always put them all in a zip file and refer to them as “SOMETHING = textures.zip::path/in/zip.dds”).

There are currently three shaders supporting UV2:
- `nePerPixelMultiMap_AT_NMDetail_stickers`;
- `smCarPaint` (and derivatives);
- `stPerPixelMultiMap_specular` (and stPerPixelMultiMap_specular_damage_dirt).

Shader `smCarPaint` is easier to configure using “materials_carpaint.ini”, and that also includes stickers. Just look for StickersTexture, StickersMapsTexture and StickersCoverDetails parameters (just a reminder, with those material_… things you can always open the files themselves, they are fully documented in their first halves).

For others, a shader replacement might look something like this:

```ini
[SHADER_REPLACEMENT_...]
MATERIALS = …
SHADER = nePerPixelMultiMap_AT_NMDetail_stickers
PROP_... = extStickersMode, 1
RESOURCE_0 = txStickers
RESOURCE_FILE_0 = my_texture_pack.zip::stickers.dds
```

Property `extStickersMode` is a bunch of flags, as in, just sum the values you need to get the required behaviour. Currenly supported:

- `1`: activate the stickers layer (although any other flag activates it too, and it’s always active with `nePerPixelMultiMap_AT_NMDetail_stickers` shader);
- `2`: alpha of stickers will affect alpha of diffuse texture too, meaning details texture will be hidden by stickers;
- `4`: use additional `txStickersMaps` slot to alter `txMaps` as well (only in places where alpha of `txStickersMaps` is non-zero);
- `8`: available to `nePerPixelMultiMap_AT_NMDetail_stickers` only, use additional `txStickersNormals` slot to alter `txNormal`, added in v0.1.80-preview446.

So if, for example, you want to use both details hiding and `txStickersMaps`, just sum them all together giving you `1+2+4=7`. If you only need details hiding, use `1+2=3`.

### Known limitations

- While cars LOD generator in CM supports UV2, it might still get somewhat messed up, use carefully. Some models might even require further tweaking of Simplygon rules.
- UV2 uses half precision, should be all right in 0…1 range, but going outside of it too far might introduce artifacts.

### Use case hints

- When looking for UV2 patch files, CSP checks skin folders first, so that can be used for creating some advanced skins.
