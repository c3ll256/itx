# Remove the stacked legacy corner pads copied by late panel reinforcement, then
# rebuild one compact block at each top/bottom corner on the final front/rear
# inner faces. The original screwjoint-kit axes and engage cuts are preserved.
final_corner_width_x = param('final_corner_width_x', 12.0)
final_corner_depth_y = param('final_corner_depth_y', 12.0)
final_corner_height_z = param('final_corner_height_z', 10.0)
final_corner_panel_overlap = param('final_corner_panel_overlap', 0.50)
final_corner_cleanup_width_x = param('final_corner_cleanup_width_x', 22.0)
final_corner_cleanup_depth_y = param('final_corner_cleanup_depth_y', 22.0)
final_corner_cleanup_height_z = param('final_corner_cleanup_height_z', 20.0)
final_corner_cleanup_skin_inset = param('final_corner_cleanup_skin_inset', 0.35)
final_corner_expected = param('final_corner_expected', 8)

assert final_corner_width_x == 12.0
assert final_corner_depth_y == 12.0
assert final_corner_height_z == 10.0
assert final_corner_panel_overlap > final_corner_cleanup_skin_inset
assert len(slim2_corner_joints) == int(final_corner_expected)

final_corner_outer_x = frame_outer_x
final_corner_center_x_abs = final_corner_outer_x - final_corner_width_x / 2
final_corner_front_y = front_final_inner_y - final_corner_depth_y / 2 + final_corner_panel_overlap
final_corner_rear_y = rear_final_inner_y + final_corner_depth_y / 2 - final_corner_panel_overlap
final_corner_lower_z = base_t
final_corner_upper_z = H - cap_t - cap_inner_t

joint_index = 0
rebuilt_corner_count = 0
for sy in (-1, 1):
    rebuilt = rear_panel if sy < 0 else front_panel
    inner_y = rear_final_inner_y if sy < 0 else front_final_inner_y
    block_y = final_corner_rear_y if sy < 0 else final_corner_front_y
    cleanup_total_depth = final_corner_cleanup_depth_y + final_corner_cleanup_skin_inset
    for sx in (-1, 1):
        cleanup_x = sx * (final_corner_outer_x - final_corner_cleanup_width_x / 2)
        if sy < 0:
            lower_cleanup = Box(
                final_corner_cleanup_width_x,
                cleanup_total_depth,
                final_corner_cleanup_height_z,
                align=(Align.CENTER, Align.MIN, Align.MIN),
            ).moved(Location((cleanup_x, inner_y - final_corner_cleanup_skin_inset, final_corner_lower_z)))
            upper_cleanup = Box(
                final_corner_cleanup_width_x,
                cleanup_total_depth,
                final_corner_cleanup_height_z,
                align=(Align.CENTER, Align.MIN, Align.MAX),
            ).moved(Location((cleanup_x, inner_y - final_corner_cleanup_skin_inset, final_corner_upper_z)))
        else:
            lower_cleanup = Box(
                final_corner_cleanup_width_x,
                cleanup_total_depth,
                final_corner_cleanup_height_z,
                align=(Align.CENTER, Align.MAX, Align.MIN),
            ).moved(Location((cleanup_x, inner_y + final_corner_cleanup_skin_inset, final_corner_lower_z)))
            upper_cleanup = Box(
                final_corner_cleanup_width_x,
                cleanup_total_depth,
                final_corner_cleanup_height_z,
                align=(Align.CENTER, Align.MAX, Align.MAX),
            ).moved(Location((cleanup_x, inner_y + final_corner_cleanup_skin_inset, final_corner_upper_z)))
        rebuilt = (rebuilt - lower_cleanup - upper_cleanup).clean()

        block_x = sx * final_corner_center_x_abs
        lower_block = Box(
            final_corner_width_x,
            final_corner_depth_y,
            final_corner_height_z,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((block_x, block_y, final_corner_lower_z)))
        upper_block = Box(
            final_corner_width_x,
            final_corner_depth_y,
            final_corner_height_z,
            align=(Align.CENTER, Align.CENTER, Align.MAX),
        ).moved(Location((block_x, block_y, final_corner_upper_z)))
        rebuilt = (rebuilt + lower_block + upper_block).clean()

        bottom_joint = slim2_corner_joints[joint_index]
        top_joint = slim2_corner_joints[joint_index + 1]
        joint_index += 2
        rebuilt = (rebuilt - bottom_joint.engage_cuts - top_joint.engage_cuts).clean()
        rebuilt_corner_count += 2

    if sy < 0:
        rear_panel = rebuilt
    else:
        front_panel = rebuilt

assert joint_index == len(slim2_corner_joints)
assert rebuilt_corner_count == int(final_corner_expected)
assert front_panel.solids().__len__() == 1
assert rear_panel.solids().__len__() == 1
publish('front_panel', front_panel, 'Single front corner blocks')
publish('rear_panel', rear_panel, 'Single rear corner blocks')
print(f'FINAL_SINGLE_CORNERS_PASS: {rebuilt_corner_count} compact {final_corner_width_x:.0f}x{final_corner_depth_y:.0f}x{final_corner_height_z:.0f} mm blocks rebuilt once on final skin faces; stacked legacy pads removed.')