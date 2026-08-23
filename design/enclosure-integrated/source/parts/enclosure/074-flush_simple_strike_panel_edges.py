# Match the removable side-panel front/rear edges to the 0.35 mm chamfered
# end-panel interface. This removes the last sub-millimetre repair ears while
# retaining every final steel-strike recess inside the solid edge margin.
simple_strike_edge_inset_y = param('simple_strike_edge_inset_y', end_panel_vertical_chamfer)
simple_strike_flush_depth_y = D - 2.0 * simple_strike_edge_inset_y
simple_strike_flush_height_z = param('simple_strike_flush_height_z', H - base_t - cap_t)
simple_strike_flush_thickness_x = param('simple_strike_flush_thickness_x', panel_t + 0.40)
simple_strike_flush_corner_radius = param('simple_strike_flush_corner_radius', case_panel_corner_radius)

assert simple_strike_edge_inset_y >= end_panel_vertical_chamfer
assert simple_strike_flush_depth_y < D
assert simple_strike_flush_corner_radius == case_panel_corner_radius

for sx, side_shape in ((-1, left_panel), (1, right_panel)):
    side_x = sx * (W / 2.0 - panel_t / 2.0)
    flush_envelope = Box(
        simple_strike_flush_thickness_x,
        simple_strike_flush_depth_y,
        simple_strike_flush_height_z,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((side_x, 0.0, base_t)))
    flush_edges = [e for e in flush_envelope.edges() if _line_parallel(e, 'x')]
    assert len(flush_edges) == 4
    flush_envelope = fillet(flush_edges, simple_strike_flush_corner_radius)
    revised = (side_shape & flush_envelope).clean()
    assert revised.solids().__len__() == 1
    assert abs(revised.bounding_box().size.Y - simple_strike_flush_depth_y) < 0.01
    if sx < 0:
        left_panel = revised
    else:
        right_panel = revised

publish('left_panel', left_panel, 'Flush left magnet edge')
publish('right_panel', right_panel, 'Flush right magnet edge')
print(f'SIMPLE_STRIKE_EDGE_PASS: side-panel depth={simple_strike_flush_depth_y:.2f} mm with {simple_strike_edge_inset_y:.2f} mm front/rear inset; repair ears removed.')