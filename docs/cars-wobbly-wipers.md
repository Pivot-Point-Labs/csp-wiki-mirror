# Wobbly Wipers

If a car has wiper animations, they could also be used to add wipers vibrating on higher speeds.

### Syntax

```ini
[WIPERS]
WIND_THRESHOLDS_KMH = 60, 150  ; speed for wipers to start vibrating and for maximum vibration
WIND_AMPLITUDE_MULT = 1        ; multiplier for amplitude
WIND_FREQUENCY_MULT = 1        ; multiplier for frequency
WIND_OFFSET = 0.03             ; base animation progress to vibrate around
```

`WIND_OFFSET` is needed, because animation for wipers doesn’t start moving at the first frame, so wobbling it in first frames often results in no visible motion at all. That value adds some base animation progress around which, wipers wobble, and resulting offset gradually grows from 0 to `WIND_OFFSET` as speed grows from 0 to `WIND_THRESHOLDS_KMH`.

### Guessing

Settings listed in **Syntax** paragraph are the ones used by default for all cars.

### Features to add later

- Guess thresholds/amplitude mult. based on production year;
- Add response to G-forces or uneven surfaces.
