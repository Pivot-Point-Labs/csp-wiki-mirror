# App Icons

To make distributing apps easier, with CSP you can now keep app icons within app folder.

For that, store those PNG files in “apps/python/\<appfolder>/icons”, in PNG format. CSP would look for a file with a name of an app name (the one used in `ac.newApp()`), and if nothing found, it would try and load “app.png”.

Please note: unlike original AC icons where you had to have a version for app active and inactive, here, only a single version is needed. And don’t use that circular shape here either, instead, just use a regular picture covering whole area. CSP would generate the rest automatically if necessary (in case new taskbar style is disabled).

Here is an example of how icons might look like and how they should be located:

<img src="https://i.imgur.com/Ph3nYgr.png">
