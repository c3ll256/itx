# Re-cut only the end-panel adhesive magnet interfaces after late geometry.
# Side-panel steel recesses are intentionally deferred to the one final strike
# operation after honeycomb generation; this cell never modifies side panels.
connection_cleanup_extra_depth = param('connection_cleanup_extra_depth', 0.15)
connection_cleanup_face_trim = param('connection_cleanup_face_trim', 0.35)

# Front and rear vertical 10 x 5 x 2 mm magnet pockets: restore one flat floor
# while keeping the opening exactly at the side-panel inner face.
cleaned_end_panels = []
for sy, panel in ((1, front_panel), (-1, rear_panel)):
    cleaned = panel
    station_y = sy * panel_magnet15_station_y
    for sx in (-1, 1):
        pocket_x = sx * panel_magnet15_pocket_center_x_abs
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

# Trim only thin exterior lips on the end panels. The side-panel exterior and
# full original outline remain untouched.
front_trim = Box(W + 4, connection_cleanup_face_trim, H + 4, align=(Align.CENTER, Align.MIN, Align.MIN)).moved(Location((0, D / 2, -2)))
rear_trim = Box(W + 4, connection_cleanup_face_trim, H + 4, align=(Align.CENTER, Align.MAX, Align.MIN)).moved(Location((0, -D / 2, -2)))
front_panel = (front_panel - front_trim).clean()
rear_panel = (rear_panel - rear_trim).clean()

assert all(p.solids().__len__() == 1 for p in (front_panel, rear_panel, left_panel, right_panel))
publish('front_panel', front_panel, 'Clean front magnet slots')
publish('rear_panel', rear_panel, 'Clean rear magnet slots')
publish('left_panel', left_panel, 'Unmodified left honeycomb panel')
publish('right_panel', right_panel, 'Unmodified right honeycomb panel')
print('CONNECTION_STEPS_CLEAN: end-panel adhesive pockets re-cut; all side-panel cleanup, refill, and exterior trimming retired.')