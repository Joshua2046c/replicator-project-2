backboard_width = param("backboard_width", 180.0)
backboard_slope_length = param("backboard_slope_length", 110.0)
front_thickness = param("front_thickness", 8.0)
backboard_top_slope_deg = param("backboard_top_slope_deg", 10.0)
groove_top_width = param("groove_top_width", 6.0)
groove_depth = param("groove_depth", 6.0)
groove_apex_front_offset = param("groove_apex_front_offset", 1.0)
groove_top_offset = param("groove_top_offset", 32.0)
pocket_width = param("pocket_width", 24.0)
pocket_height = param("pocket_height", 16.0)
pocket_corner_radius = param("pocket_corner_radius", 4.0)
pocket_depth = param("pocket_depth", 4.0)
pocket_left_margin = param("pocket_left_margin", 4.0)
pocket_top_offset = param("pocket_top_offset", 10.0)

# Flat-bottom wedge rests directly on the desk. The top face rises at 10 degrees.
slope_run = backboard_slope_length * cos(radians(backboard_top_slope_deg))
slope_rise = backboard_slope_length * sin(radians(backboard_top_slope_deg))
slope_plane = Location((0, 0, front_thickness), (backboard_top_slope_deg, 0, 0))

pocket_x = -backboard_width / 2 + pocket_left_margin + pocket_width / 2
pocket_s = backboard_slope_length - pocket_top_offset - pocket_height / 2
groove_s = backboard_slope_length - groove_top_offset - groove_top_width / 2

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

# V-shaped groove profile in side view: the 6 mm top mouth descends to one
# slightly forward-offset point, matching the red-marked section.
groove_profile = Polygon(
    (0, -groove_top_width / 2),
    (0, groove_top_width / 2),
    (groove_depth, -groove_apex_front_offset),
)
v_groove_prism = Rot(Y=90) * extrude(
    groove_profile,
    amount=backboard_width + 2,
    both=True,
)
side_to_side_v_groove = slope_plane * Pos(0, groove_s, 0) * v_groove_prism

# Separate rounded rectangular blind pocket keeps its exterior sidewall intact.
pocket_profile = RectangleRounded(pocket_width, pocket_height, pocket_corner_radius)
rounded_rectangle_pocket = slope_plane * Pos(pocket_x, pocket_s, 0) * extrude(
    pocket_profile,
    amount=-pocket_depth,
)

wedge_backboard = backboard - side_to_side_v_groove - rounded_rectangle_pocket
publish("inclined_plate", wedge_backboard, "Wedge backboard")