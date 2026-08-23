# Final adhesive-magnet pass.
# Front only: remove every legacy local backing land, attach each compact cup
# directly to the original 2 mm front-panel edge skin, and move the matching
# side-panel steel recess to the same Y center. No rectangular backing guard or
# hidden connection neck is retained. Rear stations remain unchanged.
simple_magnet_height_z = param('simple_glued_magnet_height_z', 10.0)
simple_magnet_width_y = param('simple_glued_magnet_width_y', 5.0)
simple_magnet_depth_x = param('simple_glued_magnet_depth_x', 2.0)
simple_magnet_planar_clearance = param('simple_glued_magnet_planar_clearance', 0.50)
simple_magnet_depth_clearance = param('simple_glued_magnet_depth_clearance', 0.0)
simple_magnet_back_wall_x = param('simple_glued_magnet_back_wall_x', 1.20)
simple_magnet_wall_y = param('simple_glued_magnet_wall_y', 1.20)
simple_magnet_wall_z = param('simple_glued_magnet_wall_z', 1.20)
simple_front_panel_overlap_y = param('simple_front_glued_magnet_panel_overlap_y', 0.20)
simple_magnet_panel_overlap_y = param('simple_glued_magnet_panel_overlap_y', 0.50)
simple_magnet_side_inset_x = param('simple_glued_magnet_side_inset_x', 0.40)
simple_front_cleanup_width_x = param('simple_front_glued_magnet_cleanup_width_x', 10.0)
simple_magnet_cleanup_width_x = param('simple_glued_magnet_cleanup_width_x', 20.0)
simple_magnet_cleanup_depth_y = param('simple_glued_magnet_cleanup_depth_y', 22.0)
simple_magnet_cleanup_height_z = param('simple_glued_magnet_cleanup_height_z', 24.0)
simple_magnet_expected_count = param('simple_glued_magnet_expected_count', 8)
simple_front_expected_count = param('simple_front_glued_magnet_expected_count', 4)

simple_magnet_pocket_depth_x = simple_magnet_depth_x + simple_magnet_depth_clearance
simple_magnet_pocket_width_y = simple_magnet_width_y + simple_magnet_planar_clearance
simple_magnet_pocket_height_z = simple_magnet_height_z + simple_magnet_planar_clearance
simple_magnet_carrier_depth_x = simple_magnet_pocket_depth_x + simple_magnet_back_wall_x
simple_magnet_carrier_width_y = simple_magnet_pocket_width_y + 2.0 * simple_magnet_wall_y
simple_magnet_carrier_height_z = simple_magnet_pocket_height_z + 2.0 * simple_magnet_wall_z
simple_magnet_outer_x = final_side_interface_x - simple_magnet_side_inset_x
simple_magnet_carrier_center_x_abs = simple_magnet_outer_x - simple_magnet_carrier_depth_x / 2.0
simple_magnet_pocket_center_x_abs = simple_magnet_outer_x - simple_magnet_pocket_depth_x / 2.0

# The edge band retains the original 2 mm panel skin. Cups fuse directly to its
# inner face; the reinforced central panel datum is deliberately not used here.
simple_front_attach_face_y = panel_magnet15_end_inner_face_y
simple_front_carrier_max_y = simple_front_attach_face_y + simple_front_panel_overlap_y
simple_front_carrier_center_y = simple_front_carrier_max_y - simple_magnet_carrier_width_y / 2.0
simple_front_carrier_min_y = simple_front_carrier_max_y - simple_magnet_carrier_width_y
simple_front_pocket_center_y = simple_front_carrier_center_y
simple_front_inward_projection_y = simple_front_attach_face_y - simple_front_carrier_min_y
simple_front_strike_center_y = simple_front_pocket_center_y
simple_front_strike_shift_y = simple_front_strike_center_y - final_front_station_y
simple_rear_station_y = rear_final_inner_y + simple_magnet_carrier_width_y / 2.0 - simple_magnet_panel_overlap_y
simple_magnet_station_zs = (side_station_z_low, side_station_z_high)

assert simple_magnet_pocket_width_y == 5.50
assert simple_magnet_pocket_height_z == 10.50
assert simple_magnet_pocket_depth_x == 2.00
assert simple_magnet_back_wall_x >= 1.20
assert simple_magnet_wall_y >= 1.20 and simple_magnet_wall_z >= 1.20
assert simple_magnet_carrier_depth_x == 3.20
assert simple_magnet_carrier_width_y == 7.90
assert simple_magnet_carrier_height_z == 12.90
assert 0.10 <= simple_front_panel_overlap_y <= 0.25
assert simple_front_inward_projection_y <= 8.0
assert simple_magnet_side_inset_x >= end_panel_vertical_chamfer
assert simple_front_cleanup_width_x >= simple_magnet_carrier_depth_x + 2.0
assert simple_front_cleanup_width_x < simple_magnet_cleanup_width_x
assert 1.0 <= simple_front_strike_shift_y <= 3.0

