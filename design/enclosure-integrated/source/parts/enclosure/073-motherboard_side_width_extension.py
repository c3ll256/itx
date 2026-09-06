# Physical print-fit correction: the installed AXP120-X67 sits about 4 mm
# beyond the former motherboard-side inner plane because the earlier CAD fit
# estimate omitted the CPU/socket stack height. Insert exactly 8 mm only on +X,
# preserving every central motherboard, rear-I/O, GPU, SFX, fan, and button datum.
motherboard_side_extension_x = param('motherboard_side_extension_x', 8.0)
motherboard_side_main_split_x = param('motherboard_side_main_split_x', 63.0)
motherboard_side_edge_split_x = param('motherboard_side_edge_split_x', 57.5)
motherboard_side_corner_band_z = param('motherboard_side_corner_band_z', 20.0)
motherboard_side_boolean_overlap = param('motherboard_side_boolean_overlap', 0.02)

assert abs(motherboard_side_extension_x - 8.0) < 0.001
assert motherboard_side_main_split_x > fan80_center_x + FAN80_FRAME_MM / 2.0 - 0.1
assert motherboard_side_edge_split_x > fan120_center_x + fan120_grille_diameter / 2.0
assert motherboard_side_edge_split_x < motherboard_side_main_split_x
assert motherboard_side_corner_band_z > final_corner_height_z

pre_width_bounds = {
    'base': base.bounding_box(),
    'top_cap': top_cap.bounding_box(),
    'front_panel': front_panel.bounding_box(),
    'rear_panel': rear_panel.bounding_box(),
    'left_panel': left_panel.bounding_box(),
    'right_panel': right_panel.bounding_box(),
}


def _stretch_piece_positive_x(piece, split_x, extension_x):
    if piece is None or piece.solids().__len__() == 0:
        return None
    bb = piece.bounding_box()
    if bb.max.X <= split_x + 1e-6:
        return piece
    if bb.min.X >= split_x - 1e-6:
        return piece.moved(Location((extension_x, 0.0, 0.0)))
    split_plane = Plane.YZ.offset(split_x)
    fixed_half = split(piece, bisect_by=split_plane, keep=Keep.BOTTOM)
    moving_half = split(piece, bisect_by=split_plane, keep=Keep.TOP).moved(Location((extension_x, 0.0, 0.0)))
    cross_section = section(piece, section_by=split_plane)
    bridge = extrude(cross_section, amount=extension_x, dir=(1.0, 0.0, 0.0))
    return (fixed_half + bridge + moving_half).clean()


def _stretch_full(shape, split_x):
    stretched = _stretch_piece_positive_x(shape, split_x, motherboard_side_extension_x)
    assert stretched is not None and stretched.solids().__len__() == 1
    return stretched


def _stretch_front_piecewise(shape):
    bb = shape.bounding_box()
    z_low = bb.min.Z + motherboard_side_corner_band_z
    z_high = bb.max.Z - motherboard_side_corner_band_z
    span_x = bb.size.X + 2.0 * motherboard_side_extension_x + 40.0
    span_y = bb.size.Y + 40.0
    overlap = motherboard_side_boolean_overlap
    lower_region = Box(span_x, span_y, z_low - bb.min.Z + overlap, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0.0, bb.center().Y, bb.min.Z)))
    middle_region = Box(span_x, span_y, z_high - z_low + 2.0 * overlap, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0.0, bb.center().Y, z_low - overlap)))
    upper_region = Box(span_x, span_y, bb.max.Z - z_high + overlap, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0.0, bb.center().Y, z_high - overlap)))
    lower_piece = shape & lower_region
    middle_piece = shape & middle_region
    upper_piece = shape & upper_region
    lower_stretched = _stretch_piece_positive_x(lower_piece, motherboard_side_edge_split_x, motherboard_side_extension_x)
    middle_stretched = _stretch_piece_positive_x(middle_piece, motherboard_side_main_split_x, motherboard_side_extension_x)
    upper_stretched = _stretch_piece_positive_x(upper_piece, motherboard_side_edge_split_x, motherboard_side_extension_x)
    result = (lower_stretched + middle_stretched + upper_stretched).clean()
    assert result.solids().__len__() == 1
    return result

base = _stretch_full(base, motherboard_side_edge_split_x)
top_cap = _stretch_full(top_cap, motherboard_side_edge_split_x)
front_panel = _stretch_front_piecewise(front_panel)
# Keep the rear-panel split beyond the complete SFX hole pattern. This avoids
# stretching any SFX hole into a slot, so no local fill or patch is required.
assert motherboard_side_main_split_x > corrected_hole_x + sfx_corrected_hole_diameter / 2.0 + 1.0
rear_panel = _stretch_full(rear_panel, motherboard_side_main_split_x)
right_panel = right_panel.moved(Location((motherboard_side_extension_x, 0.0, 0.0)))
# GPU side remains the fixed datum.
left_panel = left_panel

