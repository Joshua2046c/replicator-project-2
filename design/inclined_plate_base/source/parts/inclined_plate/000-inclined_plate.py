backboard_width = param("backboard_width", 180.0)
backboard_slope_length = param("backboard_slope_length", 110.0)
front_thickness = param("front_thickness", 8.0)
backboard_top_slope_deg = param("backboard_top_slope_deg", 9.0)
groove_top_width = param("groove_top_width", 10.0)
groove_depth = param("groove_depth", 8.0)
groove_apex_front_offset = param("groove_apex_front_offset", 4.434472411622152)
groove_top_offset = param("groove_top_offset", 32.0)
pocket_width = param("pocket_width", 24.0)
pocket_depth = param("pocket_depth", 7.0)
inclined_plate_edge_radius = param("inclined_plate_edge_radius", 3.0)
inclined_plate_bottom_chamfer = param("inclined_plate_bottom_chamfer", 0.5)
inclined_plate_grip_width = param("inclined_plate_grip_width", 2.5)
inclined_plate_grip_depth = param("inclined_plate_grip_depth", 1.0)
inclined_plate_grip_pitch = param("inclined_plate_grip_pitch", 7.5)
inclined_plate_grip_margin = param("inclined_plate_grip_margin", 6.0)
sn = sin(radians(backboard_top_slope_deg))
cs = cos(radians(backboard_top_slope_deg))
slope_run = backboard_slope_length * cs
slope_rise = backboard_slope_length * sn
slope_plane = Location((0, 0, front_thickness), (backboard_top_slope_deg, 0, 0))
groove_s = backboard_slope_length - groove_top_offset - groove_top_width / 2
body = Wedge(backboard_width, slope_run, front_thickness, 0, 0, backboard_width, front_thickness + slope_rise, align=(Align.CENTER, Align.MIN, Align.MIN))
terrace_start = groove_s
cut = slope_plane * Pos(-backboard_width/2-1, terrace_start, -pocket_depth) * Box(pocket_width+1, backboard_slope_length-terrace_start+5, pocket_depth+5, align=(Align.MIN,Align.MIN,Align.MIN))
body = body - cut
round_edges = []
for e in body.edges():
    c = e.center()
    ly = c.Y*cs+(c.Z-front_thickness)*sn
    if c.Z > 0.001 and abs(ly-terrace_start)>1e-5:
        round_edges.append(e)
body = fillet(round_edges, radius=inclined_plate_edge_radius)
bottom_edges = [e for e in body.edges() if abs(e.bounding_box().min.Z)<1e-6 and abs(e.bounding_box().max.Z)<1e-6]
body = chamfer(bottom_edges, length=inclined_plate_bottom_chamfer)
eps = 0.1
lean = groove_apex_front_offset / groove_depth
groove_profile = Polygon((-eps, -groove_top_width / 2 + eps * lean), (-eps, groove_top_width / 2 + eps * lean), (groove_depth, groove_top_width / 2 - groove_apex_front_offset), (groove_depth, -groove_top_width / 2 - groove_apex_front_offset), align=None)
groove_prism = Rot(Y=90) * extrude(groove_profile, amount=backboard_width/2+1, both=True)
body = body - slope_plane * Pos(0,groove_s,0) * groove_prism
usable_run = groove_s-groove_top_width/2-2*inclined_plate_grip_margin
count = int((usable_run-inclined_plate_grip_width)//inclined_plate_grip_pitch)+1
assert count > 0 and inclined_plate_grip_pitch > inclined_plate_grip_width
pattern_run = (count-1)*inclined_plate_grip_pitch+inclined_plate_grip_width
start_s = (groove_s-groove_top_width/2-pattern_run)/2
# Capsule outline: semicircular plan-view ends, not a fillet of the slot lips.
profile = SlotOverall(backboard_width-2*inclined_plate_grip_margin,inclined_plate_grip_width)
for i in range(count):
    tool = slope_plane * Pos(0,start_s+i*inclined_plate_grip_pitch+inclined_plate_grip_width/2,-inclined_plate_grip_depth) * extrude(profile,amount=inclined_plate_grip_depth+eps)
    body = body - tool
assert len(body.solids()) == 1
assert body.is_valid
print('Grip count',count,'plan envelope',backboard_width,slope_run)
publish("inclined_plate",body,"Round-ended grip cradle")