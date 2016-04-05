import bpy
from bpy.props import *
import vse_transitions

#
# Custom properties for Transition object to read as transition options
#
bpy.types.TransformSequence.transition_type = EnumProperty(
    items = [('counterclock', 'Counterclock', 'to or from counterclockwise rotation'),
             ('clockwise', 'Clockwise', 'to or from a clockwise rotation'),
             ('scale_down', 'Scale down', 'to or from small scale (zoom out)'),
             ('scale_up', 'Scale up', 'to or from large scale (zoom in)'),
             ('unfade', 'Unfade', 'to or from opaque'),
             ('fade', 'Fade', 'to or from transparent'),
             ('bottom', 'Bottom', 'to or from bottom'),
             ('top', 'Top', 'to or from top'),
             ('right', 'Right', 'to or from right edge'),
             ('left', 'Left', 'to or from left edge')],
    name = 'Type',
    description = 'Type of transition to add to this strip'
    )

bpy.types.TransformSequence.transition_placement = EnumProperty(
    items = [('in', 'In', 'Add transition to left edge of strip'),
             ('out', 'Out', 'Add transition to right edge of strip'),
             ('mid', 'Mid', 'Add transition at the current frame')],
    name = 'Placement',
    description = 'Where to add transition within this strip'
    )

bpy.types.TransformSequence.transition_frames = IntProperty (
    name = 'Duration (frames)', 
    default = 10,
    description = 'Number of frames the transition will last'
    )

bpy.types.TransformSequence.transition_strength = FloatProperty (
    name = 'Strength', 
    default = 1.0, 
    min = 0.0, 
    max = 2.0, 
    description = 'Change the impact of the effect (defaults to 1.0 = 100%)'
    )

# bpy.types.TransformSequence.transition_in = BoolProperty(
#     name = 'In',
#     description = 'Add edge transition (duration counted forwards from left edge of this strip)'
#     )

# bpy.types.TransformSequence.transition_out = BoolProperty(
#     name = 'Out',
#     description = 'Add edge transition (duration counted backwards from right edge of this strip)'
#     )
    
# bpy.types.TransformSequence.transition_mid = BoolProperty(
#     name = 'Current Frame',
#     description = 'Add transition at this point (duration counted forwards from current frame)'
#     )

class CustomTransitionsPanel (bpy.types.Panel):
    """Create a Panel in Strip Properties"""
    bl_label = 'Transitions'
    bl_idname = 'strip.transitions_panel'
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    def draw (self, context):
        strip = context.scene.sequence_editor.active_strip
        # drop down menu for selecting transition function
        self.layout.row().prop(strip,'transition_type')
        # integer input for setting transition length in frames
        self.layout.row().prop(strip,'transition_frames')
        self.layout.row().prop(strip,'transition_strength')
        # check boxes for toggling transition in/out/mid
        #row_1 = self.layout.split(0.4)
        #row_1.prop(strip,'transition_in')
        #row_1.prop(strip,'transition_out')
        #self.layout.row().prop(strip,'transition_mid')
        # button series for choosing placement (in/out/current)
        self.layout.prop(strip,'transition_placement', expand=True)
        # execute button
        self.layout.separator()
        self.layout.operator('strip.transition_add', text="Keyframe Transition")
        self.layout.operator('strip.transition_delete', text="/!\\ Clear Keyframe Fields /!\\")

class AddTransition (bpy.types.Operator):
    bl_label = 'Add Transitions'
    bl_idname = 'strip.transition_add'
    bl_description = 'Use transition settings to create keyframes in active strip'
    def execute (self, context):
        try:
            Transition.handler()
        except:
            raise NotImplementedError('Method Transition.handler() not implemented in Transition object')
        return{'FINISHED'}

class DeleteTransition (bpy.types.Operator):
    bl_label = 'Delete Transitions'
    bl_idname = 'strip.transition_delete'
    bl_description = 'Delete ALL visible keyframes from strip transition fields (opacity, position, scale, rotation)'
    def execute (self, context):
        try:
            Transition.clear(context.scene.sequence_editor.active_strip)
        except:
            raise NotImplementedError('Method Transition.clear(strip) not implemented in Transition object')
        return{'FINISHED'}

def register():
    bpy.utils.register_class(CustomTransitionsPanel)
    bpy.utils.register_class(AddTransition)
    bpy.utils.register_class(DeleteTransition)

def unregister():
    bpy.utils.unregister_class(CustomTransitionsPanel)
    bpy.utils.unregister_class(AddTransition)
    bpy.utils.unregister_class(DeleteTransition)

if __name__ == '__main__':
    register()
    #unregister()