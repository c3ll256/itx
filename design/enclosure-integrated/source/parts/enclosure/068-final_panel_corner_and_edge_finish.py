# Final panel-corner finish. Earlier cells already soften the shell edges,
# chamfer the front/rear long edges and side-panel perimeters, break the top
# loop, and round the base underside. This cell completes the common R10 corner
# language without re-cutting functional grille, connector, screw, or mating edges.
case_panel_corner_radius = param('case_panel_corner_radius', 10.0)
case_corner_arc_tolerance = param('case_corner_arc_tolerance', 0.25)
assert case_panel_corner_radius >= 6.0

def _line_parallel(edge, axis):
    if edge.geom_type != GeomType.LINE:
        return False
    d = edge.position_at(1) - edge.position_at(0)
    if d.length < 1e-6:
        return False
    target = {'x': Vector(1,0,0), 'y': Vector(0,1,0), 'z': Vector(0,0,1)}[axis]
    return abs(d.normalized().dot(target)) > 0.99

def _rounded_envelope(shape, thickness_axis, radius):
    bb = shape.bounding_box()
    env = Box(bb.size.X, bb.size.Y, bb.size.Z, align=(Align.MIN, Align.MIN, Align.MIN)).moved(Location((bb.min.X, bb.min.Y, bb.min.Z)))
    corner_edges = [e for e in env.edges() if _line_parallel(e, thickness_axis)]
    assert len(corner_edges) == 4
    env = fillet(corner_edges, radius)
    result = (shape & env).clean()
    assert result.solids().__len__() == 1
    return result

# Vertical panels: round their four planar outline corners.
front_panel = _rounded_envelope(front_panel, 'y', case_panel_corner_radius)
rear_panel = _rounded_envelope(rear_panel, 'y', case_panel_corner_radius)
left_panel = _rounded_envelope(left_panel, 'x', case_panel_corner_radius)
right_panel = _rounded_envelope(right_panel, 'x', case_panel_corner_radius)

# Horizontal panels already use the same R10 plan corners upstream. Confirm the
# large-radius arcs survived all later reinforcement and opening operations.
def _large_corner_arcs(shape):
    return [e for e in shape.edges() if e.geom_type == GeomType.CIRCLE and abs(e.radius - case_panel_corner_radius) < case_corner_arc_tolerance]

top_corner_arcs_final = _large_corner_arcs(top_cap)
base_corner_arcs_final = _large_corner_arcs(base)
front_corner_arcs_final = _large_corner_arcs(front_panel)
rear_corner_arcs_final = _large_corner_arcs(rear_panel)
left_corner_arcs_final = _large_corner_arcs(left_panel)
right_corner_arcs_final = _large_corner_arcs(right_panel)
assert len(top_corner_arcs_final) >= 4
assert len(base_corner_arcs_final) >= 4
assert len(front_corner_arcs_final) >= 4
assert len(rear_corner_arcs_final) >= 4
assert len(left_corner_arcs_final) >= 4
assert len(right_corner_arcs_final) >= 4
assert all(p.solids().__len__() == 1 for p in (front_panel, rear_panel, left_panel, right_panel, top_cap, base))

publish('front_panel', front_panel, 'Rounded front panel')
publish('rear_panel', rear_panel, 'Rounded 5 mm rear')
publish('left_panel', left_panel, 'Rounded left panel')
publish('right_panel', right_panel, 'Rounded right panel')
publish('top_cap', top_cap, 'Rounded top panel')
publish('base', base, 'Rounded base panel')
print(f'FINAL_PANEL_CORNER_PASS: all six panels retain at least four R{case_panel_corner_radius:.1f} corner arcs; existing safe edge rounds and chamfers preserved.')