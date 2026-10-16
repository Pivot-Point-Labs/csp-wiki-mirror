# Exhaust Smoke

Exhaust smoke template (incomplete)

Usable parameters:
```SPREAD, GROW, STARTING_SIZE, SPAWN_OFFSET, LIFE, SPEED, INTENSITY,  SPEED_THRESHOLD```
Use two values rather than one. First one is for coasting, and second is for gas fully pressed (after GAS_LAG is applied)

```ini
[BASIC]
DIESEL_ENGINE = 0 		; or 1

[PARTICLES_FX_EXHAUST_...]
POSITION = -0.56, 0.28, -2.1 		; self explanatory
DIRECTION = 0, 0.3, -1 			; self explanatory
COLOR = 0.75,0.8,1 			; RGB blend - 0,0,0 is black, 1,1,1 is white
LIFE = 1, 2 				; how long particles last in the air before disappearing
SPEED = 0.5, 1 				; how fast smoke particles fly from the exhaust
SPREAD = 0.25				; initial spread of particles
STARTING_SIZE = 0.04			; initial size of particles
SPAWN_OFFSET = 0.02			; initial spawn point offset (length-wise)
INTENSITY = 0.3, 0.5			; smoke intensity
TEMPERATURE_LAG = 1 			; engine heating up (1 to disable)
SPEED_THRESHOLD = 15, 100 		; speed at which the smoke disappears
```



Default values:
```cpp
float2 p_spread_k = {0.25f};
float2 p_grow_k = {-0.4f};
float2 p_starting_size = {0.03f};
float2 p_spawn_offset = {0.02f};
float2 p_life = {1.6f, 2.f};
float2 p_speed = {0.4f, 0.8f};
float2 p_intensity = {0.2f, 0.4f};
float2 p_temperature_threshold = {40.f, 60.f};
float2 p_speed_threshold = {5.f, 20.f};```
