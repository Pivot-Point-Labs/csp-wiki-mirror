# Tyre Types

There are certain settings CSP tries to guess based on tyre names, but sometimes with custom tyre names it doesn’t work as expected (since it’s a racing sim, fallback tyre type is always a slick, which can make cars with tyres with unexpected names behave extra slippery during the rain).

Instead of learning all the guessing rules and tinkering with names, please consider adding a new `TYPE_HINT` parameter next to regular `NAME` and `SHORT_NAME`. Some types support optional modifiers set as `TYPE_HINT_MODIFIER` as well. Known values:

- `TREADED`: regular street tyres, good at driving on water or gravel.
- `VINTAGE_PERFORMANCE`: older sporty tyres.
- `RACING_TREADED`: racing tyres that can channel water away, but not good at gravel.
- `SLICK`: slick tyres, terrible on anything wet.
- `SEMISLICK`: semislick tyres, have some difficulties on wet surfaces.
- `RAIN`: actual rain tyres (if any present, CSP won’t generate rain tyres).
- `GRAVEL`: tyres for offroading (added in 0.2.4-preview1).
  - `TYPE_HINT_MODIFIER = RALLY1`: modern aggressive rally tyres.
- `ICE`: studded tyres (added in 0.2.5).
  - `TYPE_HINT_MODIFIER = RALLY`: more aggressive studs.
  - Other available parameters:
    - `_SFX_ICE_FORCE_MULT_K` = 0.4: base grip multiplier on ice.
    - `_SFX_ICE_DAMP_MULT_K` = 1.4: grip multiplier on snow.
    - `_SFX_ICE_BASE_SIZE` = 1400: load threshold (in kg) on each wheel. Below this threshold, grip increases proportionally to weight.
    - `_SFX_ICE_BASE_STIFF` = 0.0005: how quickly grip stops increasing once the load passes the 'base size' threshold.

Note: type `GRAVEL` activates SurfacesFX for the session. If track doesn’t have surface types set explicitly, CSP will guess surface type based on surface parameters, and also alter the way sand physics functions (before 0.2.8, it’d also alter grass physics).
