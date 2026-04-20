from typing import Annotated, Callable, List, Literal, Tuple
import bpy
import sys
from bpy.types import Context, Event
from bpy.types import ShaderNodeGroup
from bpy.types import Image
from bpy.types import ShaderNodeTexImage
from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp

IDMaskSockets = Tuple[bpy.types.NodeSocketColor, bpy.types.NodeSocketFloat, bpy.types.NodeSocketColor, bpy.types.NodeSocketFloat]
IDMaskImageNodes = Tuple[ShaderNodeTexImage, ShaderNodeTexImage, ShaderNodeTexImage, ShaderNodeTexImage, ShaderNodeTexImage, ShaderNodeTexImage, ShaderNodeTexImage, ShaderNodeTexImage]
IDMaskImages = Tuple[Image, Image, Image, Image, Image, Image, Image, Image]

from .. import IDMask
def _make_id_mask_images(path: Path) -> IDMaskImages:
    if path.suffix == ".dds":
        mask = IDMask.from_array(path)
    elif path.suffix == ".png":
        mask = IDMask.from_strip_path(path)
    else:
        assert False

    name = path.stem

    td = mkdtemp()
    # placeholder block for a `with TemporaryDirectory as td` statement. 
    # This is omitted because I don't want the directories getting cleaned up right now
    if True: 
        td_path = Path(td)
        channel_paths = mask.save_channels(td_path, name)

        def load_image(path: Path) -> bpy.types.Image:
            im = bpy.data.images.load(path.as_posix(), check_existing=False)
            im.name = path.stem
            im.pack()
            # This is imporant; Color space transforms on these will really mess up the shader's behavior
            im.colorspace_settings.name = "Non-Color" #type: ignore
            return im
        
        images = tuple(load_image(path) for path in channel_paths)
    
    assert len(images) == 8
    return images

def _save_id_mask_array_from_images(dest_path: Path, images: IDMaskImages):
    td = mkdtemp()
    # placeholder block for a `with TemporaryDirectory as td` statement. 
    # This is omitted because I don't want the directories getting cleaned up right now
    if True: 
        td_path = Path(td)
        
        # unpack them to the temp dir
        for image in images:
            out_name = (td_path / image.name).with_suffix(".png").as_posix()
            image.save(filepath=out_name)

        id_mask = IDMask.from_channels_dir(td_path)
    
    with open(dest_path, 'wb') as out_file:
        out_file.write(id_mask.to_array().getbuffer())

EXPECTED_NODE_NAME_PART = "HD2 Shader Template"

def is_group_patched(main_group: ShaderNodeGroup) -> bool:
    SHADER_GROUP_NAMES = {
        "ID Mask Array": "ID Mask Array L1",
        "ID Mask Array(alpha)": "ID Mask Array L1(alpha)"
    }

    SHADER_GROUP_ADDED_INPUTS = [
        "ID Mask Array L2",
        "ID Mask Array L2(alpha)"
    ]

    for input in main_group.inputs:
        if input.name in SHADER_GROUP_ADDED_INPUTS or input.name in SHADER_GROUP_NAMES.values():
            return True

    return False

def trace_to_textures(input: bpy.types.NodeSocket) -> List[bpy.types.ShaderNodeTexImage]:
    '''Recursively search the input node tree for all Texture shader nodes. Texture nodes are returned in-order.'''
    if input.links is None or len(input.links) == 0:
        return []
    
    source_node = input.links[0].from_node
    #print("source node:", source_node)

    if isinstance(source_node, bpy.types.ShaderNodeTexImage):
        return [source_node]
    
    if source_node is None or source_node.inputs is None:
        #print("inputs dead end")
        return []
    
    found_recurse = []
    for input in source_node.inputs:
        #print("recursing on input:", input)
        found_recurse.extend(trace_to_textures(input))
    
    return found_recurse

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

def _tree_bounding_box(tree: bpy.types.ShaderNodeTree) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    '''computes and returns the bounding box of the given shader tree in top-left bottom-right form'''
    lx,hy = 0,0
    hx,ly = 0,0

    if len(tree.nodes) == 0:
        return (lx, hy), (hx, ly)
    
    lx,hy = tree.nodes[0].location.xy
    hx,ly = tree.nodes[0].location.xy

    for node in tree.nodes:
        x,y = node.location.xy

        lx = min(lx,x)
        hx = max(hx, x)

        ly = min(ly, y)
        hy = max(hy, y)
    
    return (lx, hy), (hx, ly)

