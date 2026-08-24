# Clip shallow strike-repair geometry to the removable side-panel envelope.
# Side panels span only the net depth between the front and rear panel skins;
# they do not extend to the enclosure's full exterior depth.
simple_strike_trim_depth_y = D - 2.0 * panel_t
simple_strike_trim_height_z = param('simple_strike_trim_height_z', H - base_t - cap_t)
simple_strike_trim_thickness_x = param('simple_strike_trim_thickness_x', panel_t + 0.40)
simple_strike_trim_corner_radius = param('simple_strike_trim_corner_radius', case_panel_corner_radius)
simple_strike_trim_expected_depth_y = simple_strike_trim_depth_y

assert simple_strike_trim_depth_y == D - 2.0 * panel_t
assert simple_strike_trim_expected_depth_y == simple_strike_trim_depth_y
assert simple_strike_trim_corner_radius == case_panel_corner_radius

for sx, side_shape in ((-1, left_panel), (1, right_panel)):
    side_x = sx * (W / 2.0 - panel_t / 2.0)
    trim_envelope = Box(
        simple_strike_trim_thickness_x,
        simple_strike_trim_depth_y,
        simple_strike_trim_height_z,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((side_x, 0.0, base_t)))
    trim_edges = [e for e in trim_envelope.edges() if _line_parallel(e, 'x')]
    assert len(trim_edges) == 4
    trim_envelope = fillet(trim_edges, simple_strike_trim_corner_radius)
    revised = (side_shape & trim_envelope).clean()
    assert revised.solids().__len__() == 1
    assert abs(revised.bounding_box().size.Y - simple_strike_trim_expected_depth_y) < 0.01
    if sx < 0:
        left_panel = revised
    else:
        right_panel = revised

publish('left_panel', left_panel, 'Net-depth left strike recesses')
publish('right_panel', right_panel, 'Net-depth right strike recesses')
print(f'SIDE_NET_DEPTH_PASS: side panels clipped to {simple_strike_trim_depth_y:.1f} mm depth with R{simple_strike_trim_corner_radius:.1f} corners; no edge tabs remain.')