# Eight adhesive-fixed 10 x 5 x 2 mm rectangular magnets with matching steel
# strike recesses. Legacy 15 mm parameter records remain readable, while the
# new panel_magnet10 parameters exclusively drive the revised geometry.
legacy_panel_magnet15_width_y = param('panel_magnet15_width_y', 15.0)
legacy_panel_magnet15_height_z = param('panel_magnet15_height_z', 10.0)
legacy_panel_magnet15_depth_x = param('panel_magnet15_depth_x', 4.0)
panel_magnet15_width_y = param('panel_magnet10_width_y', 10.0)
panel_magnet15_height_z = param('panel_magnet10_height_z', 5.0)
panel_magnet15_depth_x = param('panel_magnet10_depth_x', 2.0)
panel_magnet15_pocket_clearance = param('panel_magnet10_pocket_clearance', 0.20)
panel_magnet15_back_wall_x = param('panel_magnet10_back_wall_x', 2.0)
panel_magnet15_carrier_width_y = param('panel_magnet10_carrier_width_y', 14.0)
panel_magnet15_carrier_height_z = param('panel_magnet10_carrier_height_z', 9.0)
panel_magnet15_expected = param('panel_magnet10_expected', 8)
panel_magnet15_station_inset_y = param('panel_magnet10_station_inset_y', 10.0)
panel_magnet15_steel_thickness_x = param('panel_magnet10_steel_thickness_x', 1.0)
panel_magnet15_steel_clearance = param('panel_magnet10_steel_clearance', 0.30)
panel_magnet15_steel_depth_clearance = param('panel_magnet10_steel_depth_clearance', 0.15)
panel_magnet15_side_patch_width_y = param('panel_magnet10_side_patch_width_y', 12.0)
panel_magnet15_side_patch_height_z = param('panel_magnet10_side_patch_height_z', 8.0)
panel_magnet15_carrier_edge_radius = param('panel_magnet10_carrier_edge_radius', 0.8)

panel_magnet15_pocket_depth = panel_magnet15_depth_x + panel_magnet15_pocket_clearance
panel_magnet15_pocket_width = panel_magnet15_width_y + panel_magnet15_pocket_clearance
panel_magnet15_pocket_height = panel_magnet15_height_z + panel_magnet15_pocket_clearance
panel_magnet15_carrier_depth = panel_magnet15_pocket_depth + panel_magnet15_back_wall_x
panel_magnet15_station_y = D / 2 - panel_magnet15_station_inset_y
assert panel_magnet15_width_y == 10.0
assert panel_magnet15_height_z == 5.0
assert panel_magnet15_depth_x == 2.0
assert panel_magnet15_back_wall_x >= 1.6

panel_magnet15_count = 0
for sy in (-1, 1):
    panel = front_panel if sy > 0 else rear_panel
    station_y = sy * panel_magnet15_station_y
    for sx in (-1, 1):
        carrier_x = sx * (frame_outer_x - panel_magnet15_carrier_depth / 2)
        pocket_x = sx * (frame_outer_x - panel_magnet15_pocket_depth / 2)
        for zz in (side_station_z_low, side_station_z_high):
            carrier = Box(panel_magnet15_carrier_depth, panel_magnet15_carrier_width_y, panel_magnet15_carrier_height_z, align=(Align.CENTER, Align.CENTER, Align.CENTER)).moved(Location((carrier_x, station_y, zz)))
            carrier_edges = [e for e in carrier.edges() if e.geom_type == GeomType.LINE]
            if carrier_edges:
                carrier = fillet(carrier_edges, panel_magnet15_carrier_edge_radius)
            pocket = Box(panel_magnet15_pocket_depth, panel_magnet15_pocket_width, panel_magnet15_pocket_height, align=(Align.CENTER, Align.CENTER, Align.CENTER)).moved(Location((pocket_x, station_y, zz)))
            panel = (panel + carrier).clean()
            panel = (panel - pocket).clean()
            panel_magnet15_count += 1
    if sy > 0:
        front_panel = panel
    else:
        rear_panel = panel
assert panel_magnet15_count == int(panel_magnet15_expected)

panel_magnet15_slot_width = panel_magnet15_width_y + panel_magnet15_steel_clearance
panel_magnet15_slot_height = panel_magnet15_height_z + panel_magnet15_steel_clearance
panel_magnet15_slot_depth = panel_magnet15_steel_thickness_x + panel_magnet15_steel_depth_clearance
panel_magnet15_side_count = 0
updated_side_panels = []
for sx, panel in ((-1, left_panel), (1, right_panel)):
    revised = panel
    panel_x = sx * (W / 2 - panel_t / 2)
    inner_face_x = sx * (W / 2 - panel_t)
    pocket_center_x = inner_face_x + sx * panel_magnet15_slot_depth / 2
    for sy in (-1, 1):
        station_y = sy * panel_magnet15_station_y
        for zz in (side_station_z_low, side_station_z_high):
            patch = Box(panel_t, panel_magnet15_side_patch_width_y, panel_magnet15_side_patch_height_z, align=(Align.CENTER, Align.CENTER, Align.CENTER)).moved(Location((panel_x, station_y, zz)))
            strike = Box(panel_magnet15_slot_depth, panel_magnet15_slot_width, panel_magnet15_slot_height, align=(Align.CENTER, Align.CENTER, Align.CENTER)).moved(Location((pocket_center_x, station_y, zz)))
            revised = (revised + patch).clean()
            revised = (revised - strike).clean()
            panel_magnet15_side_count += 1
    updated_side_panels.append(revised)
left_panel, right_panel = updated_side_panels
assert panel_magnet15_side_count == int(panel_magnet15_expected)
assert front_panel.solids().__len__() == 1 and rear_panel.solids().__len__() == 1
assert left_panel.solids().__len__() == 1 and right_panel.solids().__len__() == 1
publish('front_panel', front_panel, 'Front adhesive magnets')
publish('rear_panel', rear_panel, 'Rear adhesive magnets')
publish('left_panel', left_panel, 'Left adhesive strikes')
publish('right_panel', right_panel, 'Right adhesive strikes')
print('MAGNET10_ADHESIVE_PASS: eight 10x5x2 mm adhesive magnet pockets and matching steel strike recesses; no retention screws.')