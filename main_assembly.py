from build123d import *

# Import finished parts
from RetroPad_Bottom import final_bottom_shell
from RetroPad_Top import final_top_shell
from RetroPad_Button import final_buttons
from RetroPad_D_Pad import final_D_Pad

# Position parts into assembly
positioned_buttons = Location((0, 0, 0)) * final_buttons
positioned_top_shell = Location((0, 0, 22.424)) * final_top_shell
positioned_D_Pad = Location((0, 0, 0)) * final_D_Pad

# Assign colors for visual distinction
final_bottom_shell.color = Color("darkgray")
positioned_buttons.color = Color("red")
positioned_top_shell.color = Color("lightgray")
positioned_D_Pad.color = Color("blue")

# Assemble and export
my_device = Compound(label="Main Assembly", children=[
    final_bottom_shell,
    positioned_buttons,
    positioned_top_shell,
    positioned_D_Pad
])

export_step(my_device, "Complete_Device_Assembly.step")