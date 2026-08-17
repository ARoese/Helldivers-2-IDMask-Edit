from bpy.types import NodeTree, Material
import bpy
import typing
from typing import List, Tuple
from ..tree import trace_to_textures
from ..images import IDMaskImages, id_mask_from_blender_channels
from ....utils.IDMask import PackedChannels

# This module is created using https://extensions.blender.org/add-ons/node-to-python/
# don't expect any documentation in there
from .idmask_debug_material import shader_nodetree_node_group, onehot_8_1_node_group, debug_idmask_1_node_group
#from .idmask_debug_export import onehot_8_1_node_group, debug_idmask_1_node_group
    
def _internal_create_idmask_debug_material():
    # Maps node tree creation functions to the node tree 
    # name, such that we don't recreate node trees unnecessarily
    node_tree_names : dict[typing.Callable, str] = {}

    onehot_8 = onehot_8_1_node_group(node_tree_names)
    node_tree_names[onehot_8_1_node_group] = onehot_8.name

    debug_idmask = debug_idmask_1_node_group(node_tree_names)
    node_tree_names[debug_idmask_1_node_group] = debug_idmask.name

    shader_nodetree = shader_nodetree_node_group(node_tree_names)
    node_tree_names[shader_nodetree_node_group] = shader_nodetree.name

    return shader_nodetree

class IDMaskDebugMaterial:
    mat: Material

    def __init__(self, material: Material):
        if not self.is_debug_material(material):
            raise ValueError(f"The given material, {material.name}, is not a valid IDMask debug material")
        self.mat = material

    @classmethod
    def is_debug_material(cls, material: Material) -> bool:
        nt = material.node_tree
        if nt is None:
            #print("Debug material node tree is None")
            return False
        
        group = nt.nodes.find("Group")
        if group == -1:
            #print("Failed to find group")
            return False
        
        group = nt.nodes[group]
        assert isinstance(group, bpy.types.ShaderNodeGroup)
        if "debug idmask" not in group.node_tree.name: #type: ignore
            print(f"'debug idmask' not in '{group.node_tree.name}'") #type: ignore
            return False
        
        return True
    
    def get_layer_nodes(self) -> Tuple[List[bpy.types.ShaderNodeTexImage], bpy.types.ShaderNodeTexImage]:
        '''returns layer nodes and pattern mask node'''
        nt = self.mat.node_tree
        assert nt is not None

        output = nt.nodes["Material Output"]
        trace = trace_to_textures(output.inputs[0])
        layers = trace[:-1]
        pattern_mask = trace[-1]
        return layers, pattern_mask
    
    def get_layer_images(self) -> Tuple[IDMaskImages, bpy.types.Image] | None:
        '''returns layers and pattern mask'''
        layers, pattern_mask = self.get_layer_nodes()
        layers = [i.image for i in layers]
        if any(i is None for i in layers) or pattern_mask.image is None:
            return None
        
        tup = tuple(i for i in layers if i is not None)
        assert len(tup) == 8

        return tup, pattern_mask.image
    
    def set_layer_images(self, images: IDMaskImages):
        image_nodes, _ = self.get_layer_nodes()

        for inode,image in zip(image_nodes, images):
            inode.image = image
    
    def set_pattern_mask_image(self, pattern_mask: bpy.types.Image):
        _, pattern_mask_node = self.get_layer_nodes()

        pattern_mask_node.image = pattern_mask

    def get_pattern_mask_image(self) -> bpy.types.Image | None:
        _, pattern_mask_node = self.get_layer_nodes()

        return pattern_mask_node.image

    def make_idmask(self) -> PackedChannels:
        r = self.get_layer_images()
        if r is None:
            raise ValueError("Attempted to save channels from material with empty image nodes")
        
        channels, pattern_mask = r
        
        return id_mask_from_blender_channels(list(channels))

def create_idmask_debug_material() -> IDMaskDebugMaterial:
    mat = _internal_create_idmask_debug_material()

    return IDMaskDebugMaterial(mat)

def debug_material_from(mat: Material) -> IDMaskDebugMaterial | None:
    if IDMaskDebugMaterial.is_debug_material(mat):
        return IDMaskDebugMaterial(mat)
    
    return None