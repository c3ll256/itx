# Remove the stacked legacy corner pads copied by late panel reinforcement, then
# rebuild one compact block at each top/bottom corner. Cleanup starts at the
# final inner-panel datum and proceeds only into the enclosure, so it cannot
# create shallow exterior recesses, raised skin strips, or bridge an aperture.
final_corner_width_x = param('final_corner_width_x', 12.0)
final_corner_depth_y = param('final_corner_depth_y', 12.0)
final_corner_height_z = param('final_corner_height_z', 10.0)
final_corner_panel_overlap = param('final_corner_panel_overlap', 0.50)
final_corner_cleanup_width_x = param('final_corner_cleanup_width_x', 22.0)
final_corner_cleanup_depth_y = param('final_corner_cleanup_depth_y', 22.0)
final_corner_cleanup_height_z = param('final_corner_cleanup_height_z', 20.0)
final_corner_cleanup_skin_inset = param('final_corner_cleanup_skin_inset', 0.0)
final_corner_expected = param('final_corner_expected', 8)

assert final_corner_width_x == 12.0
assert final_corner_depth_y == 12.0
assert final_corner_height_z == 10.0
assert final_corner_panel_overlap > final_corner_cleanup_skin_inset
assert final_corner_cleanup_skin_inset == 0.0
assert len(slim2_corner_joints) == int(final_corner_expected)

# Capture the nominal R10 end-panel envelopes before the corner blocks are
# rebuilt. The previous corner pass already established the intended panel
# width, height, and radius; using these pre-block bounds prevents the blocks
# themselves from enlarging the envelope and escaping the rounded outline.
def _final_corner_envelope(shape):
    bb = shape.bounding_box()
    env = Box(
        bb.size.X,
        bb.size.Y,
        bb.size.Z,
        align=(Align.MIN, Align.MIN, Align.MIN),
    ).moved(Location((bb.min.X, bb.min.Y, bb.min.Z)))
    envelope_edges = [e for e in env.edges() if _line_parallel(e, 'y')]
    assert len(envelope_edges) == 4
    return fillet(envelope_edges, case_panel_corner_radius)

front_nominal_corner_envelope = _final_corner_envelope(front_panel)
rear_nominal_corner_envelope = _final_corner_envelope(rear_panel)

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
    nominal_envelope = rear_nominal_corner_envelope if sy < 0 else front_nominal_corner_envelope
    inner_y = rear_final_inner_y if sy < 0 else front_final_inner_y
    block_y = final_corner_rear_y if sy < 0 else final_corner_front_y
    for sx in (-1, 1):
        cleanup_x = sx * (final_corner_outer_x - final_corner_cleanup_width_x / 2)
        if sy < 0:
            lower_cleanup = Box(
                final_corner_cleanup_width_x,
                final_corner_cleanup_depth_y,
                final_corner_cleanup_height_z,
                align=(Align.CENTER, Align.MIN, Align.MIN),
            ).moved(Location((cleanup_x, inner_y, final_corner_lower_z)))
            upper_cleanup = Box(
                final_corner_cleanup_width_x,
                final_corner_cleanup_depth_y,
                final_corner_cleanup_height_z,
                align=(Align.CENTER, Align.MIN, Align.MAX),
            ).moved(Location((cleanup_x, inner_y, final_corner_upper_z)))
        else:
            lower_cleanup = Box(
                final_corner_cleanup_width_x,
                final_corner_cleanup_depth_y,
                final_corner_cleanup_height_z,
                align=(Align.CENTER, Align.MAX, Align.MIN),
            ).moved(Location((cleanup_x, inner_y, final_corner_lower_z)))
            upper_cleanup = Box(
                final_corner_cleanup_width_x,
                final_corner_cleanup_depth_y,
                final_corner_cleanup_height_z,
                align=(Align.CENTER, Align.MAX, Align.MAX),
            ).moved(Location((cleanup_x, inner_y, final_corner_upper_z)))
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

    # Final subtractive-only envelope trim: the fixing blocks now follow the
    # same R10 X/Z corner arcs as the panel instead of leaving square tabs.
    rebuilt = (rebuilt & nominal_envelope).clean()
    assert rebuilt.solids().__len__() == 1
    if sy < 0:
        rear_panel = rebuilt
    else:
        front_panel = rebuilt

assert joint_index == len(slim2_corner_joints)
assert rebuilt_corner_count == int(final_corner_expected)
assert front_panel.solids().__len__() == 1
assert rear_panel.solids().__len__() == 1
publish('front_panel', front_panel, 'R10-trimmed front corner fixing blocks')
publish('rear_panel', rear_panel, 'R10-trimmed rear corner fixing blocks')
print(f'FINAL_SINGLE_CORNERS_PASS: {rebuilt_corner_count} compact {final_corner_width_x:.0f}x{final_corner_depth_y:.0f}x{final_corner_height_z:.0f} mm blocks rebuilt once and clipped to the nominal R{case_panel_corner_radius:.0f} panel envelopes.')