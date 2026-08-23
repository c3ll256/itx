# The broad strike-pocket repair patches are intentionally larger than the old
# recesses. Clip their harmless excess back to the exact side-panel envelope so
# no magnet-interface repair tab projects beyond the 256 mm case depth.
final_side_trim_depth_y = param('final_side_trim_depth_y', D)
final_side_trim_height_z = param('final_side_trim_height_z', H - base_t - cap_t)
final_side_trim_thickness_x = param('final_side_trim_thickness_x', panel_t + 0.40)
final_side_trim_expected_depth = param('final_side_trim_expected_depth', D)

assert final_side_trim_depth_y == D
assert final_side_trim_expected_depth == D

for sx, side_shape in ((-1, left_panel), (1, right_panel)):
    side_x = sx * (W / 2 - panel_t / 2)
    trim_env = Box(
        final_side_trim_thickness_x,
        final_side_trim_depth_y,
        final_side_trim_height_z,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((side_x, 0.0, base_t)))
    x_edges = [e for e in trim_env.edges() if _line_parallel(e, 'x')]
    assert len(x_edges) == 4
    trim_env = fillet(x_edges, case_panel_corner_radius)
    revised = (side_shape & trim_env).clean()
    assert revised.solids().__len__() == 1
    assert abs(revised.bounding_box().size.Y - final_side_trim_expected_depth) < 0.01
    if sx < 0:
        left_panel = revised
    else:
        right_panel = revised

publish('left_panel', left_panel, 'Trimmed left magnet interface')
publish('right_panel', right_panel, 'Trimmed right magnet interface')
print(f'FINAL_SIDE_TRIM_PASS: both side panels restored to {final_side_trim_depth_y:.1f} mm depth with R{case_panel_corner_radius:.1f} corners; strike pockets retained and repair ears removed.')