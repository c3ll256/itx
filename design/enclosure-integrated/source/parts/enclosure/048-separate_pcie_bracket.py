# Recreate the former fused dual-slot shelf as a support-free printable L bracket.
# Two GPU bracket screws retain the card ears; two rear-facing M3 screws retain
# this separate part to solid lands on the rear panel.
# The shelf footprint comes from the rear-panel aperture cell, so it follows the
# card position and stays inside the case outline instead of being set by hand.
pcie_bracket_shelf_depth_y = param('pcie_bracket_shelf_depth_y', flange_d)
pcie_bracket_shelf_thickness_z = param('pcie_bracket_shelf_thickness_z', flange_t)
pcie_bracket_lift_z = param('pcie_bracket_lift_z', 2.0)
pcie_bracket_tab_width_x = param('pcie_bracket_tab_width_x', 10.0)
pcie_bracket_tab_min_width_x = param('pcie_bracket_tab_min_width_x', 6.0)
pcie_bracket_tab_depth_y = param('pcie_bracket_tab_depth_y', 3.2)
pcie_bracket_tab_height_z = param('pcie_bracket_tab_height_z', 16.0)
pcie_bracket_tab_opening_gap_x = param('pcie_bracket_tab_opening_gap_x', 1.0)
pcie_bracket_rear_screw_z_offset = param('pcie_bracket_rear_screw_z_offset', 10.0)
pcie_bracket_rear_engagement = param('pcie_bracket_rear_engagement', 4.2)
pcie_bracket_gpu_engagement = param('pcie_bracket_gpu_engagement', 2.4)
pcie_bracket_gpu_ear_thickness = param('pcie_bracket_gpu_ear_thickness', bracket_t)
pcie_bracket_expected_gpu_screws = param('pcie_bracket_expected_gpu_screws', 2)
pcie_bracket_expected_rear_screws = param('pcie_bracket_expected_rear_screws', 2)
pcie_bracket_outline_margin_x = param('pcie_bracket_outline_margin_x', 3.0)
# User-measured correction from the rear exterior view: +X is screen-right and
# negative Y moves rearward/outside. Both GPU-ear axes move together so the
# standard 20.32 mm slot pitch is preserved.
pcie_bracket_gpu_axis_right_x = param('pcie_bracket_gpu_axis_right_x', 3.6)
pcie_bracket_gpu_axis_outward_y = param('pcie_bracket_gpu_axis_outward_y', 3.6)

pcie_bracket_width_x = flange_w
pcie_bracket_base_z = flange_z + pcie_bracket_lift_z
# Extend only the rear/outboard edge by the same amount as the Y correction so
# the shifted M3 holes retain the original edge land instead of breaking open.
pcie_bracket_effective_shelf_depth_y = pcie_bracket_shelf_depth_y + pcie_bracket_gpu_axis_outward_y
pcie_bracket_effective_shelf_y = flange_y - pcie_bracket_gpu_axis_outward_y / 2.0

pcie_shelf = Box(
    pcie_bracket_width_x,
    pcie_bracket_effective_shelf_depth_y,
    pcie_bracket_shelf_thickness_z,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((pcie_shelf_center_x, pcie_bracket_effective_shelf_y, pcie_bracket_base_z)))

# The outboard land is narrower than the inboard one at this card position, so
# each retention tab is sized to the land it actually stands on.
pcie_tab_y = -D/2 - pcie_bracket_tab_depth_y/2
pcie_tab_specs = []
for pcie_tab_edge_x, pcie_tab_aperture_edge_x in (
    (pcie_shelf_x_min, pcie_aperture_x_min),
    (pcie_shelf_x_max, pcie_aperture_x_max),
):
    pcie_tab_land = abs(pcie_tab_aperture_edge_x - pcie_tab_edge_x) - pcie_bracket_tab_opening_gap_x
    pcie_tab_w = min(pcie_bracket_tab_width_x, pcie_tab_land)
    pcie_tab_dir = 1.0 if pcie_tab_edge_x > pcie_tab_aperture_edge_x else -1.0
    pcie_tab_x = pcie_tab_aperture_edge_x + pcie_tab_dir * (
        pcie_bracket_tab_opening_gap_x + pcie_tab_w / 2
    )
    pcie_tab_specs.append((pcie_tab_x, pcie_tab_w, pcie_tab_land))

