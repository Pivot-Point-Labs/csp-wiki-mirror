Here are some things which could help you with setting up car for Custom Shaders Patch or just in general with making a new car. Like a continuation for those old posts in that old blog I had. :)

# General tips

- According to PBR formulas, best value for `ksFresnelEXP` is 5, and you can calculate `ksFresnelMaxLevel` as `min(1, ksFresnelC * 50)` ([source](https://seblagarde.files.wordpress.com/2015/07/course_notes_moving_frostbite_to_pbr_v32.pdf), page 78). Not sure if it’s applicable everywhere, but for certain materials like plastic, glass or chrome, I’d recommend to use these values.

- It might be better to not use `IsTransparent` flag for meshes if you know it won’t be rendered over background (like some headlights glass which isn’t poking out that much), instead, just move it to the end by adjusting priorities and you would save a bit of FPS and improve overall look (plus, if you have several layers of overlays, it would make it much easier to set up right).

- Use `ksPerPixelMultiMap_damage_dirt` shader for car paint even if you’re not setting damage or dirt (just fill those slots with transparent textures). And in general, I’d suggest to keep things similar to how Kunos do it.

# Custom Shaders Patch

- Always make sure to have proper `COCKPIT_HR` node: patch uses it all the time to distinguish between interior and exterior with guessing role of lights, applying interior masking, adjusting reflection in rear view mirrors and so on.

- Make surfaces to cast shadows from two sides with `DOUBLE_FACE_SHADOW_BIASED`:

  ```ini
  [SHADER_REPLACEMENT_...]
  MESHES = tailight_SUB0, taillight_emissiveA, taillight_emissive, body, body_top, boot_cover,\
    material:needle_body, bouton_dashboard
  DOUBLE_FACE_SHADOW_BIASED = 1
  ```

  There is also a `DOUBLE_FACE_SHADOW` option, but `DOUBLE_FACE_SHADOW_BIASED` would automatically add a bit of bias to reduce self-shadowing. Don’t overuse this option though, as it might increase time it takes to draw shadows (to draw two faces).

- This piece would increase sharpness of SSLR reflections by 80%:

  ```ini
  [SHADER_REPLACEMENT_...]
  MATERIALS = EXT_Lights_base
  PROP_0 = extExtraSharpLocalReflections, 0.8
  ```

  Good for some chrome pieces which don’t have sharp reflections to make them look less weird, but could benefit from sharp local reflections.

- Working with `SHADER_REPLACEMENT` sections, prefer to refer to materials rather than meshes where possible. If you’re changing material properties or textures in there, new material will be created for each mesh.
