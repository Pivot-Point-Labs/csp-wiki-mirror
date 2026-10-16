# Wobbly Bits

Wobbly bits feature helps to move nodes according to G-forces and gravity direction. Could be used for front wings oscillating after hitting a bump, or for meshes on driver’s window, or for things that might hang from rear view mirror.

You can think of it similar to how needles move with analog instruments. Set the name of node to move, specify a point it’s bound to, and it would start moving around.

If you want your mesh to flex, it should be skinned. Bind one end to some bone, and then move that bone with `WOBBLY_BIT_N` section. And if there is no need for flexing — let’s say, it’s some toy hanging from rear view mirror — you can just wobble its parent node.

### Syntax

```ini
[WOBBLY_BIT_0]
NAME = FRONT_SPOILER_LEFT_SIDE  ; name of the node to move
CONNECTED_TO = 0, 0.148, 1.86   ; point to which node is attached to, and around which it will rotate
MAX_RANGE = 0.05                ; max range node can move from its original position
DAMPENING_LAG = 0.93            ; think of it as usual AC lag value, trying to zero node’s speed
G_GAIN = 2                      ; how much G-forces affect node’s speed
GRAVITY_GAIN = 3                ; how much gravity affects node’s speed
OFFSET_GAIN = 2000              ; how strong is returning force
STIFF_AXIS = 0, 0, 1            ; optional higher stiffness axis to reduce movement along it
STIFF_AXIS_STIFFNESS = 0.7      ; now stiff is optional stiffness axis
G_FILTER = 0                    ; temporal filter for G-forces
DEFAULT_GRAVITY_INCLUDED_ALREADY = 1 ; either `0` or `1`; set it to `1` if you don’t want gravity to skew your stuff when car is in neutral position
```

As you can see, there is nothing physically accurate about it. But it’s more flexible this way.

If you want your piece to flap around as if there is no stiffness, you can start with something like that:

```ini
MAX_RANGE = 1         ; to remove any boundaries
DAMPENING_LAG = 0.99  ; to reduce friction
OFFSET_GAIN = 0       ; actual zero stiffness
G_GAIN = 2
GRAVITY_GAIN = 3
G_FILTER = 0
DEFAULT_GRAVITY_INCLUDED_ALREADY = 0
STIFF_AXIS_STIFFNESS = 0
```

### Guessing

Can’t guess this stuff, at least not yet.

### Features to add later

- Air affecting movement as well;
- Find a way to turn regular meshes to skinned for this to work;
- Extra options, or new feature, to simulate ropes behavior (?).
