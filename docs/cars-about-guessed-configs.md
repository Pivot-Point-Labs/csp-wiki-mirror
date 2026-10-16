# About Guessed Configs

There are so many cars, it would take a long time to prepare configs for every single one of them. To save time, patch instead not only relies on configs, but also, tries to guess a lot of parameters based on things like car model, textures or even car class and manufacturing year (from “ui_car.json”).

If you would want to check what was exactly was guessed:

- Go to “Assetto Corsa/cfg” in your “Documents” folder;
- In it, make a folder called `extension_cars_guessed`;
- Run the game and patch will store in there the guessed configuration.

### Very important tips

- Do not edit that file expecting any changes in game, patch doesn’t read anything in that folder;
- Do not copy the whole guessed config as your custom config. Instead, please, copy wrongly guessed values and change them. Guessing is constantly being revised and improved, and if you would copy something guessed like this, you would be stuck with older values;
- In some cases, it might be better to poke me and tell me to fix guessing. If you think patch guesses something wrong, please let me know.

### Preparing for guessing

- To save yourself some time, make sure to have correct car information set:
  - Please consider using either “street” or “race” for car class (tag in "ui\ui_car.json"), same way Kunos use it. That is one of most crucial values. For example, race cars won’t even get low beams by default;
  - Use tags like “openwheeler”, “open wheeler”, “singleseater”, “f1” or “kart” only for open wheelers. This is how both patch and Content Manager actually check if car is open wheeler or not. Not a bit deal for CM, but patch won’t even let you turn on the headlights on open wheelers by default.
  - If headlight params are not set and car has “rally” tag, in some cases it’ll switch to rally mode with more intense headlights;
  - Another important parameter is year. It affects shape of headlights, instruments behavior, default frequency of hazards, even sparks color for F1 cars;
  - Patch takes into account other things like manufacturer country or car power and weight, so it’s better to just keep things in order;
- Of course, you can [define all those options by hand](cars-general-options.md) instead of relying on guessing, but why add extra work?

### More pro tips
- To create a config, make a new file in “Documents/Assetto Corsa/cfg/cars”, or in “assettocorsa/extension/config/cars”. Or, if you’re working on a new car, use “assettocorsa/content/cars/\<carfolder\>/extension/ext_config.ini”;
- You can edit configs during the race to see the changes without restarting the game;
- note: live reloading works for most settings, but not all, like not for [MODEL_REPLACEMENT...] and such