# Re-drill the final 113 x 51.5 mm SFX pattern after the width operation. This
# block is subtraction-only: there are no hole fills, patches, collars, or local
# material additions. Reopen the existing 12 x 12 mm driver passages as well.
sfx_redrill_points = corrected_points
sfx_redrill_depth_y = rear_panel.bounding_box().size.Y + 4.0
sfx_redrill_center_y = rear_panel.bounding_box().center().Y
sfx_driver_start_y = -D / 2.0 + panel_t + 0.05
sfx_axis_residual = 0.0
sfx_driver_residual = 0.0
for x, z in sfx_redrill_points:
    driver_clearance = Box(
        sfx_corrected_driver_width,
        sfx_corrected_driver_depth,
        sfx_corrected_driver_height,
        align=(Align.CENTER, Align.MIN, Align.CENTER),
    ).moved(Location((x, sfx_driver_start_y, z)))
    round_hole = Cylinder(
        sfx_corrected_hole_diameter / 2.0,
        sfx_redrill_depth_y,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.X, 90).moved(Location((x, sfx_redrill_center_y, z)))
    rear_panel = ((rear_panel - driver_clearance) - round_hole).clean()

    axis_probe = Cylinder(
        sfx_corrected_hole_diameter * 0.35,
        sfx_redrill_depth_y,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.X, 90).moved(Location((x, sfx_redrill_center_y, z)))
    sfx_axis_residual += sum(s.volume for s in (rear_panel & axis_probe).solids())

    driver_probe = Box(
        sfx_corrected_driver_width - 0.6,
        sfx_corrected_driver_depth - 0.6,
        sfx_corrected_driver_height - 0.6,
        align=(Align.CENTER, Align.MIN, Align.CENTER),
    ).moved(Location((x, sfx_driver_start_y + 0.3, z)))
    sfx_driver_residual += sum(s.volume for s in (rear_panel & driver_probe).solids())

assert len(sfx_redrill_points) == 4
assert sfx_axis_residual < 0.01
assert sfx_driver_residual < 0.05
assert rear_panel.solids().__len__() == 1

post_width_bounds = {
    'base': base.bounding_box(),
    'top_cap': top_cap.bounding_box(),
    'front_panel': front_panel.bounding_box(),
    'rear_panel': rear_panel.bounding_box(),
    'left_panel': left_panel.bounding_box(),
    'right_panel': right_panel.bounding_box(),
}
for name in ('base', 'top_cap', 'front_panel', 'rear_panel'):
    assert abs(post_width_bounds[name].min.X - pre_width_bounds[name].min.X) < 0.05
    assert abs((post_width_bounds[name].max.X - pre_width_bounds[name].max.X) - motherboard_side_extension_x) < 0.05
assert abs(post_width_bounds['left_panel'].min.X - pre_width_bounds['left_panel'].min.X) < 0.05
assert abs((post_width_bounds['right_panel'].min.X - pre_width_bounds['right_panel'].min.X) - motherboard_side_extension_x) < 0.05
assert abs((post_width_bounds['right_panel'].max.X - pre_width_bounds['right_panel'].max.X) - motherboard_side_extension_x) < 0.05

# User physical measurement: the installed cooler is approximately 4 mm proud
# of the former panel inner plane. This is evidence explaining the 8 mm width
# correction, not a CAD-derived minimum-clearance requirement.
USER_MEASURED_COOLER_PROTRUSION_MM = 4.0
estimated_physical_remaining_space_mm = motherboard_side_extension_x - USER_MEASURED_COOLER_PROTRUSION_MM
assert estimated_physical_remaining_space_mm > 0.0

publish('base', base, 'Base widened on motherboard side')
publish('top_cap', top_cap, 'Top widened on motherboard side')
publish('front_panel', front_panel, 'Front widened on motherboard side')
publish('rear_panel', rear_panel, 'Rear widened and SFX re-drilled')
publish('left_panel', left_panel, 'Fixed GPU-side panel')
publish('right_panel', right_panel, 'Outward motherboard-side panel')
print(f'MOTHERBOARD_SIDE_WIDTH_PASS: +X side extended exactly {motherboard_side_extension_x:.1f} mm; rear split X={motherboard_side_main_split_x:.1f} mm stays beyond all SFX holes; four Ø{sfx_corrected_hole_diameter:.1f} mm holes re-drilled at {sfx_corrected_horizontal_spacing:.1f} x {sfx_corrected_vertical_spacing:.1f} mm with no fill operations; fixed GPU-side datum retained.')