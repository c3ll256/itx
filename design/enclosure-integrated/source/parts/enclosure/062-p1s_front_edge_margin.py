# Final print-axis and assembled-depth audit for the corrected flat front.
# The top and base plates now run the full case depth: 256 mm equals the P1S
# build-area limit exactly, so no front-edge recess is taken. Only the real
# machine limit is asserted; no extra self-imposed margin is applied.
print_margin_case_width = param('case_width', W)
print_margin_case_depth = param('case_depth', D)
print_margin_case_height = param('case_height', H)
print_margin_base_thickness = param('base_thickness', base_t)
print_margin_top_outer_thickness = param('top_cap_thickness', cap_t)
print_margin_top_inner_thickness = param('top_cap_inner_thickness', cap_inner_t)
p1s_axis_limit = param('p1s_axis_limit', 256.0)

base_bb = base.bounding_box()
top_bb = top_cap.bounding_box()
left_bb = left_panel.bounding_box()
right_bb = right_panel.bounding_box()
front_bb = front_panel.bounding_box()
rear_bb = rear_panel.bounding_box()

assembled_depth = (
    max(front_bb.max.Y, base_bb.max.Y, top_bb.max.Y)
    - min(rear_bb.min.Y, base_bb.min.Y, top_bb.min.Y)
)

assert base.solids().__len__() == 1 and top_cap.solids().__len__() == 1
# Every printable panel must still fit the real P1S build area on all three axes.
for bb in (base_bb, top_bb, left_bb, right_bb, front_bb, rear_bb):
    assert max(bb.size.X, bb.size.Y, bb.size.Z) <= p1s_axis_limit + 0.001

# Top and base now span the complete case depth and sit flush front and rear.
assert abs(base_bb.size.Y - D) < 0.01
assert abs(top_bb.size.Y - D) < 0.01
assert abs(base_bb.min.Y + D / 2) < 0.01 and abs(base_bb.max.Y - D / 2) < 0.01
assert abs(top_bb.min.Y + D / 2) < 0.01 and abs(top_bb.max.Y - D / 2) < 0.01
assert abs(front_bb.max.Y - D / 2) < 0.01
assert abs(assembled_depth - D) < 0.01

publish('base', base, 'Full-depth base')
publish('top_cap', top_cap, 'Full-depth top')
print(
    f'FULL_DEPTH_PLATES_PASS: base={base_bb.size.Y:.1f}, top={top_bb.size.Y:.1f}, '
    f'side={left_bb.size.Y:.1f} mm; max printed axis {p1s_axis_limit:.0f} mm; '
    f'assembled depth={assembled_depth:.1f} mm, top and base flush at both ends.'
)