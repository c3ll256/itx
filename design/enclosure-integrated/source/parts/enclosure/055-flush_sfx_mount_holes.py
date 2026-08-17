# Keep the rear-panel exterior planar and remove local collars only at the four
# SFX PSU mounting holes. Do not modify the four corner enclosure fasteners.
rear_flush_outer_plane_y = param('rear_flush_outer_plane_y', -D / 2)
rear_flush_outer_trim_depth = param('rear_flush_outer_trim_depth', 2.0)
rear_flush_trim_width = param('rear_flush_trim_width', W + 4.0)
rear_flush_trim_height = param('rear_flush_trim_height', H + 4.0)
rear_outer_trimmer = Box(
    rear_flush_trim_width,
    rear_flush_outer_trim_depth,
    rear_flush_trim_height,
    align=(Align.CENTER, Align.MAX, Align.MIN),
).moved(Location((0, rear_flush_outer_plane_y, -2.0)))
rear_panel = (rear_panel - rear_outer_trimmer).clean()

sfx_flush_zone_diameter = param('sfx_flush_zone_diameter', 16.0)
sfx_flush_inner_plane_y = param('sfx_flush_inner_plane_y', -D / 2 + panel_t)
sfx_flush_inner_cut_depth = param('sfx_flush_inner_cut_depth', 30.0)
sfx_flush_inner_center_y = sfx_flush_inner_plane_y + sfx_flush_inner_cut_depth / 2
for x, z in sfx_mount_points:
    sfx_inner_shaver = Cylinder(
        sfx_flush_zone_diameter / 2,
        sfx_flush_inner_cut_depth,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.X, 90).moved(Location((x, sfx_flush_inner_center_y, z)))
    rear_panel = (rear_panel - sfx_inner_shaver).clean()
assert rear_panel.solids().__len__() == 1
assert len(final_rear_case_joints) == 4
publish('rear_panel', rear_panel, 'Flush PSU mount holes')
print('REAR_CORNERS_PRESERVED: four enclosure corner fasteners untouched; only four SFX mounting-hole collars flattened.')