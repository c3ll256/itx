# Final adhesive-magnet pass.
# Front only: simplify each station into one shallow edge-integrated cup. The
# existing front-panel skin supplies the exterior Y wall, so the printed carrier
# needs only one inner Y wall, top/bottom walls, and the X backing wall.
# Rear stations retain the previously accepted compact rectangular carriers.
simple_magnet_height_z = param('simple_glued_magnet_height_z', 10.0)
simple_magnet_width_y = param('simple_glued_magnet_width_y', 5.0)
simple_magnet_depth_x = param('simple_glued_magnet_depth_x', 2.0)
simple_magnet_planar_clearance = param('simple_glued_magnet_planar_clearance', 0.50)
simple_magnet_depth_clearance = param('simple_glued_magnet_depth_clearance', 0.0)
simple_magnet_back_wall_x = param('simple_glued_magnet_back_wall_x', 1.20)
simple_magnet_wall_y = param('simple_glued_magnet_wall_y', 1.20)
simple_magnet_wall_z = param('simple_glued_magnet_wall_z', 1.20)
simple_front_outer_skin_y = param('simple_front_glued_magnet_outer_skin_y', 1.20)
simple_magnet_panel_overlap_y = param('simple_glued_magnet_panel_overlap_y', 0.50)
simple_magnet_side_inset_x = param('simple_glued_magnet_side_inset_x', 0.40)
simple_magnet_cleanup_width_x = param('simple_glued_magnet_cleanup_width_x', 20.0)
simple_magnet_cleanup_depth_y = param('simple_glued_magnet_cleanup_depth_y', 22.0)
simple_magnet_cleanup_height_z = param('simple_glued_magnet_cleanup_height_z', 24.0)
simple_magnet_expected_count = param('simple_glued_magnet_expected_count', 8)
simple_front_expected_count = param('simple_front_glued_magnet_expected_count', 4)

simple_magnet_pocket_depth_x = simple_magnet_depth_x + simple_magnet_depth_clearance
simple_magnet_pocket_width_y = simple_magnet_width_y + simple_magnet_planar_clearance
simple_magnet_pocket_height_z = simple_magnet_height_z + simple_magnet_planar_clearance
simple_magnet_carrier_depth_x = simple_magnet_pocket_depth_x + simple_magnet_back_wall_x
simple_rear_carrier_width_y = simple_magnet_pocket_width_y + 2.0 * simple_magnet_wall_y
simple_front_carrier_width_y = simple_magnet_pocket_width_y + simple_magnet_wall_y
simple_magnet_carrier_height_z = simple_magnet_pocket_height_z + 2.0 * simple_magnet_wall_z
simple_magnet_outer_x = final_side_interface_x - simple_magnet_side_inset_x
simple_magnet_carrier_center_x_abs = simple_magnet_outer_x - simple_magnet_carrier_depth_x / 2.0
simple_magnet_pocket_center_x_abs = simple_magnet_outer_x - simple_magnet_pocket_depth_x / 2.0

# The old edge-only panel skin begins at this nominal inner face. Clean every
# legacy protrusion inward from it while preserving the complete exterior skin.
simple_front_nominal_inner_y = panel_magnet15_end_inner_face_y
simple_front_pocket_max_y = front_final_outer_y - simple_front_outer_skin_y
simple_front_pocket_center_y = simple_front_pocket_max_y - simple_magnet_pocket_width_y / 2.0
simple_front_carrier_max_y = simple_front_pocket_max_y
simple_front_carrier_center_y = simple_front_carrier_max_y - simple_front_carrier_width_y / 2.0
simple_front_carrier_min_y = simple_front_carrier_max_y - simple_front_carrier_width_y
simple_front_inward_projection_y = simple_front_nominal_inner_y - simple_front_carrier_min_y
simple_front_skin_fuse_overlap_y = simple_front_carrier_max_y - simple_front_nominal_inner_y
simple_rear_station_y = rear_final_inner_y + simple_rear_carrier_width_y / 2.0 - simple_magnet_panel_overlap_y
simple_magnet_station_zs = (side_station_z_low, side_station_z_high)

assert simple_magnet_pocket_width_y == 5.50
assert simple_magnet_pocket_height_z == 10.50
assert simple_magnet_pocket_depth_x == 2.00
assert simple_magnet_back_wall_x >= 1.20
assert simple_magnet_wall_y >= 1.20 and simple_magnet_wall_z >= 1.20
assert simple_front_outer_skin_y >= 1.20
assert simple_magnet_carrier_depth_x == 3.20
assert simple_front_carrier_width_y == 6.70
assert simple_rear_carrier_width_y == 7.90
assert simple_magnet_carrier_height_z == 12.90
assert simple_front_inward_projection_y <= 5.0
assert simple_front_skin_fuse_overlap_y >= 1.20
assert simple_magnet_side_inset_x >= end_panel_vertical_chamfer

simple_magnet_pocket_count = 0
simple_front_pocket_count = 0
simple_front_carriers = []
simple_rear_carriers = []

