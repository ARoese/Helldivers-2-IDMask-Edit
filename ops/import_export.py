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
from ..utils.IDMask import PackedChannels

from .utils.idmask_debug_material import create_idmask_debug_material
from .utils.images import IDMaskImages, make_id_mask_images, id_mask_array_from_images
from ..utils import IDMask, sdf_mask

from .utils.idmask_debug_material import IDMaskDebugMaterial

from PIL import Image as PILImage

class IDMask_Import(bpy.types.Operator):
    '''utility superclass for operations that import an IDMask'''
    filepath: bpy.props.StringProperty(name="ID Mask Path", subtype="FILE_PATH") #type: ignore
    is_sdf: bpy.props.BoolProperty(default=True, name="Is SDF", description="Assume the given mask is an SDF. SDFs have soft, blurry edges. This will allow intuitive fine editing of the imported mask.") #type: ignore
    sdf_upscale_target: bpy.props.IntProperty(name="Target Resolution", default=1024, min=32, description="The resolution that this mask will be edited at. You can set this very high, as it can be downscaled on export.") #type: ignore

    filter_glob: bpy.props.StringProperty(
        default="*.png;*.dds",
        options={'HIDDEN'},
    ) #type: ignore

    def draw(self, context):
        layout = self.layout
        assert layout is not None

        layout.label(text="Select a 2-layer RGBA dds file or png strip to import", icon='INFO')
        
        layout.prop(self, "is_sdf")
        if self.is_sdf:
            layout.prop(self, "sdf_upscale_target")

    def invoke(self, context: Context, event: Event) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        assert context.window_manager is not None
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def read_picked_mask(self) -> Tuple[str, PackedChannels]:
        '''read the IDMask picked by the user, applying SDF conversion as needed. Returns the mask, and the name associated with that mask'''
        id_mask_array_path = Path(self.filepath)
        id_mask_array = IDMask.from_file(id_mask_array_path)

        if self.is_sdf:
            id_mask_array = id_mask_array.upscale_at((self.sdf_upscale_target, self.sdf_upscale_target))

        return (id_mask_array_path.stem, id_mask_array)

class IDMask_Export(bpy.types.Operator):
    '''utility superclass for operations that export an IDMask'''
    filepath: bpy.props.StringProperty(name="ID Mask Array Path", subtype="FILE_PATH") #type: ignore
    
    filter_glob: bpy.props.StringProperty(
        default="*.dds",
        options={'HIDDEN'},
    ) #type: ignore

    to_sdf: bpy.props.BoolProperty(default=False, name="as SDF", description="Export to a SDF at a lower resolution. See the README to understand what this means.") #type: ignore
    sdf_downscale_target: bpy.props.IntProperty(name="SDF resolution", default=256, min=32, description="The resolution of the exported SDF.") #type: ignore

    def draw(self, context):
        layout = self.layout
        assert layout is not None

        layout.label(text="Export to a .dds file.", icon='INFO')
                
        layout.prop(self, "to_sdf")
        if self.to_sdf:
            layout.prop(self, "sdf_downscale_target")

    def invoke(self, context: Context, event: Event) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        assert context.window_manager is not None
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def write_mask(self, mask: PackedChannels):
        '''write the given IDMask to the location picked by the user, applying SDF conversion as needed.'''
        out_path = Path(self.filepath)
        if out_path.suffix == ".blend":
            raise Exception("Refusing to overwrite blend file!")

        if self.to_sdf:
            mask = mask.downscale_sdf((self.sdf_downscale_target, self.sdf_downscale_target))

        with open(out_path, 'wb') as out_file:
            out_file.write(mask.to_array().getbuffer())

