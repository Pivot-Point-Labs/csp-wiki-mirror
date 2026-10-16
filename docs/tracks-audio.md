# Audio

If needed, you can create a soundbank for a track and attach various audio events to different points on a track. [Here is an example](https://mega.nz/#!LhZx3YyR!Qe6DoRgMZ5KeQHNiy0WcnM4WfxbA8w5N0fpfiYH9-CE).

For it to work, you need to locate files like so:

- `content/tracks/<trackfolder>`
  - `extension/`
    - `sfx/`
      - `GUIDs.txt`
      - `sfx.bank`
    - `ext_config.ini`

And in “ext_config.ini”, write:

```ini
; First, it needs to define soundbank to use:

[SOUNDBANK_0]
BANK = sfx/sfx.bank    ; as you can see here, you can name those files differently
GUIDS = sfx/GUIDs.txt  ; but for a start, name them like that, just in case

; Then, define events in soundbank

[EVENT_0]
ID = event/path      ; event path, as you can see it in GUIDs.txt
REVERB_RESPONSE = 1  ; should event respond to reverb

; Positioning:
POSITION = X, Y, Z   ; position of an audio source in space
                     ; (you can use Object Inspector to quickly find out position,
                     ; just click anywhere and copy coordinates)
DIRECTION = 0, 0, 1  ; direction of audio event

; Volumes:
VOLUME = 1                  ; base volume
CAMERA_INTERIOR_MULT = 0.2  ; volume multiplier for interior cameras
CAMERA_EXTERIOR_MULT = 1    ; volume multiplier for exterior cameras like chase cam
CAMERA_TRACK_MULT = 1       ; volume multiplier for track cameras

; Parameters:
INPUT_KEY_0 = some_parameter
INPUT_VALUE_0 = 0.5
INPUT_KEY_1 = different_parameter
INPUT_VALUE_2 = 1.5

; You can, of course, use same event in several points, with different parameters:

[EVENT_1]
ID = event/path
POSITION = 0, 0, 10
; and so on

; And, in case you would need something more complex, for each number, such as
; volume, volume multiplier or input value, you can use a varying value instead
; of a constant.

[CONDITION_0]
; This condition will return 0 during the day, and 1 at night:
NAME = NIGHT_VOLUME
INPUT = SUN
LUT = (| 0=0 | 88=0 | 88=1 | 180=1 |)
LAG = 0.97

[EVENT_2]
ID = event/path
INPUT_KEY_0 = some_parameter
INPUT_VALUE_0 = NIGHT_VOLUME

[EVENT_...]
; audio event following an animated object:
ID = event/path
RELATIVE_TO = node_name  ; or mesh_name

; and so on
```
