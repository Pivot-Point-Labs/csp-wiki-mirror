# Extra Replay Data

Car scripts can write extra replay data via controller inputs. This feature was added in the **0.2.3** update. Simply define a schema in the car.ini file, and then use script controller inputs to read/write data that will get stored as replay data. Try and keep the number of replay inputs low.

**`car.ini`:**

```ini
[_EXTENSION]
SCRIPT_INPUTS_REPLAY = 100:uint8, 101:unorm8, 102:half
```

```ini
[_EXTENSION]
SCRIPT_INPUTS_REPLAY = 100:uint8, unorm8, half, uint8 ;INDEX == 100, INDEX == 101, INDEX == 102, INDEX == 103
```
Replay inputs can be added in the form of `<INDEX>:<TYPE>`. You can also define inputs with just `<TYPE>`, and their INDEX will be incremented from the last explicitly defined INDEX value.

Known types:
- `h`, `half`: 2 bytes, floating point (roughly, from 1/65536 to 65536);
- `f`, `float`: 4 bytes, floating point;
- `i8`, `int8`, `char`: 1 byte, from -128 to 127;
- `u8`, `uint8`, `byte`: 1 byte, from 0 to 255;
- `i16`, `int16`, `short`: 2 bytes, from -32768 to 32767;
- `u16`, `uint16`, `ushort`: 2 bytes, from 0 to 65535;
- `i32`, `int32`, `int`: 4 bytes, can be negative;
- `u32`, `uint32`, `uint`: 4 bytes, positive integers only;
- `unorm8`: 1 byte, from 0 to 1;
- `norm8`: 1 byte, from -1 to 1;
- `unorm16`: 2 bytes, from 0 to 1;
- `norm16`: 2 bytes, from -1 to 1;

_If your defined schema ever changes, any replays that were saved with the previous schema, will no longer replay the extra data that was recorded._

**Car physics `script.lua`:**
```lua
function script.update(dt)
  local data = ac.accessCarPhysics()

  -- Data written to these controllers is stored in the replay data
  data.controllerInputs[100] = 1
  data.controllerInputs[101] = 2
  data.controllerInputs[102] = 3
end
```
