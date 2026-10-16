# What is it all about?

Content auto-updates system (CUP) is a new feature of Content Manager allowing to automatically receive notifications and offers to update for cars, tracks and apps (more will be added later). For it to work, mod creator needs to publish information about latest versions of their content and links to get that update from.

# If you’re installing mods

From time to time, for some mods, you might see something like this:

<a href="https://i.imgur.com/4ivjaJG.png" target="_blank"><img src="https://i.imgur.com/4ivjaJG.png" width="400" /></a>

Or, if new versions are found, Content Manager will notify you in main menu:

<a href="https://i.imgur.com/OeUcxSi.png" target="_blank"><img src="https://i.imgur.com/OeUcxSi.png" width="400" /></a>

Click on those buttons with green arrow and it would either start a download or open a page in web-browser where you can get the update from (for paid mods and such). Even if CM would start downloading update automatically, you would still need to agree to install it in main menu, as usual. At least for now, that’s the system. Those buttons also have a context menu:

<a href="https://i.imgur.com/8D4390f.png" target="_blank"><img src="https://i.imgur.com/8D4390f.png" width="400" /></a>

Here, you can skip an update, stop the whole mod from even updating, or mark update as broken if the link doesn’t work or doesn’t contain the right update. Please keep in mind, modders register new versions with URLs to get the update from, and we all might make a mistake now and then, so you can use that option to let them know something is not right.

# If you’re making mods

Please contact me, and I’ll add you in a system for registering new updates. It’s all very roughly made, but seems to work. I’m not good at making those server-side things.

Once you’re in that system, click here to add a new item:

<a href="https://i.imgur.com/xyBFMYV.png" target="_blank"><img src="https://i.imgur.com/xyBFMYV.png" width="400" /></a>

In appearing window, pick the type and enter the ID (which is the name of the folder) in lowercase. Be careful: unlike everything else, type and ID can’t be changed later. After that, click “Add new item”, and after it’s added, enter the rest of details:

<a href="https://i.imgur.com/Cw4liLT.png" target="_blank"><img src="https://i.imgur.com/Cw4liLT.png" width="400" /></a>

- **Name**: regular human-readable name, how it’s shown in UI;
- **Version** (required): latest version of your thing, in normal format app can compare (it looks for numbers and compares corresponding numbers);
- **Update URL** (required): URL opening for users when they press update button with green arrow. Could be either a download URL or a webpage with the update, for things like paid mods (see tips for more info);
- **Information URL**: URL containing details about the thing;
- **Other IDs**: if your update contains more than one thing (like, we published both Peugeot 504 and Peugeot 504 TN in the same archive), add secondary IDs (aka names of folders) in there, separate by comma;
- **Authors**, **changelog**: nothing special here, but keep it short, please, there is not a lot of space in UI. Put all the extra details on the webpage, and maybe add a note saying “for detailed changelog, [url="http://webpage/..."]click here[/url]” (you can use BB-codes here);
- **Limited** option: turn it on to mark URL as non-download one, for paid mods. If it’s on, press on update button will open mod in web browser. Otherwise, app will start a download;
- **Clean installation** option: turn it on to suggest users to use clean installation for the new update (will make it a default option);
- Switch in the top right corner: turn it off to hide entry from registry completely.

### Very important tip

If you want users to be able to download updates automatically, I would like to ask you to use something Content Manager is able to download from smoothly and reliably. Here are some of recommended ways:

- Google Drive (15 GB free): even allows to continue download from the middle if first attempt failed there;
- Mega.nz (15 GB free): unlike the rest, this one has proper API for downloads, so it should be the most reliable;
- OneDrive (5 GB free): seems to be working well at the moment;
- Yandex.Disk (10 GB free): keep in mind it’s banned in Ukraine, but other than that, works very smootly, has some sort of API;
- Dropbox (2 GB free): I think it’s easy to hit quota limit with it, but other than that, it’s pretty much perfect;
- MediaFire: seems to work for now, but this one might not be very reliable;
- ShareMods: same, works, but might break at any point;
- Direct link: of course, that’s the best way, if possible.

Of course, there are a few websites for hosting mods for Assetto Corsa, but unfortunately they’re not compatible with Content Manager, so if reuploading is not an option, it might be better to set updates to work in limited mode. But I would highly recommend to reupload updates in such case.

### Other tips

- If you have several cars, tracks or apps in the same archive, create an entry only for the first one, and put others in “Other IDs” section. Or, of course, you could set separate entries if you have extra time, but there wouldn’t be a lot of advantage.
- Content Manager caches information about updates in “%LOCALAPPDATA%\AcTools Content Manager\Temporary\CUP” (just copy-paste this path to Windows Explorer, it’ll find the right folder) for a few hours. To check if update works, delete that folder and restart the app.
- Usernames are all in lower case because I’m not good at programming those things.

# If you’re interested in making your own updates registry for your website

If that’s the case, please contact me. API is very, very simple to recreate, it’s basically just a four different requests: list of all, information about one, download link (redirecting to actual URL) and POST-request for complaining.

# One last detail

CUP stands for Content Updates, let’s say, Project. I made this system back in 2018, forgot what’s last letter is for.
