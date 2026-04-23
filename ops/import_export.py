from typing import Annotated, Callable, List, Literal, Tuple
import bpy
from bpy.types import Context, Event
from bpy.types import ShaderNodeGroup
from bpy.types import Image
from pathlib import Path

from .utils.custom_types import *
from .utils import accurate_shader
from .utils import images as image_util
from .utils import tree as tree_util

class ExportToArrayOperator(bpy.types.Operator):
    bl_idname = "hd2visual.export_to_array"
    bl_label = "Export to Array"
    bl_options = {'REGISTER'}

    filepath: bpy.props.StringProperty(name="ID Mask Array Path", subtype="FILE_PATH") #type: ignore

    filter_glob: bpy.props.StringProperty(
        default="*.dds",
        options={'HIDDEN'},
    ) #type: ignore

    def draw(self, context):
        layout = self.layout
        assert layout is not None

        layout.label(text="Export to a .dds file.", icon='INFO')

    def invoke(self, context: Context, event: Event) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        assert context.window_manager is not None
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context: Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        an = context.active_node
        active_tree = context.space_data.edit_tree #type: ignore
        assert isinstance(active_tree, bpy.types.ShaderNodeTree)

        assert active_tree is not None
        assert isinstance(an, ShaderNodeGroup)
        mg = accurate_shader.AccurateShaderMainGroup(an)
        assert an.node_tree is not None
        
        input_texture_nodes = mg.get_idmask_channel_texture_nodes()
        assert input_texture_nodes is not None

        out_path = Path(self.filepath)
        if out_path.suffix == ".blend":
            raise Exception("Refusing to overwrite blend file!")
        
        def get_images(nodes: IDMaskImageNodes) -> IDMaskImages:
            images = tuple(node.image for node in nodes if node.image is not None)
            assert len(images) == 8
            return images
        
        images = get_images(input_texture_nodes)
        
        image_util.save_id_mask_array_from_images(out_path, images)

        return {'FINISHED'}
    
    @classmethod
    def poll(cls, context: Context) -> bool:
        an = context.active_node
        if not isinstance(an, ShaderNodeGroup):
            cls.poll_message_set(f"A node group must be selected.")
            return False
        
        if not accurate_shader.is_main_node_group(an, cls.poll_message_set):
            return False
        
        mg = accurate_shader.AccurateShaderMainGroup(an)
        
        if not mg.is_patched():
            cls.poll_message_set(f"The shader group must be patched first, before it can be exported.")
            return False
        return True

class MakeEditableOperator(bpy.types.Operator):
    bl_idname = "hd2visual.make_editable"
    bl_label = "Make Editable"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(name="ID Mask Path", subtype="FILE_PATH") #type: ignore

    filter_glob: bpy.props.StringProperty(
        default="*.png;*.dds",
        options={'HIDDEN'},
    ) #type: ignore

    def draw(self, context):
        layout = self.layout
        assert layout is not None

        layout.label(text="Select a 2-layer RGBA dds file to import", icon='INFO')

    @classmethod
    def _construct_id_mask_input_nodes(cls, tree: bpy.types.ShaderNodeTree, images: IDMaskImages) -> IDMaskSockets:
        ul,_ = tree_util.tree_bounding_box(tree)
        full_texture_node_height = 300.0
        ul = ul[0]-400.0, ul[1]+full_texture_node_height*9
        def make_uv() -> bpy.types.ShaderNodeUVMap:
            n = tree.nodes.new("ShaderNodeUVMap")
            assert isinstance(n, bpy.types.ShaderNodeUVMap)
            n.uv_map = "UVMap" # This is the uv map the shader expects to be used
            n.location.xy = ul[0]-400.0,ul[1]-800
            return n

        def make_cc() -> bpy.types.ShaderNodeCombineColor:
            n = tree.nodes.new("ShaderNodeCombineColor")
            assert isinstance(n, bpy.types.ShaderNodeCombineColor)
            n.mode = "RGB"
            n.location.xy = ul[0]+400.0, ul[1]-full_texture_node_height
            return n
            
        uv_map = make_uv()
        def make_tex(image: Image) -> bpy.types.ShaderNodeTexImage:
            nonlocal ul
            n = tree.nodes.new("ShaderNodeTexImage")
            assert isinstance(n, bpy.types.ShaderNodeTexImage)
            assert image.colorspace_settings is not None
            n.image = image
            # This is imporant; Color space transforms on these will really mess up the shader's behavior
            n.image.colorspace_settings.name = "Non-Color" #type: ignore
            tree.links.new(n.inputs[0], uv_map.outputs[0])
            n.location.xy = ul
            ul = ul[0], ul[1]-full_texture_node_height

            return n
        
        def make_layer_outputs(images: Tuple[Image, Image, Image, Image]) -> Tuple[bpy.types.NodeSocketColor, bpy.types.NodeSocketFloat]:
            '''Make 4 non-color image textures, and swizzle their black/white outputs to RGBA of a color'''
            cc = make_cc()
            r,g,b,a = (make_tex(image) for image in images)

            tree.links.new(cc.inputs[0], r.outputs["Color"])
            tree.links.new(cc.inputs[1], g.outputs["Color"])
            tree.links.new(cc.inputs[2], b.outputs["Color"])

            # Color -> float is mixing, but blender allows this and it's fine.
            # Outputting the Color output for the a channel is what is supposed to happen here. 
            # The actual data for that channel IS in the color!
            return cc.outputs["Color"], a.outputs["Color"] #type: ignore
        
        l1 = make_layer_outputs(images[:4])
        l2 = make_layer_outputs(images[4:])

        return (*l1, *l2)

    def invoke(self, context: Context, event: Event) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        assert context.window_manager is not None
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context: Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        an = context.active_node
        active_tree = context.space_data.edit_tree #type: ignore
        assert isinstance(active_tree, bpy.types.ShaderNodeTree)

        assert active_tree is not None
        assert isinstance(an, ShaderNodeGroup)
        assert an.node_tree is not None

        mg = accurate_shader.AccurateShaderMainGroup(an)

        #id_mask_array_path = Path("test/14455190118267868905.dds")
        id_mask_array_path = Path(self.filepath)

        # make the id mask images from the array
        id_mask_channels = image_util.make_id_mask_images(id_mask_array_path)

        # patch up the shader if needed
        if not mg.is_patched():
            mg.modify_shader_for_editing()

        # get the IDMask group inputs
        inputs = mg.get_group_inputs()

        # try and get existing texture inputs, and create them if necessary
        # either way, the new channels get assigned
        id_mask_channel_nodes = mg.get_idmask_channel_texture_nodes()
        if id_mask_channel_nodes is None:
            # construct the input nodes
            texture_outputs = self._construct_id_mask_input_nodes(active_tree, id_mask_channels)
            
            #link them up
            for input, output in zip(inputs, texture_outputs):
                active_tree.links.new(input, output)
        else:
            # change the texture nodes to point to the new channels
            for node, image in zip(id_mask_channel_nodes, id_mask_channels):
                node.image = image

        return {'FINISHED'}
    
    @classmethod
    def poll(cls, context: Context) -> bool:
        an = context.active_node
        
        if not accurate_shader.is_main_node_group(an, cls.poll_message_set):
            return False
        
        return True