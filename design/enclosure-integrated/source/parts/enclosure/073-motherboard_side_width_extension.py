# Physical print-fit correction: the installed AXP120-X67 sits proud of the
# motherboard-side panel. Insert an 8 mm strip only on +X, preserving every
# central motherboard, rear-I/O, GPU, SFX, fan, and button datum.
motherboard_side_extension_x = param('motherboard_side_extension_x', 8.0)
motherboard_side_main_split_x = param('motherboard_side_main_split_x', 63.0)
motherboard_side_edge_split_x = param('motherboard_side_edge_split_x', 57.5)
motherboard_side_corner_band_z = param('motherboard_side_corner_band_z', 20.0)
motherboard_side_boolean_overlap = param('motherboard_side_boolean_overlap', 0.02)

assert motherboard_side_extension_x > 0.0
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
rear_panel = _stretch_full(rear_panel, motherboard_side_edge_split_x)
right_panel = right_panel.moved(Location((motherboard_side_extension_x, 0.0, 0.0)))
# GPU side remains the fixed datum.
left_panel = left_panel

# The +X width split passes through the two right-hand SFX clearance holes. A
# raw stretch would turn each circular hole into an 8 mm horizontal slot. Fill
# only the stretched void to the right of the split, then recut the unchanged
# 4.2 mm SFX clearance circle at its original chassis datum. These are free
# through-clearances: the screw threads into the purchased PSU, not the print.
SFX_SLOT_REPAIR_X_OVERLAP_MM = 1.5
SFX_SLOT_REPAIR_Z_MARGIN_MM = 1.0
SFX_SLOT_REPAIR_FUSE_OVERLAP_MM = 0.3
SFX_SLOT_REPAIR_PROBE_MARGIN_MM = 0.2
sfx_repair_hole_x = sfx_psu_width / 2.0 - sfx_mount_horizontal_inset
sfx_repair_z_values = (
    base_t + sfx_mount_vertical_inset,
    base_t + sfx_psu_height - sfx_mount_vertical_inset,
)
rear_after_stretch_bb = rear_panel.bounding_box()
sfx_slot_fill_start_x = motherboard_side_edge_split_x - SFX_SLOT_REPAIR_FUSE_OVERLAP_MM
sfx_slot_fill_width_x = motherboard_side_extension_x + SFX_SLOT_REPAIR_X_OVERLAP_MM + SFX_SLOT_REPAIR_FUSE_OVERLAP_MM
sfx_slot_fill_height_z = sfx_final_hole_diameter + SFX_SLOT_REPAIR_Z_MARGIN_MM
sfx_round_recut_depth_y = rear_after_stretch_bb.size.Y + 2.0
sfx_round_recut_center_y = rear_after_stretch_bb.center().Y
for z in sfx_repair_z_values:
    stretched_slot_fill = Box(
        sfx_slot_fill_width_x,
        rear_after_stretch_bb.size.Y,
        sfx_slot_fill_height_z,
        align=(Align.MIN, Align.MIN, Align.CENTER),
    ).moved(Location((
        sfx_slot_fill_start_x,
        rear_after_stretch_bb.min.Y,
        z,
    )))
    rear_panel = (rear_panel + stretched_slot_fill).clean()
    round_recut = Cylinder(
        sfx_final_hole_diameter / 2.0,
        sfx_round_recut_depth_y,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.X, 90).moved(Location((
        sfx_repair_hole_x,
        sfx_round_recut_center_y,
        z,
    )))
    rear_panel = (rear_panel - round_recut).clean()

# Probe the restored axes and the former slot tails. Hole axes must be empty;
# material must be restored to the right of the intended circular edge.
sfx_repair_axis_residual = 0.0
sfx_repair_tail_missing = 0.0
sfx_tail_probe_start_x = sfx_repair_hole_x + sfx_final_hole_diameter / 2.0 + SFX_SLOT_REPAIR_PROBE_MARGIN_MM
sfx_tail_probe_end_x = motherboard_side_edge_split_x + motherboard_side_extension_x - SFX_SLOT_REPAIR_PROBE_MARGIN_MM
sfx_tail_probe_width_x = sfx_tail_probe_end_x - sfx_tail_probe_start_x
assert sfx_tail_probe_width_x > 1.0
for z in sfx_repair_z_values:
    axis_probe = Cylinder(
        sfx_final_hole_diameter * 0.35,
        sfx_round_recut_depth_y,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.X, 90).moved(Location((sfx_repair_hole_x, sfx_round_recut_center_y, z)))
    sfx_repair_axis_residual += sum(s.volume for s in (rear_panel & axis_probe).solids())
    tail_probe = Box(
        sfx_tail_probe_width_x,
        max(0.8, rear_after_stretch_bb.size.Y - 0.4),
        0.8,
        align=(Align.MIN, Align.CENTER, Align.CENTER),
    ).moved(Location((sfx_tail_probe_start_x, sfx_round_recut_center_y, z)))
    sfx_repair_tail_missing += sum(s.volume for s in (tail_probe - rear_panel).solids())
assert sfx_repair_axis_residual < 0.01
assert sfx_repair_tail_missing < 0.05
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
    assert abs(post_width_bounds[name].max.X - (pre_width_bounds[name].max.X + motherboard_side_extension_x)) < 0.05
assert abs(post_width_bounds['left_panel'].min.X - pre_width_bounds['left_panel'].min.X) < 0.05
assert abs(post_width_bounds['right_panel'].min.X - (pre_width_bounds['right_panel'].min.X + motherboard_side_extension_x)) < 0.05
assert abs(post_width_bounds['right_panel'].max.X - (pre_width_bounds['right_panel'].max.X + motherboard_side_extension_x)) < 0.05

# The reference cooler's outer fan face is X=73.3 mm in the current hardware
# datum. The moved panel inner face must now leave at least 8 mm of real space.
AXP120_OUTER_FAN_FACE_X_MM = 73.3
motherboard_side_inner_face_x = post_width_bounds['right_panel'].min.X
motherboard_side_cooler_gap_x = motherboard_side_inner_face_x - AXP120_OUTER_FAN_FACE_X_MM
assert motherboard_side_cooler_gap_x >= 8.0

publish('base', base, 'Base widened on motherboard side')
publish('top_cap', top_cap, 'Top widened on motherboard side')
publish('front_panel', front_panel, 'Front widened on motherboard side')
publish('rear_panel', rear_panel, 'Rear widened with round SFX holes')
publish('left_panel', left_panel, 'Fixed GPU-side panel')
publish('right_panel', right_panel, 'Outward motherboard-side panel')
print(f'MOTHERBOARD_SIDE_WIDTH_PASS: +X side extended {motherboard_side_extension_x:.1f} mm; base outer X={post_width_bounds["base"].min.X:.1f}..{post_width_bounds["base"].max.X:.1f} mm; cooler-to-panel inner gap={motherboard_side_cooler_gap_x:.1f} mm; two stretched SFX slots restored to round {sfx_final_hole_diameter:.1f} mm holes; fixed GPU-side datum retained.')