simple_magnet_pocket_count = 0
simple_front_pocket_count = 0
simple_front_strike_count = 0
simple_front_carriers = []
simple_rear_carriers = []
simple_front_contact_volume = 0.0

# Front: erase the whole legacy 10 x 22 x 24 mm feature envelope up to the
# original panel inner face, then add only the compact cup. Its 0.2 mm overlap
# with the untouched panel skin is the complete structural connection.
rebuilt_front = front_panel
for sx in (-1, 1):
    cleanup_x = sx * (simple_magnet_outer_x - simple_front_cleanup_width_x / 2.0)
    for zz in simple_magnet_station_zs:
        cleanup = Box(
            simple_front_cleanup_width_x,
            simple_magnet_cleanup_depth_y,
            simple_magnet_cleanup_height_z,
            align=(Align.CENTER, Align.MAX, Align.CENTER),
        ).moved(Location((cleanup_x, simple_front_attach_face_y, zz)))
        rebuilt_front = (rebuilt_front - cleanup).clean()

        carrier_x = sx * simple_magnet_carrier_center_x_abs
        pocket_x = sx * simple_magnet_pocket_center_x_abs
        carrier = Box(
            simple_magnet_carrier_depth_x,
            simple_magnet_carrier_width_y,
            simple_magnet_carrier_height_z,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((carrier_x, simple_front_carrier_center_y, zz)))
        pocket = Box(
            simple_magnet_pocket_depth_x,
            simple_magnet_pocket_width_y,
            simple_magnet_pocket_height_z,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((pocket_x, simple_front_pocket_center_y, zz)))
        direct_contact = carrier & rebuilt_front
        simple_front_contact_volume += direct_contact.volume
        assert direct_contact.solids().__len__() == 1
        rebuilt_front = (rebuilt_front + carrier - pocket).clean()
        simple_front_carriers.append(carrier)
        simple_front_pocket_count += 1
        simple_magnet_pocket_count += 1
front_panel = rebuilt_front

# Restore each old front strike recess from the side-panel inner face and cut a
# replacement at the exact new magnet-pocket center. Rear strike recesses stay
# at their accepted locations.
for sx, side_shape in ((-1, left_panel), (1, right_panel)):
    revised_side = side_shape
    side_inner_x = sx * final_side_interface_x
    repair_center_x = side_inner_x + sx * final_strike_repair_depth / 2.0
    strike_center_x = side_inner_x + sx * final_strike_depth / 2.0
    for zz in simple_magnet_station_zs:
        old_front_strike_repair = Box(
            final_strike_repair_depth,
            final_strike_patch_width_y,
            final_strike_patch_height_z,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((repair_center_x, final_front_station_y, zz)))
        aligned_front_strike = Box(
            final_strike_depth,
            simple_magnet_pocket_width_y,
            simple_magnet_pocket_height_z,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((strike_center_x, simple_front_strike_center_y, zz)))
        revised_side = (revised_side + old_front_strike_repair - aligned_front_strike).clean()
        simple_front_strike_count += 1
    if sx < 0:
        left_panel = revised_side
    else:
        right_panel = revised_side

# Rear: preserve the existing cleanup envelope, carrier dimensions and positions.
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
            simple_magnet_carrier_width_y,
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
    'front-magnets': 'four compact 10x5x2 mm adhesive cups directly fused to the original front-panel edge skin',
    'rear-magnets': 'four existing compact 10x5x2 mm adhesive pockets; no screw',
    'side-strikes': 'four front steel recesses aligned to the direct-mounted cups; four rear recesses retained',
}

assert simple_front_pocket_count == int(simple_front_expected_count)
assert simple_front_strike_count == int(simple_front_expected_count)
assert simple_magnet_pocket_count == int(simple_magnet_expected_count)
assert simple_front_contact_volume > 4.0 * simple_magnet_carrier_depth_x * simple_magnet_carrier_height_z * 0.15
assert simple_front_fan_intersection < 0.01
assert simple_rear_psu_intersection < 0.01
assert all(p.solids().__len__() == 1 for p in (front_panel, rear_panel, left_panel, right_panel))
assert all(simple_magnet_connections.values())

publish('front_panel', front_panel, 'Direct-mount front magnet cups')
publish('rear_panel', rear_panel, 'Simple rear magnet pockets')
publish('left_panel', left_panel, 'Aligned left front strikes')
publish('right_panel', right_panel, 'Aligned right front strikes')
print(
    f'FRONT_MAGNET_DIRECT_MOUNT_PASS: four compact 10x5x2 mm adhesive cups; '
    f'pocket={simple_magnet_pocket_height_z:.1f}x{simple_magnet_pocket_width_y:.1f}x'
    f'{simple_magnet_pocket_depth_x:.1f} mm; no backing lands or hidden necks; '
    f'direct panel overlap={simple_front_panel_overlap_y:.2f} mm; '
    f'front strike shift={simple_front_strike_shift_y:.2f} mm with exact center alignment; '
    f'total contact={simple_front_contact_volume:.2f} mm^3; '
    f'carrier/fan intersection={simple_front_fan_intersection:.3f} mm^3; rear unchanged.'
)