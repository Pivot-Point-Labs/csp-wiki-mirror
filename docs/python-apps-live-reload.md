# Live Reload

Since CSP 0.1.76 there is now an option to reload apps live, allowing to edit them without restarting Assetto Corsa to see the changes. You can find it in Python Apps Debug, in “Live reload” section:

![Screenshot](https://files.acstuff.ru/shared/qiuQ/20211021-215221.png)

Just click a Reload button, or check “Reload automatically” checkbox and app would be reloaded automatically if any of py-files would change.

To reload an app, CSP would destroy all of its apps and then reload its main module and any modules it imported from app folder. This could be important: if your app imports modules from outside of its folder, those ones would not get reloaded, so unless they are stateless, errors or even crashes might occur.

Please note: when loading, CSP would not call `acShutdown` function because AC isn’t actually shutting down. If your app has some resources it would need to release, like shutting down an HTTP server, define `ext_acReload` function and release resources there. And, to add to that, `ext_acReload` would only be called when app is reloaded, so you might want to use something like this:

```py
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

def ext_acReload():
  httpd.shutdown()

def acShutdown():
  ext_acReload()
  # all the other shutdown-related things, like writing down best lap time
```

If `ext_acReload` function would throw an exception, reload would not proceed to make sure program wouldn’t reload into an invalid state. If you would end up in that situation accidentally, you can override this behaviour from the context menu:

![Screenshot](https://files.acstuff.ru/shared/yU8g/20211021-220321.png)
