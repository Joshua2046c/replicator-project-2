backboard_width = param("backboard_width", 180.0)
backboard_slope_length = param("backboard_slope_length", 110.0)
front_thickness = param("front_thickness", 8.0)
backboard_top_slope_deg = param("backboard_top_slope_deg", 15.0)
groove_height = param("groove_height", 6.0)
groove_depth = param("groove_depth", 4.0)
opening_width = param("opening_width", 24.0)
opening_height = param("opening_height", 16.0)
opening_corner_radius = param("opening_corner_radius", 4.0)
opening_left_offset = param("opening_left_offset", 0.0)
opening_top_offset = param("opening_top_offset", 10.0)
opening_rear_tilt_deg = param("opening_rear_tilt_deg", 30.0)

# Flat-bottom wedge rests directly on the desk. The upper plane rises at 15 degrees.
slope_run = backboard_slope_length * cos(radians(backboard_top_slope_deg))
slope_rise = backboard_slope_length * sin(radians(backboard_top_slope_deg))
slope_plane = Location((0, 0, front_thickness), (backboard_top_slope_deg, 0, 0))

# The opening is placed in the upper-left groove end. Its local X position makes
# its left edge meet the backboard's left edge, as shown by the latest markup.
opening_x = -backboard_width / 2 + opening_left_offset + opening_width / 2
opening_s = backboard_slope_length - opening_top_offset - opening_height / 2

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

# This shallow groove spans the complete sloped-face width without severing the
# base. It is 4 mm deep, matching the original user depth requirement.
full_width_groove = slope_plane * Pos(0, opening_s, 0) * Box(
    backboard_width,
    groove_height,
    groove_depth,
    align=(Align.CENTER, Align.CENTER, Align.MAX),
)

# The rounded rectangular opening is a through-cut inside the groove. It leans
# toward the back (+local Y) while cutting through the board, as requested.
opening_profile = RectangleRounded(opening_width, opening_height, opening_corner_radius)
rear_tilted_opening = slope_plane * Pos(opening_x, opening_s, 0) * Rot(X=opening_rear_tilt_deg) * extrude(
    opening_profile,
    amount=120,
    both=True,
)

wedge_backboard = backboard - full_width_groove - rear_tilted_opening
publish("inclined_plate", wedge_backboard, "Wedge backboard")