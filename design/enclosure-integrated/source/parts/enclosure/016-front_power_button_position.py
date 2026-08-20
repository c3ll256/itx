# Front-panel exterior is the +Y face; positive X appears on the exterior viewer's left.
# Keep the established left-side X position and mirror the former lower button
# centre about the usable panel height so it moves to the upper-left corner.
power_x = param('power_button_x', 50.0)
power_z = param('power_button_z', 227.0)
power_hole_radius = param('power_button_radius', 6.1)
power_cut_depth = param('power_button_cut_depth', 8.0)
front_fillet_radius = param('front_panel_fillet_radius', 1.0)
front_fillet_min_edge = param('front_panel_fillet_min_edge', 210.0)
power_min_edge_clearance = param('power_button_min_edge_clearance', 15.0)

front_panel_bottom_z = base_t
front_panel_top_z = H - cap_t
front_panel = Box(
    W, panel_t, H - base_t - cap_t,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((0, front_y, base_t)))
power_cutter = Cylinder(
    power_hole_radius, power_cut_depth,
    align=(Align.CENTER, Align.CENTER, Align.CENTER),
).rotate(Axis.X, 90).moved(Location((power_x, front_y, power_z)))
front_panel = (front_panel - power_cutter).clean()
front_edges = vertical_edges(front_panel, front_fillet_min_edge)
if front_edges:
    front_panel = fillet(front_edges, front_fillet_radius)

power_side_edge_clearance = W / 2.0 - abs(power_x) - power_hole_radius
power_bottom_edge_clearance = power_z - front_panel_bottom_z - power_hole_radius
power_top_edge_clearance = front_panel_top_z - power_z - power_hole_radius
assert power_x > 0.0  # +X is exterior-view left on the +Y front face.
assert power_side_edge_clearance > power_min_edge_clearance
assert power_top_edge_clearance > power_min_edge_clearance
assert power_bottom_edge_clearance > power_min_edge_clearance
assert front_panel.solids().__len__() == 1
publish('front_panel', front_panel, 'Upper-left power panel')
print(
    f'FRONT_POWER_POSITION: exterior upper-left center x={power_x:.1f} mm, '
    f'z={power_z:.1f} mm; side/top clearances '
    f'{power_side_edge_clearance:.1f}/{power_top_edge_clearance:.1f} mm.'
)
