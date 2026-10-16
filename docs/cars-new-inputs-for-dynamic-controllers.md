# Dynamic Controller Updates

CSP adds new inputs that could be used in dynamic physics controllers (along with existing ones like `LATG`):

- `HEADLIGHTS`;
- `CLUTCH`;
- `HANDBRAKE`;
- `HORN`;
- `GEAR_ALT`: unlike original `GEAR`, this one does not go through neutral when shifting;
- `LIGHT_EXTRA_A`;
- `LIGHT_EXTRA_B`;
- `LIGHT_EXTRA_C`;
- `LIGHT_EXTRA_D`;
- `LIGHT_EXTRA_E` (added in 0.1.76);
- `LIGHT_EXTRA_F` (added in 0.1.76);
- `AXLES_DIFFERENCE_RELATIVE`: relative difference in angular speed of axles (averaging wheels angular speed);
- `AXLES_DIFFERENCE_ABSOLUTE`: absolute difference;
- `AXLES_DIFFERENCE_SIGNED`: above zero if front axle spins faster than rear one;
- `FRONT_AXLE_DIFFERENCE_RELATIVE`: relative difference in angular speed of front wheels;
- `FRONT_AXLE_DIFFERENCE_ABSOLUTE`: absolute difference;
- `FRONT_AXLE_DIFFERENCE_SIGNED`: above zero if left wheel is faster;
- `REAR_AXLE_DIFFERENCE_RELATIVE`: same, but for rear axle;
- `REAR_AXLE_DIFFERENCE_ABSOLUTE`;
- `REAR_AXLE_DIFFERENCE_SIGNED`;
- `DAMAGE_ENGINE`: from 0 to 1 (added in 0.1.76);
- `DAMAGE_GEARBOX`: from 0 to 1 (added in 0.1.76);

Also, since 0.1.77 car physics can use Lua script which can access car state, do its computation and set 8 different values:

- `SCRIPT_0`;
- `SCRIPT_1`;
- `SCRIPT_2`;
- `SCRIPT_3`;
- `SCRIPT_4`;
- `SCRIPT_5`;
- `SCRIPT_6`;
- `SCRIPT_7`;

The number of script controllers was increased to 256 (0-255), in CSP version 0.2.1.
