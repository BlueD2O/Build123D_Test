from build123d import *

# Import finished parts
from RetroPad_Bottom import final_bottom_shell
from RetroPad_Top import final_top_shell
from RetroPad_Button import final_button
from RetroPad_D_Pad import final_D_Pad

button_x_gap = 20 * MM
button_y_gap = 17 * MM

# Position parts into assembly
positioned_button = Location((0, 0, 0)) * final_button
x_axis_locs = list(GridLocations(button_x_gap, 0, x_count=2, y_count=1))
y_axis_locs = list(GridLocations(0, button_y_gap, x_count=1, y_count=2))
x_axis_buttons=[loc*positioned_button for loc in x_axis_locs]
y_axis_buttons=[loc*positioned_button for loc in y_axis_locs]
# duplicate_center_button = positioned_button.moved(Location((0, 0, 0)))
# GridLocations((button_x_gap/2),0, x_count=2, y_count=1)
# positioned_button.move

positioned_top_shell = Location((0, 0, 22.424)) * final_top_shell
positioned_D_Pad = Location((0, 0, 0)) * final_D_Pad

# Assign colors for visual distinction
final_bottom_shell.color = Color("gray")
for btn in x_axis_buttons:
    btn.color = Color("red")
for btn in y_axis_buttons:
    btn.color = Color("red")
positioned_top_shell.color = Color("lightgray")
positioned_D_Pad.color = Color("blue")

# Assemble and export
my_device = Compound(label="Main Assembly", children=[
    final_bottom_shell,
    *x_axis_buttons,
    *y_axis_buttons,
    positioned_top_shell,
    positioned_D_Pad
])

export_step(my_device, "STEP_Files/Complete_Device_Assembly.step")