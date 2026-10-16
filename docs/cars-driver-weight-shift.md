# Driver Weight Shift for Karts

Driver shift is a new feature added in v0.1.80-preview428 (it was added some time before, but needed a revision, along with body flex). It allows for drivers to shift their weight left and right. In 99% cases you won’t need it (there are seatbelts) and even if you’d add it, with a weight of a car it wouldn’t make a difference, but if you’re making a lightweight kart, it might be useful. Drivers can shift weight by holding buttons or using VR or TrackIR head tracking.

To use it, add to `car.ini`:

```ini
[_EXTENSION_DRIVER]
MASS=75                 ; mass of a driver (should also be included in car mass, as usual)
SHIFT_RANGE=0.3         ; physical shift range
SHIFT_VISUAL_RANGE=0.5  ; visual shift range
NEGATIVE_MASS=1         ; if set to 1, neutral driver position won’t shift center of gravity
SHIFT_MULTIPLIER=0.25   ; how much of driver mass actually moves (drivers realistically would only move upper half of their torso)
```
