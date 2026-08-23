# Re-cut the motherboard rear I/O interface after the 5 mm rear skin has
# reached final thickness. Keep the full standard through aperture, but make
# the inner seating rebate shallow: the user requested about 1 mm depth.
# The selected ASUS board uses a pre-mounted I/O shield, so a thin snap-in
# sheet-metal clip land is not required here.
final_io_aperture_overcut_y = param('final_io_aperture_overcut_y', 0.50)
final_io_recess_overcut_y = param('final_io_recess_overcut_y', 0.30)
final_io_recess_depth_y = param('final_io_recess_depth_y', 1.00)
final_io_single_land_expected = param('final_io_single_land_expected', 1)

final_io_outer_y = rear_panel.bounding_box().min.Y
final_io_inner_y = final_io_outer_y + rear_target_thickness
final_io_aperture_depth = rear_target_thickness + 2 * final_io_aperture_overcut_y
final_io_recess_y0 = final_io_inner_y - final_io_recess_depth_y
final_io_recess_cut_depth = final_io_recess_depth_y + final_io_recess_overcut_y
final_io_remaining_wall_y = rear_target_thickness - final_io_recess_depth_y

assert final_io_recess_depth_y > 0.0
assert final_io_recess_depth_y < rear_target_thickness
assert final_io_remaining_wall_y >= 1.2
assert final_io_recess_cut_depth > final_io_recess_depth_y
assert int(final_io_single_land_expected) == 1

# Guarantee one clean rectangular through opening across the complete final skin.
final_io_aperture = Box(
    io_cut_w,
    final_io_aperture_depth,
    io_cut_h,
    align=(Align.CENTER, Align.MIN, Align.MIN),
).moved(Location((io_cut_x, final_io_outer_y - final_io_aperture_overcut_y, io_cut_z0)))
rear_panel = (rear_panel - final_io_aperture).clean()

# Cut only a shallow inner-face rebate within the existing I/O keep-out. This
# preserves the opening location while avoiding the previous deep pocket.
final_io_shallow_recess = Box(
    io_clip_outer_w,
    final_io_recess_cut_depth,
    io_clip_outer_h,
    align=(Align.CENTER, Align.MIN, Align.MIN),
).moved(Location((io_cut_x, final_io_recess_y0, io_clip_outer_z0)))
rear_panel = (rear_panel - final_io_shallow_recess).clean()

assert rear_panel.solids().__len__() == 1
assert abs((final_io_inner_y - final_io_recess_y0) - final_io_recess_depth_y) < 0.001
publish('rear_panel', rear_panel, 'Shallow motherboard I-O rebate')
print(f'FINAL_IO_SHALLOW_REBATE_PASS: {final_io_recess_depth_y:.1f} mm inner rebate around {io_cut_w:.2f}x{io_cut_h:.2f} mm aperture; {final_io_remaining_wall_y:.1f} mm rear skin remains.')