class ExportToArrayOperator(IDMask_Export):
    bl_idname = "hd2visual.export_to_array"
    bl_label = "Export to Array"
    bl_options = {'REGISTER'}

    def execute_accurate_shader(self, context: Context):
        ao = context.active_object
        assert ao is not None
        am = ao.active_material
        assert am is not None

        mg = accurate_shader.from_material(am)
        assert mg is not None

        active_tree = am.node_tree
        assert active_tree is not None
        
        input_texture_nodes = mg.get_idmask_channel_texture_nodes()
        assert input_texture_nodes is not None
        
        def get_images(nodes: IDMaskImageNodes) -> IDMaskImages:
            images = tuple(node.image for node in nodes if node.image is not None)
            assert len(images) == 8
            return images
        
        images = get_images(input_texture_nodes)
        
        mask = image_util.id_mask_array_from_images(images)
        self.write_mask(mask)

    def execute_debug_material(self, context: Context):
        ao = context.active_object
        assert ao is not None
        am = ao.active_material
        assert am is not None
        am = IDMaskDebugMaterial(am)

        images = am.get_layer_images()
        assert images is not None
        layer_images, pattern_image = images

        id_mask = id_mask_array_from_images(layer_images)
        self.write_mask(id_mask)

    def execute(self, context: Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        ao = context.active_object
        assert ao is not None
        am = ao.active_material
        assert am is not None

        if accurate_shader.from_material(am) is not None:
            self.execute_accurate_shader(context)
        else:
            self.execute_debug_material(context)

        return {'FINISHED'}

    @classmethod
    def poll(cls, context: Context) -> bool:
        ao = context.active_object
        if ao is None or ao.active_material is None:
            cls.poll_message_set("An editable material must be active")
            return False
        
        am = ao.active_material
        if am.node_tree is None:
            cls.poll_message_set("Active material node tree is None")
            return False

        if IDMaskDebugMaterial.is_debug_material(am):
            return True
        
        if (mg := accurate_shader.from_material(ao.active_material, cls.poll_message_set)) is None:
            return False
        
        if not mg.is_patched():
            cls.poll_message_set(f"The shader group must be patched first, before it can be exported.")
            return False
        return True

class ImportIDMaskOperator(IDMask_Import):
    '''Import an ID mask from either a .dds or a .png strip'''
    bl_idname = "hd2visual.import_idmask"
    bl_label = "Import IDMask"
    bl_options = {'REGISTER', 'UNDO'}

    def execute_accurate_shader(self, context: Context):
        ao = context.active_object
        assert ao is not None
        am = ao.active_material
        assert am is not None

        mg = accurate_shader.from_material(am)
        assert mg is not None

        active_tree = am.node_tree
        assert active_tree is not None

        #id_mask_array_path = Path("test/14455190118267868905.dds")
        name, id_mask_array = self.read_picked_mask()

        # make the id mask images from the array
        id_mask_channels = image_util.make_id_mask_images(id_mask_array, name)
        mg.set_idmask_images(id_mask_channels)

    def execute_debug_material(self, context: Context):
        ao = context.active_object
        assert ao is not None
        am = ao.active_material
        assert am is not None
        am = IDMaskDebugMaterial(am)

        name, id_mask_array = self.read_picked_mask()

        # make the id mask images from the array
        id_mask_channels = make_id_mask_images(id_mask_array, name)
        am.set_layer_images(id_mask_channels)

    def execute(self, context: Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        ao = context.active_object
        assert ao is not None
        am = ao.active_material
        assert am is not None

        if IDMaskDebugMaterial.is_debug_material(am):
            self.execute_debug_material(context)
        else:
            self.execute_accurate_shader(context)
        return {'FINISHED'}
    
    @classmethod
    def poll(cls, context: Context) -> bool:
        ao = context.active_object
        if ao is None or ao.active_material is None:
            cls.poll_message_set("An editable material must be active")
            return False

        am = ao.active_material
        if am.node_tree is None:
            cls.poll_message_set("Active material node tree is None")
            return False

        if IDMaskDebugMaterial.is_debug_material(am):
            return True

        if accurate_shader.from_material(am, cls.poll_message_set) is None:
            return False
        
        return True

class ImportPatternMaskOperator(bpy.types.Operator):
    '''Import a pattern mask from either a PNG or a strip'''
    bl_idname = "hd2visual.import_pattern_mask"
    bl_label = "Import pattern mask"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(name="ID Mask Path", subtype="FILE_PATH") #type: ignore
    is_sdf: bpy.props.BoolProperty(default=True, name="Is SDF", description="Assume the given mask is an SDF. SDFs have soft, blurry edges. This will allow intuitive fine editing of the imported mask.") #type: ignore
    sdf_upscale_target: bpy.props.IntProperty(name="Target Resolution", default=1024, min=32, description="The resolution that this mask will be edited at. You can set this very high, as it can be downscaled on export.") #type: ignore

    filter_glob: bpy.props.StringProperty(
        default="*.png;*.dds",
        options={'HIDDEN'},
    ) #type: ignore

    def draw(self, context):
        layout = self.layout
        assert layout is not None

        layout.label(text="Select a png or dds to import", icon='INFO')
        
        layout.prop(self, "is_sdf")
        if self.is_sdf:
            layout.prop(self, "sdf_upscale_target")

    def invoke(self, context: Context, event: Event) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        assert context.window_manager is not None
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute_accurate_shader(self, context: Context, pattern_mask_image: bpy.types.Image):
        ao = context.active_object
        assert ao is not None
        am = ao.active_material
        assert am is not None

        mg = accurate_shader.from_material(am)
        assert mg is not None

        active_tree = am.node_tree
        assert active_tree is not None

        pmn = mg.find_pattern_mask_node()
        assert pmn is not None

        pmn.image = pattern_mask_image

    def execute_debug_material(self, context: Context, pattern_mask_image: bpy.types.Image):
        ao = context.active_object
        assert ao is not None
        am = ao.active_material
        assert am is not None
        am = IDMaskDebugMaterial(am)

        am.set_pattern_mask_image(pattern_mask_image)

    def execute(self, context: Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        ao = context.active_object
        assert ao is not None
        am = ao.active_material
        assert am is not None

        pm_path = Path(self.filepath)
        if not ".dds" in pm_path.name:
            pm_image = PILImage.open(pm_path)
        else:
            pm_image = IDMask.from_array(pm_path).channels[0]

        if self.is_sdf:
            pm_image = sdf_mask.sdf_channel_to_straight(pm_image, (self.sdf_upscale_target, self.sdf_upscale_target))

        pm_image = image_util.blender_image_from_pillow_image(pm_image)

        if IDMaskDebugMaterial.is_debug_material(am):
            self.execute_debug_material(context, pm_image)
        else:
            self.execute_accurate_shader(context, pm_image)
        return {'FINISHED'}


    @classmethod
    def poll(cls, context: Context) -> bool:
        ao = context.active_object
        if ao is None or ao.active_material is None:
            cls.poll_message_set("An editable material must be active")
            return False

        am = ao.active_material
        if am.node_tree is None:
            cls.poll_message_set("Active material node tree is None")
            return False

        if IDMaskDebugMaterial.is_debug_material(am):
            return True

        if (mg := accurate_shader.from_material(am, cls.poll_message_set)) is None:
            return False

        if not mg.is_patched():
            cls.poll_message_set("Material must be patched before adding a pattern mask")
            return False

        if mg.find_pattern_mask_node() is None:
            cls.poll_message_set("Could not find pattern mask node")
            return False
        
        return True

class ExportPatternMaskOperator(bpy.types.Operator):
    '''Export a pattern mask from either a PNG or a strip'''
    bl_idname = "hd2visual.export_pattern_mask"
    bl_label = "Export pattern mask"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(name="ID Mask Array Path", subtype="FILE_PATH") #type: ignore
    filter_glob: bpy.props.StringProperty(
        default="*.png",
        options={'HIDDEN'},
    ) #type: ignore

    to_sdf: bpy.props.BoolProperty(default=False, name="as SDF", description="Export to a SDF at a lower resolution. See the README to understand what this means.") #type: ignore
    sdf_downscale_target: bpy.props.IntProperty(name="SDF resolution", default=256, min=32, description="The resolution of the exported SDF.") #type: ignore

    def draw(self, context):
        layout = self.layout
        assert layout is not None

        layout.label(text="Select a png location to export to", icon='INFO')
        
        layout.prop(self, "to_sdf")
        if self.to_sdf:
            layout.prop(self, "sdf_downscale_target")

    def invoke(self, context: Context, event: Event) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        assert context.window_manager is not None
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    @classmethod
    def accurate_shader_get_pm(cls, context: Context) -> bpy.types.Image | None:
        ao = context.active_object
        if ao is None:
            return None
        am = ao.active_material
        if am is None:
            return None

        mg = accurate_shader.from_material(am)
        if mg is None:
            return None

        pmn = mg.find_pattern_mask_node()
        if pmn is None:
            return None

        return pmn.image

    @classmethod
    def debug_material_get_pm(cls, context: Context) -> bpy.types.Image | None:
        ao = context.active_object
        if ao is None:
            return None
        am = ao.active_material
        if am is None:
            return None
        am = IDMaskDebugMaterial(am)

        return am.get_pattern_mask_image()

    def execute(self, context: Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        ao = context.active_object
        assert ao is not None
        am = ao.active_material
        assert am is not None

        pm_path = Path(self.filepath)
        if pm_path.suffix == ".blend":
            raise Exception("Refusing to overwrite blend file!")

        if IDMaskDebugMaterial.is_debug_material(am):
            pm = self.debug_material_get_pm(context)
        else:
            pm = self.accurate_shader_get_pm(context)

        assert pm is not None
        pm = image_util.pillow_image_from_blender_image(pm)

        if self.to_sdf:
            pm = sdf_mask.channel_into_sdf(pm).resize((self.sdf_downscale_target, self.sdf_downscale_target))

        pm.save(pm_path)
        
        return {'FINISHED'}


    @classmethod
    def poll(cls, context: Context) -> bool:
        ao = context.active_object
        if ao is None or ao.active_material is None:
            cls.poll_message_set("An editable material must be active")
            return False

        am = ao.active_material
        if am.node_tree is None:
            cls.poll_message_set("Active material node tree is None")
            return False

        if IDMaskDebugMaterial.is_debug_material(am):
            pm = cls.debug_material_get_pm(context)
            if pm is None:
                cls.poll_message_set("No pattern mask to export")
                return False
            return True

        if (mg := accurate_shader.from_material(am, cls.poll_message_set)) is None:
            return False

        if not mg.is_patched():
            cls.poll_message_set("Material must be patched before adding a pattern mask")
            return False

        if mg.find_pattern_mask_node() is None:
            cls.poll_message_set("Could not find pattern mask node")
            return False

        if cls.accurate_shader_get_pm(context) is None:
            cls.poll_message_set("No pattern mask to export")
            return False
        
        return True


class AddIDMask(bpy.types.Operator):
    bl_idname = "hd2visual.add_idmask"
    bl_label = "Debug IDMask Material"
    bl_options = {'REGISTER', 'UNDO'}

    mask_dim: bpy.props.IntProperty(name="Mask Dim", default=1024, min=32, max=8192) #type: ignore

    def execute(self, context: Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        ao = context.active_object
        assert ao is not None
        assert hasattr(ao.data, "materials")
        
        def make_channel_image(channel_number: int) -> bpy.types.Image:
            return bpy.data.images.new(f"idmask_channel-{channel_number}", self.mask_dim, self.mask_dim, is_data=True)
        
        debug_material = create_idmask_debug_material()
        channel_images = tuple(make_channel_image(n) for n in range(8))
        pattern_mask_image = make_channel_image(9)
        
        ci: IDMaskImages = channel_images #type: ignore # tuple length cast. This is safe here, since it is created just above with 8 elements
        debug_material.set_layer_images(ci)
        debug_material.set_pattern_mask_image(pattern_mask_image)

        if len(ao.material_slots) > 0:
            ao.material_slots[0].material = debug_material.mat
        else:
            assert isinstance(ao.data, bpy.types.Mesh)
            ao.data.materials.append(debug_material.mat)
            
        return {'FINISHED'}
    
    @classmethod
    def poll(cls, context: Context) -> bool:
        ao = context.active_object
        if ao is None:
            cls.poll_message_set("No active object")
            return False

        if not hasattr(ao.data, "materials"):
            cls.poll_message_set("Active object cannot have materials")
            return False
        
        return True