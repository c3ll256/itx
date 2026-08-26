# Restore both historical and current corner-hole envelopes, then reapply only
# the four current printed-screw-joint-v1 through cuts per panel.
# The user's measured M3 countersunk head reaches 5.8 mm at its widest point.
# Keep the screw joint kit as the geometry authority and offset its exact cut
# rather than hand-modeling a replacement countersink.
top_corner_repair_patch_diameter = param('top_corner_repair_patch_diameter', 12.0)
top_corner_repair_patch_height = param('top_corner_repair_patch_height', cap_t + cap_inner_t)
base_corner_repair_patch_diameter = param('base_corner_repair_patch_diameter', 12.0)
base_corner_repair_patch_height = param('base_corner_repair_patch_height', base_t + foot_height)
corner_repair_legacy_y = param('corner_repair_legacy_y', post_y)
corner_repair_current_y = param('corner_repair_current_y', screw_y)
corner_repair_patch_y = (corner_repair_legacy_y + corner_repair_current_y) / 2
corner_repair_legacy_x = param('corner_repair_legacy_x', post_x)
corner_repair_current_x = param('corner_repair_current_x', screw_x)
corner_repair_patch_x = (corner_repair_legacy_x + corner_repair_current_x) / 2
top_corner_countersink_cut_offset = param('top_corner_countersink_cut_offset', 0.20)
MEASURED_M3_COUNTERSUNK_HEAD_DIAMETER_MM = 5.8  # User caliper measurement, 2026-08-26.
assert 0.10 <= top_corner_countersink_cut_offset <= 0.35

# Fill the complete double-hole footprint in both printable parts.
for sy in (-1, 1):
    for sx in (-1, 1):
        px = sx * corner_repair_patch_x
        py = sy * corner_repair_patch_y
        top_patch = Cylinder(
            top_corner_repair_patch_diameter / 2,
            top_corner_repair_patch_height,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((px, py, H - top_corner_repair_patch_height)))
        base_patch = Cylinder(
            base_corner_repair_patch_diameter / 2,
            base_corner_repair_patch_height,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((px, py, -foot_height)))
        top_cap = (top_cap + top_patch).clean()
        base = (base + base_patch).clean()

# Reuse and offset the exact kit-generated cuts from the active slim corner
# joints. The offset preserves the conical seat while adding print/hardware
# allowance for the measured 5.8 mm head.
active_bottom_corner_joints = slim2_corner_joints[0::2]
active_top_corner_joints = slim2_corner_joints[1::2]
for joint in active_bottom_corner_joints:
    bottom_cut = offset(
        joint.through_cuts[0],
        amount=top_corner_countersink_cut_offset,
        kind=Kind.INTERSECTION,
    )
    base = (base - bottom_cut).clean()
for joint in active_top_corner_joints:
    top_cut = offset(
        joint.through_cuts[0],
        amount=top_corner_countersink_cut_offset,
        kind=Kind.INTERSECTION,
    )
    top_cap = (top_cap - top_cut).clean()

assert len(active_bottom_corner_joints) == 4
assert len(active_top_corner_joints) == 4
assert base.solids().__len__() == 1 and top_cap.solids().__len__() == 1
publish('top_cap', top_cap, 'Measured-head top seats')
publish('base', base, 'Measured-head base holes')
print(
    f'MEASURED_COUNTERSUNK_HEAD_PASS: restored four corner envelopes per panel and '
    f'applied {top_corner_countersink_cut_offset:.2f} mm offsets to the kit-owned cuts '
    f'for the measured Ø{MEASURED_M3_COUNTERSUNK_HEAD_DIAMETER_MM:.1f} mm M3 heads.'
)