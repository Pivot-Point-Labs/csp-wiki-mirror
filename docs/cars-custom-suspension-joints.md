# Cars: Custom suspension joints

### **Deprecated; please see COSMIC Suspension for better solution**

Highly experimental option for altering suspension geometry, which might help with some unusual cases. Please be very careful when setting it up and consider disabling FFB first just in case.

All changes are done in “suspensions.ini”, file can be edited live (making things even more unstable: definitely disable FFB before doing that).

### Adding new links

```ini
[_EXTRA_LINK_...]
TYPE = DISTANCE     ; possible values: FIXED, BALL, SLIDER, DISTANCE
FROM = BODY         ; possible values: BODY, HUB_LF, HUB_RF, HUB_LR, HUB_RR
TO = HUB_LF         ; possible values: BODY, HUB_LF, HUB_RF, HUB_LR, HUB_RR
CFM = 0.0000001     ; constraint force mixing
ERP = 0.3           ; error correction parameter
DEBUG_COLOR = R, G, B ; optional color for debug render

; And connection points (body ID and coordinates relative to it):
ANCHOR = BODY, X, Y, Z    ; position for BALL joint
AXIS = BODY, X, Y, Z      ; direction for SLIDER joint
FROM_POS = BODY, X, Y, Z  ; first point for DISTANCE joint
TO_POS = HUB_LF, X, Y, Z  ; second point for DISTANCE joint
```

#### Joint types

- `FIXED`: simple fixed joint ensuring the constant relative position and orientation (special CFM and ERP values can make it softer);

- `BALL`: connection via freely spinning socket ensuring constant distance between objects, uses `ANCHOR` point for rotating around:

  <img src="https://files.acstuff.ru/shared/hcP7/20221025-145018.png" width="200">

- `SLIDER`: basic slider connection, uses `AXIS` direction for sliding:

  <img src="https://files.acstuff.ru/shared/zZBk/20221025-145332.png" width="200">

- `DISTANCE`: connection ensuring distance between points, uses `FROM_POS` and `TO_POS` values:

  <img src="https://files.acstuff.ru/shared/PbU1/20221025-145918.png" width="200">

#### About CFM and ERP

Those values regulate rigidity and damping of a joint. For more details please consult [ODE guide](http://ode.org/ode-latest-userguide.html#sec_3_8_0).

### Altering original AC joints

Usually simply adding new joints on top of existing ones would only fix geometry in a certain position making the whole thing pretty unusable. But with this thing you can also alter existing joints or even completely disable them. Again, please be very careful with the whole FFB thing when doing so.

First, you need to get the description of original joints. To do that simply add this to “suspensions.ini”:

```ini
[_AC_LINK_ALTERATION]
PRINT_OUT = 1
```

And CSP would print out the list of existing joints in “Documents/Assetto Corsa/logs/custom_shaders_patch.log” (search for “Printing out original AC links” header). Knowing joints, their types and indices you can now alter their parameters like so:

```ini
[_AC_LINK_ALTERATION_...]
WHEELS = …      ; list of wheels to affect
LINKS = …       ; list of zero-based joint indices to affect
DEACTIVATE = 0  ; set to 1 to completely deactivate a joint
CFM = …         ; if set, alters joint’s constraint force mixing value
ERP = …         ; if set, alters joint’s error correction parameter
```

Available keywords for `WHEELS`:

- `LF`, `RF`, `LR`, `RR`;
- `LEFT_FRONT`, `RIGHT_FRONT`, `LEFT_REAR`, `RIGHT_REAR`;
- `LEFT`, `RIGHT`, `FRONT`, `REAR` (affecting two wheels at once);
- `ALL` (affecting all wheels).
