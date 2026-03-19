from build123d import *

# 1. Import the final variables from your 4 separate python files
# Syntax: from [filename_without_py] import [variable_name]
from RetroPad_Bottom import final_bottom_shell
from RetroPad_Top import final_top_shell
from RetroPad_Button import final_buttons
from RetroPad_D_Pad import final_D_Pad


# 2. Shift the parts into position using Location math
# Multiplying a Location by a part creates a moved copy of it!
positioned_buttons = Location((0, 0, 0)) * final_buttons
positioned_top_shell = Location((0, 0, 22.424)) * final_top_shell
positioned_D_Pad = Location((0, 0, 0)) * final_D_Pad

# (Optional) Give them colors so they are easy to tell apart in your viewer!
final_bottom_shell.color = Color("darkgray")
positioned_buttons.color = Color("red")
positioned_top_shell.color = Color("lightgray")
positioned_D_Pad.color = Color("blue")

# 3. Create the Assembly Tree using Compound
my_device = Compound(label="Main Assembly", children=[
    final_bottom_shell,  # Stays at exactly (0,0,0)
    positioned_buttons, 
    positioned_top_shell,
    positioned_D_Pad
])

# 4. Export the entire tree as a single STEP file!
export_step(my_device, "Complete_Device_Assembly.step")