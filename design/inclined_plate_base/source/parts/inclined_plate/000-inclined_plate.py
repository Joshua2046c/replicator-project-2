backboard_width = param("backboard_width", 180.0)
backboard_slope_length = param("backboard_slope_length", 110.0)
front_thickness = param("front_thickness", 8.0)
backboard_top_slope_deg = param("backboard_top_slope_deg", 38.0)
opening_width = param("opening_width", 24.0)
opening_height = param("opening_height", 16.0)
opening_corner_radius = param("opening_corner_radius", 4.0)
opening_left_offset = param("opening_left_offset", 24.0)
opening_top_offset = param("opening_top_offset", 25.0)
groove_width = param("groove_width", 6.0)
groove_depth = param("groove_depth", 4.0)
groove_cut_angle_from_surface_deg = param("groove_cut_angle_from_surface_deg", 65.0)
groove_front_offset = param("groove_front_offset", 12.0)

# A flat-bottom wedge rests directly on the desk. The sloped top is the
# requested 38 degree backboard surface.
slope_run = backboard_slope_length * cos(radians(backboard_top_slope_deg))
slope_rise = backboard_slope_length * sin(radians(backboard_top_slope_deg))
slope_plane = Location((0, 0, front_thickness), (backboard_top_slope_deg, 0, 0))

opening_x = -backboard_width / 2 + opening_left_offset + opening_width / 2
opening_s = backboard_slope_length - opening_top_offset - opening_height / 2
groove_s = opening_s
groove_length = groove_s - groove_front_offset
groove_center_s = groove_front_offset + groove_length / 2
# The tool is 25 degrees from the surface normal, hence 65 degrees from the surface.
groove_tilt_from_normal_deg = 90 - groove_cut_angle_from_surface_deg

# Wedge has a complete horizontal underside (z=0). Its top face rises from
# front_thickness to front_thickness + slope_rise over the horizontal run.
backboard = Wedge(
    backboard_width,
    slope_run,
    front_thickness,
    0,
    0,
    backboard_width,
    front_thickness + slope_rise,
    align=(Align.CENTER, Align.MIN, Align.MIN),
)

# The opening is a genuine R4 rounded-rectangle, cut normal to the top surface.
opening_profile = RectangleRounded(opening_width, opening_height, opening_corner_radius)
opening_cutter = slope_plane * Pos(opening_x, opening_s, 0) * extrude(
    opening_profile,
    amount=120,
    both=True,
)

# The groove path is parallel to the long sloped edges. Its cutter travels
# 4 mm at 65 degrees to the surface, rather than angling across the face.
groove_cutter = slope_plane * Pos(opening_x, groove_center_s, 0) * Rot(Y=-groove_tilt_from_normal_deg) * Box(
    groove_width,
    groove_length,
    groove_depth,
    align=(Align.CENTER, Align.CENTER, Align.MAX),
)

wedge_backboard = backboard - opening_cutter - groove_cutter
publish("inclined_plate", wedge_backboard, "Wedge backboard")