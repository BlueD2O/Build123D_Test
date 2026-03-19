from build123d import *

total_length = 135 * MM
total_width = 53 * MM
total_height = 22.424 * MM
bottom_shell_height = 9.6 * MM
bottom_shell_wall_height = 16.424 * MM
rectangular_cutout__height = 14.824 * MM
rectangular_cutout__length = 37.039 * MM
rectangular_cutout__center_z = 12.012 * MM
top_shell_height = 12.824 * MM
top_shell_wall_height = 9.824 * MM
top_shell_standoff_height = 11.824 * MM
base_thickness = 3 * MM
wall_thickness = 1 * MM
corner_chamfer = 10.429 * MM
base_outer_chamfer = 3 * MM



with BuildPart() as top_shell:
    # 1. Start with a hollow box (open top)
    Box(total_length, total_width, top_shell_height, align=(Align.CENTER, Align.CENTER, Align.MAX))
    #select the corner edges and chamfer them
    corner_edges = top_shell.edges().filter_by(Axis.Z)
    chamfer(corner_edges, length=corner_chamfer)
    # Shell it (remove top face)
    bottom_face = top_shell.faces().sort_by(Axis.Z)[0]
    offset(amount=-wall_thickness, openings=bottom_face)
    # 2. SELECT the internal floor
    # Index [0] is the bottom-most exterior face. 
    # Index [1] is the interior floor face.
    floor = top_shell.faces().filter_by(GeomType.PLANE).sort_by(Axis.Z)[-2]
    # 3. EXTRUDE the floor UP by 2mm
    # This adds 2mm of thickness to the base of your hollow body
    extrude(floor,amount=(base_thickness-wall_thickness),mode=Mode.ADD)

    top_shell_new_floor = top_shell.faces().filter_by(GeomType.PLANE).sort_by(Axis.Z)[-2]

    #select the bottom face and chamfer the outer edges
    bottom_face = top_shell.faces().sort_by(Axis.Z)[-1]
    chamfer(bottom_face.edges(), length=base_outer_chamfer)

    # 6. select the front side wall face and add a rectangular cutout
    front_wall_outer_face = top_shell.faces().filter_by(Axis.Y).sort_by(Axis.Y)[-1]
    with BuildSketch(front_wall_outer_face) as cutout_sketch:
        # Draw a rectangle cutout
        with Locations((1.5, 0)):
            Rectangle(rectangular_cutout__height, rectangular_cutout__length)

    extrude(amount=-wall_thickness*3, mode=Mode.SUBTRACT)

    #create holder bracket for connector
    connector_slot_outer_face = top_shell.faces().filter_by(Axis.Y).sort_by(Axis.Y)[2]
    rectangular_bracket_length = 35.239 * MM
    rectangular_bracket_width = 20.953 * MM
    rectangular_bracket_height = 11.824 * MM
    rectangular_bracket_thickness = 2 * MM
    rectangular_bracket_center_z = 8.912 * MM
    with BuildSketch(connector_slot_outer_face) as bracket_sketch:
        # Draw a cuboid of bracket size
        with Locations((-(rectangular_bracket_center_z-(base_thickness/2)), 0)):
            Rectangle(rectangular_bracket_height, rectangular_bracket_length)
    extrude(amount=-rectangular_bracket_width, mode=Mode.ADD)

    #cut the bracket from the outer face to make slot
    with BuildSketch(connector_slot_outer_face) as bracket_slot_sketch:
        # Draw a cuboid of bracket slot size
        with Locations((-(rectangular_bracket_center_z-(base_thickness/2)), 0)):
            Rectangle(rectangular_bracket_height, rectangular_bracket_length-4)
    extrude(amount=-1*(rectangular_bracket_width-2), mode=Mode.SUBTRACT)


    #create the central standoff

    with BuildSketch(top_shell_new_floor) as central_standoff_sketch:
        with Locations((0, 11.5)):
            #draw the main outer circle
            Circle(4)
            #draw the smaller inner circle and subtract it to make a hollow standoff
            Circle(2.6, mode=Mode.SUBTRACT)
    extrude(amount=top_shell_standoff_height, mode=Mode.ADD)


    #create the corner standoffs and distribute them along X and Y axes

    
    with BuildSketch(top_shell_new_floor) as corner_standoff_sketch:
        with GridLocations(x_spacing=105, y_spacing=25, x_count=2, y_count=2):
            with Locations((0, -1)):
                #draw the main outer circle
                Circle(2.5)
                #draw the smaller inner circle and subtract it to make a hollow standoff
                Circle(1.1, mode=Mode.SUBTRACT)
    extrude(amount=top_shell_standoff_height, mode=Mode.ADD)

    #create the elliptical peg
    ellipse_x_radius = 17.229 * MM
    ellipse_y_radius = 15.409 * MM
    peg_height = 7.474 * MM
    ellipse_center_x = -38 * MM
    ellipse_center_y = 1 * MM
    peg_thickness = 1 * MM

    peg_overlap = 0  # overlap into the floor for a clean Boolean union
    peg_plane = Plane.XY.offset(-(base_thickness - peg_overlap))

    # Step 1: Add the OUTER solid ellipse (clean analytical curve, no offset())
    with BuildSketch(peg_plane) as peg_outer_sketch:
        with Locations((ellipse_center_x, ellipse_center_y)):
            Ellipse(ellipse_x_radius, ellipse_y_radius)
    extrude(amount=-(peg_height + peg_overlap), mode=Mode.ADD)

    # Step 2: Subtract the INNER ellipse to create the hollow ring
    with BuildSketch(peg_plane) as peg_inner_sketch:
        with Locations((ellipse_center_x, ellipse_center_y)):
            Ellipse(ellipse_x_radius - peg_thickness, ellipse_y_radius - peg_thickness)
    extrude(amount=-(peg_height + peg_overlap), mode=Mode.SUBTRACT)

    #cutout for D-Pad
    dpad_cutout1_length = 30 * MM
    dpad_cutout1_width = 10.021 * MM
    dpad_cutout2_length = 10 * MM
    dpad_cutout2_width = 27 * MM

    with BuildSketch(top_shell_new_floor) as dpad_cutout_sketch:
        with Locations((ellipse_center_x, -ellipse_center_y)):
            Rectangle(dpad_cutout1_length, dpad_cutout1_width)
            Rectangle(dpad_cutout2_length, dpad_cutout2_width)
    extrude(amount=-(base_thickness), mode=Mode.SUBTRACT)

    #button slot cutouts
    button_slot_radius = 5 * MM
    button_slot_depth = 10.474 * MM
    button_slot_thickness = 1 * MM
    button_slot_pattern_center = (38 * MM, -1 * MM)
    rectangular_guide_cutout_width = 2 * MM
    rectangular_guide_cutout_length = ((button_slot_radius+button_slot_thickness)*2) * MM

    
    with BuildSketch(top_shell_new_floor) as button_slot_cutout_sketch:
        with Locations(button_slot_pattern_center):
            with GridLocations(x_spacing=20*MM, y_spacing=0, x_count=2, y_count=1):
                Circle(button_slot_radius)
            with GridLocations(x_spacing=0, y_spacing=17*MM, x_count=1, y_count=2):
                Circle(button_slot_radius)
    extrude(amount=-button_slot_depth, mode=Mode.SUBTRACT)

    with BuildSketch(top_shell_new_floor) as button_slot_guide_sketch:
        with Locations(button_slot_pattern_center):
            with GridLocations(x_spacing=20*MM, y_spacing=0, x_count=2, y_count=1):
                Circle(button_slot_radius+button_slot_thickness, mode=Mode.ADD)
                offset(amount=-button_slot_thickness, mode=Mode.SUBTRACT)
            with GridLocations(x_spacing=0, y_spacing=17*MM, x_count=1, y_count=2):
                Circle(button_slot_radius+button_slot_thickness, mode=Mode.ADD)
                offset(amount=-button_slot_thickness, mode=Mode.SUBTRACT)
    extrude(amount=button_slot_depth-base_thickness, mode=Mode.ADD)

    with BuildSketch(top_shell_new_floor) as button_slot_rectangular_guide_sketch:
        with Locations(button_slot_pattern_center):
            with GridLocations(x_spacing=20*MM, y_spacing=0, x_count=2, y_count=1):
                Rectangle(rectangular_guide_cutout_length, rectangular_guide_cutout_width)
                Rectangle(rectangular_guide_cutout_width, rectangular_guide_cutout_length)
            with GridLocations(x_spacing=0, y_spacing=17*MM, x_count=1, y_count=2):
                Rectangle(rectangular_guide_cutout_length, rectangular_guide_cutout_width)
                Rectangle(rectangular_guide_cutout_width, rectangular_guide_cutout_length)
    extrude(amount=(button_slot_depth-base_thickness), mode=Mode.SUBTRACT)



    

final_top_shell = top_shell.part

if __name__ == "__main__":
    export_step(final_top_shell, "test_top_shell.step")

    export_stl(final_top_shell, "test_top_shell.stl")