# More About Color Grading

Let’s say we have some filter which produces picture like that, and we don’t like it:

![Boring old picture](https://i.imgur.com/HOLWR3b.jpg)

First step: make a screenshot of it, like the one here. Then, open it in your favourite image editor, and paste [neutral color grading image](https://i.imgur.com/fTxYwA0.png) on top of it, in some corner:

![Screenshot of some image editor](https://i.imgur.com/OoE0sIC.png)

Don’t forget to merge the layers, so you would adjust colors of both things at the same time:

![Merged layers](https://i.imgur.com/0DQ9V6d.png)

After that, do any of color transformations you might like. Curves, saturation, contracts, auto-color, auto-contrast, hue, tint, any other effect that relies on original pixel color and nothing else:

![Curves transformation](https://i.imgur.com/X3LHD0S.png)

Then, carefully cut out your color grading image and save it separately, as PNG file:

![Cutting carefully…](https://i.imgur.com/PvJ3KBk.png)

*Please, be extra careful at this step. Color grading texture should have resolution like 16×256, or 32×1024 (in other words, N×N²), everything else won’t work.*

Go [here](http://b64.io/) and drag’n’drop your newly created image onto that green area, and then, copy resulting [base64 link](https://en.wikipedia.org/wiki/Base64) containing all the image into the clipboard:

![Copying link](https://i.imgur.com/Pu8zadc.png)

And simply paste it as `EXT_COLOR_GRADING/FILE` in your PP-filter (you can do all of that while AC is running):


```ini
[EXT_COLOR_GRADING]
ENABLED = 1
FILE = data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABAAAAAAgCAIAAAADnJ3xAAABYUlEQVR42u3cu27CQBQE0PEDEvmxhv//2VQUSZFui/U9RxRUI2sK5BFrT0mSLMmeHMmebElLjqQlLbmS8/O9Ja9kT1qyJV+fz5KsyZzMyZRfpu75a+f8q3P+1jn/3Tl/75x/uv5b57fO+cfg178P/vtzDH79o+c/Ouc/B89f5P+bPw+ePw2e3/f+eQ4AAFDG+ncRAAAAdx4ATQkAAFBnAOxKAACAOgPgUAIAANQZAKcSAACgzgBwBAgAAAoNAEeAAACg0AC4lAAAAHUGgH8AAACg0ADwEDAAABQaAI4AAQBAoQHgLUAAAFBoALyUAAAAdQaAh4ABAKDQAGhKAACAOgPAMwAAAFBoAHgNKAAAFBoAmxIAAKDOAPhWAgAAGAAAAMANB8BTCQAAUGcAPJQAAAB1BsCqBAAAqDMAZiUAAIABAAAAGAAAAMDIA2BSAgAAGAAAAMDtOAAEAAAGAAAAcEc/8uQidWnw6SkAAAAASUVORK5CYII=
```

Enjoy the new look!

![Screenshot with color grading applied](https://i.imgur.com/iiYrx0e.jpg)
