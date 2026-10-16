# Setup Items Driven By Controllers

Setup controllers allow to hide a certain setup item and instead control it live with a dynamic controller. With [new inputs](cars-new-inputs-for-dynamic-controllers.md) it means you can now tie certain setup items to extra buttons, things like headlights state or even values set live [by physics script written in Lua](cars-physics-scripts.md).

To configure a setup item for this purpose, simply add “EXT_CONTROLLER” value like so:

```ini
[ROD_LENGTH_LR]
TAB=SUSPENSIONS
SHOW_CLICKS=2
…
HELP=HELP_LR_RODLENGTH
EXT_CONTROLLER=ctrl_setup_rod_length.ini
```

And prepare a new controller as usual (same as used by AC physics):

```ini
[CONTROLLER_0]
COMBINATOR=ADD
INPUT=BRAKE
LUT=(| 0=400 | 1=4000 |)
FILTER=0
UP_LIMIT=1000000
DOWN_LIMIT=0
```

(In this particular example I tied suspension height to brake button so car would jump when brakes are pressed [like so](https://files.acstuff.ru/shared/RK9e/20210907-175443.mp4).)

*Note: currently the system doesn’t work with new setup items added by CSP, fix is coming with 0.1.80.*

*Pro tip: if you’re tying things to extra A/B/C/D/E/F switches, you can get them to work [in toggle or hold-to-activate mode, or block them from changing in some conditions](cars-extra-switches.md) (for example, if car is moving). Something like this could be used to recreate top speed switch of a Bugatti, for example.*
