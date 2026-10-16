# Strict Mode

When dealing with Python apps, original Assetto Corsa is quite forgiving with its errors, ignoring if incorrect number of arguments was provided or if there was any other failure. While it could help in some cases, in general it might make it more difficult to develop apps, not getting errors reported correctly.

Because of that, CSP adds an optional strict mode, in which errors would actually be thrown to an app to deal with. I’d recommend to use it when developing a new app.

To activate a strict mode, simply call a function somewhere in the beginning of the app:

```py
ac.ext_setStrictMode()
```
