**Just to clarify: pack KN5s while they are in their original folders, do not move them anywhere.**

If you need to protect your models from being edited or stolen, Custom Shaders Patch can encrypt them now. Encrypted models would only work with Assetto Corsa with Custom Shaders Patch installed, or, optionally, with Custom Showroom of Content Manager. In original Assetto Corsa models will look like this:

![Example of failed decryption](https://i.imgur.com/iOrMALP.jpg)

Encryption works for both cars and tracks. Please read these lists carefully, there are some important points:

# What are the limitations?

- 👉 **Do not encrypt Kunos or someone else’s content without permission, or your encrypted files would either break or get decrypted. Also, CSP might start showing a warning about stolen content.** 👈
- By default, your cars won’t work in Custom Showroom.
  - If you want for them to work, let me know and I’ll add a support for your encryption to the next Content Manager update.
  - Please keep it mind it might make it easier to steal your models.
- Anybody could still get original model with textures using certain tools to intercept data from GPU.
- I’m not an expert by any means, there are most likely some major mistakes I made that make it easy to decrypt things.
- Make sure your car or track folder doesn’t have upper case characters.
- Whole thing won’t work if you have several meshes named the same.
- Names of meshes and textures should be no longer than 200 characters.

# How to keep things safe?

- Do not share your encrypters! That is pretty much as releasing all your content decrypted, if some people would want to reverse engineer it.
- If your encrypted car, when unpacked, looks too smooth, make sure meshes are not scaled too much.
- If you’re encrypting someone’s content without permission, they might get a decrypter for your models and do whatever they want with it.
  - If there is an argument over a stolen mod, but original one is a low-effort port, to a point where it’s possible it wasn’t stolen, but car was ported separately and it’s just a coincidence, nobody gets anything.

# How to use it:

Your encryptor consists of two parts, `kn5enc_….exe` and `kn5enc_…_acdchecksum.exe`:

- Use `kn5enc_….exe` if you only want to protect model.
- Use `kn5enc_…_acdchecksum.exe` if you have your data packed into “data.acd” and want to protect it from changes, as well as protect model.
  - This mode protects data from changes, but doesn’t encrypt it. People would still be able to see and copy it, but once it’s changed, model would stop to work. Helps to prevent people changing physics and re-releasing car under their name as a “fixed” or “tuned” version.

To encrypt a model:

- Pick a mode.
- Launch corresponding executable.
  - No need to copy it in car folder or anything like that.
- It’ll show you a file selection dialog, select a KN5 to encrypt from there.
  - Keep KN5 in original car or track folder.
- After encryption is complete, there would be a new KN5 next to original, with `_encrypted.kn5` postfix.
  - Replace original one by that new one manually.
  - Make sure to make a backup version of original model, there is no way to decrypt a model!

# Other tips:

<details><summary>Less important stuff, hidden to avoid turning people away with a lot of text.</summary>

## Changelog

There are three versions so far, easiest way to distringuish is by file size of a ZIP:

- v1 (914 KB): initial release;
- v2 (701 KB): protection for encrypter, much better support for heavy models, some warnings, sligthly improved security for encrypted content;
- v3 (695 KB): better warnings, actually showing which meshes have the same name, for example.

Contact me if you need an updated version.

## Other notes

First of all, I’d like to ask you to reconsider encrypting your models. I believe general openness of Assetto Corsa is a great thing, and, for example, looking closer into how other cars are made helped me massively to learn how to do my own cars. And there might be nothing wrong if somebody would tune some car for their own personal use. But, of course, there are some people out there who like to mess up with models and re-release them as their own, for some strange reason focusing on some specific type of cars. If your model might attract those people, encryption is completely justified, of course (although, considering that those people pretty much never add anything valuable, it’s better to simply ignore them).

If somebody stole your content and encrypted it without permission, I’m very sorry about that. You can [contact me](https://acstuff.ru/app/#contacts) so we could try and resolve it together. If some agreement couldn’t be found, I’ll prepare you a special decryptor which could work with a key of that particular person, to either get modified model, decrypt models for public re-release or just release decryptor for everybody to use.

Adding support for your encryption in Custom Showroom might make things more vulnerable, adding another point of entry with C# which might be easier to reverse engineer. There is another option for your cars to work there though, and that option is to create a new model specifically for Content Manager. Just make a new unencrypted KN5 and add it to `lods.ini` with `[LOD_HR]` section — it would be completely ignored by Assetto Corsa, but Content Manager would use it as default model. And, of course, make it unusuable considering it won’t be encrypted: add MeshSmooth to make it too detailed for smooth FPS in Assetto Corsa, or maybe remove whole interior or wheels, or merge everything together, or do all of the above.

You’ll find that encrypted model might take less disk space comparing to original: it’s normal as encrypter also applies lossless compression for textures to save disk space and speed up loading.

Oh, and you can also drag’n’drop KN5s onto EXEs. I wanted to make that main part as simple as possible, so I thought it would be better to avoid any choices like that.

Thank you for reading all that! If you want to get your own encryption tool, please [contact me](https://acstuff.ru/app/#contacts).

</details>
