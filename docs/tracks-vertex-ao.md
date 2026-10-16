Per-vertex ambient occlusion helps to add some smooth ambient shadows at zero FPS cost.

# Introduction

### How to use it simply?

Just download the latest version, extract EXE-file in some folder and then drag’n’drop track’s “models_….ini” file or, if missing, track’s KN5 model onto it. Console window should appear, just wait for it to close and it’s ready to go.

![Console window](https://i.imgur.com/EbSzp2m.png)

# More details

### How it works?

For it to work, tracks need to be prepared (kind of like baking AO textures). Whole thing can function in one of two different modes: either by modifying original KN5 and replacing some unnecessary data in there by occlusion values, or by generating a new “.vao-patch” file for given KN5 model or set of models in “models_….ini” (and, yes, this way you can have different occlusion for the same model depending on its surroundings set via different “models_….ini” files).

### Why “.vao-patch”?

While modified KN5 models would still remain fully compatible with original AC with no visual glitches, I think “.vao-patch” approach is much better, and here’s why: with it, if you’d change something like a texture or material in original KN5, you wouldn’t need to rebake it. In some cases, you could even alter geometry or add and remove objects and generated AO would still remain valid. A lot of times, of course, you would want to remake it anyway, but if it’s just a small tweak to something like starting grid arrangement or slightly moved spectators, why would you want to rebake everything just for that?

### How to configure it?

Since it’s a console app, with command line! Or, even better, create a new file called “baked shadows params.txt” (or “baked_shadows_params.txt”, for those who would share it on Discord) in a folder where KN5 files are located, and enter all the parameters in there. Each line — new parameter, empty lines are allowed, and you can use “#” for comments.

By the way, if you’re not a particular fan of console apps, all source code is available [here](https://github.com/gro-ove/actools/tree/master/CustomTracksBakery). Please feel free to fork the project and change it to be more user-friendly. Simply replace Program.cs initializing and running MainBakery by something you think would be better. Or even replace whole AO calculation algorithm, of course, I went with the simplest one I could think of just to try and make AO a bit colorful without spending too much time on it.
