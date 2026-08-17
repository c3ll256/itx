# Final print-axis and assembled-depth audit for the corrected flat front.
# The GPU body now ends inside the enclosure, so no external GPU nose bulge
# contributes to the assembled depth.
print_margin_case_width = param('case_width', W)
print_margin_case_depth = param('case_depth', D)
print_margin_case_height = param('case_height', H)
print_margin_base_thickness = param('base_thickness', base_t)
print_margin_top_outer_thickness = param('top_cap_thickness', cap_t)
print_margin_top_inner_thickness = param('top_cap_inner_thickness', cap_inner_t)
p1s_front_edge_recess = param('p1s_front_edge_recess', 1.5)
p1s_min_edge_margin = param('p1s_min_edge_margin', 1.0)
p1s_axis_limit = param('p1s_axis_limit', 256.0)

p1s_trim_depth = D - p1s_front_edge_recess
p1s_trim_center_y = -p1s_front_edge_recess / 2
p1s_trim_mask = Box(
    W + 4, p1s_trim_depth, H + 20,
    align=(Align.CENTER, Align.CENTER, Align.CENTER),
).moved(Location((0, p1s_trim_center_y, H / 2)))
base = (base & p1s_trim_mask).clean()
top_cap = (top_cap & p1s_trim_mask).clean()

base_bb = base.bounding_box()
top_bb = top_cap.bounding_box()
left_bb = left_panel.bounding_box()
right_bb = right_panel.bounding_box()
front_bb = front_panel.bounding_box()
rear_bb = rear_panel.bounding_box()
base_front_overlap = base_bb.max.Y - front_bb.min.Y
top_front_overlap = top_bb.max.Y - front_bb.min.Y
assembled_depth = (
    max(front_bb.max.Y, base_bb.max.Y, top_bb.max.Y)
    - min(rear_bb.min.Y, base_bb.min.Y, top_bb.min.Y)
)

assert base.solids().__len__() == 1 and top_cap.solids().__len__() == 1
for bb in (base_bb, top_bb, left_bb, right_bb, front_bb, rear_bb):
    assert max(bb.size.X, bb.size.Y, bb.size.Z) <= p1s_axis_limit + 0.001
assert base_bb.size.Y <= D - p1s_min_edge_margin
assert top_bb.size.Y <= D - p1s_min_edge_margin
assert abs(base_bb.min.Y + D / 2) < 0.001
assert abs(top_bb.min.Y + D / 2) < 0.001
assert base_front_overlap >= 0.4 and top_front_overlap >= 0.4
assert abs(front_bb.max.Y - D / 2) < 0.01
assert abs(assembled_depth - D) < 0.01

publish('base', base, 'Base with print margin')
publish('top_cap', top_cap, 'Top with print margin')
print(
    f'PRINT_AXIS_FLAT_FRONT_PASS: base={base_bb.size.Y:.1f}, top={top_bb.size.Y:.1f}, '
    f'side={left_bb.size.Y:.1f}, max axis <= {p1s_axis_limit:.0f} mm; '
    f'assembled depth={assembled_depth:.1f} mm with no GPU bulge.'
)