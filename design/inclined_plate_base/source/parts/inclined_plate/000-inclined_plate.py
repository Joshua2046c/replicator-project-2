panel_width = param("panel_width", 180.0)
panel_height = param("panel_height", 110.0)
panel_thickness = param("panel_thickness", 8.0)
panel_corner_radius = param("panel_corner_radius", 8.0)
panel_slope_deg = param("panel_slope_deg", 38.0)
opening_width = param("opening_width", 24.0)
opening_height = param("opening_height", 16.0)
opening_corner_radius = param("opening_corner_radius", 4.0)
opening_top_offset = param("opening_top_offset", 25.0)
groove_width = param("groove_width", 6.0)
groove_depth = param("groove_depth", 4.0)
groove_slope_deg = param("groove_slope_deg", 65.0)
base_depth = param("base_depth", 60.0)
base_thickness = param("base_thickness", 8.0)
base_front_overhang = param("base_front_overhang", 45.0)

# The panel is authored flat in XY. Its lower long edge becomes the connection
# to the horizontal foot after the 38 degree rotation about X.
opening_y = panel_height - opening_top_offset
groove_length = (panel_width ** 2 + panel_height ** 2) ** 0.5 * 1.35
base_center_y = -base_front_overhang + base_depth / 2

with BuildPart() as plate_builder:
    with BuildSketch():
        RectangleRounded(panel_width, panel_height, panel_corner_radius, align=(Align.CENTER, Align.MIN))
        with Locations((0, opening_y)):
            RectangleRounded(opening_width, opening_height, opening_corner_radius, mode=Mode.SUBTRACT)
    extrude(amount=panel_thickness)
    with Locations(Location((0, opening_y, panel_thickness - groove_depth / 2), (0, 0, groove_slope_deg))):
        Box(groove_length, groove_width, groove_depth, mode=Mode.SUBTRACT)

# A horizontal foot overlaps the lower part of the inclined panel, creating a
# fused, stable one-piece base rather than relying on a narrow lower edge.
inclined_plate_solid = plate_builder.part.rotate(Axis.X, panel_slope_deg)
base_foot = Pos(0, base_center_y, 0) * Box(panel_width, base_depth, base_thickness, align=(Align.CENTER, Align.CENTER, Align.MIN))
base = inclined_plate_solid + base_foot
publish("inclined_plate", base, "Inclined plate base")