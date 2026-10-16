# Sparks

Sparks are emitted during collisions, from collision point along a plane tangent to track’s collider surface. Well, that’s how it’s supposed to work.

Look, behavior and lifespan of particles could be adjusted for different colliders. By default patch uses what’s supposed to be steel-like sparks for regular cars and assumes car body is from carbon for open wheelers, so they don’t get any sparks from regular collisions. Patch also tries to find a collider for skidpad (should be centered on X axis, longer than 1.8 meters and less than 1 meter in width) and treat it as made out of steel, for cars made before 1994, or titanium for cars made after 2014. Of course, a lot of those settings can be explicitly set via config, although, as always, I would recommend to set as few settings as possible, and keep if semantical instead of, for example, setting colors.

Since most settings are collider-specific, you can also set them in data/colliders.ini.

### Syntax

```ini
[PARTICLES_FX]
SPARKS_AS = STEEL 			; base material tags for all the colliders including collider.kn5
BODY_SPARKS_AS = CARBON 	; material tags for collider.kn5
COLLIDER_0_SPARKS_AS = TITANIUM, SKIDPAD ; material tags for COLLIDER_0 in colliders.ini
COLLIDER_1_SPARKS_AS = IRON ; material tags for COLLIDER_0 in colliders.ini
```

### Guessing

Settings listed in **Syntax** paragraph are the ones used by default for all cars.

### Features to add later

- LIST_OF_FEATURES.
