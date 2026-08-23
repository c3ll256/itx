# Eight adhesive-fixed 10 x 5 x 2 mm magnets in compact inward-facing
# rectangular pockets. No screw, pilot hole, boss, or mechanical retainer is
# used: the magnet is bonded directly to the 1.2 mm pocket back wall.
# The long 10 mm axis is vertical so the carrier stays narrow at the panel edge.
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

# The pocket opens flush at the removable side panel's inner face. The carrier
# remains wholly inside the enclosure outline and overlaps the end panel by only
# 0.4 mm, avoiding the old bulky flange while preserving a clean fused joint.
panel_magnet15_interface_face_x = W / 2 - panel_t
panel_magnet15_carrier_center_x_abs = panel_magnet15_interface_face_x - panel_magnet15_carrier_depth / 2
panel_magnet15_pocket_center_x_abs = panel_magnet15_interface_face_x - panel_magnet15_pocket_depth / 2
panel_magnet15_end_inner_face_y = D / 2 - panel_t
panel_magnet15_station_y = panel_magnet15_end_inner_face_y - panel_magnet15_carrier_width_y / 2 + panel_magnet15_panel_overlap_y
# Compatibility datum consumed by the downstream side-panel honeycomb keepout.
panel_magnet15_station_inset_y = D / 2 - panel_magnet15_station_y
panel_magnet15_repair_station_y = D / 2 - panel_magnet15_repair_inset_y

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
assert panel_magnet15_carrier_center_x_abs + panel_magnet15_carrier_depth / 2 <= panel_magnet15_interface_face_x + 0.01
assert panel_magnet15_repair_station_y + panel_magnet15_side_patch_width_y / 2 <= D / 2 + 0.01
assert panel_magnet15_front_skin_guard > 0.0

# Remove the old long front-panel carrier/flange at all four front stations,
# stopping 0.05 mm short of the inner skin. The new carrier then overlaps that
# protected skin by 0.4 mm and fuses as one solid without rebuilding a thick pad.
front_cleanup_center_y = panel_magnet15_end_inner_face_y - panel_magnet15_front_skin_guard - panel_magnet15_front_cleanup_depth_y / 2
for sx in (-1, 1):
    cleanup_x = sx * (panel_magnet15_interface_face_x - panel_magnet15_front_cleanup_depth_x / 2)
    for zz in (side_station_z_low, side_station_z_high):
        front_cleanup = Box(
            panel_magnet15_front_cleanup_depth_x,
            panel_magnet15_front_cleanup_depth_y,
            panel_magnet15_front_cleanup_height_z,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((cleanup_x, front_cleanup_center_y, zz)))
        front_panel = (front_panel - front_cleanup).clean()

panel_magnet15_count = 0
for sy in (-1, 1):
    panel = front_panel if sy > 0 else rear_panel
    station_y = sy * panel_magnet15_station_y
    for sx in (-1, 1):
        carrier_x = sx * panel_magnet15_carrier_center_x_abs
        pocket_x = sx * panel_magnet15_pocket_center_x_abs
        for zz in (side_station_z_low, side_station_z_high):
            carrier = Box(
                panel_magnet15_carrier_depth,
                panel_magnet15_carrier_width_y,
                panel_magnet15_carrier_height_z,
                align=(Align.CENTER, Align.CENTER, Align.CENTER),
            ).moved(Location((carrier_x, station_y, zz)))
            pocket = Box(
                panel_magnet15_pocket_depth,
                panel_magnet15_pocket_width,
                panel_magnet15_pocket_height,
                align=(Align.CENTER, Align.CENTER, Align.CENTER),
            ).moved(Location((pocket_x, station_y, zz)))
            panel = (panel + carrier).clean()
            panel = (panel - pocket).clean()
            panel_magnet15_count += 1
    if sy > 0:
        front_panel = panel
    else:
        rear_panel = panel
assert panel_magnet15_count == int(panel_magnet15_expected)

# Restore old oversized strike cutouts only within the original 2 mm side-panel
# skin, then cut one compact matching recess for each steel strike plate.
panel_magnet15_slot_width = panel_magnet15_width_y + panel_magnet15_steel_clearance
panel_magnet15_slot_height = panel_magnet15_height_z + panel_magnet15_steel_clearance
panel_magnet15_slot_depth = panel_magnet15_steel_thickness_x + panel_magnet15_steel_depth_clearance
panel_magnet15_side_count = 0
updated_side_panels = []
for sx, panel in ((-1, left_panel), (1, right_panel)):
    revised = panel
    panel_x = sx * (W / 2 - panel_t / 2)
    inner_face_x = sx * panel_magnet15_interface_face_x
    pocket_center_x = inner_face_x + sx * panel_magnet15_slot_depth / 2
    for sy in (-1, 1):
        station_y = sy * panel_magnet15_station_y
        repair_station_y = sy * panel_magnet15_repair_station_y
        for zz in (side_station_z_low, side_station_z_high):
            patch = Box(
                panel_t,
                panel_magnet15_side_patch_width_y,
                panel_magnet15_side_patch_height_z,
                align=(Align.CENTER, Align.CENTER, Align.CENTER),
            ).moved(Location((panel_x, repair_station_y, zz)))
            strike = Box(
                panel_magnet15_slot_depth,
                panel_magnet15_slot_width,
                panel_magnet15_slot_height,
                align=(Align.CENTER, Align.CENTER, Align.CENTER),
            ).moved(Location((pocket_center_x, station_y, zz)))
            revised = (revised + patch).clean()
            revised = (revised - strike).clean()
            panel_magnet15_side_count += 1
    updated_side_panels.append(revised)
left_panel, right_panel = updated_side_panels
assert panel_magnet15_side_count == int(panel_magnet15_expected)
assert front_panel.solids().__len__() == 1 and rear_panel.solids().__len__() == 1
assert left_panel.solids().__len__() == 1 and right_panel.solids().__len__() == 1
publish('front_panel', front_panel, 'Thin glued magnets')
publish('rear_panel', rear_panel, 'Thin glued magnets')
publish('left_panel', left_panel, 'Compact strike recesses')
publish('right_panel', right_panel, 'Compact strike recesses')
print(f'MAGNET_GLUE_V2_PASS: eight 10x5x2 mm adhesive pockets; carrier={panel_magnet15_carrier_depth:.1f}x{panel_magnet15_carrier_width_y:.1f}x{panel_magnet15_carrier_height_z:.1f} mm; walls={panel_magnet15_back_wall_x:.1f}/{panel_magnet15_wall_y:.1f}/{panel_magnet15_wall_z:.1f} mm; old front flanges removed; no screw features.')