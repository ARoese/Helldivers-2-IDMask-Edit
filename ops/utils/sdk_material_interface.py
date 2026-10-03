from typing import Tuple
from pathlib import Path

import bpy
from bpy.types import Material
from bpy.types import ShaderNodeTexImage, ShaderNode
from bpy.types import Image

from .tree import trace_to_textures
_SDK_MISSING_ERROR_STRING = "Helldivers 2 SDK is not installed, or it is unresolvably different. Create an issue on github or otherwise contact this addon's author. DO NOT CONTACT THE HELLDIVERS 2 SDK AUTHOR ABOUT THIS."

def get_hd2_object_id(obj: bpy.types.Object) -> int | None:
    try:
        id_str: str = obj["Z_ObjectID"]
        return int(id_str)
    except:
        print(f"Failed to find object ID of '{obj.name}'")
        return None

# reference operator definition
# class ManuallyLoadArchivesOperator(Operator):
# bl_label = "Load Archive By ID"
# bl_idname = "helldiver2.archives_import_manual"
# bl_description = "Loads Archive by Archive ID"
#
# archive_id: StringProperty(name="Archive ID")
def load_archive(archive_id: int):
    try:
        archives_import_manual: bpy.types.Operator = bpy.ops.helldiver2.archives_import_manual #type: ignore
    except:
        raise Exception(_SDK_MISSING_ERROR_STRING)

    # TODO: This has incorrect behvaior if you submit it in decimal. It appears to try to support 
    # both hex and dec, but you need to submit hex without the 0x for it to work properly.
    # A fix should be submitted upstream
    archives_import_manual(archive_id=f"{archive_id:x}") # type: ignore

# reference operator definition
# import texture from archive button
#class SaveTextureFromDDSOperator(Operator, ImportHelper):
#    bl_label = "Import DDS"
#    bl_idname = "helldiver2.texture_savefromdds"
#    bl_description = "Override Current Texture with a Selected DDS File"
#
#    filter_glob: StringProperty(default='*.dds', options={'HIDDEN'})
#    object_id: StringProperty(options={"HIDDEN"})
#    def execute(self, context):
#        if PatchesNotLoaded(self):
#            return {'CANCELLED'}
#        EntriesIDs = IDsFromString(self.object_id)
#        for EntryID in EntriesIDs:
#            SaveImageDDS(self.filepath, EntryID)
#        
#        # Redraw
#        for area in context.screen.areas:
#            if area.type == "VIEW_3D": area.tag_redraw()
#
#        return{'FINISHED'}
def add_dds_to_patch(object_id: int, dds_path: Path):
    try:
        save_from_dds_operator: bpy.types.Operator = bpy.ops.helldiver2.texture_savefromdds #type: ignore
    except:
        raise Exception(_SDK_MISSING_ERROR_STRING)
    
    save_from_dds_operator(filepath=dds_path.as_posix(), object_id=f"{object_id}") # type: ignore


# reference operator definition
#class AddMaterialOperator(Operator):
#    bl_label = "Add Material"
#    bl_idname = "helldiver2.material_add"
#    bl_description = "Adds a New Material to Current Active Patch"
#
#    global Global_Materials
#    selected_material: EnumProperty(items=Global_Materials, name="Template", default=0)
#
#    def execute(self, context):
#        if PatchesNotLoaded(self):
#            return {'CANCELLED'}
#        
#        CreateModdedMaterial(self.selected_material)
#
#        # Redraw
#        for area in context.screen.areas:
#            if area.type == "VIEW_3D": area.tag_redraw()
#        LoadEntryLists()
#        
#        return{'FINISHED'}
#
#    def invoke(self, context, event):
#        return context.window_manager.invoke_props_dialog(self)

# Armor LUT index: 8
# Armor LUT definition: ("armorlut", "Armor LUT", "An advanced material using multiple mask textures and LUTs to texture the mesh only advanced users should be using this. Sourced from the base game material on Armors")
def poll_create_sdk_lut_material() -> str | None:
    try:
        # we know this exists because it's a dependency
        material_add_operator = bpy.ops.helldiver2.material_add #type: ignore
        if material_add_operator.poll():
            return None
        else:
            return "SDK lut material create poll failed. You probably need to create a new patch."
    except:
        return _SDK_MISSING_ERROR_STRING

def create_sdk_lut_material() -> Material:
    try:
        # we know this exists because it's a dependency
        material_add_operator = bpy.ops.helldiver2.material_add #type: ignore
    except:
        raise Exception(_SDK_MISSING_ERROR_STRING)
    
    #material_add_operator.selected_material = 8

    before_materials = set(material for material in bpy.data.materials)
    material_add_operator(selected_material="armorlut")

    for material in bpy.data.materials:
        if material not in before_materials:
            return material
    
    raise Exception("sdk material creation failed")

def _is_main_node(node: ShaderNode) -> bool:
    input_names = set(inp.name for inp in node.inputs)
    for indicator_name in ["Decal", "Pattern LUT", "Normal", "Pattern Mask", "ID Mask Array", "Primary LUT"]:
        if indicator_name not in input_names:
            return False
    
    return True

def setup_sdk_lut_material(
        sdk_material: Material, 
        decal: Image | None = None,
        pattern_lut: Image | None = None,
        normal: Image | None = None,
        pattern_mask: Image | None = None,
        id_mask_array: Image | None = None,
        primary_lut: Image | None = None
    ) -> None:
    assert sdk_material.use_nodes
    assert sdk_material.node_tree is not None
    main_node = None
    for node in sdk_material.node_tree.nodes:
        if not isinstance(node, ShaderNode):
            continue
        if _is_main_node(node):
            main_node = node
            break
    
    if main_node is None:
        raise Exception("Failed to find lut material's main node")
    
    for image, dest_node_name in [
        (decal, "Decal"),
        (pattern_lut, "Pattern LUT"),
        (normal, "Normal"),
        (pattern_mask, "Pattern Mask"),
        (id_mask_array, "ID Mask Array"),
        (primary_lut, "Primary LUT")
        ]:
        if image is None:
            continue

        if image.packed_file is not None:
            raise Exception("Cannot use packed file in lut material")
        
        tttr = trace_to_textures(main_node.inputs[dest_node_name])
        if not tttr:
            raise Exception(f"Failed to trace to texture for input node {dest_node_name}")
        
        tttr[0].image = image