# Front: remove old laminations/carriers from the nominal inner skin datum and
# replace each with one embedded cup. The exterior panel skin closes the cup;
# no separate outer Y rail or hidden connector remains.
rebuilt_front = front_panel
for sx in (-1, 1):
    cleanup_x = sx * (final_side_interface_x - simple_magnet_cleanup_width_x / 2.0)
    for zz in simple_magnet_station_zs:
        cleanup = Box(
            simple_magnet_cleanup_width_x,
            simple_magnet_cleanup_depth_y,
            simple_magnet_cleanup_height_z,
            align=(Align.CENTER, Align.MAX, Align.CENTER),
        ).moved(Location((cleanup_x, simple_front_nominal_inner_y, zz)))
        rebuilt_front = (rebuilt_front - cleanup).clean()

        carrier_x = sx * simple_magnet_carrier_center_x_abs
        pocket_x = sx * simple_magnet_pocket_center_x_abs
        carrier = Box(
            simple_magnet_carrier_depth_x,
            simple_front_carrier_width_y,
            simple_magnet_carrier_height_z,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((carrier_x, simple_front_carrier_center_y, zz)))
        pocket = Box(
            simple_magnet_pocket_depth_x,
            simple_magnet_pocket_width_y,
            simple_magnet_pocket_height_z,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((pocket_x, simple_front_pocket_center_y, zz)))
        rebuilt_front = (rebuilt_front + carrier - pocket).clean()
        simple_front_carriers.append(carrier)
        simple_front_pocket_count += 1
        simple_magnet_pocket_count += 1
front_panel = rebuilt_front

# Rear: preserve the existing compact carrier dimensions and positions.
rebuilt_rear = rear_panel
for sx in (-1, 1):
    cleanup_x = sx * (final_side_interface_x - simple_magnet_cleanup_width_x / 2.0)
    for zz in simple_magnet_station_zs:
        cleanup = Box(
            simple_magnet_cleanup_width_x,
            simple_magnet_cleanup_depth_y,
            simple_magnet_cleanup_height_z,
            align=(Align.CENTER, Align.MIN, Align.CENTER),
        ).moved(Location((cleanup_x, rear_final_inner_y, zz)))
        rebuilt_rear = (rebuilt_rear - cleanup).clean()

        carrier_x = sx * simple_magnet_carrier_center_x_abs
        pocket_x = sx * simple_magnet_pocket_center_x_abs
        carrier = Box(
            simple_magnet_carrier_depth_x,
            simple_rear_carrier_width_y,
            simple_magnet_carrier_height_z,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((carrier_x, simple_rear_station_y, zz)))
        pocket = Box(
            simple_magnet_pocket_depth_x,
            simple_magnet_pocket_width_y,
            simple_magnet_pocket_height_z,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((pocket_x, simple_rear_station_y, zz)))
        rebuilt_rear = (rebuilt_rear + carrier - pocket).clean()
        simple_rear_carriers.append(carrier)
        simple_magnet_pocket_count += 1
rear_panel = rebuilt_rear

simple_front_carrier_shape = Compound(children=simple_front_carriers)
simple_rear_carrier_shape = Compound(children=simple_rear_carriers)
simple_front_fan_intersection = sum((simple_front_carrier_shape & body).volume for body in fan80_bodies)
simple_rear_psu_intersection = (simple_rear_carrier_shape & fan120_psu_proxy).volume
simple_magnet_connections = {
    'front-magnets': 'four edge-integrated 10x5x2 mm adhesive cups; panel skin is outer wall',
    'rear-magnets': 'four existing compact 10x5x2 mm adhesive pockets; no screw',
    'side-strikes': 'existing compact inner-face steel recesses retained',
}

assert simple_front_pocket_count == int(simple_front_expected_count)
assert simple_magnet_pocket_count == int(simple_magnet_expected_count)
assert simple_front_fan_intersection < 0.01
assert simple_rear_psu_intersection < 0.01
assert front_panel.solids().__len__() == 1 and rear_panel.solids().__len__() == 1
assert all(simple_magnet_connections.values())

publish('front_panel', front_panel, 'Embedded front magnet cups')
publish('rear_panel', rear_panel, 'Simple rear magnet pockets')
print(
    f'FRONT_MAGNET_SIMPLIFY_PASS: four embedded 10x5x2 mm adhesive cups; '
    f'pocket={simple_magnet_pocket_height_z:.1f}x{simple_magnet_pocket_width_y:.1f}x'
    f'{simple_magnet_pocket_depth_x:.1f} mm; front carrier={simple_magnet_carrier_depth_x:.1f}x'
    f'{simple_front_carrier_width_y:.1f}x{simple_magnet_carrier_height_z:.1f} mm; '
    f'inward projection={simple_front_inward_projection_y:.1f} mm; '
    f'front fan intersection={simple_front_fan_intersection:.3f} mm^3; rear unchanged.'
)