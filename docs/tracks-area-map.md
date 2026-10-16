# Area Map

For some extra effects, CSP keeps takes a shot of a track around the camera, in particular, track height, surface color and occlusion. With that information, it’s possible to:
- Collide particles with track surface, walls and other geometry;
- Precisely align skidmarks and static tyre marks along track surface, even if physics surface is not aligned that well;
- Make sure dust particles and skidmarks match the color of underlying surface;
- Take occlusion into account when drawing skidmarks inside tunnels;
- Align dynamic (Lua-driven) track lines along the surface as well;
- And more.

To configure these maps explicitly, add:

```ini
[AREA_HEIGHT_MAP]
GEOMETRY_MATERIALS=…
GEOMETRY_MESHES=…
COLOR_MATERIALS=…
COLOR_MESHES=…
```

`GEOMETRY_…` ones are used for heightmap and occlusion samping, and `COLOR_…` ones are for coloring smoke, particles and skidmarks, so generally I’d advice to put grass, dirt, sand and such to `COLOR`, and all other meshes cars might possibly be over to `GEOMETRY`. For example, don’t put curbs as `COLOR`, or you might get red smoke going off them (although, CSP will filter out color in an extra step to be safe).

By default, CSP uses bounced light geometry as `GEOMETRY`, and grass and puddles as `COLOR`, and usually it should be working well. Just make sure bounced light geometry is configured correctly, and please don’t just use a `SURFACE_MATERIALS=?` unless your track is extra simple.

Since 0.3.0-preview331, there is a tool available on Objects Inspector you can use to verify those maps.
