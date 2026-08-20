# User decision: the lower-front Mini-ITX support standing on the base is
# removed. Its floor area is now used by the front bottom intake fan, and the
# board keeps its rear-lower point plus the two upper points.
# Only the retired underside screw path has to be closed again.
retired_front_mb_patch_diameter = param('retired_front_mb_patch_diameter', 11.0)
retired_front_mb_patch_overlap_z = param('retired_front_mb_patch_overlap_z', 0.2)
retired_front_mb_expected_mounts = param('retired_front_mb_expected_mounts', 0)

def solid_volume(shape):
    if shape is None:
        return 0.0
    return sum(s.volume for s in shape.solids())

retired_front_mb_patch = Cylinder(
    retired_front_mb_patch_diameter / 2,
    base_t + retired_front_mb_patch_overlap_z,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((front_floor_anchor_x, lower_mount_ys[1], 0.0)))
base = (base + retired_front_mb_patch).clean()
base = (base & Box(
    W + 10.0, D + 10.0, base_t + foot_height,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((0, 0, -foot_height)))).clean()

# The retired screw axis must be solid again in the finished base.
retired_front_mb_probe = Cylinder(
    2.4, base_t,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((front_floor_anchor_x, lower_mount_ys[1], 0.0)))
retired_front_mb_void = retired_front_mb_probe.volume - solid_volume(base & retired_front_mb_probe)

mb_mount_inventory = {
    'rear-lower': 'rear-panel integrated standoff, printed-screw-joint-v1',
    'upper-rear': 'top-panel fused arm, printed-screw-joint-v1',
    'upper-front': 'top-panel fused arm, printed-screw-joint-v1',
}
assert int(retired_front_mb_expected_mounts) == 0
assert base.solids().__len__() == 1
assert retired_front_mb_void < 1.0
assert abs(base.bounding_box().max.Z - base_t) < 0.01
assert len(mb_mount_inventory) == 3 and all(mb_mount_inventory.values())
publish('base', base, 'Base without front MB post')
print(
    f'FRONT_MB_POST_REMOVED: lower-front Mini-ITX support deleted; underside screw path at '
    f'x={front_floor_anchor_x:.1f}, y={lower_mount_ys[1]:.1f} closed with residual void '
    f'{retired_front_mb_void:.3f} mm^3; three board mounting points remain.'
)
