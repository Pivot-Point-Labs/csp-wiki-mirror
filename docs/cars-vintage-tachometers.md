# Vintage Tachometers

First of all, it’s not a bug, [they do work like this](https://www.youtube.com/watch?v=klptXsXwCjI). :D

And, of course, it can be disabled in patch settings if needed. The whole thing allows for tachometer to move in steps as well as to get some inertia for its needle, [which might be useful for some other cases](https://youtu.be/qlwNLkbd9lQ?t=108).

### Syntax

```ini
[INSTRUMENTS]
RPM_VINTAGE = 0              ; set to 1 to enable the whole thing
RPM_VINTAGE_ROUND_TO = 413   ; to what RPMs needle should snap
RPM_VINTAGE_DELAY = 0.5      ; delay between updates
RPM_VINTAGE_SPEED_LAG = 0.4  ; inertia value, from 0 to 1 (needle won’t move with 1)
RPM_VINTAGE_LIMIT = 0        ; set to some value to add upper bound if needed
```

Those settings would give you impulse tachometers. If you want instead needle not to snap, but to wobble around because of itertia, you can use something like this:

```ini
[INSTRUMENTS]
RPM_VINTAGE = 1
RPM_VINTAGE_ROUND_TO = 1
RPM_VINTAGE_DELAY = 0
RPM_VINTAGE_SPEED_LAG = 0.95
```

You can change those settings during the race or replay to adjust them more nicely.

### Guessing

Guesser would enable it for cars from 1947 to 1983 for race cars (with more conditions inside, depending on if car is open-wheeler or not, or on its country of manufacturing), or for British street cars manufactured from 1955 to 1969. Not a great system, of course, but in general it works, and for specific cases, configs are always available. If you have any suggestions on how to tweak it though, let us know.
