import bpy
from typing import Callable
from bpy.types import ShaderNodeGroup

from ..utils.images import id_mask_from_blender_channels, id_mask_from_blender_strip
from .custom_types import *
from .tree import trace_to_textures
from ...IDMask import PackedChannels as PackedChannelsType

EXPECTED_NODE_NAME_PART = "HD2 Shader Template"

def _throw_away(*inp) -> None:
    return

def is_main_node_group(node: bpy.types.Node | None, fail_reason: Callable[[str], None] = _throw_away) -> bool:
    if not isinstance(node, ShaderNodeGroup):
        fail_reason(f"The {EXPECTED_NODE_NAME_PART} node group must be selected.")
        return False
    
    if EXPECTED_NODE_NAME_PART not in node.label:
        fail_reason(f"Wrong name: The {EXPECTED_NODE_NAME_PART} shader node group must be selected. This one is '{node.label}'")
        return False
    
    return True

class AccurateShaderMainGroup:
    ref: ShaderNodeGroup
    def __init__(self, ref: ShaderNodeGroup):
        self.ref = ref
        assert is_main_node_group(ref)

    def is_patched(self) -> bool:
        SHADER_GROUP_NAMES = {
            "ID Mask Array": "ID Mask Array L1",
            "ID Mask Array(alpha)": "ID Mask Array L1(alpha)"
        }

        SHADER_GROUP_ADDED_INPUTS = [
            "ID Mask Array L2",
            "ID Mask Array L2(alpha)"
        ]

        for input in self.ref.inputs:
            if input.name in SHADER_GROUP_ADDED_INPUTS or input.name in SHADER_GROUP_NAMES.values():
                return True

        return False

    def get_group_inputs(self) -> IDMaskSockets:
        inputs = self.ref.inputs
        assert self.is_patched()

        l1 = inputs["ID Mask Array L1"]
        l1a = inputs["ID Mask Array L1(alpha)"]
        l2 = inputs["ID Mask Array L2"]
        l2a = inputs["ID Mask Array L2(alpha)"]

        assert isinstance(l1, bpy.types.NodeSocketColor)
        assert isinstance(l1a, bpy.types.NodeSocketFloat)
        assert isinstance(l2, bpy.types.NodeSocketColor)
        assert isinstance(l2a, bpy.types.NodeSocketFloat)

        return l1, l1a, l2, l2a

    def get_idmask_channel_texture_nodes(self) -> IDMaskImageNodes | None:
        '''gets the IDMask input textures, if available. Requires that the group be patched.'''
        assert self.is_patched()

        inputs = self.get_group_inputs()
        texture_nodes = []
        for input in inputs:
            texture_nodes.extend(trace_to_textures(input))
        
        if not len(texture_nodes) >= 8:
            return None
        texture_nodes = tuple(texture_nodes)[:8] # take the first 8

        # texture nodes SHOULD be in-order here, because of how _trace_to_textures works.
        return texture_nodes
    
    def get_primary_lut_texture_node(self) -> ShaderNodeTexImage | None:
        '''gets the texture node for the primary lut'''

        nodes = trace_to_textures(self.ref.inputs["Primary Material LUT"])
        if nodes:
            return nodes[0]
        
        return None
    
    def get_secondary_lut_texture_node(self) -> ShaderNodeTexImage | None:
        '''gets the texture node for the secondary lut'''

        nodes = trace_to_textures(self.ref.inputs["Secondary Material LUT"])
        if nodes:
            return nodes[0]
        
        return None
    
    def get_normal_texture_node(self) -> ShaderNodeTexImage | None:
        '''gets the texture node for the normal map'''

        nodes = trace_to_textures(self.ref.inputs["Normal Map"])
        if nodes:
            return nodes[0]
        
        return None
    
    def get_idmask(self) -> PackedChannelsType | None:
        if self.is_patched():
            tns = self.get_idmask_channel_texture_nodes()
            if tns is None:
                return None
            res = [tn.image for tn in tns if tn.image is not None]
            if len(res) != len(tns):
                return None
            
            mask = id_mask_from_blender_channels(res)
        else:
            tn = trace_to_textures(self.ref.inputs["ID Mask Array"])
            if not tn:
                return None
            
            if tn[0].image is None:
                return None
            
            mask = id_mask_from_blender_strip(tn[0].image)
        
        if mask.num_channels() != 8:
            raise ValueError(f"Expected 8 channels. Got {mask.num_channels()}")
        
        return mask

    def find_pattern_mask_node(self) -> bpy.types.ShaderNodeTexImage | None:
        tl = trace_to_textures(self.ref.inputs["Pattern Mask Array"])
        if len(tl) == 0:
            return None

        return tl[0]
    
    def modify_shader_for_editing(self):
        mg = self.ref
        assert mg.inputs is not None
        assert mg.node_tree is not None

        # interface modifications
        nti: bpy.types.NodeTreeInterface = mg.node_tree.interface #type: ignore

        nti.new_socket("ID Mask Array L2", in_out="INPUT", socket_type="NodeSocketColor")
        nti.new_socket("ID Mask Array L2(alpha)", in_out="INPUT", socket_type="NodeSocketFloat")

        gi = mg.node_tree.nodes["Group Input"]
        l2 = gi.outputs["ID Mask Array L2"]
        l2a = gi.outputs["ID Mask Array L2(alpha)"]

        nti.items_tree["ID Mask Array"].name = "ID Mask Array L1" #type: ignore
        nti.items_tree["ID Mask Array(alpha)"].name = "ID Mask Array L1(alpha)" #type: ignore

        # internal group modifications 
        
        found = [node for node in mg.node_tree.nodes if node.label == "ID Mask Array 02"]
        id_mask_array_02 = found[0]
        assert len(found) == 1
        assert isinstance(id_mask_array_02, bpy.types.ShaderNodeTexImage)

        
        # use the newly created inputs instead
        color_dest = id_mask_array_02.outputs['Color'].links[0].to_socket #type: ignore
        alpha_dest = id_mask_array_02.outputs['Alpha'].links[0].to_socket #type: ignore
        assert isinstance(color_dest, bpy.types.NodeSocket)
        assert isinstance(alpha_dest, bpy.types.NodeSocket)
        mg.node_tree.links.new(color_dest, l2)
        mg.node_tree.links.new(alpha_dest, l2a)

def find_main_group(obj: bpy.types.Object) -> AccurateShaderMainGroup | None:
    for ms in obj.material_slots:
        if ms.material is None:
            continue

        if not ms.material.use_nodes:
            continue
        
        if ms.material.node_tree is None:
            continue
        
        for node in ms.material.node_tree.nodes:
            if node is None:
                continue
            if isinstance(node, bpy.types.ShaderNodeGroup) and is_main_node_group(node):
                return AccurateShaderMainGroup(node)
            
