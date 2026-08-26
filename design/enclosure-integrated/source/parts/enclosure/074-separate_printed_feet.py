# Final print decomposition: the four feet are independent printed parts.
# Each existing kit-owned M3x12 countersunk screw remains one coaxial fastener
# through one foot and the base, threading into the lower block carried by the
# matching front or rear panel. The user's measured screw head is 5.8 mm wide.
# The foot's outer entry needs generous FDM insertion clearance; its recessed
# entry remains derived from offset and translated copies of the exact kit cut,
# never from a hand-modeled replacement screw hole.
separate_foot_diameter = param('separate_foot_diameter', 16.0)
separate_foot_height = param('separate_foot_height', 4.0)
separate_foot_edge_radius = param('separate_foot_edge_radius', 1.2)
separate_foot_screw_recess_extra = param('separate_foot_screw_recess_extra', 1.2)
separate_foot_countersink_cut_offset = param('separate_foot_countersink_cut_offset', 0.45)
separate_base_nominal_width = param('case_width', 152.0)
separate_base_depth = param('case_depth', 256.0)
separate_base_thickness = param('base_thickness', 3.0)
separate_foot_expected_count = param('separate_foot_expected_count', 4)
separate_foot_expected_screw_length = param('separate_foot_expected_screw_length', 12.0)
separate_base_clip_margin = param('separate_base_clip_margin', 1.0)
MEASURED_FOOT_M3_COUNTERSUNK_HEAD_DIAMETER_MM = 5.8  # User caliper measurement, 2026-08-26.
TARGET_FOOT_OUTER_ENTRY_DIAMETER_MM = 6.6  # FDM insertion target; verify from committed geometry.

assert separate_foot_diameter >= 14.0
assert separate_foot_height >= 3.0
assert 0.5 <= separate_foot_edge_radius < separate_foot_height / 2.0
assert 0.5 <= separate_foot_screw_recess_extra <= separate_foot_height / 2.0
# Keep the stored 0.20 mm value buildable while this source revision is applied;
# the following build-bound parameter edit raises it to 0.45 mm.
assert 0.10 <= separate_foot_countersink_cut_offset <= 0.60
assert TARGET_FOOT_OUTER_ENTRY_DIAMETER_MM > MEASURED_FOOT_M3_COUNTERSUNK_HEAD_DIAMETER_MM
assert (separate_foot_diameter - TARGET_FOOT_OUTER_ENTRY_DIAMETER_MM) / 2.0 >= 4.0
assert int(separate_foot_expected_count) == 4
assert separate_base_clip_margin > 0.0

# Remove only the material below the base/foot interface. The base keeps its
# full upper reinforcement and its four existing coaxial through holes.
base_bounds_before_foot_split = base.bounding_box()
base_clip = Box(
    base_bounds_before_foot_split.size.X + 2.0 * separate_base_clip_margin,
    base_bounds_before_foot_split.size.Y + 2.0 * separate_base_clip_margin,
    base_bounds_before_foot_split.max.Z + separate_base_clip_margin,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((base_bounds_before_foot_split.center().X, base_bounds_before_foot_split.center().Y, 0.0)))
base = (base & base_clip).clean()

