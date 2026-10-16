# Tracks: Distant emissives

Distant emissives help to reduce lights flickering with distance. The way it works, it find a piece of emissive mesh and generates a glowing billboard (square always “looking” at camera), and gradually replaces regular emissiveness with that billboard with distance. [Comparison screenshots](https://acstuff.ru/u/comparison/F7T) (notice how uneven is glow in original screenshot).

New glow consists of two parts, smaller dot in the center and much larger billboard visible in foggy conditions, creating a cheap lit up fog effect like so:

![img](https://acstuff.ru/patch/screens/03_Distant%20emissives%20in%20fog.jpg)

### Syntax

```ini
[INCLUDE: common/materials_track.ini]

[Material_DistantEmissive]
Meshes =                 ; list of meshes which should have those billboards created for them
UseAlpha = 0             ; set to 1 if original shader is ksPerPixelAlpha, so alpha property would be used
UseEmissiveTexture = 0   ; set to 1 to use txEmissive texture
FloodlightPower = 0.0    ; increase value for floodlight mode, so emissiveness would increase if camera is right in front
FloodlightEXP = 20.0     ; increase for more focused floodlight effect
DistantGlowTextured = 1  ; use slightly blurried sample from txDiffuse for distant glow
BrightnessMult = 1.0     ; multiplier for brightness
DotMaxDistance = 2000.0  ; max distance for dot glow (starts fading out at half of it)
```

You can check other parameters in “common/materials_track.ini”, in `[TEMPLATE: Material_DistantEmissive]`. although I would recommend to keep them to their default values.

The way Custom Shader Patch generates billboards, it uses a simple clusterisation algorithm, to avoid creating way too many glowing areas too close. Here is how you can adjust those settings (please avoid lowering them too much, or it would damage the performance):

```ini
[DISTANT_GLOW]
THRESHOLD = 50 ; threshold within single mesh
SHARED_THRESHOLD = 25 ; threshold shared between all meshes: this way, there won’t be a glowing area from mesh A too close to glowing area from mesh B
IGNORE_SHARED_THRESHOLD = 0 ; ignore shared threshold; really not recommended, if it would happen that there would be a lot of those areas in a compact space, FPS might drop too much, there would be a lot of blending to do
```
