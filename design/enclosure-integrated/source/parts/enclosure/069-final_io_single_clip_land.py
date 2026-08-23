# Normalize the motherboard rear I/O surround after the rear panel has reached
# its final 5 mm thickness. Earlier reinforcement copied a legacy deep rebate
# through several laminated layers; first restore this local zone to one
# continuous slab, then cut one through aperture and one shallow inner rebate.
final_io_aperture_overcut_y = param('final_io_aperture_overcut_y', 0.50)
final_io_recess_overcut_y = param('final_io_recess_overcut_y', 0.30)
final_io_recess_depth_y = param('final_io_recess_depth_y', 1.00)
final_io_single_land_expected = param('final_io_single_land_expected', 1)

# Fixed boolean overlap, not a user-facing fit dimension.
FINAL_IO_RESTORE_MARGIN_XZ_MM = 0.60

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

# Fill the complete legacy laminated rebate zone back to the final exterior and
# interior planes. The small X/Z overlap guarantees a single fused wall while
# leaving both panel faces flush.
final_io_restore_slab = Box(
    io_clip_outer_w + 2.0 * FINAL_IO_RESTORE_MARGIN_XZ_MM,
    rear_target_thickness,
    io_clip_outer_h + 2.0 * FINAL_IO_RESTORE_MARGIN_XZ_MM,
    align=(Align.CENTER, Align.MIN, Align.MIN),
).moved(Location((
    io_cut_x,
    final_io_outer_y,
    io_clip_outer_z0 - FINAL_IO_RESTORE_MARGIN_XZ_MM,
)))
rear_panel = (rear_panel + final_io_restore_slab).clean()

# Re-cut one clean rectangular through opening across the complete final skin.
final_io_aperture = Box(
    io_cut_w,
    final_io_aperture_depth,
    io_cut_h,
    align=(Align.CENTER, Align.MIN, Align.MIN),
).moved(Location((io_cut_x, final_io_outer_y - final_io_aperture_overcut_y, io_cut_z0)))
rear_panel = (rear_panel - final_io_aperture).clean()

# Cut only one shallow inner-face rebate. No exterior rebate or intermediate
# shoulder remains, so the I/O surround has a simple two-level section.
final_io_shallow_recess = Box(
    io_clip_outer_w,
    final_io_recess_cut_depth,
    io_clip_outer_h,
    align=(Align.CENTER, Align.MIN, Align.MIN),
).moved(Location((io_cut_x, final_io_recess_y0, io_clip_outer_z0)))
rear_panel = (rear_panel - final_io_shallow_recess).clean()

# Probe the middle of the left rebate land. It must be one continuous wall from
# the exterior face to the shallow rebate floor, with no legacy intermediate gap.
final_io_probe_x = io_cut_x - io_cut_w / 2.0 - io_clip_keepout / 2.0
final_io_probe_z = io_cut_z0 + io_cut_h / 2.0
final_io_land_probe = rear_panel & Box(
    0.8,
    rear_target_thickness + 0.4,
    0.8,
    align=(Align.CENTER, Align.CENTER, Align.CENTER),
).moved(Location((
    final_io_probe_x,
    final_io_outer_y + rear_target_thickness / 2.0,
    final_io_probe_z,
)))
final_io_probe_thickness_y = final_io_land_probe.bounding_box().size.Y

assert rear_panel.solids().__len__() == 1
assert final_io_land_probe.solids().__len__() == 1
assert abs((final_io_inner_y - final_io_recess_y0) - final_io_recess_depth_y) < 0.001
assert abs(final_io_probe_thickness_y - final_io_remaining_wall_y) < 0.01, f'I/O land thickness={final_io_probe_thickness_y:.3f}'
publish('rear_panel', rear_panel, 'Single shallow motherboard I-O rebate')
print(f'FINAL_IO_SINGLE_REBATE_PASS: legacy laminated pocket restored; one {final_io_recess_depth_y:.1f} mm inner rebate around {io_cut_w:.2f}x{io_cut_h:.2f} mm aperture; continuous land={final_io_probe_thickness_y:.1f} mm.')