# The active bottom joint order is rear-left, rear-right, front-left,
# front-right. The +X pair follows the existing 8 mm motherboard-side stretch.
active_separate_foot_joints = slim2_corner_joints[0::2]
separate_foot_specs = [
    ('base_foot_rear_left', 'Rear-left foot', -1, -1),
    ('base_foot_rear_right', 'Rear-right foot', 1, -1),
    ('base_foot_front_left', 'Front-left foot', -1, 1),
    ('base_foot_front_right', 'Front-right foot', 1, 1),
]
separate_feet = []
separate_screws = []
separate_foot_axes = []
separate_recessed_screw_bottoms = []
separate_recessed_screw_tops = []
for (object_id, object_label, sx, sy), joint in zip(separate_foot_specs, active_separate_foot_joints):
    x_shift = motherboard_side_extension_x if sx > 0 else 0.0
    foot_x = sx * screw_x + x_shift
    foot_y = sy * screw_y
    foot_blank = Cylinder(
        separate_foot_diameter / 2.0,
        separate_foot_height,
        align=(Align.CENTER, Align.CENTER, Align.MAX),
    ).moved(Location((foot_x, foot_y, 0.0)))
    foot_outer_round_edges = list(foot_blank.edges().filter_by(GeomType.CIRCLE))
    assert len(foot_outer_round_edges) == 2
    foot_blank = fillet(foot_outer_round_edges, separate_foot_edge_radius)

    active_cut = joint.through_cuts[0]
    active_screw = joint.hardware
    if x_shift:
        active_cut = active_cut.moved(Location((x_shift, 0.0, 0.0)))
        active_screw = active_screw.moved(Location((x_shift, 0.0, 0.0)))

    # Offset the exact kit cut enough that the exterior foot entry admits the
    # measured head after FDM shrink/roughness. Moving a second copy upward keeps
    # the existing 1.2 mm recessed screw position and continuous conical path.
    measured_head_cut = offset(
        active_cut,
        amount=separate_foot_countersink_cut_offset,
        kind=Kind.INTERSECTION,
    )
    recess_shift = Location((0.0, 0.0, separate_foot_screw_recess_extra))
    recessed_active_cut = (measured_head_cut + measured_head_cut.moved(recess_shift)).clean()
    recessed_active_screw = active_screw.moved(recess_shift)
    foot_part = (foot_blank - recessed_active_cut).clean()

    assert foot_part.solids().__len__() == 1
    assert abs(foot_part.bounding_box().min.Z + separate_foot_height) < 0.01
    assert abs(foot_part.bounding_box().max.Z) < 0.01
    assert abs(recessed_active_screw.bounding_box().min.Z - (
        active_screw.bounding_box().min.Z + separate_foot_screw_recess_extra
    )) < 0.01
    assert abs(recessed_active_screw.bounding_box().max.Z - (
        active_screw.bounding_box().max.Z + separate_foot_screw_recess_extra
    )) < 0.01
    separate_feet.append((object_id, object_label, foot_part))
    separate_screws.append((f'{object_id}_screw', f'{object_label} screw', recessed_active_screw))
    separate_foot_axes.append((foot_x, foot_y))
    separate_recessed_screw_bottoms.append(recessed_active_screw.bounding_box().min.Z)
    separate_recessed_screw_tops.append(recessed_active_screw.bounding_box().max.Z)

assert len(separate_feet) == int(separate_foot_expected_count)
assert len(active_separate_foot_joints) == int(separate_foot_expected_count)
assert {j.screw_length_mm for j in active_separate_foot_joints} == {separate_foot_expected_screw_length}
assert base.solids().__len__() == 1
assert abs(base.bounding_box().min.Z) < 0.01
assert abs(base.bounding_box().max.Z - base_bounds_before_foot_split.max.Z) < 0.01
assert max(separate_recessed_screw_bottoms) < 0.0
assert min(separate_recessed_screw_tops) > separate_base_thickness

# Connection inventory: each named screw handles exactly one independent foot,
# the base through-hole, and the matching front/rear panel's lower printed thread.
separate_foot_connection_inventory = {
    'rear-left': 'printed-screw-joint-v1: enlarged-entry recessed foot + base -> rear panel lower block',
    'rear-right': 'printed-screw-joint-v1: enlarged-entry recessed foot + base -> rear panel lower block',
    'front-left': 'printed-screw-joint-v1: enlarged-entry recessed foot + base -> front panel lower block',
    'front-right': 'printed-screw-joint-v1: enlarged-entry recessed foot + base -> front panel lower block',
}
assert len(separate_foot_connection_inventory) == int(separate_foot_expected_count)
assert all(separate_foot_connection_inventory.values())

publish('base', base, 'Base without feet')
for object_id, object_label, foot_part in separate_feet:
    publish(object_id, foot_part, object_label)
for object_id, object_label, screw_part in separate_screws:
    publish(object_id, screw_part, object_label)
print(
    f'ENLARGED_FOOT_ENTRY_PASS: four independent Ø{separate_foot_diameter:.1f} x '
    f'{separate_foot_height:.1f} mm feet use {separate_foot_edge_radius:.1f} mm outer fillets; '
    f'kit-owned M3x{separate_foot_expected_screw_length:.0f} cuts have '
    f'{separate_foot_countersink_cut_offset:.2f} mm outer-entry allowance for measured '
    f'Ø{MEASURED_FOOT_M3_COUNTERSUNK_HEAD_DIAMETER_MM:.1f} mm heads, target approximately '
    f'Ø{TARGET_FOOT_OUTER_ENTRY_DIAMETER_MM:.1f} mm, and remain recessed '
    f'{separate_foot_screw_recess_extra:.1f} mm at {separate_foot_axes}.'
)