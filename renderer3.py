bl_info = {
    "name": "Render Compare",
    "author": "Hank Ravich",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Render > Render Compare",
    "description": "Renders the scene with two different settings and compares the results",
    "warning": "",
    "wiki_url": "",
    "category": "Render",
}

import bpy
import os
import numpy as np

class RenderCompareSettings(bpy.types.PropertyGroup):
    resolution_x1: bpy.props.IntProperty(
        name="Resolution X1",
        description="Render resolution X for the first render",
        default=1920,
        min=1,
        soft_max=8192,
    )
    resolution_y1: bpy.props.IntProperty(
        name="Resolution Y1",
        description="Render resolution Y for the first render",
        default=1080,
        min=1,
        soft_max=8192,
    )
    samples1: bpy.props.IntProperty(
        name="Samples1",
        description="Render samples for the first render",
        default=128,
        min=1,
        soft_max=8192,
    )
    resolution_x2: bpy.props.IntProperty(
        name="Resolution X2",
        description="Render resolution X for the second render",
        default=1920,
        min=1,
        soft_max=8192,
    )
    resolution_y2: bpy.props.IntProperty(
        name="Resolution Y2",
        description="Render resolution Y for the second render",
        default=1080,
        min=1,
        soft_max=8192,
    )
    samples2: bpy.props.IntProperty(
        name="Samples2",
        description="Render samples for the second render",
        default=128,
        min=1,
        soft_max=8192,
    )

class RENDER_COMPARE_OT_operator(bpy.types.Operator):
    bl_idname = "render.compare"
    bl_label = "Render Compare"
    bl_description = "Render and compare with different settings"

    def calculate_noise_score(self, image):
        width, height = image.size
        pixels = np.array(image.pixels[:]).reshape(height, width, 4)
        grayscale_pixels = np.dot(pixels[..., :3], [0.299, 0.587, 0.114])
        return (np.std(grayscale_pixels) ** 2) * 1e6

    def execute(self, context):
        scene = context.scene
        render = scene.render
        cycles = scene.cycles
        settings = scene.render_compare_settings

        # Save current render settings
        original_filepath = render.filepath
        original_resolution_x = render.resolution_x
        original_resolution_y = render.resolution_y
        original_samples = cycles.samples

        # Render with custom settings for the first render
        render.resolution_x = settings.resolution_x1
        render.resolution_y = settings.resolution_y1
        cycles.samples = settings.samples1
        render.filepath = "//render1.png"
        bpy.ops.render.render(write_still=True)

        # Render with custom settings for the second render
        render.resolution_x = settings.resolution_x2
        render.resolution_y = settings.resolution_y2
        cycles.samples = settings.samples2
        render.filepath = "//render2.png"
        bpy.ops.render.render(write_still=True)

        # Load rendered images
        bpy.ops.image.open(filepath="//render1.png", relative_path=True)
        bpy.ops.image.open(filepath="//render2.png", relative_path=True)

        render1_image = bpy.data.images['render1.png']
        render2_image = bpy.data.images['render2.png']

        # Calculate noise scores
        noise_score1 = self.calculate_noise_score(render1_image)
        noise_score2 = self.calculate_noise_score(render2_image)

        # Remove loaded images
        bpy.data.images.remove(render1_image)
        bpy.data.images.remove(render2_image)

        # Restore original render settings
        render.filepath = original_filepath
        render.resolution_x = original_resolution_x
        render.resolution_y = original_resolution_y
        cycles.samples = original_samples

        self.report({'INFO'}, f"Noise score 1: {noise_score1:.2f}, Noise score 2: {noise_score2:.2f}")

        return {'FINISHED'}

class RENDER_COMPARE_PT_panel(bpy.types.Panel):
    bl_label = "Render Compare"
    bl_idname = "RENDER_COMPARE_PT_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.render_compare_settings

        col = layout.column(align=True)
        col.label(text="First Render Settings:")
        col.prop(settings, "resolution_x1")
        col.prop(settings, "resolution_y1")
        col.prop(settings, "samples1")

        col = layout.column(align=True)
        col.label(text="Second Render Settings:")
        col.prop(settings, "resolution_x2")
        col.prop(settings, "resolution_y2")
        col.prop(settings, "samples2")

        layout.operator("render.compare")

def register():
    bpy.utils.register_class(RenderCompareSettings)
    bpy.types.Scene.render_compare_settings = bpy.props.PointerProperty(type=RenderCompareSettings)
    bpy.utils.register_class(RENDER_COMPARE_OT_operator)
    bpy.utils.register_class(RENDER_COMPARE_PT_panel)

def unregister():
    bpy.utils.unregister_class(RENDER_COMPARE_PT_panel)
    bpy.utils.unregister_class(RENDER_COMPARE_OT_operator)
    bpy.utils.unregister_class(RenderCompareSettings)
    del bpy.types.Scene.render_compare_settings

if __name__ == "__main__":
    register()
