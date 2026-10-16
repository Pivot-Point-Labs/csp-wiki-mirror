# Dirt on Tyres

Since **v0.1.25-preview27**, now tracks can set custom tyres dirt parameters, used by Tyres FX. Both pieces of grass and dirt are drawn as gradients between two colors (this way, I could fit normals, alpha and that gradient into RGBA texture).

It looks better if those colors match colors of textures. Plus, maybe, you have a snowy track, for example: in this case, you can set dirt color to white.

To distinguish between grass and dirt surfaces, `WAV` parameter is used. If it’s `grass.wav`, it’s a piece of grass!

### Syntax

```ini
[DIRT]
DIRT_COLOR_A = 153, 136, 101, 0.004  ; first dirt color
DIRT_COLOR_B = 81, 72, 56, 0.004     ; second dirt color
GRASS_COLOR_A = 52, 80, 48, 0.006    ; first grass color
GRASS_COLOR_B = 42, 51, 34, 0.006    ; second grass color
DIRT_GAIN = 1.0                      ; how fast dirt would be accumulated
DIRT_FADE_GAIN = 1.0                 ; how fast dirt would fade
GRASS_GAIN = 1.0                     ; how fast grass would be accumulated
GRASS_FADE_GAIN = 1.0                 ; how fast grass would fade
```

`DIRT_FADE_GAIN` and `GRASS_FADE_GAIN` would not have a lot of effect: when car returns on a track, it’s its physical dirty level that is used to calculate dirt loss. But when you move from grass to dirt, or from dirt to grass, then those parameters specify how quickly other type of dirt would be vanished.
