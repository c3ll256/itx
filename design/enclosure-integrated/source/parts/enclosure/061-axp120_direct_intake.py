import math
# Unified full-coverage honeycomb ventilation on both side panels. This replaces the
# former circular AXP120 intake ring, so both sides read as one continuous hex mesh.
# The cutters are extruded BOTH ways from the panel mid-plane so every cell is a real
# through hole rather than a surface recess.
honeycomb_hex_across_flats = param('honeycomb_hex_across_flats', 17.0)
honeycomb_web_thickness = param('honeycomb_web_thickness', 2.8)
honeycomb_margin_ends_y = param('honeycomb_margin_ends_y', 6.0)
honeycomb_margin_bottom_z = param('honeycomb_margin_bottom_z', 6.0)
honeycomb_margin_top_z = param('honeycomb_margin_top_z', 6.0)
honeycomb_magnet_keepout_radius = param('honeycomb_magnet_keepout_radius', 16.0)
honeycomb_cut_overtravel = param('honeycomb_cut_overtravel', 1.0)
# A shallow recess on the inside of the right panel gives the 67 mm-tall cooler
# envelope a real 2.0 mm fit/air gap while retaining a printable 1.2 mm web depth
# and preserving the unchanged x=76 mm exterior surface.
axp_side_recess_diameter = param('axp_side_recess_diameter', 124.0)
axp_side_recess_depth = param('axp_side_recess_depth', 0.8)
axp_side_recess_overtravel = param('axp_side_recess_overtravel', 0.2)
axp_side_min_remaining_wall = param('axp_side_min_remaining_wall', 1.2)
axp_side_recess_center_y = param('axp_side_recess_center_y', -42.0)
axp_side_recess_center_z = param('axp_side_recess_center_z', 169.0)
# Fixed external-reference result: PCB component face x=5.8 plus the purchased
# Thermalright AXP120-X67 67 mm height gives the outer envelope at x=72.8 mm.
AXP120_ENVELOPE_OUTER_X_MM = 72.8

# Pointy-top hex grid derived from the across-flats dimension.
hex_circumradius = honeycomb_hex_across_flats / math.sqrt(3.0)
hex_pitch_y = honeycomb_hex_across_flats + honeycomb_web_thickness
hex_pitch_z = 1.5 * hex_circumradius + honeycomb_web_thickness * math.sqrt(3.0) / 2.0
hex_half_depth = panel_t / 2 + honeycomb_cut_overtravel

field_y_min = -D / 2 + panel_t + honeycomb_margin_ends_y
field_y_max = D / 2 - panel_t - honeycomb_margin_ends_y
field_z_min = base_t + honeycomb_margin_bottom_z
field_z_max = H - cap_t - honeycomb_margin_top_z

# Magnet strike stations must keep solid material for the steel pockets.
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
# both=True keeps the prism centred on the sketch plane, so after the 90 deg rotation
# it spans the complete panel thickness with overtravel on each face.
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

# Recess only the inside of the right-panel webs over the AXP120 fan field. The
# existing hex holes remain through holes; this operation moves the local solid
# inner face from x=74.0 to x=74.8 without changing the exterior or magnet lands.
assert abs(panel_t - (axp_side_recess_depth + axp_side_min_remaining_wall)) < 0.001
right_panel_inner_x = W / 2.0 - panel_t
axp_recess_cut_depth = axp_side_recess_depth + axp_side_recess_overtravel
axp_recess_center_x = right_panel_inner_x + axp_side_recess_depth - axp_recess_cut_depth / 2.0
axp_recess = Cylinder(
    axp_side_recess_diameter / 2.0,
    axp_recess_cut_depth,
    align=(Align.CENTER, Align.CENTER, Align.CENTER),
).rotate(Axis.Y, 90).moved(Location((
    axp_recess_center_x,
    axp_side_recess_center_y,
    axp_side_recess_center_z,
)))
right_panel = (right_panel - axp_recess).clean()

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

axp_recessed_inner_x = right_panel_inner_x + axp_side_recess_depth
axp_true_side_clearance = axp_recessed_inner_x - AXP120_ENVELOPE_OUTER_X_MM
assert axp_true_side_clearance >= 2.0 - 0.001
assert axp_side_min_remaining_wall >= 1.2
assert honeycomb_web_thickness >= 2.5
assert left_panel.solids().__len__() == 1 and right_panel.solids().__len__() == 1
assert abs(right_panel.bounding_box().max.X - W / 2.0) < 0.001

open_area_per_side = len(hex_centers) * math.sqrt(3.0) / 2.0 * honeycomb_hex_across_flats ** 2
publish('left_panel', left_panel, 'Left full honeycomb')
publish('right_panel', right_panel, 'Right honeycomb with AXP recess')
print(
    f'HONEYCOMB_THROUGH_PASS: {len(hex_centers)} through cells per side, '
    f'{honeycomb_hex_across_flats:.1f} mm across flats, {honeycomb_web_thickness:.1f} mm web, '
    f'pitch {hex_pitch_y:.1f} x {hex_pitch_z:.1f} mm, ~{open_area_per_side:.0f} mm2 open area per side, '
    f'AXP true clearance {axp_true_side_clearance:.1f} mm with {axp_side_min_remaining_wall:.1f} mm local web depth; '
    f'residual {residual_volume:.3f} mm3.'
)
