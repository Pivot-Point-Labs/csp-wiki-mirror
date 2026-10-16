# General Options

Some general extended physics options. All of these are for “surfaces.ini”:

```ini
[_EXTENSION]
REQUIRED_VERSION = 2000  ; Track can be set to require a certain version of CSP. Use it if you rely
                         ; on a certain CSP feature that was added in one of later builds.
```

### Timezone and coordinates

For Weather FX to function correctly, it’s always a huge help if track coordinates and timezone are set in “surfaces.ini”. Otherwise, CSP will try to guess, but sometimes it’s simply impossible, and it could lead to time of day online getting out of sync.

```ini
[WEATHER_FX]
LATITUDE = 36.25            ; Latitude in degrees, use a number (so 36° 15' becomes 36.25)
LONGITUDE = 121.5           ; Longitude in degrees, also use a number

; Use either name of the timezone:
TIMEZONE_ID = Europe/Paris  ; Timezone ID (TZ database name). If set like that, DST would be computed
                            ; automatically based on the current date, taking into account possible future updates.

; Or, explicit offset of the timezone:
TIMEZONE = 0                ; Offset from UTC in seconds; if DST is needed, add it here. For a track, setting ID is
                            ; a better option.
```

These settings, set in “surfaces.ini”, will override settings in track config, or any settings that might be shipped with CSP, and are a great way
to make things more robust overall. And unlike other options mentioned, this one doesn’t require to enable extended physics at all.

### Defaults

These options are enabled by default, but can be disabled if needed:

```ini
[_EXTENSION]
REAL_MASS_ONLINE = 1                    ; Use real mass for rigidbodies of remote cars online
ALIGNED_CARS_POSITIONING = 1            ; Orient cars along surface normal when positioning (improves
                                        ; stability on tilted surfaces)
RANDOMIZED_CARS_POSITIONING = 0.1, 0.1  ; Slightly randomize car positions and orientations when
                                        ; when positioning. First value in meters randomizes position,
                                        ; second is for orientation.

PIT_ALTITUDE = 0          ; based on pits, set real altitude of a track in meters, see at the end for another method
```

Also, enabling custom track physics automatically activates box collider detection for [dynamic physics objects](tracks-dynamic-physics-objects.md).

### Base collision tweaks (disabled by default)

```ini
[_EXTENSION]
RIGID_FLOOR_COLLISIONS = 0  ; Use rigid (hard) collisions with floor
RIGID_WALLS_COLLISIONS = 0  ; Use rigid (hard) collisions with walls
RIGID_DIRT_COLLISIONS = 0   ; Use rigid (hard) collisions with dirty floor areas
```

It’s not that good of an idea to use any of it, but it might help with cars falling through ground. For more precise configuration check out [separate post about configuring collision parameters in detail](tracks-collision-parameters.md).

### Integrity verification

Track can verify integrity of some of its files:

```ini
[_VERIFY_INTEGRITY_...]
ONLINE_ONLY = 0   ; Set to 1 to verify file only in an online race
FILE = …          ; File path relative to track’s data folder
CHECKSUM = …      ; SHA256 checksum
```

You can use an online tool [like this]( https://emn178.github.io/online-tools/sha256_checksum.html) to generate a checksum.

### Permissions

Tracks with extended physics can grant additional permissions to other things like Lua scripts:

```ini
[_SCRIPTING_PHYSICS]
ALLOW_TRACK_SCRIPTS = 0     ; Allow track scripts to access physics API
ALLOW_DISPLAY_SCRIPTS = 0   ; Allow track display scripts to access physics API
ALLOW_NEW_MODE_SCRIPTS = 0  ; Allow new mode scripts to access physics API
ALLOW_TOOLS = 0             ; Allow tools scripts to access physics API
ALLOW_APPS = 0              ; Allow Lua apps to access physics API
ALLOW_TRACK_SCRIPTS_DYNAMIC_OBJECTS = 0  ; Set to 1 to any script to create and manipulate rigidbodies
                                         ; only (I doublt it would be easy to cheat with those)

[_EXTRA_PERMISSIONS]
ALLOW_CUSTOM_AI_MANIPULATION = 0  ; Set to 1 to allow custom AIs on this track
```

More information about custom AIs is available [here](other-things-custom-ai.md).

### Miscellaneous

For goofing around you can change the gravity, although currently that change would not apply online to make sure things are fair:

```ini
[_EXTENSION]
GRAVITY = -9.8
```

### Track Altitude

```ini
[ALTITUDE]
BASE = 0   ; set real altitude in meter, also based on pit0 position
```
