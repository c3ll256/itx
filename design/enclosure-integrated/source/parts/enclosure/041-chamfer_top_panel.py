# Round the four case corners in plan view: the top plate's vertical corner edges
# become arcs, so the case outline is a rounded rectangle instead of a sharp box.
# This is the XY corner radius, not the top-face edge break.
case_corner_radius = param('case_corner_radius', 10.0)
top_skin_chamfer = param('top_skin_chamfer', 0.40)
top_corner_tolerance = param('top_corner_tolerance', 1.0)
top_corner_safety_factor = param('top_corner_safety_factor', 0.9)
top_skin_edge_min_length = param('top_skin_edge_min_length', 100.0)

assert case_corner_radius > 0.0

def is_vertical(edge):
    d = edge.position_at(1) - edge.position_at(0)
    return d.length > 1e-6 and abs(d.normalized().dot(Vector(0, 0, 1))) > 0.99

def at_outer_corner(edge):
    mid = edge.position_at(0.5)
    return (
        abs(abs(mid.X) - W / 2) < top_corner_tolerance
        and abs(abs(mid.Y) - D / 2) < top_corner_tolerance
    )

# The four full-height corner edges of the outer plate.
top_corner_edges = [
    e for e in top_cap.edges()
    if e.geom_type == GeomType.LINE and is_vertical(e) and at_outer_corner(e)
]
assert len(top_corner_edges) == 4, f'expected 4 corner edges, found {len(top_corner_edges)}'

top_corner_max = top_cap.max_fillet(top_corner_edges, tolerance=0.1, max_iterations=40)
top_corner_applied = min(case_corner_radius, top_corner_max * top_corner_safety_factor)
assert top_corner_applied > 2.0, f'top plate tolerates only R{top_corner_max:.2f} mm at the corners'
top_cap = fillet(top_corner_edges, top_corner_applied)

# Break the complete top-face outer loop, now made of four straights plus the four
# new corner arcs. Screw-hole circles are excluded by their much smaller radius.
top_face_z = top_cap.bounding_box().max.Z

def on_top_face(edge):
    return all(abs(edge.position_at(t).Z - top_face_z) < 0.05 for t in (0.0, 0.5, 1.0))

top_loop_edges = []
for e in top_cap.edges():
    if not on_top_face(e):
        continue
    if e.geom_type == GeomType.LINE and e.length >= top_skin_edge_min_length:
        top_loop_edges.append(e)
    elif e.geom_type == GeomType.CIRCLE and e.radius >= top_corner_applied * 0.5:
        top_loop_edges.append(e)
assert len(top_loop_edges) >= 8
top_cap = chamfer(top_loop_edges, top_skin_chamfer)

assert top_cap.solids().__len__() == 1
top_bb = top_cap.bounding_box()
assert abs(top_bb.size.X - W) < 0.01 and abs(top_bb.size.Y - D) < 0.01

publish('top_cap', top_cap, 'Rounded corner top')
print(
    f'TOP_CORNER_ROUND_PASS: 4 plan corners at R{top_corner_applied:.2f} mm '
    f'(kernel max R{top_corner_max:.2f}); {len(top_loop_edges)} top-face loop edges '
    f'broken at {top_skin_chamfer:.2f} mm; footprint still {W:.0f} x {D:.0f} mm.'
)