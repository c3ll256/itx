import math
# Unified full-coverage honeycomb ventilation on both side panels. The former
# circular AXP120 intake ring and its shallow inner-face recess are retired, so
# both side panels now use the same flat 2 mm section and continuous hex field.
honeycomb_hex_across_flats = param('honeycomb_hex_across_flats', 17.0)
honeycomb_web_thickness = param('honeycomb_web_thickness', 2.8)
honeycomb_margin_ends_y = param('honeycomb_margin_ends_y', 6.0)
honeycomb_margin_bottom_z = param('honeycomb_margin_bottom_z', 6.0)
honeycomb_margin_top_z = param('honeycomb_margin_top_z', 6.0)
honeycomb_magnet_keepout_radius = param('honeycomb_magnet_keepout_radius', 16.0)
honeycomb_cut_overtravel = param('honeycomb_cut_overtravel', 1.0)

# Pointy-top hex grid derived from the across-flats dimension.
hex_circumradius = honeycomb_hex_across_flats / math.sqrt(3.0)
hex_pitch_y = honeycomb_hex_across_flats + honeycomb_web_thickness
hex_pitch_z = 1.5 * hex_circumradius + honeycomb_web_thickness * math.sqrt(3.0) / 2.0
hex_half_depth = panel_t / 2 + honeycomb_cut_overtravel

field_y_min = -D / 2 + panel_t + honeycomb_margin_ends_y
field_y_max = D / 2 - panel_t - honeycomb_margin_ends_y
field_z_min = base_t + honeycomb_margin_bottom_z
field_z_max = H - cap_t - honeycomb_margin_top_z

# Magnet strike stations keep solid material for the shallow steel pockets.
magnet_station_y = D / 2 - panel_magnet15_station_inset_y
keepout_centers = [
    (sy * magnet_station_y, zz)
    for sy in (-1, 1)
    for zz in (side_station_z_low, side_station_z_high)
]

def hex_clears_magnets(y_center, z_center):
    for keep_y, keep_z in keepout_centers:
        if (y_center - keep_y) ** 2 + (z_center - keep_z) ** 2 < honeycomb_magnet_keepout_radius ** 2:
            return False
    return True

hex_centers = []
row = 0
z_center = field_z_min + hex_circumradius
while z_center <= field_z_max - hex_circumradius:
    row_offset = hex_pitch_y / 2.0 if row % 2 else 0.0
    y_center = field_y_min + hex_circumradius + row_offset
    while y_center <= field_y_max - hex_circumradius:
        if hex_clears_magnets(y_center, z_center):
            hex_centers.append((y_center, z_center))
        y_center += hex_pitch_y
    z_center += hex_pitch_z
    row += 1
assert len(hex_centers) > 80

hex_profile = RegularPolygon(hex_circumradius, 6, major_radius=True)
# both=True keeps the prism centred on the sketch plane, so after the 90 degree
# rotation every cutter spans the complete panel thickness with overtravel.
hex_prism = extrude(hex_profile, hex_half_depth, both=True).rotate(Axis.Y, 90)

def panel_honeycomb_cutter(panel_x_center):
    cutter = None
    for y_c, z_c in hex_centers:
        cell = hex_prism.moved(Location((panel_x_center, y_c, z_c)))
        cutter = cell if cutter is None else cutter + cell
    return cutter

left_panel_x = -W / 2 + panel_t / 2
right_panel_x = W / 2 - panel_t / 2
left_panel = (left_panel - panel_honeycomb_cutter(left_panel_x)).clean()
right_panel = (right_panel - panel_honeycomb_cutter(right_panel_x)).clean()

# Each cell must be a genuine through hole: a probe spanning the full panel
# thickness at every hex centre has to find no remaining material.
probe_side = honeycomb_hex_across_flats * 0.5
residual_volume = 0.0
for panel, panel_x in ((left_panel, left_panel_x), (right_panel, right_panel_x)):
    for y_c, z_c in hex_centers:
        probe = Box(
            panel_t, probe_side, probe_side,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((panel_x, y_c, z_c)))
        residual_volume += sum(s.volume for s in (panel & probe))
assert residual_volume < 1.0, f'honeycomb cells are not through: {residual_volume:.2f} mm^3 remain'
assert honeycomb_web_thickness >= 2.5
assert left_panel.solids().__len__() == 1 and right_panel.solids().__len__() == 1
assert abs(left_panel.bounding_box().min.X + W / 2.0) < 0.001
assert abs(right_panel.bounding_box().max.X - W / 2.0) < 0.001

open_area_per_side = len(hex_centers) * math.sqrt(3.0) / 2.0 * honeycomb_hex_across_flats ** 2
publish('left_panel', left_panel, 'Left flat honeycomb')
publish('right_panel', right_panel, 'Right flat honeycomb')
print(
    f'HONEYCOMB_FLAT_PASS: {len(hex_centers)} through cells per side, '
    f'{honeycomb_hex_across_flats:.1f} mm across flats, {honeycomb_web_thickness:.1f} mm web, '
    f'pitch {hex_pitch_y:.1f} x {hex_pitch_z:.1f} mm, ~{open_area_per_side:.0f} mm2 open area per side; '
    f'legacy CPU-side circular recess removed; residual {residual_volume:.3f} mm3.'
)