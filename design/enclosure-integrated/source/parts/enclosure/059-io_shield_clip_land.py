# Standard ATX-family I/O-shield clip land, based on microATX Interface
# Specification v1.2 Figure 4. Keep the exterior aperture simple and flush;
# recess only the inner face so the stamped shield can clip over a compliant edge.
IO_SHIELD_CLIP_MIN_T_MM = 0.94
IO_SHIELD_CLIP_MAX_T_MM = 1.32
IO_SHIELD_CLIP_TARGET_T_MM = 1.00  # near the compliant minimum for easier FDM insertion
IO_SHIELD_KEEP_OUT_MM = 2.54
io_shield_keepout_extra_mm = param('io_shield_keepout_extra_mm', 0.0)
io_shield_recess_overcut_y = param('io_shield_recess_overcut_y', 0.30)
assert io_shield_keepout_extra_mm >= 0.0
assert io_shield_recess_overcut_y >= 0.05
assert IO_SHIELD_CLIP_MIN_T_MM <= IO_SHIELD_CLIP_TARGET_T_MM <= IO_SHIELD_CLIP_MAX_T_MM
assert panel_t > IO_SHIELD_CLIP_TARGET_T_MM

io_clip_keepout = IO_SHIELD_KEEP_OUT_MM + io_shield_keepout_extra_mm
io_clip_outer_w = io_cut_w + 2.0 * io_clip_keepout
io_clip_outer_h = io_cut_h + 2.0 * io_clip_keepout
io_clip_outer_x0 = io_cut_x - io_clip_outer_w / 2.0
io_clip_outer_z0 = io_cut_z0 - io_clip_keepout
rear_outer_face_y = -D / 2.0
rear_inner_face_y = rear_outer_face_y + panel_t
io_clip_recess_y0 = rear_outer_face_y + IO_SHIELD_CLIP_TARGET_T_MM
io_clip_recess_depth_y = rear_inner_face_y - io_clip_recess_y0 + io_shield_recess_overcut_y

assert io_clip_outer_x0 >= -W / 2.0 + 0.01
assert io_clip_outer_x0 + io_clip_outer_w <= W / 2.0 - 0.01
assert io_clip_outer_z0 >= base_t + 0.01
assert io_clip_outer_z0 + io_clip_outer_h <= H - cap_t - 0.01
assert abs(io_cut_w - (io_shield_nominal_short + 2.0 * io_shield_edge_clearance)) < 0.001
assert abs(io_cut_h - (io_shield_nominal_long + 2.0 * io_shield_edge_clearance)) < 0.001
assert io_shield_edge_clearance <= 0.35

io_clip_recess = Box(
    io_clip_outer_w,
    io_clip_recess_depth_y,
    io_clip_outer_h,
    align=(Align.CENTER, Align.MIN, Align.MIN),
).moved(Location((io_cut_x, io_clip_recess_y0, io_clip_outer_z0)))
rear_panel = (rear_panel - io_clip_recess).clean()

assert rear_panel.solids().__len__() == 1
assert abs((io_clip_recess_y0 - rear_outer_face_y) - IO_SHIELD_CLIP_TARGET_T_MM) < 0.001
publish('rear_panel', rear_panel, 'Rear panel I-O clip land')
print(f'IO_SHIELD_CLIP_FIT_PASS: aperture={io_cut_w:.2f} x {io_cut_h:.2f} mm, clip edge={IO_SHIELD_CLIP_TARGET_T_MM:.2f} mm, recess overcut={io_shield_recess_overcut_y:.2f} mm.')