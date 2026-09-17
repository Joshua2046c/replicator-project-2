backboard_width = param("backboard_width", 180.0)
backboard_slope_length = param("backboard_slope_length", 110.0)
front_thickness = param("front_thickness", 8.0)
backboard_top_slope_deg = param("backboard_top_slope_deg", 10.0)
groove_top_width = param("groove_top_width", 10.0)
groove_depth = param("groove_depth", 8.0)
groove_apex_front_offset = param("groove_apex_front_offset", 4.618802153517006)
groove_top_offset = param("groove_top_offset", 32.0)
pocket_width = param("pocket_width", 24.0)
pocket_height = param("pocket_height", 16.0)
pocket_corner_radius = param("pocket_corner_radius", 4.0)
pocket_depth = param("pocket_depth", 7.0)
pocket_left_margin = param("pocket_left_margin", 7.0)
pocket_top_offset = param("pocket_top_offset", 10.0)
inclined_plate_edge_radius = param("inclined_plate_edge_radius", 3.0)
inclined_plate_bottom_chamfer = param("inclined_plate_bottom_chamfer", 0.5)
sn = sin(radians(backboard_top_slope_deg))
cs = cos(radians(backboard_top_slope_deg))
slope_run = backboard_slope_length * cs
slope_rise = backboard_slope_length * sn
slope_plane = Location((0, 0, front_thickness), (backboard_top_slope_deg, 0, 0))
pocket_x = -backboard_width / 2 + pocket_left_margin + pocket_width / 2
pocket_s = backboard_slope_length - pocket_top_offset - pocket_height / 2
groove_s = backboard_slope_length - groove_top_offset - groove_top_width / 2
body = Wedge(backboard_width, slope_run, front_thickness, 0, 0, backboard_width, front_thickness + slope_rise, align=(Align.CENTER, Align.MIN, Align.MIN))
# Finish the exterior before cutting the device interface: no slot edge is filleted.
long_edges = [e for e in body.edges() if e.bounding_box().size.X > backboard_width - 0.01 and e.center().Z > 0.001]
body = fillet(long_edges, radius=inclined_plate_edge_radius)
end_edges = [e for e in body.edges() if abs(abs(e.center().X) - backboard_width / 2) < 1e-5 and e.bounding_box().size.X < 1e-5 and e.center().Z > 0.001]
body = fillet(end_edges, radius=inclined_plate_edge_radius)
pocket_profile = RectangleRounded(pocket_width, pocket_height, pocket_corner_radius)
body = body - slope_plane * Pos(pocket_x, pocket_s, 0) * extrude(pocket_profile, amount=-pocket_depth)
pocket_edges = []
for e in body.edges():
    c = e.center()
    local_y = c.Y * cs + (c.Z-front_thickness) * sn
    local_z = -c.Y * sn + (c.Z-front_thickness) * cs
    if abs(c.X-pocket_x) <= pocket_width/2 + 0.01 and abs(local_y-pocket_s) <= pocket_height/2 + 0.01 and (abs(local_z)<1e-5 or abs(local_z+pocket_depth)<1e-5):
        pocket_edges.append(e)
body = fillet(pocket_edges, radius=inclined_plate_edge_radius)
bottom_edges = [e for e in body.edges() if abs(e.bounding_box().min.Z)<1e-6 and abs(e.bounding_box().max.Z)<1e-6]
body = chamfer(bottom_edges, length=inclined_plate_bottom_chamfer)
eps = 0.1
lean = groove_apex_front_offset / groove_depth
groove_profile = Polygon((-eps, -groove_top_width / 2 + eps * lean), (-eps, groove_top_width / 2 + eps * lean), (groove_depth, groove_top_width / 2 - groove_apex_front_offset), (groove_depth, -groove_top_width / 2 - groove_apex_front_offset), align=None)
groove_prism = Rot(Y=90) * extrude(groove_profile, amount=backboard_width / 2 + 1, both=True)
body = body - slope_plane * Pos(0, groove_s, 0) * groove_prism
assert len(body.solids()) == 1
assert body.is_valid
publish("inclined_plate", body, "Rounded iPad cradle")