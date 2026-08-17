# Re-cut every magnet interface after all screw-joint bosses and repair patches
# have replayed. This removes the visible stepped lips while preserving the
# carrier back walls, centered screw engagement, and steel-strike pockets.
connection_cleanup_extra_depth = param('connection_cleanup_extra_depth', 0.15)
connection_cleanup_face_trim = param('connection_cleanup_face_trim', 0.35)

# Front and rear 15 x 10 x 4 mm magnet pockets: restore one flat pocket floor.
cleaned_end_panels = []
for sy, panel in ((1, front_panel), (-1, rear_panel)):
    cleaned = panel
    station_y = sy * panel_magnet15_station_y
    for sx in (-1, 1):
        pocket_x = sx * (frame_outer_x - panel_magnet15_pocket_depth / 2)
        for zz in (side_station_z_low, side_station_z_high):
            recut = Box(
                panel_magnet15_pocket_depth + connection_cleanup_extra_depth,
                panel_magnet15_pocket_width,
                panel_magnet15_pocket_height,
                align=(Align.CENTER, Align.CENTER, Align.CENTER),
            ).moved(Location((pocket_x - sx * connection_cleanup_extra_depth / 2, station_y, zz)))
            cleaned = (cleaned - recut).clean()
    cleaned_end_panels.append(cleaned)
front_panel, rear_panel = cleaned_end_panels

# Side-panel steel strike pockets: remove patch lips and restore flat recesses.
cleaned_side_panels = []
for sx, panel in ((-1, left_panel), (1, right_panel)):
    cleaned = panel
    inner_face_x = sx * (W / 2 - panel_t)
    pocket_center_x = inner_face_x + sx * (panel_magnet15_slot_depth + connection_cleanup_extra_depth) / 2
    for sy in (-1, 1):
        station_y = sy * panel_magnet15_station_y
        for zz in (side_station_z_low, side_station_z_high):
            recut = Box(
                panel_magnet15_slot_depth + connection_cleanup_extra_depth,
                panel_magnet15_slot_width,
                panel_magnet15_slot_height,
                align=(Align.CENTER, Align.CENTER, Align.CENTER),
            ).moved(Location((pocket_center_x, station_y, zz)))
            cleaned = (cleaned - recut).clean()
    cleaned_side_panels.append(cleaned)
left_panel, right_panel = cleaned_side_panels

# Trim only thin exterior repair lips back to the nominal six panel planes.
front_trim = Box(W + 4, connection_cleanup_face_trim, H + 4, align=(Align.CENTER, Align.MIN, Align.MIN)).moved(Location((0, D / 2, -2)))
rear_trim = Box(W + 4, connection_cleanup_face_trim, H + 4, align=(Align.CENTER, Align.MAX, Align.MIN)).moved(Location((0, -D / 2, -2)))
left_trim = Box(connection_cleanup_face_trim, D + 4, H + 4, align=(Align.MAX, Align.CENTER, Align.MIN)).moved(Location((-W / 2, 0, -2)))
right_trim = Box(connection_cleanup_face_trim, D + 4, H + 4, align=(Align.MIN, Align.CENTER, Align.MIN)).moved(Location((W / 2, 0, -2)))
front_panel = (front_panel - front_trim).clean()
rear_panel = (rear_panel - rear_trim).clean()
left_panel = (left_panel - left_trim).clean()
right_panel = (right_panel - right_trim).clean()

assert all(p.solids().__len__() == 1 for p in (front_panel, rear_panel, left_panel, right_panel))
publish('front_panel', front_panel, 'Clean front connections')
publish('rear_panel', rear_panel, 'Clean rear connections')
publish('left_panel', left_panel, 'Clean left connections')
publish('right_panel', right_panel, 'Clean right connections')
print('CONNECTION_STEPS_CLEAN: eight magnet pockets, eight strike recesses, and four exterior panel faces re-cut without changing the centered screw interfaces.')