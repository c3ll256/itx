# Retire the four obsolete Y-axis rear-face fastener holes while preserving
# the active Z-axis top/base corner joints and the four SFX mounting holes.
rear_cleanup_patch_width_x = param('rear_cleanup_patch_width_x', 8.0)
rear_cleanup_patch_height_z = param('rear_cleanup_patch_height_z', 8.0)
rear_cleanup_patch_depth_y = param('rear_cleanup_patch_depth_y', panel_t)
rear_cleanup_hole_x = param('rear_cleanup_hole_x', post_x)
rear_cleanup_hole_z_low = param('rear_cleanup_hole_z_low', 30.0)
rear_cleanup_hole_z_high = param('rear_cleanup_hole_z_high', 247.0)
rear_cleanup_top_bridge_min = param('rear_cleanup_top_bridge_min', 2.0)

rear_cleanup_centers = [
    (-rear_cleanup_hole_x, rear_cleanup_hole_z_low),
    ( rear_cleanup_hole_x, rear_cleanup_hole_z_low),
    (-rear_cleanup_hole_x, rear_cleanup_hole_z_high),
    ( rear_cleanup_hole_x, rear_cleanup_hole_z_high),
]
for x, z in rear_cleanup_centers:
    patch = Box(
        rear_cleanup_patch_width_x,
        rear_cleanup_patch_depth_y,
        rear_cleanup_patch_height_z,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location((x, rear_y, z)))
    rear_panel = (rear_panel + patch).clean()

# The standard motherboard I/O opening is shifted down as a whole; its size is
# unchanged. This leaves a continuous top skin rather than a cut-through notch.
rear_cleanup_io_top = mitx_board_z_min + mitx_board_height + io_shield_edge_clearance
rear_cleanup_skin_top = H - cap_t
rear_cleanup_bridge = rear_cleanup_skin_top - rear_cleanup_io_top
assert rear_cleanup_bridge >= rear_cleanup_top_bridge_min - 0.05
assert rear_top_bottom_joint_count == 4
assert len(sfx_mount_points) == 4
assert rear_panel.solids().__len__() == 1
publish('rear_panel', rear_panel, 'Clean rear face with continuous top bridge')
print(f'REAR_SURFACE_CLEANUP_PASS: retired 4 obsolete face holes; top bridge={rear_cleanup_bridge:.2f} mm; active top/base joints=4; SFX holes=4.')