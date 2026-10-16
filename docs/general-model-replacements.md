# Model Replacements

Model replacements allow to remove, replace or insert bits of 3D models. For example, could be useful for tweaking original Kunos models without editing any KN5 files (for example, adding street lights). Another possible application is to replace car parts for certain skins, so, for example, certain skin could have something like different rims.

### Syntax

```ini
[MODEL_REPLACEMENT_...]
ACTIVE = 1        ; set to 0 to disable the whole section (default value is 1)
FILE = model.kn5  ; name of KN5 to work with (to distinguish between LODs or track KN5s)
SKINS = red?      ; list of skins to use replacement with (only for cars)

; To remove certain meshes or whole nodes containing meshes (optional):
HIDE = name1, name2  ; meshes or nodes to hide (no protected meshes)

; To insert a new 3D model (optional; but when using this, you need either INSERT_AFTER or INSERT_IN):
INSERT = new_model.kn5       ; name of KN5 to insert, should be located next to config file
INSERT_AFTER = node_or_mesh  ; node/meshmesh, after which new KN5 will be inserted
INSERT_IN = COCKPIT_HR       ; or, name of node to insert KN5 in, after the rest of its content
                             ; use one of those (if necessary, you can use both at once though)

; Extra insertion options:
MULTIPLE = 0  ; set to 1 to allow new model to be inserted more than once (by default it would only
              ; be inserted in the first found node either from INSERT_AFTER or INSERT_IN filter)
MERGE = 0     ; set to 1 to enable merge together nodes with the same names insted of duplicating them

; Options to transform inserted model:
SCALE = 1, 1, 1     ; change size: X, Y and Z axis (for car, X is left-right, Y and up-down)
ROTATION = 0, 0, 0  ; rotate: heading, pitch and roll, in degress
OFFSET = 0, 0, 0    ; move: X, Y and Z axis, in meters
```

Note: you cannot use HIDE= on any physical active "protected" meshes, like 1ROAD... or AC_POBJECT..., however you can hide them from view with [mesh adjustments](mesh-adjustment.md)

Most of those options have been added in v0.1.60, previous versions only had `FILE`, `HIDE`, `INSERT` and `INSERT_AFTER`.

If you’re replacing some exterior part of a car, keep in mind lower LOD models. And, of course, if you’re inserting new models to tracks, don’t forget to setup LOD distances. Also, just in case, whole thing wouldn’t work for meshes and nodes with names starting with “AC_” or digits, or containing “WALL”, to make sure this option couldn’t be used for cheating.

# Config templates

*Config templates are configs with some helpful stuff in them, allowing to set things up faster and easier, generating most of boilerplate automatically.*

### Custom rims (common/custom_rims.ini)

Helps to quickly replace rims for a car, needs a KN5 with a single wheel, which should be aligned like that:

<a href="https://i.imgur.com/pqfeIJi.png" target="_blank"><img src="https://i.imgur.com/pqfeIJi.png" width=400 /></a>

Here is an example of it in action for Miura:

```ini
[INCLUDE: common/custom_rims.ini]

[ReplaceRims]
File = lamborghini_miura_sv.kn5  ; name of KN5
OriginalRims = RIM_?             ; list of original rims to hide
Model = rim.kn5, 0.276, 0.238    ; KN5 with a new rim, its radius and width
Offset = 0, -0.03                ; offset for front and rear wheels (negative value move rim deeper inside)

[ReplaceRims]
File = lamborghini_miura_sv_LOD_B.kn5
OriginalRims = RIM_?
Model = rim_B.kn5, 0.276, 0.238
Offset = … ; and so on
```

If needed, you can also set `Radius` and `Width` to specify dimensions of inserted rim, but by default, config would use `RIM_RADIUS` and `WIDTH` from “tyres.ini”. Values `Offset`, `Radius` and `Width` can be either single or double: if single, they would affect both sides, if double, first value would be used for front wheels and second for rear wheels.

Whole thing can be limited to a certain side with `FrontOnly = 1` or `RearOnly = 1`. Keep in mind, you can use `[ReplaceRims]` more than once because those are [INIpp templates](https://github.com/ac-custom-shaders-patch/inipp).

Also, you can use `Skins` to set filter or list of skins for custom rims to be used with.
