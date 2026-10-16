# Optional parts

For years, the good way to do optional parts for a car that user could toggle is to add a wing, a setup item for it, and an associated animation hiding the object. While now, you could do things like using Scene API to toggle geometry, I feel like wings are still a better method: for example, they can alter aerodynamics as well, which could be great for things like optional roof. However, there is a bit of a flag: animation can’t really hide the geometry, so everything is still being drawn. To solve that, CSP can augment this approach a bit, and actually do hide things.

Generally speaking, you might not need to do anything, CSP should be able to parse most animations already. Check CSP log for “Looking for optional parts”, it should print out its process. If you see “Found”, it means that it managed to figure things out and will automatically show and hide things saving on draw calls and other expenses. And if your animation is named “roof.ksanim”, it should even switch [rain occlusion](cars-rain-occlusion-tweaks.md) automatically. Note: for CSP to consider entry hidden, it should have a scale of 5% or less of a normal scale, or be at least 40 meters away.

(By the way, if you were curious what is the best way to hide the geometry, I believe it’s to the scale to, let’s say, 0.1% of normal or less. When AC decides to draw a car, it draws everything inside of it, so moving things to ∞ isn’t going to save you a draw call, but a tiny scale at least means GPU wouldn’t have to spend time painting those pixels.)

(Nowadays, however, you can just use CM/Tools/Creator to generate efficient animations automatically.)

Still, you can configure things explicitly. Here’s how:

```ini
[WING_BASED_SWITCH_…] ; did you know you can use either “...” or “…” for this auto-increment trick to work? In UTF8, they both are three bytes, so it works out in code nicely.
WING = 0 ; 0-based wing index
POINT_0 = 0 ; point in animation, from 0.0 to 1.0 (requires at least 0.05 precision)
POINT_0_NODES = node0, node1, … ; list of nodes to show at this point of animation
POINT_1 = …
POINT_1_NODES = …
; you can add as many points as you need, but with 0.05 precision you’d realistically be limited to around 20
ALTER_SHAPE = 0 ; set to 1 to mark animation as altering shape, or to `RAIN_OCCLUSION`, and animation will generate an alternative rain occlusion map
```

A bit more rambling about what does “altering shape” mean: CSP builds a 2D depth map of a car from above and uses it for all sorts of things. In fact, there are two maps, one on GPU used for things like hiding sparks and rain drops inside the car — and than one is updated frequently and reacts to things like door animation — and another on CPU, used to figure out if camera is inside or outside the car (altering audio, rendering and a lot more). Setting `ALTER_SHAPE` to 1 would force CSP to update its CPU car heightmap, a somewhat expensive process so it’s not a thing by default. And it’ll update its GPU map automatically when an animation moves anyway.
