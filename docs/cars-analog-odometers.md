# Analog Odometers

Analog odometers are the rolling-digit kind, with each wheel slowly cranking up to the next number as the car moves. The whole thing is rendered into a dynamic texture, so the only thing the model needs to provide is a flat mesh (or a piece of texture) for the digits to be drawn onto — no separate meshes per digit, no fiddling with parented nodes.

There are two predefined sections, `[ODOMETER_MAIN]` and `[ODOMETER_TRIP]`, both wired to the saved driven distance for the current car (so they keep counting between sessions). Apart from that, you can add up to ten extra ones with `[ODOMETER_0]`…`[ODOMETER_9]`, useful for cases like cars with two trip counters or a separate display in the dashboard.

### Syntax

```ini
[ODOMETER_MAIN]
NAME = ODOMETER_MAIN_DIGITS    ; mesh to draw digits onto (or use MESHES = … for a filter)
POSITION = 8, 8                ; X, Y of the top-left corner, in texture pixels
SIZE = 240, 56                 ; width and height of the digits area, in texture pixels
COUNT = 6                      ; number of digits (default: 6 for main, 5 for trip)
DIGIT_WIDTH = 36               ; width of a single digit glyph, in texture pixels
FONT = 599_big                 ; font to use (looks for a font in content/fonts, but first, looks for `<FONT>.txt` and `<FONT>.png` in car/extension folder)
FONT_SCALE = 1                 ; extra scale for the font glyphs
FONT_OFFSET = 0                ; vertical offset for glyphs inside the digit cell
COLOR = 1, 1, 1                ; digits color
BACKGROUND = 0.12, 0.12, 0.12  ; background color behind the digits
MOVEMENT_INTERVAL = 1          ; how many units of value cause one full digit roll
JITTER = 0                     ; 0..1, adds a bit of misalignment between wheels
ROTATION = 0                   ; rotation around the center of the digits area, degrees
SCALE = 1, 1                   ; extra scale around the center of the digits area
```

`NAME` and `MESHES` work the same way as for [LED panels](cars-led-panels.md) and other dynamic-texture-based things — `NAME` is a shortcut for a single mesh, while `MESHES` allows for a regular mesh filter. As usual, instead of `POSITION`, you can use `CENTER` if it’s easier to align it that way.

If you don’t need a customized look, that’s about it. The texture will be picked up automatically (or generated, if it’s not already there as a dynamic texture for that mesh), and the value will be pulled from the saved driven distance.

### Trip and extra odometers

For `[ODOMETER_TRIP]`, value is multiplied by 10 by default, which is what you usually want — that way, the last digit shows tenths of a kilometer (or a mile, depending on units). If you want to change that behavior on a custom odometer, use `TRIP_MODE`:

```ini
[ODOMETER_0]
NAME = ODOMETER_TOTAL_2
TRIP_MODE = 0  ; show whole units only, like the main odometer
```

By default, extra odometers (`[ODOMETER_0]`…`[ODOMETER_9]`) inherit the current value from `[ODOMETER_MAIN]` if `TRIP_MODE` is set to 0, so they stay in sync with it. Otherwise, they start counting from zero when the session starts (just like `[ODOMETER_TRIP]`), which makes them useful as additional trip counters.

If, for whatever reason, you need a non-decimal multiplier (a mile odometer next to a km one, for example), use `OUTPUT_MULT`:

```ini
[ODOMETER_0]
NAME = ODOMETER_MILES
OUTPUT_MULT = 0.621371  ; convert km to miles
```

`UPPER_BOUND` is also available — by default, it’s set to `10^COUNT - 1`, so the value will roll over once it exceeds what the wheels can show. You can lower it if you need different behavior.

### Last digit highlight

Quite often, the last (rightmost) digit on a real odometer has a different background color, marking it out as the fractional one. That’s easy to set up:

```ini
[ODOMETER_TRIP]
…
LAST_DIGIT_COLOR = 1, 1, 1                  ; color of the last digit (default: same as COLOR)
LAST_DIGIT_BACKGROUND = '#a01818'           ; background under the last digit
LAST_DIGIT_BACKGROUND_LOCATION = 200, 40    ; X position and width of that background, in texture pixels
                                            ; default: covers exactly the last digit cell
```

If `LAST_DIGIT_COLOR` and `LAST_DIGIT_BACKGROUND` are both left at defaults, no extra background is drawn at all.

### Blend mode

By default, the odometer area is fully redrawn each frame: background fills the whole `SIZE` rectangle, then digits go on top. That’s the simplest case and it works well if the texture region is dedicated to the odometer.

If you want digits to be drawn on top of an existing image — say, a faceplate texture with a printed window for the wheels, or a stylized background that’s baked into the dynamic texture by something else — set `BLEND_MODE = 1`. Then `BACKGROUND` is ignored and the original texture content shows through between the glyphs:

```ini
[ODOMETER_MAIN]
…
BLEND_MODE = 1
```

In this mode, the last digit highlight (if used) will also blend over the existing image, so make sure to tweak `LAST_DIGIT_BACKGROUND` accordingly.

### Tips

- If digits look misaligned vertically, tweak `FONT_OFFSET` first, then `FONT_SCALE`. Default font is `599_big`;
- If wheels move too fast or too slow between digits, raise or lower `MOVEMENT_INTERVAL` — it controls how much of the input value corresponds to a single full roll of the rightmost wheel;
- A small amount of `JITTER` (something like 0.05) helps to avoid the “too perfect” look of digits all aligning at the same time, mimicking real mechanical wear;
- To turn an odometer off without removing the section (handy while debugging configs), use `ACTIVE = 0`;
- Saved value for `[ODOMETER_MAIN]` lives in `extension/state/odometers.ini`. CSP also checks Content Manager’s `__CM_DRIVEN_DISTANCE` and Sidekick’s odometer file, picking the highest value of those, so the count won’t reset when switching between tools.
