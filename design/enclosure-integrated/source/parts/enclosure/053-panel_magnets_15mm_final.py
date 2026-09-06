# Rear-only legacy magnet finalization.
# All obsolete front magnet carriers are removed here, before the later 5 mm
# reinforcement is created. No replacement front carrier is generated in this
# cell; the final compact front cups are authored once, in the final magnet cell.
panel_magnet15_width_y = param('panel_magnet_glue_v2_width_y', 5.0)
panel_magnet15_height_z = param('panel_magnet_glue_v2_height_z', 10.0)
panel_magnet15_depth_x = param('panel_magnet_glue_v2_depth_x', 2.0)
panel_magnet15_pocket_clearance = param('panel_magnet_glue_v2_planar_clearance', 0.20)
panel_magnet15_depth_clearance = param('panel_magnet_glue_v2_depth_clearance', 0.10)
panel_magnet15_back_wall_x = param('panel_magnet_glue_v2_back_wall_x', 1.20)
panel_magnet15_wall_y = param('panel_magnet_glue_v2_side_wall_y', 1.20)
panel_magnet15_wall_z = param('panel_magnet_glue_v2_end_wall_z', 1.20)
panel_magnet15_panel_overlap_y = param('panel_magnet_glue_v2_panel_overlap_y', 0.40)
panel_magnet15_expected = param('panel_magnet_glue_v2_expected', 8)
panel_magnet15_steel_thickness_x = param('panel_magnet_glue_v2_strike_thickness_x', 1.0)
panel_magnet15_steel_clearance = param('panel_magnet_glue_v2_strike_planar_clearance', 0.30)
panel_magnet15_steel_depth_clearance = param('panel_magnet_glue_v2_strike_depth_clearance', 0.15)
panel_magnet15_side_patch_width_y = param('panel_magnet_glue_v2_side_repair_width_y', 16.0)
panel_magnet15_side_patch_height_z = param('panel_magnet_glue_v2_side_repair_height_z', 18.0)
panel_magnet15_repair_inset_y = param('panel_magnet_glue_v2_repair_inset_y', 8.0)
panel_magnet15_front_cleanup_depth_x = param('panel_magnet_glue_v2_front_cleanup_depth_x', 10.0)
panel_magnet15_front_cleanup_depth_y = param('panel_magnet_glue_v2_front_cleanup_depth_y', 20.0)
panel_magnet15_front_cleanup_height_z = param('panel_magnet_glue_v2_front_cleanup_height_z', 20.0)
panel_magnet15_front_skin_guard = param('panel_magnet_glue_v2_front_skin_guard', 0.05)

panel_magnet15_pocket_depth = panel_magnet15_depth_x + panel_magnet15_depth_clearance
panel_magnet15_pocket_width = panel_magnet15_width_y + panel_magnet15_pocket_clearance
panel_magnet15_pocket_height = panel_magnet15_height_z + panel_magnet15_pocket_clearance
panel_magnet15_carrier_depth = panel_magnet15_pocket_depth + panel_magnet15_back_wall_x
panel_magnet15_carrier_width_y = panel_magnet15_pocket_width + 2 * panel_magnet15_wall_y
panel_magnet15_carrier_height_z = panel_magnet15_pocket_height + 2 * panel_magnet15_wall_z
panel_magnet15_interface_face_x = W / 2 - panel_t
panel_magnet15_carrier_center_x_abs = panel_magnet15_interface_face_x - panel_magnet15_carrier_depth / 2
panel_magnet15_pocket_center_x_abs = panel_magnet15_interface_face_x - panel_magnet15_pocket_depth / 2
panel_magnet15_end_inner_face_y = D / 2 - panel_t
panel_magnet15_station_y = panel_magnet15_end_inner_face_y - panel_magnet15_carrier_width_y / 2 + panel_magnet15_panel_overlap_y
panel_magnet15_station_inset_y = D / 2 - panel_magnet15_station_y
panel_magnet15_repair_station_y = D / 2 - panel_magnet15_repair_inset_y
panel_magnet15_slot_width = panel_magnet15_width_y + panel_magnet15_steel_clearance
panel_magnet15_slot_height = panel_magnet15_height_z + panel_magnet15_steel_clearance
panel_magnet15_slot_depth = panel_magnet15_steel_thickness_x + panel_magnet15_steel_depth_clearance

assert panel_magnet15_width_y == 5.0
assert panel_magnet15_height_z == 10.0
assert panel_magnet15_depth_x == 2.0
assert 0.15 <= panel_magnet15_pocket_clearance <= 0.35
assert 0.05 <= panel_magnet15_depth_clearance <= 0.20
assert panel_magnet15_back_wall_x >= 1.20
assert panel_magnet15_wall_y >= 1.20
assert panel_magnet15_wall_z >= 1.20
assert panel_magnet15_carrier_depth <= 3.40 + 0.01
assert panel_magnet15_carrier_width_y <= 7.60 + 0.01
assert panel_magnet15_carrier_height_z <= 12.60 + 0.01
assert panel_magnet15_front_skin_guard > 0.0

# Directly delete the obsolete front carrier envelope while the front is still
# the original thin panel. This operation occurs before the 5 mm reinforcement,
# so the later laminate is created as one uninterrupted plane over these zones.
front_cleanup_center_y = (
    panel_magnet15_end_inner_face_y
    - panel_magnet15_front_skin_guard
    - panel_magnet15_front_cleanup_depth_y / 2
)
for sx in (-1, 1):
    cleanup_x = sx * (
        panel_magnet15_interface_face_x
        - panel_magnet15_front_cleanup_depth_x / 2
    )
    for zz in (side_station_z_low, side_station_z_high):
        front_cleanup = Box(
            panel_magnet15_front_cleanup_depth_x,
            panel_magnet15_front_cleanup_depth_y,
            panel_magnet15_front_cleanup_height_z,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((cleanup_x, front_cleanup_center_y, zz)))
        front_panel = (front_panel - front_cleanup).clean()

# Keep only the four rear compact carriers from this historical cell.
panel_magnet15_rear_count = 0
rear_station_y = -panel_magnet15_station_y
for sx in (-1, 1):
    carrier_x = sx * panel_magnet15_carrier_center_x_abs
    pocket_x = sx * panel_magnet15_pocket_center_x_abs
    for zz in (side_station_z_low, side_station_z_high):
        carrier = Box(
            panel_magnet15_carrier_depth,
            panel_magnet15_carrier_width_y,
            panel_magnet15_carrier_height_z,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((carrier_x, rear_station_y, zz)))
        pocket = Box(
            panel_magnet15_pocket_depth,
            panel_magnet15_pocket_width,
            panel_magnet15_pocket_height,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((pocket_x, rear_station_y, zz)))
        rear_panel = (rear_panel + carrier - pocket).clean()
        panel_magnet15_rear_count += 1
assert panel_magnet15_rear_count == int(panel_magnet15_expected) // 2

# Side panels pass through unchanged. No patch, refill, strike pocket, edge ear,
# or local thickening is created here; final steel recesses are cut once later.
assert front_panel.solids().__len__() == 1 and rear_panel.solids().__len__() == 1
assert left_panel.solids().__len__() == 1 and right_panel.solids().__len__() == 1
publish('front_panel', front_panel, 'Obsolete front magnets removed')
publish('rear_panel', rear_panel, 'Rear glued magnets')
publish('left_panel', left_panel, 'Unmodified left side panel')
publish('right_panel', right_panel, 'Unmodified right side panel')
print('FRONT_LEGACY_MAGNET_DELETE_PASS: obsolete front carriers deleted; four rear carriers retained; side-panel repair geometry retired.')