pcie_tabs = []
pcie_tab_center_xs = []
for pcie_tab_x, pcie_tab_w, _land in pcie_tab_specs:
    pcie_tabs.append(Box(
        pcie_tab_w,
        pcie_bracket_tab_depth_y,
        pcie_bracket_tab_height_z,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((pcie_tab_x, pcie_tab_y, pcie_bracket_base_z))))
    pcie_tab_center_xs.append(pcie_tab_x)
pcie_bracket = (pcie_shelf + pcie_tabs[0] + pcie_tabs[1]).clean()

# Shift both GPU-ear screw axes by the user's measured +X/right and -Y/outward
# correction. The through-stack proxy follows the extended shelf footprint, and
# the printed-screw-joint kit continues to own the M3 profile and hardware.
pcie_gpu_stack_height = pcie_bracket_gpu_ear_thickness + pcie_bracket_lift_z
pcie_gpu_axis_z = flange_z - pcie_bracket_gpu_ear_thickness
pcie_gpu_axis_y = flange_y - pcie_bracket_gpu_axis_outward_y
pcie_gpu_axis_xs = tuple(x + pcie_bracket_gpu_axis_right_x for x in slot_centers)
pcie_gpu_proxy = Box(
    pcie_bracket_width_x,
    pcie_bracket_effective_shelf_depth_y - 2.0,
    pcie_gpu_stack_height,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((pcie_shelf_center_x, pcie_bracket_effective_shelf_y, pcie_gpu_axis_z)))
pcie_gpu_joints = []
for i, x in enumerate(pcie_gpu_axis_xs):
    joint = make_screw_joint_v1(
        size='M3',
        at=Location((x, pcie_gpu_axis_y, pcie_gpu_axis_z), (180, 0, 0)),
        through=[(pcie_gpu_proxy, pcie_gpu_stack_height)],
        engage_depth=pcie_bracket_gpu_engagement,
        into=pcie_bracket,
        head='socket_cap',
        strategy='auto',
        termination='through',
        material=material,
        boss='none',
        label=f'pcie-gpu-ear:{i}',
    )
    pcie_bracket = (pcie_bracket - joint.engage_cuts).clean()
    pcie_gpu_joints.append(joint)

# Screw the raised separate bracket into the rear panel through the two side tabs.
# The screw-joint kit uses local -Z as insertion; +90 degrees about X points
# local -Z from the rear exterior toward the enclosure interior (+Y).
pcie_rear_joints = []
pcie_rear_screw_z = pcie_bracket_base_z + pcie_bracket_rear_screw_z_offset
for i, (pcie_tab_x, pcie_tab_w, _land) in enumerate(pcie_tab_specs):
    tab_proxy = Box(
        pcie_tab_w,
        pcie_bracket_tab_depth_y,
        pcie_bracket_tab_height_z - 4.0,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location((pcie_tab_x, pcie_tab_y, pcie_rear_screw_z)))
    joint = make_screw_joint_v1(
        size='M3',
        at=Location((pcie_tab_x, -D/2-pcie_bracket_tab_depth_y, pcie_rear_screw_z), (90, 0, 0)),
        through=[(tab_proxy, pcie_bracket_tab_depth_y)],
        engage_depth=pcie_bracket_rear_engagement,
        into=rear_panel,
        head='socket_cap',
        strategy='auto',
        termination='blind',
        material=material,
        boss='auto',
        label=f'pcie-bracket-rear:{i}',
    )
    pcie_bracket = (pcie_bracket - joint.through_cuts[0]).clean()
    rear_panel = (rear_panel + joint.bosses - joint.engage_cuts).clean()
    pcie_rear_joints.append(joint)

