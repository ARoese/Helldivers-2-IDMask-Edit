# Helldivers 2 IDMask editing

This blender addon enables the editing of the IDMask array and pattern mask texture for advanced LUT-compatible helldivers materials. 

**This add-on is for blender 4.3**. It probably also works on other versions, but that's not guarunteed. 

## Installation
1. install the pillow library to blender's bundled python env
    - Some other add-on probably already installed it. If you use Material Combiner, then that did it for you.
    - At least one of these commands I wrote will also do it: 
        - `path\to\blender.exe -b --python-expr 'import sys, subprocess; subprocess.run([sys.executable, "-m", "pip", "install", "pillow"]);'`
        - `blender -b --python-expr 'import sys, subprocess; subprocess.run([sys.executable, "-m", "pip", "install", "pillow"]);'`
2. install the addon via edit > preferences > Add-ons > Install from disk (top right)


## Setup
1. Set up the helldivers 2 accurate shader for your model
    - See [this discord thread](https://discord.com/channels/1210541115829260328/1222290154409033889) for details and a video on how to do this
    - It comes down to exporting the mesh and associated textures. Specifically, the IDMask, Pattern mask, and LUTs
    - You need to keep a hold of the IDMask dds file exported from the game. An exr file or PNG will not work for this plugin.
    - You can also append objects from the [helldivers 2 armory](https://discord.com/channels/1210541115829260328/1446534760045482046), which has this set up for each armor set
2. Modify the shader and import the IDMask dds
    1. in the node view of the shader, select and right click the main node. This will be named something like "HD2 Shader Template"
    2. Click the "Make Editable" option in the context menu.
        - Clicking this option again will give you the opportunity to import a different IDMask. The new channels will overwrite the old ones, and the shader will stay clean. This could be useful if you're painting variants.
    3. Select the IDMask array dds you exported from helldivers.
        - You do not need to pre-process this file at all. Directly exported via the sdk or filediver should be fine. IDMasks exported using this addon should also work.

Note: Once you modify the shader in step 2, then the original script that is used to "update" it will PROBABLY not work anymore. It's most likely to just shred it. Just re-creating it is probably best.

When these docs mention "The main group" or "The main node", they mean this one on the right
![main node](README_assets/main_node.png)

## Usage
### General painting
The addon adds a toolbar accessible by pressing N in the 3d viewer in texture paint mode which allows quickly switching between materials being painted. If a material was not set up for painting, then these buttons will not be clickable. Hover over them to see why.

This addon makes painting the IDMask easier, but you do still need to know how the materials interact when layered. Luckily, you will always know what the outcome will look like as you paint.
![toolbar](README_assets/toolbar.png)

### Exporting
When you're done painting and ready to make a patch or otherwise use the IDMask you just painted, you'll need to export it back to a dds. It is safe to overwrite the original DDS you imported, since this add-on makes no references to it.

#### Exporting IDMask Array
1. In the shader nodes, select and right click the main group (same thing from the setup)
2. Click "Export to IDMask Array"
3. Select your output file. Existing files will be overwritten.
    - This output file can be added to a patch however you'd like

#### Exporting Pattern Mask
The pattern mask doesn't need any special treatment. Although there is a button for quickly editing it, there is no special process for exporting it. If you added it as an external file, then the changes will be saved automatically by blender when prompted. Otherwise, you'll need to unpack or directly save the image. Basically, do the inverse of however you originally added it to the accurate shader.

## Other Notes
- This add-on is platform-independent. I develop on linux, but there's no reason it won't work on Windows. The only platform-dependent stuff is the calls to Texassemble, and the platform is detected automatically.
    - On linux, a sufficiently mature wine install and prefix should be available. If it can play a game, then it can do this. If your setup is weird, then modify the shim at `deps/texassemble` accordingly.

- Texassemble from [DirectXTex](https://github.com/microsoft/DirectXTex) is used internally. Its license is included at `deps/LICENSE`.

## TODO
I will accept pull requests for anything that can be justified, but these are priorities

- More restricted file types on import/export processes. Right now, it's the wild west. Anything that doesn't make sense will fail with a user-opaque error message, but that's not perfect. Export-wise, the file-type is ignored and a dds is emitted no matter what. This should be a little more clear in the flow.

- Add more ops so that IDMask import/export can be done from basically anywhere, rather than just via the shader nodes area. `ops/painting.py` has some code for automatically finding the main group that will help with this.

- The IDMask strip included in and used by the helldivers armory does have the information needed, but can't currently be imported and used. It'll be fairly easy to get working; the lower-level code is already written in `IDMask.py::from_strip_path()`, but there isn't a codepath that uses it in the UI.

- Better support for installing pillow
