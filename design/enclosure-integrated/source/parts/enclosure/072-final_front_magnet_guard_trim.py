# Remove the obsolete front-panel lamination copies that remain visible as
# 20 x 24 mm rectangular backing plates behind the four compact magnet carriers.
# The edge of the front panel does not receive the central 2 mm reinforcement
# layer, so its nominal interior face remains at D/2-panel_t (Y=126 mm). The
# previous cleanup used the central 5 mm datum (Y=124 mm) and left a 2 mm-deep
# local plate. Cut that complete difference only outside the final carrier's
# X/Z projection, preserving a hidden carrier-sized neck to the panel.
final_front_guard_trim_width_x = param(
    'final_front_guard_trim_width_x', panel_magnet15_front_cleanup_depth_x
)
final_front_guard_trim_height_z = param(
    'final_front_guard_trim_height_z', panel_magnet15_front_cleanup_height_z
)
final_front_guard_trim_depth_y = param('final_front_guard_trim_depth_y', 0.20)
final_front_guard_panel_overcut_y = param('final_front_guard_panel_overcut_y', 0.001)
final_front_guard_carrier_gap = param('final_front_guard_carrier_gap', 0.01)

# The old compatibility parameters remain editable, but the cutter may not be
# smaller than the known final 20 x 24 mm legacy-lamination envelope.
front_guard_cleanup_width_x = max(
    final_front_guard_trim_width_x, final_magnet_cleanup_width_x
)
front_guard_cleanup_height_z = max(
    final_front_guard_trim_height_z, final_magnet_cleanup_height_z
)
front_edge_nominal_inner_y = panel_magnet15_end_inner_face_y
front_edge_laminated_inner_y = front_final_inner_y
front_guard_residual_depth_y = front_edge_nominal_inner_y - front_edge_laminated_inner_y

assert front_guard_cleanup_width_x >= final_magnet_cleanup_width_x
assert front_guard_cleanup_height_z >= final_magnet_cleanup_height_z
assert 1.90 <= front_guard_residual_depth_y <= 2.10
assert final_front_guard_trim_depth_y > 0.0
assert final_front_guard_trim_depth_y < 0.30
assert final_front_guard_panel_overcut_y <= 0.002
assert final_front_guard_carrier_gap > 0.0

front_guard_trim_min_y = front_edge_laminated_inner_y - final_front_guard_trim_depth_y
front_guard_trim_max_y = front_edge_nominal_inner_y + final_front_guard_panel_overcut_y
front_guard_trim_total_depth_y = front_guard_trim_max_y - front_guard_trim_min_y
front_guard_trim_center_y = (front_guard_trim_min_y + front_guard_trim_max_y) / 2
front_guard_cleanup_x_abs = final_side_interface_x - front_guard_cleanup_width_x / 2

for sx in (-1, 1):
    guard_x = sx * front_guard_cleanup_x_abs
    carrier_x = sx * final_carrier_center_x_abs
    for zz in (side_station_z_low, side_station_z_high):
        legacy_guard_zone = Box(
            front_guard_cleanup_width_x,
            front_guard_trim_total_depth_y,
            front_guard_cleanup_height_z,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((guard_x, front_guard_trim_center_y, zz)))
        carrier_neck_keep = Box(
            final_magnet_carrier_depth + 2 * final_front_guard_carrier_gap,
            front_guard_trim_total_depth_y + 2 * final_front_guard_carrier_gap,
            final_magnet_carrier_height + 2 * final_front_guard_carrier_gap,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((carrier_x, front_guard_trim_center_y, zz)))
        exposed_backing_only = (legacy_guard_zone - carrier_neck_keep).clean()
        front_panel = (front_panel - exposed_backing_only).clean()

assert front_panel.solids().__len__() == 1
publish('front_panel', front_panel, 'Front magnets with carrier-sized hidden necks')
print(
    f'FRONT_MAGNET_BACKING_TRIM_PASS: removed four exposed '
    f'{front_guard_cleanup_width_x:.1f}x{front_guard_cleanup_height_z:.1f} mm '
    f'legacy lamination plates over {front_guard_residual_depth_y:.3f} mm residual depth; '
    f'compact carriers, pockets, and carrier-sized hidden panel necks retained.'
)