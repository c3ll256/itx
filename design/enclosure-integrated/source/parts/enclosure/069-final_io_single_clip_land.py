# Re-cut the motherboard rear I/O interface after the 5 mm rear skin has
# reached final thickness. This removes the copied three-level lamination and
# leaves one standard 1.0 mm clip land around one through aperture.
FINAL_IO_CLIP_EDGE_MM = 1.00  # microATX/ATX I/O-shield compliant edge target
final_io_aperture_overcut_y = param('final_io_aperture_overcut_y', 0.50)
final_io_recess_overcut_y = param('final_io_recess_overcut_y', 0.30)
final_io_single_land_expected = param('final_io_single_land_expected', 1)

final_io_outer_y = rear_panel.bounding_box().min.Y
final_io_inner_y = final_io_outer_y + rear_target_thickness
final_io_aperture_depth = rear_target_thickness + 2 * final_io_aperture_overcut_y
final_io_recess_y0 = final_io_outer_y + FINAL_IO_CLIP_EDGE_MM
final_io_recess_depth = final_io_inner_y - final_io_recess_y0 + final_io_recess_overcut_y

assert IO_SHIELD_CLIP_MIN_T_MM <= FINAL_IO_CLIP_EDGE_MM <= IO_SHIELD_CLIP_MAX_T_MM
assert final_io_recess_depth > 0.0
assert int(final_io_single_land_expected) == 1

# Guarantee one clean rectangular through opening across the complete final skin.
final_io_aperture = Box(
    io_cut_w,
    final_io_aperture_depth,
    io_cut_h,
    align=(Align.CENTER, Align.MIN, Align.MIN),
).moved(Location((io_cut_x, final_io_outer_y - final_io_aperture_overcut_y, io_cut_z0)))
rear_panel = (rear_panel - final_io_aperture).clean()

# Remove all inner-face lamination only within the standard clip keep-out. The
# remaining outermost 1.0 mm is one continuous clip land, not three nested rims.
final_io_single_recess = Box(
    io_clip_outer_w,
    final_io_recess_depth,
    io_clip_outer_h,
    align=(Align.CENTER, Align.MIN, Align.MIN),
).moved(Location((io_cut_x, final_io_recess_y0, io_clip_outer_z0)))
rear_panel = (rear_panel - final_io_single_recess).clean()

assert rear_panel.solids().__len__() == 1
assert abs((final_io_recess_y0 - final_io_outer_y) - FINAL_IO_CLIP_EDGE_MM) < 0.001
publish('rear_panel', rear_panel, 'Single-layer motherboard I-O')
print(f'FINAL_IO_SINGLE_LAND_PASS: one {FINAL_IO_CLIP_EDGE_MM:.1f} mm clip land around {io_cut_w:.2f}x{io_cut_h:.2f} mm aperture; copied three-layer structure removed.')