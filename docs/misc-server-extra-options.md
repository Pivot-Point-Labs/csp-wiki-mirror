Update v0.1.69 brings an ability to add extra parameters to servers: a simple INI configuration file hidden in a welcome message. The way it works, message wouldn’t be visible to people with original Assetto Corsa or Assetto Corsa with CSP newer than v0.1.69.

# Available options

### Racing rules

It might be a good idea to set some strict limit for CSP version if you’re using those (setting it to at least 0.1.69 for basic options), to make sure everybody would race in the same rules and conditions.

```ini
[EXTRA_RULES]
ALLOW_WRONG_WAY = 1                  ; Allow cars to drive either way
MAX_METERS_WRONG_WAY = 100           ; Available since 0.2.0, maximum distance allowed to drive wrong way before penalty is applied

; Available since 0.1.76:
ENFORCE_BACK_TO_PITS_PENALTY = 1     ; Adds penalty during race when using back-to-pits AC command, same
                                     ; as when using “back to pits” in pause menu
ENFORCE_BACK_TO_PITS_STOP = 1        ; Stops back-to-pits AC command from working if car is moving

; Available since 0.1.77:
LIMIT_LOCK_CONTROLS_TIME = 60        ; Upper cap for each locking controls penalty in seconds
LIMIT_LOCK_CONTROLS_TOTAL_TIME = 90  ; Upper cap for total of locking controls penalty in seconds (on some
                                     ; large laps without it penalty might get so large rejoining server
                                     ; would be the only valid course of action)
UNFIT_FOR_DRIVETHROUGH_PENALTY = X, Y, Z, radius  ; Defines a sphere in which entering pits would not
                                     ; count as serving drivethrough penalty (like second pitlane on Spa,
                                     ; parameters for it are “-202.04, 12.54, -857.77, 50”)

; Available since 0.1.78 (previous versions had a bug, so please make sure to set 0.1.78 as required):
NO_BACK_TO_PITS = 1                  ; Disallow back-to-pits AC command and “back to pits” in pause menu
                                     ; (admin would still be able to teleport cars back if needed)
NO_BACK_TO_PITS_OUTSIDE_OF_PITS = 1  ; Same, but only if car is not in its pits position

; Available since 0.1.78:
INVALIDATE_LAP_TIME_IN_PITS = 1      ; Invalidate lap time if car ever goes through pits (for tracks with
                                     ; pitlane surfaces not marked as invalid)
REQUIRED_MODULES = lighting_fx, weather_fx  ; Optional list of required modules (just use the names of
                                     ; their configs), if set, live setting changes are disabled
REQUIRE_NEW_LAP_FOR_DRIVETHROUGH_PENALTY = 1 ; If set, drivers getting drivethrough penalty wouldn’t be
                                     ; able to just reverse back and do it here and now
HIDE_MAP = 1                         ; Hides default AC map app (users could still use third-party apps)

; Available since 0.1.79:
SLIPSTREAM_MULT = 1                  ; Can be used to increase or decrease the intensity of slipstream effect

DISABLE_RAIN_PHYSICS = 0             ; Set to 1 to disable rain physics

; Available since 0.2.1:
PITS_ORDER = F<TR>                   ; Fuel, Tires, Repair
                                     ; Angle brackets around things that can be done in parallel, default AC behaviour is <FTR>

; Available since 0.2.3:
SURFACES_FX = 0                      ; Enable the SurfacesFX module

; Available since 0.2.5:
DISABLE_AUTOBRAKING = 1              ; Enable the physics experiment to disable the autobrake

AFK_AUTOKICK = 5, OPTION             ; Time in minutes
                                     ; Available options, pick only one:
                                     ; SPEED: Cars travelling less than 0.4km/h on average
                                     ; INPUT: Monitors car inputs and mouse movements
```

### Pit speed limiter settings

Available since 0.1.76. Changes the way pit speed limiter works.

```ini
[PITS_SPEED_LIMITER]
DISABLE_FORCED = 1                              ; Disable forced pits speed limiter
KEEP_COLLISIONS = 1                             ; Activate collisions between cars in pits
SPEED_KMH = 80                                  ; Alter pits speed limiter value; default is 80
SPEEDING_PENALTY = DRIVE_THROUGH                ; Penalty for violation (for now, either DRIVE_THROUGH
                                                ; or TELEPORT_TO_PITS with locking controls)
SPEEDING_PENALTY_LAPS = 3
SPEEDING_SUBSEQUENT_PENALTY = TELEPORT_TO_PITS  ; Optional, stricter penalty for a second violation
SPEEDING_SUBSEQUENT_PENALTY_TIME = 30           ; How long controls will be locked, in seconds
```

