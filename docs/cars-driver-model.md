# Driver Model

Few options affecting driver model.

### Shadowed driver

If you’re not using [vertex ambient occlusion](https://github.com/ac-custom-shaders-patch/acc-bakeryoptix), another way to stop driver head from glowing (without occlusion it looks way too bright from exterior cameras) is to set a virtual occlusion sphere above driver head:

```ini
[SHADOWED_DRIVER]
OPACITY = 0.7       ; shadow opacity
OFFSET = 1          ; how high is the sphere above driver head
RADIUS_INNER = 1    ; inner fully shadowed radius
RADIUS_OUTER = 1.6  ; outer not-at-all shadowed radius
```

### Replace driver model

This particular tweak can be useful for a custom skin using a different driver model:

```ini
[DRIVER3D_MODEL]
NAME = driver_80  ; file name from content/drivers (without “.kn5” extension)

; Don’t forget to list to hide:
[DRIVER3D_HIDE_OBJECT_...]
NAME = DRIVER:HELMET_SUB0
```
