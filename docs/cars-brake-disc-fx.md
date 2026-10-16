# Brake Disc FX

New shader for brake discs, with anisotropic lighting, dynamic wear and new heating.

<a href="https://gfycat.com/AdorableJampackedFantail"><img src="https://thumbs.gfycat.com/AdorableJampackedFantail-size_restricted.gif" height="400" ></a>
<a href="https://gfycat.com/AdeptIdealisticIlladopsis"><img src="https://thumbs.gfycat.com/AdeptIdealisticIlladopsis-size_restricted.gif" height="400" ></a>

*Never mind holes glowing too early, that is fixed now.*

Patch would go and find all meshes using `ksBrakeDisc` shader, and switch it to `ksBrakeDiscFX`, adding a few parameters for the whole thing to work. If you’re using `ksBrakeDisc` for something else, you can disable the whole thing with settings:

### Basic settings (recommended to change if needed)

```ini
[BRAKEDISC_FX]
ACTIVE = 1             ; set to 0 to disable the whole thing if car uses ksBrakeDisc shader for something else
CERAMIC = 0            ; use ceramic look
CARVED = 0             ; add a bit of carving, radial lines (fast for shader to compute)
CARVED_FREQUENCY = 20  ; increase to make more lines
GLOW_OFFSET = 0.8      ; increase to offset heated and worn center more to the center, decrease to offset it more to the outside area; with 0.5, it would be in the middle

; Patch guesses holes from alpha-channel of txDiffuse. Holes don’t glow or reflect stuff and look dark:
ALPHA_MASK = 0.1, 0.2  ; hole is everything with alpha below 0.1, everything with alpha above 0.2 is not a hole, in-between is a transition

; Patch can also estimate deepenings based on luminance and normal texture. Deepenings glow with a delay (but fully heated, glow more) and are a bit occluded:
LUMINOCITY_MASK = 0.01, 0.02  ; everything darker than 0.01 is a deepening
NORMAL_MASK = 0.5, 0.3        ; everything looking away more than 50% is a deepening

; Patch would try and guess size of brake disc and its inside area from its mesh, but if it fails:
DISC_RADIUS = 0.25           ; radius of a brake disc
DISC_INTERNAL_RADIUS = 0.15  ; radius of an inside part of a brake disc

; Another feature is that patch would mask reflections with rim, stopping brake disc from reflecting sky if looked at a angle. By default it would use rim radius and 60% of wheel width (for the distance between brake disc and exterior part) from “tyres.ini”, could be changed if needed:
RIM_RADIUS = 0.35  ; inside radius of a rim
RIM_HEIGHT = 0.2   ; distance between surface of brake disc and vertical surface of a wheel rim
```

To customize front or rear discs separately, use `[BRAKEDISC_FX_FRONT]` or `[BRAKEDISC_FX_REAR]`. Settings given as an example are default values in most cases.

### Debug settings

```ini
[BRAKEDISC_FX]
DEBUG = 0  ; set to 1 to highlight shape:
    ; • cyan is for the actual disc;
    ; • yellow is for the deepenings;
    ; • dark blue is for the inside part;
    ; • pink is for the outside part;
    ; • red is for the borders;
    ; • black is for holes.
WEAR_FORCE = 0.5  ; force certain wear level
GLOW_FORCE = 0.5  ; force certain glow level
```

### Other settings (not that recommended to change)

```ini
OVERRIDE_NORMAL_MAP = 1   ; set to 0 to use original normal map
OVERRIDE_DIFFUSE_MAP = 1  ; set to 0 to use original diffuse map
WEAR_MULT = 1.0           ; please do not change this one unless you want to set it to 0 or something; general multiplier might change in the future
GLOW_MULT = 1.0           ; adjust glowing intensity
ROUGHNESS = 0.2, 0.9      ; X and Y material roughness, giving that radial anisotropic specular

; Following material settings are in pairs: first number for new disc, second for worn. Default values depend on if it’s a ceramic or non-ceramic disc:
REFLECTION_F0 = 0.08, 0.44      ; base reflection intensity; ceramic: 0.16, 0.44
REFLECTION_SHARPNESS = 10, 200  ; aka ksSpecularEXP for reflection blurriness; ceramic: 10, 10
SPECULAR = 0.5, 1               ; specular intensity

```

Please avoid editing those, especially material settings, unless you need to recreate some unusual material. If it’s a regular metal or ceramic disc and default settings are not good, let’s discuss it instead. I would really want to see AC content becoming more standardised.

### Guessing

By default, patch would assign ceramic brakes to racing cars and open wheelers no earlier than 1990, and some sporty cars made after 2004–2010. [See also](cars-about-guessed-configs.md)

### Features to add later

- Adjust wear intensity.