pcie_gpu_hardware = Compound(children=[j.hardware for j in pcie_gpu_joints])
pcie_rear_hardware = Compound(children=[j.hardware for j in pcie_rear_joints])
pcie_connection_inventory = {
    'gpu-ears-to-pcie-bracket': 'printed-screw-joint-v1 x2 with user-measured X/Y correction',
    'pcie-bracket-to-rear-panel': 'printed-screw-joint-v1 x2',
}
pcie_overlap = pcie_bracket & rear_panel
pcie_bracket_bb = pcie_bracket.bounding_box()
pcie_gpu_y_land = pcie_gpu_axis_y - pcie_bracket_bb.min.Y
assert pcie_bracket_lift_z >= 0.0
assert pcie_bracket_gpu_axis_right_x >= 0.0
assert pcie_bracket_gpu_axis_outward_y >= 0.0
assert abs(pcie_bracket_bb.min.Z - pcie_bracket_base_z) < 0.01
assert abs((pcie_bracket_base_z - flange_z) - pcie_bracket_lift_z) < 0.01
assert len(pcie_gpu_joints) == int(pcie_bracket_expected_gpu_screws)
assert len(pcie_rear_joints) == int(pcie_bracket_expected_rear_screws)
assert all(pcie_connection_inventory.values())
assert pcie_bracket.solids().__len__() == 1 and rear_panel.solids().__len__() == 1
assert pcie_overlap is None or pcie_overlap.volume < 0.02
# Both tabs must still be wide enough to carry an M3 screw.
for _x, pcie_tab_w, _land in pcie_tab_specs:
    assert pcie_tab_w >= pcie_bracket_tab_min_width_x
# The whole bracket must stay inside the case X outline at the moved card position.
assert pcie_bracket_bb.min.X >= -W/2 + pcie_bracket_outline_margin_x - 0.001
assert pcie_bracket_bb.max.X <= W/2 - pcie_bracket_outline_margin_x + 0.001
# Shifted axes retain their slot pitch and remain fully inside shelf material.
assert abs((pcie_gpu_axis_xs[1] - pcie_gpu_axis_xs[0]) - slot_pitch) < 0.001
assert min(pcie_gpu_axis_xs) >= pcie_shelf_x_min + 3.0
assert max(pcie_gpu_axis_xs) <= pcie_shelf_x_max - 3.0
assert pcie_gpu_y_land >= 3.0
assert pcie_gpu_axis_y <= pcie_bracket_bb.max.Y - 3.0
publish('rear_panel', rear_panel, 'Rear with raised PCIe mounts')
publish('pcie_bracket', pcie_bracket, 'Shifted dual-slot bracket')
publish('pcie_gpu_screws', pcie_gpu_hardware, 'Shifted GPU screws')
publish('pcie_rear_screws', pcie_rear_hardware, 'Raised PCIe rear screws')
print(
    f'PCIE_GPU_AXIS_SHIFT_PASS: GPU axes right +{pcie_bracket_gpu_axis_right_x:.1f} mm '
    f'and outward -{pcie_bracket_gpu_axis_outward_y:.1f} mm to '
    f'x={pcie_gpu_axis_xs[0]:.2f}/{pcie_gpu_axis_xs[1]:.2f}, y={pcie_gpu_axis_y:.2f}; '
    f'pitch={pcie_gpu_axis_xs[1]-pcie_gpu_axis_xs[0]:.2f} mm, rear Y land={pcie_gpu_y_land:.1f} mm; '
    f'bracket y={pcie_bracket_bb.min.Y:.1f}..{pcie_bracket_bb.max.Y:.1f} mm.'
)