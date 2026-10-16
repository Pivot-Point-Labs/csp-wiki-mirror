# Digital Instruments

This is a temporary and somewhat hacky approach, doesn’t allow to define new digital instruments, but instead, only to replace text on original Kunos instruments defined in “data/digital_instruments.ini”.

### Syntax

```ini
[DI_DRIVEN_TOTAL_...]
DIGITAL_ITEM = 0
DIGITAL_ITEM_NUMBER_FORMAT = 06.0
UPPER_BOUND = 999999

[DI_DRIVEN_SESSION_...]
DIGITAL_ITEM = 1
DIGITAL_ITEM_NUMBER_FORMAT = 05.1
UPPER_BOUND = 999999

[DI_GEAR_...]
DIGITAL_ITEM = 2
DIGITAL_ITEM_NUMBER_FORMAT = GEAR  ; only supported from v0.1.61
```

So, first of all, [input type](cars-instruments-inputs.md) is set in section name (for backwards compatibility and what not). After that, you can set other input options, such as `INPUT_LAG`, in that section as usual.

Other key value, `DIGITAL_ITEM`, refers to index of digital instrument in “data/digital_instruments.ini”. Just use the number after “_” in its section name.

Other values (in application order):
- `VALUE_OFFSET`: offsets value (although now you can just use `INPUT_ADD`);
- `UPPER_BOUND`: optionally limits maximum value to avoid overflowing;
- `OUTPUT_MULTIPLIER`: multiplier for value (and again, `INPUT_MULT` might be a better option);

### Formats

With `DIGITAL_ITEM_NUMBER_FORMAT` you can set format for value. It could be one of keywords for specially prepared formats, or basic C-style format string. Or, even more basic, in case “%” sign is missing, it’s parsed as follows:

- Number before dot sets amount of digits to display before dots;
- If that number starts with 0, extra digits will be zeroes. Otherwise, it would be spaces.
- Number after dot sets number of digits after the dot.

Special formats:

- `GEAR`: by default `R` for -1, `N` for 0 and numbers for values above, for `[DI_GEAR_...]`. You can replace `R` and `N` like so:
  ```ini
  [DI_GEAR_...]
  DIGITAL_ITEM_NUMBER_FORMAT = GEAR, Rev, Neut
  ```

- `GEAR_AUTO`: same, but uses `D` for numbers above 0. And, again, you can replace words like so:
  ```ini
  [DI_GEAR_...]
  DIGITAL_ITEM_NUMBER_FORMAT = GEAR_AUTO, reverse, neutral, drive
  ```

- `COMPASS`: turns degress into compass abbreviation, like `N`, `SE` or `NNE`. By default limited by two letters, to allow third letter, use:
  ```ini
  [DI_WIND_DIR_...]
  DIGITAL_ITEM_NUMBER_FORMAT = COMPASS, LARGE
  ```

- `TIME`: useful for `[DI_TIME_...]` to show time of day. Second parameter is [C format string for time](https://www.geeksforgeeks.org/strftime-function-in-c/):
  ```ini
  [DI_TIME_...]
  DIGITAL_ITEM_NUMBER_FORMAT = TIME, '%I:%M %p'  ; 12-hour format
    ; By the way, notice quotes. If string is more that a simple word, better
    ; to use those to avoid confusion with things like commas
  ```

- `LAP_TIME`: formats racing time nicely, with minutes, seconds and milliseconds. If needed, hours would be added at front too. You can use second parameter to replace text for time which isn’t set yet, by default it’s “-:--:--”:
  ```ini
  [DI_LAP_TIME_...]
  DIGITAL_ITEM_NUMBER_FORMAT = LAP_TIME, none
  ```


### Features to add later

- Add new digital instruments implementation not relying on original one.
