# Audio

With patch, you can alter volume or pitch of specific audio events, alter events’ input parameters, or use extra parameters in your soundbank.

### Syntax

That’s how volumes can be adjusted:

```ini
[AUDIO_VOLUME]
ENGINE_EXT = 1.0
ENGINE_INT = 1.0
GEAR_EXT = 1.0
GEAR_INT = 1.0
BODYWORK = 1.0
WIND = 1.0
DIRT = 1.0
DOWN_SHIFT = 1.0
HORN = 1.0
GEAR_GRIND = 1.0
BACKFIRE_EXT = 1.0
BACKFIRE_INT = 1.0
TRACTION_CONTROL_EXT = 1.0
TRACTION_CONTROL_INT = 1.0
TRANSMISSION = 1.0
LIMITER = 1.0
TURBO = 1.0

; New options added in 0.1.67:
HIT = 1.0
SCRAPE = 1.0
WHEEL = 1.0
SKID_EXT = 1.0
SKID_INT = 1.0
```

Similarly, pitch can be adjusted as well (added in 0.1.67):

```ini
[AUDIO_PITCH]
ENGINE_EXT = 1.0
ENGINE_INT = 1.0
GEAR_EXT = 1.0
GEAR_INT = 1.0
BODYWORK = 1.0
WIND = 1.0
DIRT = 1.0
DOWN_SHIFT = 1.0
HORN = 1.0
GEAR_GRIND = 1.0
BACKFIRE_EXT = 1.0
BACKFIRE_INT = 1.0
TRACTION_CONTROL_EXT = 1.0
TRACTION_CONTROL_INT = 1.0
TRANSMISSION = 1.0
LIMITER = 1.0
TURBO = 1.0
HIT = 1.0
SCRAPE = 1.0
WHEEL = 1.0
SKID_EXT = 1.0
SKID_INT = 1.0
```

Also, since 0.1.67 you can apply LUTs to input parameters like so:

```ini
[AUDIO_PARAMETER_TRANSFORM]
; Originally, AC would sent 10000 to soundbank, but now it’ll send 5000 instead. Or,
; it’ll send 2500 instead of 5000 — values in-between these points are linearly interpolated.
ENGINE_EXT_RPMS = (| 0=0 | 10000=5000 |)
```

Supported parameters:

- ENGINE_EXT: ENGINE_EXT_RPMS, ENGINE_EXT_THROTTLE;
- ENGINE_INT: ENGINE_INT_RPMS, ENGINE_INT_THROTTLE;
- GEAR_EXT: GEAR_EXT_STATE;
- GEAR_INT: GEAR_INT_STATE;
- BODYWORK: BODYWORK_SUSP_TRAVEL_SPEED;
- WIND: WIND_SPEED, WIND_AIR_PRESSURE;
- DIRT: DIRT_SPEED, DIRT_DIRTINESS;
- BACKFIRE_EXT: BACKFIRE_EXT_THROTTLE;
- BACKFIRE_INT: BACKFIRE_INT_THROTTLE;
- TRACTION_CONTROL_EXT: TRACTION_CONTROL_EXT_DECAY;
- TRACTION_CONTROL_INT: TRACTION_CONTROL_INT_DECAY;
- TRANSMISSION: TRANSMISSION_DRIVETRAIN_SPEED, TRANSMISSION_THROTTLE;
- LIMITER: LIMITER_DECAY;
- TURBO: TURBO_BOOST, TURBO_BOV, TURBO_BOV_DECAY;
- HIT: HIT_IMPACT_ANGLE, HIT_IMPACT_SPEED;
- SCRAPE: SCRAPE_SPEED, SCRAPE_DECAY;
- WHEEL: WHEEL_BRAKE, WHEEL_SPEED, "WHEEL_INFLATION, WHEEL_SUSPENSION_DAMAGE.

Another feature is that you can add new parameters in audio soundbanks:

```ini
[AUDIO_PROPERTIES]
TURBO_THROTTLE = 1    ; for turbo sound, “throttle” input, same as in engine event
ENGINE_EXT_BOOST = 1  ; for exterior engine sound, “boost” input, same as in turbo event
ENGINE_INT_BOOST = 1  ; for interior engine sound, “boost” input, same as in turbo event
```

### New sound events

Patch adds new car sound event as well:

- `/transmission_ext`: similar to `transmission` event, but for exterior;
  - Parameters: `drivetrain_speed` and `throttle`, same as with `transmission` event.

Also, there are some events which could be customized in soundbank, but if they’re missing, generic ones will be used:

- `/wiper_ext`: sound of moving wipers car for exterior cameras;
  - Parameters: `state` for animation status, to sync wipers movement with sound;
- `/wiper_int`: sound of moving wipers car for interior cameras;
  - Parameters: `state` for animation status, to sync wipers movement with sound.

### Features to add later

- More events to adjust;
- New car sound events (?);
- More parameters for new soundbanks (?).
