# Enabling Extended Physics

Unlike all other features focused on compatibility with original AC, all physics extensions require specifically modified car data: this way, none of existing cars behave any differently and cars utilizing new features won’t work in AC without the patch.

Support for new features can be found on the AC Custom Shaders discord server in the cphys-support-only or mod-talk channels.

Please refer to each of the pages (Aerodynamics, Suspension, etc.) for information on the features and their implementation. Note: all feature lists and example code will be kept up to date as best as possible - there will be no support for deprecated features.

---

To make sure everybody is racing in the same conditions, to use any features of extended car physics, you need to enable extended physics first. For that, open `car.ini`, find `[HEADER]` section and add `extended-` to `VERSION` value as prefix, like so:

```ini
[HEADER]
VERSION=extended-2
```

For version locking (1.74+ only)

```ini
[HEADER]
VERSION=extendedV2-1 ;still can have 1 or 2 at the end

[_EXTENSION]
REQUIRED_VERSION=2142 ;this is using the 1.79 version code as an example. Can be found easily in CM->Settings->CSP->About, titled "Shaders Patch version ID"
```

The idea is that original AC, if it would encounter that `VERSION` value, would crash (because it can’t parse this value as integer). Custom Shaders Patch, on the other hand, would catch this value, stop AC from crashing and mark loading car as a car which can use extended physics.
