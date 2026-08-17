# Helldivers 2 IDMask editing

This blender addon enables the editing of the IDMask array and pattern mask texture for advanced LUT-compatible helldivers materials. 

**This add-on is for blender 4.3**. It probably also works on other versions, but that's not guarunteed. 

## Installation
1. install the [Helldivers 2 SDK](https://github.com/Boxofbiscuits97/HD2SDK-CommunityEdition)
2. download and install the [lastest release](https://github.com/ARoese/Helldivers-2-IDMask-Edit/releases) of the addon
    - Get the top-most zip file with the version in the name, NOT the respository zip
    - install via edit > preferences > Add-ons > Install from disk (top right)
3. install python libraries
    - **Automatic installation:**
        1. Press N in 3D view to open the panels tab
        2. In the "HD2 Visual Edit" group, click the "Install libs" button
        3. Restart blender
    - Manual installation options:
        - In the blender scripting tab, in the python repl, paste and run this command: 
            - `import sys, subprocess; subprocess.run([sys.executable, "-m", "pip", "install", "-y", "pillow", "pyopencl"]);`
        - At least one of these cli commands I wrote will also do it: 
            - `path\to\blender.exe -b --python-expr 'import sys, subprocess; subprocess.run([sys.executable, "-m", "pip", "install", "pillow", "pyopencl"]);'`
            - `blender -b --python-expr 'import sys, subprocess; subprocess.run([sys.executable, "-m", "pip", "install", "pillow", "pyopencl"]);'`


## Setup
### Accurate Shader
| Solid Shading Mode | Material Preview Shading Mode |
| ------------------ | ----------------------------- |
| ![main node](README_assets/accurate_shader_paint_solid.png)   | ![main node](README_assets/accurate_shader_paint_material_preview.png) |

1. Set up the helldivers 2 accurate shader for your model
    - By far, the easiest way to do this is by exporting a unit using [filediver](https://github.com/xypwn/filediver). The resulting blender object will have the shader set up for you.
    - See [this discord thread](https://discord.com/channels/1210541115829260328/1222290154409033889) for details and a video on how to do this manually
    - It comes down to exporting the mesh and associated textures. Specifically, the IDMask, Pattern mask, and LUTs
    - You can also append objects from the [helldivers 2 armory](https://discord.com/channels/1210541115829260328/1446534760045482046), which has this set up for each armor set
2. Import the IDMask dds
    1. Right click your object
    2. Click the "Import IDMask" option in the context menu.
        - Clicking this option again will give you the opportunity to import a different IDMask. The new channels will overwrite the old ones, and the shader will stay clean. This could be useful if you're painting variants.
    3. Select the IDMask array exported from helldivers.
        - You do not need to pre-process this file at all. A dds directly exported via the sdk or filediver should be fine. IDMasks exported using this addon should also work.
        - If your texture is an SDF, (it probably is) make sure the "Is SDF" box is checked and the resolution is set high enough for your desired detail. Otherwise, the mask will be blurry. See [What is an SDF](#what-is-an-sdf) for more information on this.
        - A png strip will also work for this.
        - If you don't have the ID mask, but have the accurate shader set up, you can save it from the shader by clicking the IDMask array image texture node, and then saving the linked image.
    4. Repeat for pattern mask

> [!WARNING]
> Once you import the shader in step 2, the accurate shader node graph is modified. The original script that is used to "update" or set up the accurate shader will PROBABLY not work anymore. It's most likely to just shred the node graph. If you want to change something that requires the use of this update script, you should export your IDMask and re-create the accurate shader. If you need to update the LUT because you modified it, you can do this by clicking the "Primary Material LUT Texture" shader node to open the linked image in the image viewer, then in the hamburger menu in the top left of the image viewer use `Image > Replace` or `Image > Reload`

### Debug Material
![main node](README_assets/debug_material_example.png)  
The accurate shader can be tedious to set up, especially for custom works, so a debug material is available. This lets you paint the IDMask directly onto a model without needing to worry about setting LUTs or other textures
1. Right click the object you want to edit an ID Mask on
2. Select "Create Debug IDMask"
    - In the bottom left, you can change the mask dimensions. This cannot be adjusted later, unless you import a mask with different dimensions.
    - if you are doing step 3, ignore this value. It will be overwritten by the incoming IDMask.
3. If you have an existing IDMask file you would like to edit, right click the object again and click "Apply IDMask to Debug Material"
    - If your texture is an SDF, (it probably is) make sure the "Is SDF" box is checked and the resolution is set high enough for your desired detail. Otherwise, the mask will be blurry. See [What is an SDF](#what-is-an-sdf) for more information on this.
4. Repeat for pattern mask

> [!NOTE] 
> I recommend that you always export the IDMask whenever you're done working, even if you plan to revisit it later. The intermediate textures created and used by the plugin are easy to get mixed up, and can disappear into temporary directories if they are unpacked.
    
> [!WARNING]
> Using image dimensions that are not powers of 2 (512, 1024, 2048, etc) will crash the game when loaded. This is a general limitation of helldivers textures, but this addon will give you the footgun to allow for special cases.

## Usage
### ID Mask Painting
#### General painting
The addon adds a toolbar accessible by pressing N in the 3d viewer in texture paint mode which allows quickly switching between materials being painted. If a material was not set up for painting, then these buttons will not be clickable. Hover over them to see why. IDMask painting is particularly fluid in the material preview rendering mode. 
![toolbar](README_assets/toolbar.png)

When painting IDMasks, your brush should be set to either black or white. Switching between layers will set your brush to be black and white in order to enforce this. Colors make no sense in this context and will cause problems down the line. This can be unintuitive, especially in the debug material where your all-white strokes will appear colored, but it will make more sense if you think of colors as being strictly for identifying IDMask layers.

This addon makes painting the IDMask easier, but you do still need to know how the materials interact when layered. The accurate shader is very, very accurate (as expected) with this, and the debug shader does a fairly good job of approximating the interaction.

The debug material can alert you to ID Mask painting issues where it is unclear which LUT row should take priority. This can happen when two or more ID Mask layers are set to 1, and thus will clash. (usually the higher-numbered row takes priority) If you see two IDMask colors mixing to create a third color, (Red + Blue combining to make yellow) it means that those masks are equal or set to 1 at that location and should be adjusted.

#### Exporting
When you're done painting and ready to make a patch or otherwise use the IDMask you just painted, you'll need to export it back to a dds. It is safe to overwrite the original DDS you imported, since this add-on makes no references to it. See [What is an SDF](#what-is-an-sdf) for proper SDF-vs-binary hygeine. Generally, you should keep and edit a high-resolution array, then export that to a lower resolution SDF that you put in the patch.

> [!WARNING]
> Using image dimensions that are not powers of 2 (512, 1024, 2048, etc) will crash the game when loaded. This is a general limitation of helldivers textures, but this addon will give you the footgun to allow for special cases.

##### Exporting IDMask Array
1. Right click your object in object mode
2. Click "Export IDMask to Array"
3. Set your output file. It must be a DDS. Existing files will be overwritten.
    - This output file can be added to a patch however you'd like
    - see [What is an SDF](#what-is-an-sdf) for information on the "as SDF" option. You want to use this!

##### Exporting Pattern Mask
1. Right click your object in object mode
2. Click "Export Pattern Mask"
3. Set your output file. Existing files will be overwritten.
    - This output file can be added to a patch however you'd like
    - see [What is an SDF](#what-is-an-sdf) for information on the "as SDF" option. You want to use this!

##### What is an SDF?
When importing and exporting IDMask arrays, you can find "is SDF?" and "as SDF" checkboxes. You should look at the pretty pictures in [this whitepaper by valve](https://steamcdn-a.akamaihd.net/apps/valve/2007/SIGGRAPH2007_AlphaTestedMagnification.pdf) to see why SDFs are used in HD2 and what problem they solve. I also reference it in this explanation.

HD2 always interprets the mask textures it loads as Signed Distance Fields, (SDFs) no matter what you give it. Almost all IDMasks you get from the game are SDFs. When you are painting ID masks, you generally want to be painting a binary mask where white = paint material, and black = don't paint material, for it to be intuitive. This binary mask you paint is an acceptable degenerate case of an SDF, which is why it's fine to export it directly as a high resolution SDF. Your mask needs to be high resolution to get good detail on your model, but these high resolution textures are very resource and memory heavy. If you just naively downscale the mask, though, you start getting wiggly artifacts on non-axis-aligned edges like in Figure 1(b) (center image at the top) of the whitepaper. If you instead convert the image to an SDF, then the result is much more well-behaved when downscaled and upscaled. As an oversimplification, conversion to an SDF takes information about the edges of shapes that would normally be lost, and spreads it out across surrounding pixels so that it can be reconstructed later. The only remaining artifacts are then sharp corners getting rounded off. 

**TL;DR:** 
- SDFs look blurry, non-SDFs (binary masks) look sharp. 
- Masks exported from the game are almost always SDFs
- You should paint high resolution binary masks and export to a lower resolution SDF when you make your patch. 
- An SDF is a low-resolution blurry image that technomagically represents a higher-resolution binary mask image with clean, sharp edges. 
- If you tell this addon that a mask you're giving it is an SDF, it can convert it to a higher resolution sharp version that is nice to edit. 
- When you export a mask, you can convert it into a downscaled SDF with minimal detail loss. 
- A mask with sharper corners needs a higher resolution SDF to represent them. Smooth, predictable edges lend themselves to lower SDF resolutions.

> [!WARNING]
> Conversion to and from an SDF is not lossless. You should always retain a high-resolution version of the mask, and export a low resolution SDF that you add to a patch.

### Asset Merging
Objects using the accurate shader can be merged. This will combine the primary and secondary LUTs of the merged objects, and stack the IDMasks to conform with those new LUTs. This is required because armor primary LUTs are hard-coded. Even when using multiple armor lut materials on a single armor, they are all hard-coded to use the same primary LUT. This merging process produces a valid shared primary LUT and IDMasks that correctly index into it.
The secondary LUTs aren't useful, but they are merged anyways in case more is learned about them. These merged objects do **NOT** respect other LUT edit mods, but they will have blood and gunk visible.

> [!TIP]
> Accurate shader materials that have been modified for IDMask painting (described in the above section) will work seamlessly here. You **DON'T** need to create a new one that used the produced dds file directly.

| |                                   |                    |
|---|-----------------------------------|--------------------|
| ![toolbar](README_assets/merge_assets.png) | ![toolbar](README_assets/complex_merge_result.png)  | ![toolbar](README_assets/complex_merge_result_with_gunk.png)  |

1. Ensure a patch is active in the SDK.
    - You can click "new patch" to make a new one
2. Select all objects to be merged in object mode. 
    - Each one should have ONLY the accurate shader.
    - The active object (the last object selected and highlighted orange instead of red) matters here. It should be the unit you are eventually replacing with this merged object.
    (read: the object you will be copying helldiver properties from)
3. Click "Merge assets" in the context menu
4. Select output folder
    - The resultant object will appear black in material preview mode from this point forward. Trust the process.

> [!WARNING]
> After the merge is complete, you will not be able to edit the IDMasks and LUTs of the result using this plugin. If you make copies of the objects and merge the copies, I have seen the merge operation still end up breaking the original objects because of changes to the texture data blocks. I personally only merge as part of making a patch, and don't save the blend afterwards. Merging is quick to do, but somewhat destructive.

An SDK-compatible armor LUT material is created for each object, and the objects are merged into one. The relevant inputs are also wired up automatically. The resultant object is ready to be added to the patch.

2 files are placed into the selected output folder, where OBJECT_NAME is the name of the active object:
- `OBJECT_NAME-primary-lut-atlas.dds`: primary lut stack
- `OBJECT_NAME-secondary-lut-atlas.dds`: secondary lut stack (not useful for you)
Additionally, an id mask array is created for each merged object. They are named as `OBJECT_NAME-idmask.dds`. The armor LUT materials are automatically wired up using the textures in the accurate shader. Files were automatically converted as necessary.

5. If you are producing an armor, (you probably are) then **also** replace that armor's primary LUT with the LUT atlas (`OBJECT_NAME-primary-lut-atlas.dds`) in the patch, because that is hard-coded.
    - This overwrites the primary LUT for that entire armor set, and thus will affect other pieces of your armor. If you made sure that your active object selected
    in step 1 would also uses that armor's primary LUT, then the first 8 rows of the primary LUT atlas will be the armor set's entire primary LUT. The result is that 
    "dumb" armor pieces with only 8-channel IDMasks will still use only those rows, and your extra LUT rows are hidden away from them using IDMask channels they lack.
    - TL;DR: Make sure your active object in step 1 is something that already exists in the destination armor, or it will break everything sharing that LUT!

> [!NOTE]
> **Remember,** This resulting armor is *NOT* compatible with generic LUT replacement mods. It must be beneath them in the load order or otherwise overwrite them! The indicator that this is happening is one part of the armor looks fine but the rest is completely black. 
> 
> If you want your result to be visually consistent with other LUT edit mods, then you need to use the primary LUT contained in that mod when merging here instead of the LUT from the base game. I recommend distributing these as alternative "options" in your mod, should you choose to create them.

## Q/A
Q: I imported an IDMask and it's blurry! How do I edit this?  
A: Re-import and check "is SDF" in the file picker dialogue. Also see [What is an SDF?](#what-is-an-sdf)

## Known Issues
- When performing a merge operation, if any of the relevant textures is a data block with a broken link, (it is an external or linked image, and that link is broken) then blender will hang and just eat ram. This can happen sometimes when using arsenal shaders that have been appended from another blend file. If your material looks broken, then merging with it might fail!
- Performing the merge operation on copies of objects can break the originals. This obstructs a workflow that involves merging once and just always adding that to the patch while maintaining un-merged copies of the constituent objects in case changes want to be made later. My recommendation is to use asset merging as a step of making your patch, which will be intentionally not saved.

## Reporting Issues
If you encounter issues or need help, you can either open an issue on github or contact me (@DrLong) in the [Helldivers 2 Modding Community discord server](https://discord.gg/ZwjPaZNwH7). Make sure you ping me, because I probably won't see it otherwise.

## Other Notes
- This add-on is platform-independent. I develop on linux, but windows is supported. The only platform-dependent stuff is the calls to Texassemble, Texconv, and LUTranslate, and the platform is detected automatically.
    - On linux, a sufficiently mature wine install and prefix should be available. If it can play a game, then it can do this. If your setup is weird, then modify the shims at `deps` accordingly.

- Texassemble and Texconv from [DirectXTex](https://github.com/microsoft/DirectXTex) are used internally. Their license is included at `deps/LICENSE`.

- Recommended commands for making a release:
    1. $`git archive HEAD -o ../IDMask-Edit.zip`
    2. unzip and re-zip the IDMask-Edit zip so that it has a parent folder in the zip

    - Or run `make_release.sh`

## TODO
I will accept pull requests for anything that can be justified, but these are priorities

- Clean up code. Currently, I can't think of any features or QOL tweaks to add
