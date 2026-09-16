backboard_width = param("backboard_width", 180.0)
backboard_slope_length = param("backboard_slope_length", 110.0)
front_thickness = param("front_thickness", 8.0)
backboard_top_slope_deg = param("backboard_top_slope_deg", 20.0)
opening_width = param("opening_width", 24.0)
opening_height = param("opening_height", 16.0)
opening_corner_radius = param("opening_corner_radius", 4.0)
opening_left_offset = param("opening_left_offset", 10.0)
opening_top_offset = param("opening_top_offset", 10.0)
slot_width = param("slot_width", 156.0)
slot_height = param("slot_height", 6.0)

# Flat-bottom wedge for direct desktop placement; its top surface rises 20 degrees.
slope_run = backboard_slope_length * cos(radians(backboard_top_slope_deg))
slope_rise = backboard_slope_length * sin(radians(backboard_top_slope_deg))
slope_plane = Location((0, 0, front_thickness), (backboard_top_slope_deg, 0, 0))

# The rounded-rectangle opening is close to the upper-left outer edges.
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

# Opening and transverse slot are both normal through-cuts. The slot follows the
# backboard width, intersects the opening, and retains a 12 mm side frame.
opening_profile = RectangleRounded(opening_width, opening_height, opening_corner_radius)
opening_cutter = slope_plane * Pos(opening_x, opening_s, 0) * extrude(
    opening_profile,
    amount=120,
    both=True,
)
slot_cutter = slope_plane * Pos(0, opening_s, 0) * Box(
    slot_width,
    slot_height,
    120,
    align=(Align.CENTER, Align.CENTER, Align.CENTER),
)

wedge_backboard = backboard - opening_cutter - slot_cutter
publish("inclined_plate", wedge_backboard, "Wedge backboard")