### Custom Motion

Available since 0.1.77. This option replaces the way position for remote cars online is extrapolated. New implementation fixes an issue with car wheels detaching if car was to jump or flip, improves performance and smooths out cars motion a bit.

```ini
[EXTRA_TWEAKS]
CUSTOM_MOTION = 1, flags        ; flags are optional, separated by a comma
```

Flags:

- `SMOOTH`: available since 0.1.78, smooths out motion for cars moving slow to prevent shaking on large tracks.
- `RESET`: available since 0.2.3, resetting interpolation when car teleports (once tested and verified, might be enabled by default for all cars)


Also, available since 0.1.78, enabled custom motion allows to disable colliders for remote cars on jumps (caused by connection issues). Nearby cars with colliders disabled would flash blue. Colliders would be disabled for some time, but kept disabled if there is an ongoing contact, so that cars wouldn’t fly away from each other. Here is [this feature in action](https://files.acstuff.ru/shared/8pFk/20220427-225256.mp4) (camera focused on remote “laggy” car losing connection for a bit, collisions in pits enabled).

```ini
[EXTRA_TWEAKS]
JUMP_LIMIT = 0.3                ; Jump threshold in meters, fix is applied if remote car would suddenly
                                ; move further than that
JUMP_PAUSE_COLLISIONS_FOR = 5   ; For how long to disable collisions in seconds (default is 5)
```

### Emergency reset

Available since 0.1.78. Resets car back to pits if it is falling through ground or gets stuck in a wall somewhere.

```ini
[EMERGENCY_RESET]
FALL = 5                        ; Distance in meters, if car is below the ground more than that, it gets reset
COLLISION = 3                   ; Time in seconds, if car is stuck in a wall for more than that, it gets reset
PENALTY = 1                     ; If this optional parameter is set to 1, resetting would apply the same penalty
                                ; as manually teleporting to pits
```

### Extra data

```ini
[EXTRA_DATA]

; Available since 0.1.75:
TYRES_BLOWN_STATE = 0     ; Exchanges data on state of blown tyres for visual effects

; Available since 0.1.77:
CAMBER_TOE_STATE = 1      ; Exchanges toe and camber angles, requires enabled custom motion
CUSTOM_UPDATE_FORMAT = …  ; Custom servers can use custom protocols with variable refresh rate,
                          ; precision, batch packages, sending information about cars nearby more
                          ; frequently, etc.: actual description of those packages is given here
```

### Custom physics

Some basic physics tweaks that don’t require any custom physics stuff.

```ini
[CUSTOM_PHYSICS]
REAL_MASS = 1                    ; Set to 1 to set real mass for rigid bodies of remote cars, helps with collisions
                                 ; not working as expected (acts like multiplier for actual mass, could be above 1
                                 ; to get collisions extra bouncy or below 1 to get collisions extra soft)
EXTRAPOLATE_STATE = 1            ; Experimental option making all cars move smoother, not recommended to use

; Available since CSP 0.2.5
DISABLE_SURFACE_SNAPPING = 0,3,9 ; Comma separated list of pitbox indices (starting with 0)
                                 ; Disable the auto-snap of a vehicle to the ground. Useful for planes.

; Available since 0.1.77, servers now can completely redefine collision parameters. All the values are
; optional:
[CUSTOM_COLLISIONS]
SOFT_ERP = 0.99                  ; Error reduction parameter
SOFT_CFM = 0.0001                ; Constrain force mixing, the higher it is, the softer is the collision
BOUNCE = 0.01                    ; Bounce parameter
FRICTION = 0.25                  ; Contact friction
INTENSITY = 1                    ; Collision intensity (affects damage, audio and visual effects)
MAX_DEPTH = 0.2                  ; If set and collision depth is above that parameter, collision becomes hard: might
                                 ; help with performance
```

### Files verification

Available since 0.1.77. With this server can check existence and integrity of some AC files. You can use an online tool [like this]( https://emn178.github.io/online-tools/sha256_checksum.html) to generate a checksum.

```ini
[VERIFY_INTEGRITY_...]
FILE = content/cars/…           ; Path to a file relative to AC root folder
CHECKSUM = …                    ; SHA256 checksum

[EXTRA_TWEAKS]
VERIFY_STEAM_API_INTEGRITY = 1  ; Set to 1 to verify integrity of “steam_api64.dll”.
```

### Timezone

Available since 0.1.78. Allows to specify exact timezone offset in seconds, as well as latitude and longitude to ensure all clients would be in the same lighting conditions. By default CSP gets those values from its built-in database or track configs, but they might be out of date.

```ini
[WEATHER_FX]
TIMEZONE = 0                ; Offset from UTC in seconds; if DST is needed, add it here
LATITUDE = 36.25            ; Latitude in degrees, use a number (so 36° 15' becomes 36.25)
LONGITUDE = 121.5           ; Longitude in degrees, also use a number

; Available since 0.1.79:
TIMEZONE_ID = Europe/Paris  ; Timezone ID (TZ database name). If set like that, DST would be computed
                            ; automatically based on the current date, but setting offset explicitly
                            ; with “TIMEZONE” might be a better approach.
```

### Other online tweaks

Some random online tweaks.

```ini
[EXTRA_TWEAKS]
FORCE_HEADLIGHTS = 1            ; Forces headlights to stay on

; Available since 0.1.77:
SHOW_DISCONNECTED = 1           ; Show disconnected cars; set to WITH_COLLISIONS instead of 1 and other cars
                                ; could collide with them

; Available since 0.1.78:
ACTUAL_TRACK_TIME = 1           ; Set it to 1 if your time scale is close to 100%; used by things like train
                                ; script to sync their state across clients; without this option train time
                                ; would be: 12:00 + 2hr × SessionIndex + SessionTime
SPECTATORS_AMOUNT = 1           ; Adjust amount of spectators on track; from 0 to 1, 0 for no spectators

MIN_TIME_BETWEEN_COLLISIONS = 5 ; Available since 0.2.0 for use with server side plugins, does NOT effect player physics
                                ; Time in seconds between when batched collision information is sent to the server.
                                ; Minimum value 0.05, recommended value between 1 and 5
```
```ini
[SPECIAL_CARS]
HIDE_LABELS = …                 ; List 0-based indices of cars to hide driver name tags of, and hide them on maps
```

### Freeroam features

Just some extras for special servers. All options require CSP only server.

#### Color change
Allows to change car color in pits with a simple color picker, works with cars with regular skins:
Must also be enabled on a per-car basis within the server entry_list.ini
```ini
[CUSTOM_COLOR]
ALLOW_IN_PITS = 1
ALLOW_EVERYWHERE = 1            ; choose one or another;
```

#### Teleport
Teleports allow to define a bunch of points for cars to jump to quickly, invalidating their lap times. List of possible destinations and a teleport button are available in new chat app. For the whole thing to work, choose cars that are allowed to teleport in entry list editor in CM (with that CSP button for each entry).
Must also be enabled on a per-car basis within the server entry_list.ini

```ini
[TELEPORT_DESTINATIONS]
POINT_0 = Name          ; destination name
POINT_0_GROUP = Group   ; optional group
POINT_0_POS = X, Y, Z   ; coordinates, can be determined with Objects Inspector
POINT_0_HEADING = 0     ; heading angle in degrees
```

#### Portals
Portals for quick jumping from server to server. Requires the game to exit and relaunch in order to function, so be wary of loading times. For now quite limited: both servers would need to have the same entry list, with drivers keeping their currently driven car. Teleports car to the pitlane in the target server.

```ini
[PORTALS]
PORTAL_0 = 192.168.1.30:8081  ; Target server IP and HTTP port
PORTAL_0_POS = X, Y, Z        ; Portal position in current server
PORTAL_0_COLOR = 1, 1, 0, 1   ; optional RGB color and transparency
```

### Chat tweaks

```ini
[CHAT]
SERVER_MESSAGES_ONLY=1        ; Prevents users from sending chat messages

; Available since 0.1.76:
MESSAGES_FILTER='…'           ; Hide matching messages from other players
COMMANDS_NONADMIN_FILTER='…'  ; Hides “you are not an admin” response for commands that match this filter
SERVER_MESSAGES_FILTER='…'    ; Hides matching server messages
```

Filters use regular expressions with case-independent partial matching (so to match whole string, use `'^…$'`). Single quote symbols are not required, but it’s better to keep them to make sure symbols like “[” wouldn’t mess up INI parsing.

### Mumble voicechat integration

There are now two implementations of [Mumble](https://www.mumble.info/downloads/) integration.

Available since 0.1.75, Version 1 `[MUMBLE]` requires the client to have Mumble installed locally and running.
```ini
[MUMBLE]
SCALE = 1.0                     ; Scales world for Mumble voice chat
CONTEXT = …                     ; Optional context for Mumble; default is server IP and port
AUTOCONNECT = 'mumble://…'      ; Optional autoconnect to a certain Mumble channel when joining a server
```

Available since 0.2.0, Version 2 `[MUMBLE_INTEGRATION]` uses the built-in Mumble client contained within your CSP installation. This is a new app available in-game with new features and auto-connection with no other installation setup required by the client.

Open Content Manager and navigate to `settings > Custom Shaders Patch > GUI > New Apps > Mumble Integration` and ensure it is enabled.

```ini
[MUMBLE_INTEGRATION]
HOST = '' 			; IP or URL address of the Mumble server
PORT = 64738 			; Port of the Mumble server, default 64738
PASSWORD = ''			; Password of the Mumble server
CHANNEL = 'Root'		; Default channel to join on the Mumble server
POSITIONAL_AUDIO = true		; Move the audio with the position of the other drivers, true or false
POSITIONAL_MAX_DISTANCE = 50	; Distance where you can no longer hear other drivers
MUTE_DISTANCE = 200             ; Distance outside which other players are completely muted. Default value is infinite
```


### Replay clips

Available since 0.1.75. It adds an ability to quickly save a replay of last N seconds of a race as a separate clip, might be helpful in quickly saving potential conflict situations and resolve them further. All of that works out of the box, but extra server config can define an endpoint for drivers to automatically upload those clips once they’re saved.

Replays would be zipped and uploaded by sending a POST request with ZIP binary data in body of the request. Also, X-Car-Index header would contain an entry list index of a client.

```ini
; Available since 0.1.75:
[REPLAY_CLIPS]
UPLOAD_URL = 'https://domain.com/endpoint.php?key=X'  ; API endpoint
DURATION = 30  ; Clip duration in seconds, overriding user choice
```

### Temporary and experimental stuff

All this stuff might get removed in the future and replaced with something better.

```ini
; Activates rain, requires preview builds of CSP since rain is still in development.
[RAIN_PREVIEW]
INTENSITY = 0.5
REQUIRED = 1
WITH_PHYSICS = 1  ; Forcefully activates rain physics (make sure to enable custom car
                  ; physics in core server settings)

; Settings for rain racing line of RainFX.
[RAIN_RACING_LINE_PREVIEW]
… = …  ; Same keys and values as in “[RACING_LINE_DEV]” section of rain_fx.ini
```

### Online scripts

Available since 0.1.76. Specify a URL to a bit of code to run on client machines (with some restrictions, such as those scripts would not be able to access files outside of track and cars folders, or run processes, or other things like that). Those scripts can be used to display additional HUD elements, access car state and apply custom penalties, teleport cars upon certain conditions, control cameras, alter restrictor and ballast live, break and fix cars, apply extra forces, load and display new models, update textures live, add post-processing color corrections and much more, pretty much the same set of functions track scripts can do and more.

```ini
[SCRIPT_...]
SCRIPT = path           ; Path must be a web URL: for example, you can store your script
                        ; on https://gist.github.com and use the raw link
                        ; For development purposes, set it to the name of the file contained in
                        ; “assettocorsa/extension/lua/online” to edit scripts live.
REQUIRED = 0 		; Load required to join server, CSP closes game if script can't be loaded ; 0 or 1
REFRESH_PERIOD = 0 	; Periodic refresh of script in seconds ; 0 or more
… = …                   ; Any other parameters set in this section can be accessed by the script,
                        ; thus allowing to configure the same script to use with different servers.
```

Script URLs also support parameters substitution, so you can have it set like this:

```ini
[SCRIPT_...]
SCRIPT = 'https://myserver.com/script?s={SessionID}&t={SteamID}&c={CarID}&k={CarSkinID}&v={CSPBuildID}'
```

With that, some basic server can respond with a different script depending on the client, sending one script to a regular player and another to an admin (also, scripts can verify if player has admin rights live as well). All the parameters:

- `SessionID`: 0-based index of entry list used by the player;
- `SteamID`: player’s Steam ID;
- `CarID`: name of the user’s car folder;
- `CarSkinID`: name of the user’s skin folder;
- `CSPBuildID`: CSP build number;
- `ServerIP`: IP used to connect to the server;
- `ServerName`: server name;
- `ServerHTTPPort`: server HTTP port;
- `ServerTCPPort`: server TCP port;
- `ServerUDPPort`: server UDP port;

Server config can specify multiple scripts, although having too many of them might introduce a slight performance overhead. Don’t worry if it’s just, like, a dozen of those, but if it’s more than that, consider regrouping things somehow.

# Config encoding

To encode config in welcome message, do following steps (or just set it in Content Manager server panel):

- Get config bytes (UTF-8 encoding);
- Compress bytes using common zlib algorithm (for C#, SharpCompress can do it);
- Encode result as a base64 string (feel free to trim “=” on the end);
- Append 32 tab symbols and `$CSP0:` in front of resulting string (this way message would be hidden in original AC);
- And then attach it to the welcome message.

Here is an example from Content Manager source code:

```cs
// Actual encoding:
private static readonly string CspConfigSeparator = RepeatString("\t", 32) + "$CSP0:";

private string BuildWelcomeMessage() {
    if (string.IsNullOrWhiteSpace(CspExtraConfig)) return WelcomeMessage;
    return WelcomeMessage + CspConfigSeparator
        + ToCutBase64(CompressZlib(Encoding.UTF8.GetBytes(CspExtraConfig)));
}

// Helper functions:
public static string RepeatString(string s, int number) {
    var b = new StringBuilder();
    for (var i = 0; i < number; i++) {
        b.Append(s);
    }
    return b.ToString();
}

public static string ToCutBase64(byte[] decoded) {
    return Convert.ToBase64String(decoded).TrimEnd('=');
}

private static byte[] CompressZlib(byte[] data) {
    using (var m = new MemoryStream()) {
        using (var d = new ZlibStream(m, CompressionMode.Compress, CompressionLevel.Level6)) {
            d.WriteBytes(data);
        }
        return m.ToArray();
    }
}
```

# CSP-only servers and core options

To create a server that can only work with CSP installed, its config has to be slightly altered. Simply replace `TRACK` property in `server_cfg.ini` with `csp/<X>/../<track ID>`, where `<X>` is minimal required CSP version (build number). By creating a folder `content/csp` and moving track data such as “data/surfaces.ini” there it can work with original acServer just as well. However, a server like this can still in theory be accessed by somebody without the use of CSP, so another optional layer of protection is to edit “surfaces.ini” stored in server folder (the one acServer uses for integrity verification). Simply replace “[SURFACE_0]” by “[CSPFACE_0]” and it would alter file checksum in a certain way so that only clients running CSP would pass the integrity verification.

Update 0.1.78 also introduces extra options stored the similar way. New format now is `csp/<X>/../<O>/../<track ID>`, where O is a specifically endoded string storing additional options. Without going into too much detail about encoding with only three options available at this stage, here are the possible values:

- `B`: enable custom cars physics;
- `C`: enable custom track physics;
- `D`: enable both custom cars and track physics;
- `E`: hide pit crew;
- `F`: hide pit crew and use custom cars physics;
- `G`: hide pit crew and use custom track physics;
- `H`: hide pit crew and use custom cars and track physics.

It’s just bits of a number, and number is encoded using this string for some sort of base64-encoding with different characters: `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-`.

# Per-car flags

![https://files.acstuff.ru/shared/vRhW/20220611-014243.png](https://files.acstuff.ru/shared/vRhW/20220611-014243.png)

These tweaks are stored in skin IDs in “entry_list.ini”. Just use a slash and then base64-encode a structure with first byte for the version, second byte for the actual values and third byte acting like a checksum. [Here is how it’s done by Content Manager](https://github.com/gro-ove/actools/blob/master/AcManager.Tools/Objects/ServerDriverCspOptions.cs#L123).
