# Remove residual legacy flange material around the four rear adhesive-magnet
# stations. Preserve exactly one compact vertical carrier and its inward-facing
# 10 x 5 x 2 mm glue pocket at each location.
rear_magnet_cleanup_width_x = param('rear_magnet_glue_v2_cleanup_width_x', 16.0)
rear_magnet_cleanup_depth_y = param('rear_magnet_glue_v2_cleanup_depth_y', 18.0)
rear_magnet_cleanup_height_z = param('rear_magnet_glue_v2_cleanup_height_z', 18.0)
rear_magnet_clean_carrier_depth_x = param('rear_magnet_glue_v2_carrier_depth_x', panel_magnet15_carrier_depth)
rear_magnet_clean_carrier_width_y = param('rear_magnet_glue_v2_carrier_width_y', panel_magnet15_carrier_width_y)
rear_magnet_clean_carrier_height_z = param('rear_magnet_glue_v2_carrier_height_z', panel_magnet15_carrier_height_z)
rear_magnet_skin_guard = param('rear_magnet_glue_v2_skin_guard', 0.05)

assert abs(rear_magnet_clean_carrier_depth_x - panel_magnet15_carrier_depth) < 0.001
assert abs(rear_magnet_clean_carrier_width_y - panel_magnet15_carrier_width_y) < 0.001
assert abs(rear_magnet_clean_carrier_height_z - panel_magnet15_carrier_height_z) < 0.001
assert rear_magnet_clean_carrier_depth_x <= 3.40 + 0.01
assert rear_magnet_clean_carrier_width_y <= 7.60 + 0.01
assert rear_magnet_clean_carrier_height_z <= 12.60 + 0.01

rear_inner_face_y = -D / 2 + panel_t
rear_cleanup_center_y = rear_inner_face_y + rear_magnet_skin_guard + rear_magnet_cleanup_depth_y / 2
rear_station_y = -panel_magnet15_station_y
for sx in (-1, 1):
    carrier_x = sx * panel_magnet15_carrier_center_x_abs
    pocket_x = sx * panel_magnet15_pocket_center_x_abs
    for zz in (side_station_z_low, side_station_z_high):
        cleanup_zone = Box(
            rear_magnet_cleanup_width_x,
            rear_magnet_cleanup_depth_y,
            rear_magnet_cleanup_height_z,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((carrier_x, rear_cleanup_center_y, zz)))
        clean_carrier_keep = Box(
            rear_magnet_clean_carrier_depth_x,
            rear_magnet_clean_carrier_width_y,
            rear_magnet_clean_carrier_height_z,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((carrier_x, rear_station_y, zz)))
        flange_only = cleanup_zone - clean_carrier_keep
        rear_panel = (rear_panel - flange_only).clean()
        pocket_recut = Box(
            panel_magnet15_pocket_depth + connection_cleanup_extra_depth,
            panel_magnet15_pocket_width,
            panel_magnet15_pocket_height,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((pocket_x - sx * connection_cleanup_extra_depth / 2, rear_station_y, zz)))
        rear_panel = (rear_panel - pocket_recut).clean()
assert rear_panel.solids().__len__() == 1
publish('rear_panel', rear_panel, 'Rear thin glued magnets')
print(f'REAR_MAGNET_GLUE_V2_CLEAN: four compact {rear_magnet_clean_carrier_depth_x:.1f}x{rear_magnet_clean_carrier_width_y:.1f}x{rear_magnet_clean_carrier_height_z:.1f} mm carriers retained; legacy flange removed; no screw features.')