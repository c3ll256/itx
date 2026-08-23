# Remove the obsolete front-panel lamination copies that remained as oversized
# rectangular backing plates behind the four magnet stations. Delete the full
# legacy local plate envelope with no preserved neck; the following magnet cell
# rebuilds each compact cup as a direct overlap with the original 2 mm panel skin.
final_front_guard_trim_width_x = param(
    'final_front_guard_trim_width_x', panel_magnet15_front_cleanup_depth_x
)
final_front_guard_trim_height_z = param(
    'final_front_guard_trim_height_z', panel_magnet15_front_cleanup_height_z
)
final_front_guard_trim_depth_y = param('final_front_guard_trim_depth_y', 0.20)
final_front_guard_panel_overcut_y = param('final_front_guard_panel_overcut_y', 0.001)

# The cutter may not be smaller than the complete known legacy-lamination zone.
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

front_guard_trim_min_y = front_edge_laminated_inner_y - final_front_guard_trim_depth_y
front_guard_trim_max_y = front_edge_nominal_inner_y + final_front_guard_panel_overcut_y
front_guard_trim_total_depth_y = front_guard_trim_max_y - front_guard_trim_min_y
front_guard_trim_center_y = (front_guard_trim_min_y + front_guard_trim_max_y) / 2
front_guard_cleanup_x_abs = final_side_interface_x - front_guard_cleanup_width_x / 2
front_guard_discarded_solid_count = 0

for sx in (-1, 1):
    guard_x = sx * front_guard_cleanup_x_abs
    for zz in (side_station_z_low, side_station_z_high):
        legacy_guard_zone = Box(
            front_guard_cleanup_width_x,
            front_guard_trim_total_depth_y,
            front_guard_cleanup_height_z,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((guard_x, front_guard_trim_center_y, zz)))
        trim_result = front_panel - legacy_guard_zone
        if hasattr(trim_result, 'solids'):
            trim_solids = list(trim_result.solids())
        else:
            trim_solids = list(trim_result)
        assert len(trim_solids) >= 1
        front_guard_discarded_solid_count += len(trim_solids) - 1
        front_panel = max(trim_solids, key=lambda solid: solid.volume).clean()

assert front_panel.solids().__len__() == 1
assert front_guard_discarded_solid_count >= 4
publish('front_panel', front_panel, 'Legacy front magnet backing removed')
print(
    f'FRONT_MAGNET_BACKING_DELETE_PASS: removed four complete '
    f'{front_guard_cleanup_width_x:.1f}x{front_guard_cleanup_height_z:.1f} mm '
    f'legacy lamination zones over {front_guard_residual_depth_y:.3f} mm residual depth; '
    f'discarded {front_guard_discarded_solid_count} detached legacy solids; '
    f'no backing guard or hidden connection neck retained.'
)