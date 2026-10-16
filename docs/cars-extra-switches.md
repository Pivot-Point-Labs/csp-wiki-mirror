# Extra Switches

Cars can define up to four extra switches (or up to six switches since 0.1.76), generally referred to as EXTRA_A, EXTRA_B, etc. Users can set buttons associated with each switch in controls settings, in Patch section of Content Manager. In controls.ini they’re referred to as `__EXT_LIGHT_A`, `__EXT_LIGHT_B`, etc., because originally they were mainly meant for extra lights.

Those switches can be used as inputs for analog or digital instruments, emissive entries or animations. Also, they are available to Lua scripts as car.extraA, car.extraB, etc. And you can also use them in dynamic controllers if extended physics is activated as `LIGHT_EXTRA_A`, `LIGHT_EXTRA_B`, etc.

Since 0.1.76, extra switches can also be configurable:

```ini
[EXTRA_SWITCHES]
SWITCH_A = Role   ; Role of a switch shown during loading (optional)
SWITCH_A_FLAGS =  ; Switch flags (optional)
```

Available switch flags:

- `HOLD_MODE`: changes default behaviour from acting like a toggle to being active only when button is pressed;
- `STATIONARY_ONLY`: can be changed only if car is not moving;
- `NEURAL_GEAR_ONLY`: can be changed only in a neutral gear;
- `REQUIRES_BRAKE`: can be changed only if brake pedal is pressed;
- `KEEP_ON_RESET`: do not switch off when car teleports (added in 0.3.0-preview123).
