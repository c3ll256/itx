# Remove the remaining shallow legacy flange around the four rear-panel magnet mounts.
# Preserve one clean carrier block, its 15 x 10 x 4 pocket, and the centered M3 interface.
rear_magnet_cleanup_width_x = param('rear_magnet_cleanup_width_x', 18.0)
rear_magnet_cleanup_depth_y = param('rear_magnet_cleanup_depth_y', 20.0)
rear_magnet_cleanup_height_z = param('rear_magnet_cleanup_height_z', 22.0)
rear_magnet_clean_carrier_depth_x = param('rear_magnet_clean_carrier_depth_x', panel_magnet15_carrier_depth)
rear_magnet_clean_carrier_width_y = param('rear_magnet_clean_carrier_width_y', panel_magnet15_carrier_width_y)
rear_magnet_clean_carrier_height_z = param('rear_magnet_clean_carrier_height_z', panel_magnet15_carrier_height_z)
rear_magnet_skin_guard = param('rear_magnet_skin_guard', 0.05)
rear_inner_face_y = -D / 2 + panel_t
rear_cleanup_center_y = rear_inner_face_y + rear_magnet_skin_guard + rear_magnet_cleanup_depth_y / 2
rear_station_y = -panel_magnet15_station_y
for sx in (-1, 1):
    carrier_x = sx * (frame_outer_x - panel_magnet15_carrier_depth / 2)
    pocket_x = sx * (frame_outer_x - panel_magnet15_pocket_depth / 2)
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
publish('rear_panel', rear_panel, 'Single-level rear magnets')
print('REAR_MAGNET_FLANGES_REMOVED: four shallow legacy pads removed; one rectangular carrier retained at each magnet point.')