def _get_group_inputs(main_group: ShaderNodeGroup) -> IDMaskSockets:
    inputs = main_group.inputs
    assert is_group_patched(main_group)

    l1 = inputs["ID Mask Array L1"]
    l1a = inputs["ID Mask Array L1(alpha)"]
    l2 = inputs["ID Mask Array L2"]
    l2a = inputs["ID Mask Array L2(alpha)"]

    assert isinstance(l1, bpy.types.NodeSocketColor)
    assert isinstance(l1a, bpy.types.NodeSocketFloat)
    assert isinstance(l2, bpy.types.NodeSocketColor)
    assert isinstance(l2a, bpy.types.NodeSocketFloat)

    return l1, l1a, l2, l2a

def get_idmask_channel_texture_nodes(main_group: ShaderNodeGroup) -> IDMaskImageNodes | None:
    '''gets the IDMask input textures, if available. Requires that the group be patched.'''
    assert is_group_patched(main_group)

    inputs = _get_group_inputs(main_group)
    texture_nodes = []
    for input in inputs:
        texture_nodes.extend(trace_to_textures(input))
    
    if not len(texture_nodes) >= 8:
        return None
    texture_nodes = tuple(texture_nodes)[:8] # take the first 8

    # texture nodes SHOULD be in-order here, because of how _trace_to_textures works.
    return texture_nodes

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
        assert an.node_tree is not None

        input_texture_nodes = get_idmask_channel_texture_nodes(an)
        assert input_texture_nodes is not None

        out_path = Path(self.filepath)
        if out_path.suffix == ".blend":
            raise Exception("Refusing to overwrite blend file!")
        
        def get_images(nodes: IDMaskImageNodes) -> IDMaskImages:
            images = tuple(node.image for node in nodes if node.image is not None)
            assert len(images) == 8
            return images
        
        images = get_images(input_texture_nodes)
        
        _save_id_mask_array_from_images(out_path, images)

        return {'FINISHED'}
    
    @classmethod
    def poll(cls, context: Context) -> bool:
        an = context.active_node
        if not isinstance(an, ShaderNodeGroup):
            cls.poll_message_set(f"The {EXPECTED_NODE_NAME_PART} node group must be selected.")
            return False
        
        if an is None or EXPECTED_NODE_NAME_PART not in an.label:
            cls.poll_message_set(f"Wrong name: The {EXPECTED_NODE_NAME_PART} shader node group must be selected. This one is '{an.label}'")
            return False
        
        if not is_group_patched(an):
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
        ul,_ = _tree_bounding_box(tree)
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

    @classmethod
    def _modify_shader_group(cls, an: ShaderNodeGroup):
        assert an.inputs is not None
        assert an.node_tree is not None

        # interface modifications
        nti: bpy.types.NodeTreeInterface = an.node_tree.interface #type: ignore

        nti.new_socket("ID Mask Array L2", in_out="INPUT", socket_type="NodeSocketColor")
        nti.new_socket("ID Mask Array L2(alpha)", in_out="INPUT", socket_type="NodeSocketFloat")

        gi = an.node_tree.nodes["Group Input"]
        l2 = gi.outputs["ID Mask Array L2"]
        l2a = gi.outputs["ID Mask Array L2(alpha)"]

        nti.items_tree["ID Mask Array"].name = "ID Mask Array L1" #type: ignore
        nti.items_tree["ID Mask Array(alpha)"].name = "ID Mask Array L1(alpha)" #type: ignore

        # internal group modifications 
        
        found = [node for node in an.node_tree.nodes if node.label == "ID Mask Array 02"]
        id_mask_array_02 = found[0]
        assert len(found) == 1
        assert isinstance(id_mask_array_02, bpy.types.ShaderNodeTexImage)

        
        # use the newly created inputs instead
        color_dest = id_mask_array_02.outputs['Color'].links[0].to_socket #type: ignore
        alpha_dest = id_mask_array_02.outputs['Alpha'].links[0].to_socket #type: ignore
        assert isinstance(color_dest, bpy.types.NodeSocket)
        assert isinstance(alpha_dest, bpy.types.NodeSocket)
        an.node_tree.links.new(color_dest, l2)
        an.node_tree.links.new(alpha_dest, l2a)

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

        # TODO: Set this to self.filepath
        #id_mask_array_path = Path("test/14455190118267868905.dds")
        id_mask_array_path = Path(self.filepath)

        # patch up the shader if needed
        if not is_group_patched(an):
            self._modify_shader_group(an)

        # get the IDMask group inputs
        inputs = _get_group_inputs(an)

        # make the id mask images from the array
        id_mask_channels = _make_id_mask_images(id_mask_array_path)

        # try and get existing texture inputs, and create them if necessary
        # either way, the new channels get assigned
        id_mask_channel_nodes = get_idmask_channel_texture_nodes(an)
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
        
        if not is_main_node_group(an, cls.poll_message_set):
            return False
        
        return True