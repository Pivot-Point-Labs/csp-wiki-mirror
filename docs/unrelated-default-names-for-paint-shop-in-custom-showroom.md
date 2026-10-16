# Default Names for Paint Shop in Custom Showroom

For Paint Shop to work, it would need to know the role of each texture, and how it could be edited. All of that could be set with JSON file, but they’re quite tricky to test. It also tries to guess roles of different textures based on their names, and choose the right name is much easier than edit that mess. Here are the names it looks for:

- `car_paint.dds` — car paint, small texture with or without flakes (usually in `txDetail` slot);
- `car_paint_rims.dds` — rims color, another small solid texture (to color rims with a single texture `txDetail` way and still use alpha for blurred version, use `ksPerPixelMultiMap_AT` shader with alpha-channel in `txNormal` slot, while alpha in `txDiffuse` slot would still act like mask for `txDetail`);
- `car_paint_roll_cage.dds` — roll cage color (solid color);
- `metal_detail_roof.dds` — roof color (solid);
- `carpet.dds` — carpets (tint for existing texture);
- `cuciture.dds` — interior seams on seats and such (tint);
- `seat_logo_D.dds` — logo on seats (tint);
- `PlasticDetail_color.dds` — plastic color (solid);
- `cloth_detail.dds` — cloth color (solid);
- `TEssuto_color.dds` — cloth piece (solid);
- `cloth_seats.dds` — seats color (tint);
- `kevlar_tile.dds` — kevlar (tint);
- `alcnt.dds` — interior (tint);
- `leather.dds` — leather (tint);
- `ext_glass.dds` — glass (optional transparency);
- `caliper_detail.dds` — brake calipers (solid);
- `noise_D.dds` — cylinder head cover (solid).

Names are weird like that because I set that guessing to work with original Kunos cars and some mods. And, there are some extra colors with indices if needed:

- With `<X>` from 2 to 8:
  - `metal_detail_<X>.dds`: car paint #X (fill);
  - `metal_detail_skin_<X>.dds`: car skin #X (fill);
  - `rim_detail_<X>.dds`: rims #X (fill).
- With `<X>` from 0 to 6:
  - `interior_plastics_detail<X>.dds`: interior plastic #X (tint);
  - `carpet<X>.dds`: carpet #X (tint);
  - `INT_Trim<X>.dds`: trimming #X (tint);
  - `INT_fabric<X>.dds`: fabric #X (tint);
  - `leather_seat<X>.dds`: seat #X (tint);
  - `alcnt_cust<X>.dds`: interior #X (tint);
  - `leather_<X>.dds`: leather #X (tint).

For license plate, name textures `Plate_D.dds` and `Plate_NM.dds`. If you want `txMaps` to be configurable, use car paint shader, `ksPerPixelMultiMap_damage_dirt
`.
