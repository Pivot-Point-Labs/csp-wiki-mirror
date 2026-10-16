# Enabling Extended Physics

To make sure everybody is racing in the same conditions, to use any features of extended track physics, you need to enable extended physics first. For that, open `surfaces.ini`, find `WAV_PITCH` of `[SURFACE_0]` section and add `extended-` to its value, like so:

```ini
[SURFACE_0]
KEY=PITS
…
WAV_PITCH=extended-0
…
```

The idea is that original AC, if it would encounter that `WAV_PITCH` value, would crash (because it can’t parse this value as integer). Custom Shaders Patch, on the other hand, would catch this value, stop AC from crashing and mark that the track can use extended physics. And this is the file that’s being checked for integrity with most online servers.
