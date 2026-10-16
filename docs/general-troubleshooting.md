# Troubleshooting

As a general solution, consider running Steam integrity check. It won’t remove any new cars or tracks you might have installed, would only revert changed Assetto Corsa files back.

### Can’t find “\python33\\PyObject_CallFunction”

Make sure you have [Microsoft Visual C++ 2010 Redistributable Package (x64)](https://www.microsoft.com/en-gb/download/details.aspx?id=14632) installed ([direct link](https://files.acstuff.ru/shared/iJVd/vcredist_x64_2010.exe)). If it’s already installed, reinstalling it can help too.

### Image is flipped or split into two massive triangles which are flipped

If you’re using AMD GPU card, make sure to enable “Resolve MSAA for color” in Extra FX settings.

### Message “GPU May be overheating or overclocked”

Disable “Use DXGI Flip Model” in General settings of Custom Shaders Patch.

### Slight flicker of some parts of a track or car

Disable “Use proper physically-based sampling” in Reflections FX module.
