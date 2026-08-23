# Round the base plate's four plan corners to the same radius as the top plate so
# the case outline is a consistent rounded rectangle from top to bottom.
case_corner_radius = param('case_corner_radius', 10.0)
base_skin_chamfer = param('base_skin_chamfer', 0.40)
base_corner_tolerance = param('base_corner_tolerance', 1.0)
base_corner_safety_factor = param('base_corner_safety_factor', 0.9)
base_skin_edge_min_length = param('base_skin_edge_min_length', 100.0)
base_edge_round_radius = param('base_edge_round_radius', 2.0)
base_round_safety_factor = param('base_round_safety_factor', 0.85)
base_face_z_tolerance = param('base_face_z_tolerance', 0.05)

assert case_corner_radius > 0.0

def base_is_vertical(edge):
    d = edge.position_at(1) - edge.position_at(0)
    return d.length > 1e-6 and abs(d.normalized().dot(Vector(0, 0, 1))) > 0.99

def base_at_outer_corner(edge):
    mid = edge.position_at(0.5)
    return (
        abs(abs(mid.X) - W / 2) < base_corner_tolerance
        and abs(abs(mid.Y) - D / 2) < base_corner_tolerance
    )

# Step 1: the four vertical corner edges of the plate become arcs in plan view.
base_corner_edges = [
    e for e in base.edges()
    if e.geom_type == GeomType.LINE and base_is_vertical(e) and base_at_outer_corner(e)
]
assert len(base_corner_edges) == 4, f'expected 4 base corner edges, found {len(base_corner_edges)}'

base_corner_max = base.max_fillet(base_corner_edges, tolerance=0.1, max_iterations=40)
base_corner_applied = min(case_corner_radius, base_corner_max * base_corner_safety_factor)
assert base_corner_applied > 2.0, f'base plate tolerates only R{base_corner_max:.2f} mm at the corners'
base = fillet(base_corner_edges, base_corner_applied)

# Step 2: soften the underside outer loop, now four straights plus four corner arcs.
base_bottom_z = base.bounding_box().min.Z

def base_on_bottom_face(edge):
    return all(
        abs(edge.position_at(t).Z - base_bottom_z) < base_face_z_tolerance
        for t in (0.0, 0.5, 1.0)
    )

def base_on_outer_perimeter(edge):
    mid = edge.position_at(0.5)
    near_side = abs(abs(mid.X) - W / 2) < base_corner_applied + 1.0
    near_end = abs(abs(mid.Y) - D / 2) < base_corner_applied + 1.0
    return near_side or near_end

base_loop_edges = []
for e in base.edges():
    if not (base_on_bottom_face(e) and base_on_outer_perimeter(e)):
        continue
    if e.geom_type == GeomType.LINE and e.length >= 20.0:
        base_loop_edges.append(e)
    elif e.geom_type == GeomType.CIRCLE and e.radius >= base_corner_applied * 0.5:
        base_loop_edges.append(e)

if base_loop_edges:
    base_round_max = base.max_fillet(base_loop_edges, tolerance=0.05, max_iterations=40)
    base_round_applied = min(base_edge_round_radius, base_round_max * base_round_safety_factor)
    if base_round_applied > 0.3:
        base = fillet(base_loop_edges, base_round_applied)
    else:
        base_round_applied = 0.0
else:
    base_round_applied = 0.0

assert base.solids().__len__() == 1
base_bb = base.bounding_box()
assert abs(base_bb.size.X - W) < 0.01 and abs(base_bb.size.Y - D) < 0.01

# The plan corners must actually be arcs of the requested radius, not sharp again.
base_corner_arcs = [
    e for e in base.edges()
    if e.geom_type == GeomType.CIRCLE and abs(e.radius - base_corner_applied) < 0.2
]
assert len(base_corner_arcs) >= 4, f'only {len(base_corner_arcs)} corner arcs survived'

publish('base', base, 'Rounded corner base')
print(
    f'BASE_CORNER_ROUND_PASS: 4 plan corners at R{base_corner_applied:.2f} mm '
    f'(kernel max R{base_corner_max:.2f}); {len(base_corner_arcs)} arcs verified; '
    f'{len(base_loop_edges)} underside loop edges rounded at R{base_round_applied:.2f} mm; '
    f'footprint still {W:.0f} x {D:.0f} mm.'
)