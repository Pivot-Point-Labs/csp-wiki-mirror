Custom Shaders Patch is split in modules which could be disabled. There are a few options which aren’t a part of any module though, and some features can’t be disabled.

# Modules

## Lighting FX

Adds dynamic lighting for track and car lights, like headlights. Track lights are set by track config, car lights can be either defined in config or, if not, guessed automatically based on model, textures and various parameters such as manufacturing year. Uses [BVH accelerated shading](https://worldoffries.wordpress.com/2015/02/19/simple-alternative-to-clustered-shading-for-thousands-of-lights/) to speed up rendering and allow for hundreds of lights to be rendered at once.

Types of lights:
- Point light;
- Spot light;
- Double trimmed spot light for car headlights;
- Line light, although not very accurate one, for things like neon lights under the car.

Planned:
- Try Forward+?
- IES maps;
- Dynamic shadows.

## Extra FX

Adds additional render pass to get more information about the scene, such as scene normals maps, depth or motion buffer. With that information, new effects are possible:

- Local reflections (SSLR);
- Ambient occlusion (SSAO or, thanks to NVIDIA, HBAO+);
- New motion blur;
- Temporal anti-aliasing;
- Simple local light bounce (SSGI);
- [Scene light bounce](https://youtu.be/R9gsC5vB1Eg) (not screen-space);
- Volumetric lights;
- Fog blur.

<a href="https://i.imgur.com/as1FEAj.png" target="_blank" title="Volumetric lights"><img src="https://i.imgur.com/as1FEAj.png" width="400"></a>

# Miscellaneous tweaks

Hmm, it seems writing this post will take longer than developing the thing in the first place…
