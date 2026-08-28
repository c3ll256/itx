# Separate printable PCIe L bracket with two active GPU-ear screws,
# two alternate full clearance holes on a keyed insert, and two rear screws.
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
pcie_bracket_expected_alt_slots = param('pcie_bracket_expected_alt_slots', 2)
pcie_bracket_expected_rear_screws = param('pcie_bracket_expected_rear_screws', 2)
pcie_bracket_outline_margin_x = param('pcie_bracket_outline_margin_x', 3.0)
pcie_bracket_gpu_axis_right_x = param('pcie_bracket_gpu_axis_right_x', 3.6)
pcie_bracket_gpu_axis_outward_y = param('pcie_bracket_gpu_axis_outward_y', 3.6)

pcie_bracket_alt_slot_right_x = param('pcie_bracket_alt_slot_right_x', 5.0)
pcie_bracket_alt_slot_inward_y = param('pcie_bracket_alt_slot_inward_y', 6.0)
pcie_bracket_alt_hole_left_shift_x = param('pcie_bracket_alt_hole_left_shift_x', 1.0)
pcie_bracket_alt_hole_inward_shift_y = param('pcie_bracket_alt_hole_inward_shift_y', 1.0)
pcie_bracket_alt_slot_diameter = param('pcie_bracket_alt_slot_diameter', 3.4)
pcie_bracket_alt_slot_z_overcut = param('pcie_bracket_alt_slot_z_overcut', 0.2)
pcie_bracket_insert_depth_y = param('pcie_bracket_insert_depth_y', 3.0)
pcie_bracket_insert_overlap_y = param('pcie_bracket_insert_overlap_y', 0.8)
pcie_bracket_insert_side_wall_x = param('pcie_bracket_insert_side_wall_x', 1.5)
pcie_bracket_insert_min_wall_y = param('pcie_bracket_insert_min_wall_y', 1.2)
pcie_bracket_alt_hole_shelf_extension_y = param('pcie_bracket_alt_hole_shelf_extension_y', 0.5)
pcie_bracket_inward_relief_clearance_y = param('pcie_bracket_inward_relief_clearance_y', 0.2)
pcie_bracket_inward_relief_clearance_xz = param('pcie_bracket_inward_relief_clearance_xz', 0.2)

pcie_bracket_width_x = flange_w
pcie_bracket_base_z = flange_z + pcie_bracket_lift_z
pcie_bracket_effective_shelf_depth_y = (
    pcie_bracket_shelf_depth_y + pcie_bracket_gpu_axis_outward_y
    + pcie_bracket_alt_hole_shelf_extension_y
)
pcie_bracket_effective_shelf_y = flange_y + (
    pcie_bracket_alt_hole_shelf_extension_y - pcie_bracket_gpu_axis_outward_y
) / 2.0
pcie_shelf_inner_edge_y = pcie_bracket_effective_shelf_y + pcie_bracket_effective_shelf_depth_y/2
pcie_shelf = Box(
    pcie_bracket_width_x, pcie_bracket_effective_shelf_depth_y,
    pcie_bracket_shelf_thickness_z,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((pcie_shelf_center_x, pcie_bracket_effective_shelf_y, pcie_bracket_base_z)))

pcie_gpu_axis_z = flange_z - pcie_bracket_gpu_ear_thickness
pcie_gpu_axis_y = flange_y - pcie_bracket_gpu_axis_outward_y
pcie_gpu_axis_xs = tuple(x + pcie_bracket_gpu_axis_right_x for x in slot_centers)
pcie_gpu_alt_axis_y = pcie_gpu_axis_y + pcie_bracket_alt_slot_inward_y + pcie_bracket_alt_hole_inward_shift_y
pcie_gpu_alt_axis_xs = tuple(
    x + pcie_bracket_alt_slot_right_x - pcie_bracket_alt_hole_left_shift_x
    for x in pcie_gpu_axis_xs
)
pcie_alt_hole_radius = pcie_bracket_alt_slot_diameter/2
pcie_insert_x_min = min(pcie_gpu_alt_axis_xs) - pcie_alt_hole_radius - pcie_bracket_insert_side_wall_x
pcie_insert_x_max = max(pcie_gpu_alt_axis_xs) + pcie_alt_hole_radius + pcie_bracket_insert_side_wall_x
pcie_insert_width_x = pcie_insert_x_max - pcie_insert_x_min
pcie_insert_center_x = (pcie_insert_x_min + pcie_insert_x_max)/2
pcie_insert_y_min = pcie_shelf_inner_edge_y - pcie_bracket_insert_overlap_y
pcie_insert_y_max = pcie_shelf_inner_edge_y + pcie_bracket_insert_depth_y
pcie_insert_depth_total_y = pcie_insert_y_max - pcie_insert_y_min
pcie_insert_center_y = (pcie_insert_y_min + pcie_insert_y_max)/2
pcie_insert = Box(
    pcie_insert_width_x, pcie_insert_depth_total_y,
    pcie_bracket_shelf_thickness_z,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((pcie_insert_center_x, pcie_insert_center_y, pcie_bracket_base_z)))

pcie_tab_y = -D/2 - pcie_bracket_tab_depth_y/2
pcie_tab_specs = []
for pcie_tab_edge_x, pcie_tab_aperture_edge_x in (
    (pcie_shelf_x_min, pcie_aperture_x_min),
    (pcie_shelf_x_max, pcie_aperture_x_max),
):
    pcie_tab_land = abs(pcie_tab_aperture_edge_x - pcie_tab_edge_x) - pcie_bracket_tab_opening_gap_x
    pcie_tab_w = min(pcie_bracket_tab_width_x, pcie_tab_land)
    pcie_tab_dir = 1.0 if pcie_tab_edge_x > pcie_tab_aperture_edge_x else -1.0
    pcie_tab_x = pcie_tab_aperture_edge_x + pcie_tab_dir * (pcie_bracket_tab_opening_gap_x + pcie_tab_w/2)
    pcie_tab_specs.append((pcie_tab_x, pcie_tab_w, pcie_tab_land))
pcie_tabs = [
    Box(
        pcie_tab_w, pcie_bracket_tab_depth_y, pcie_bracket_tab_height_z,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((pcie_tab_x, pcie_tab_y, pcie_bracket_base_z)))
    for pcie_tab_x, pcie_tab_w, _land in pcie_tab_specs
]
pcie_bracket = (pcie_shelf + pcie_insert + pcie_tabs[0] + pcie_tabs[1]).clean()

# Keep the original full-width shelf relief and add a second relief for the keyed insert.
pcie_shelf_relief_depth_y = pcie_bracket_alt_hole_shelf_extension_y + pcie_bracket_inward_relief_clearance_y
pcie_shelf_relief = Box(
    pcie_bracket_width_x + 2*pcie_bracket_inward_relief_clearance_xz,
    pcie_shelf_relief_depth_y,
    pcie_bracket_shelf_thickness_z + 2*pcie_bracket_inward_relief_clearance_xz,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((
    pcie_shelf_center_x, -D/2 + pcie_shelf_relief_depth_y/2,
    pcie_bracket_base_z - pcie_bracket_inward_relief_clearance_xz,
)))
pcie_insert_relief = Box(
    pcie_insert_width_x + 2*pcie_bracket_inward_relief_clearance_xz,
    pcie_insert_depth_total_y + pcie_bracket_inward_relief_clearance_y,
    pcie_bracket_shelf_thickness_z + 2*pcie_bracket_inward_relief_clearance_xz,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((
    pcie_insert_center_x,
    pcie_insert_center_y + pcie_bracket_inward_relief_clearance_y/2,
    pcie_bracket_base_z - pcie_bracket_inward_relief_clearance_xz,
)))
rear_panel = (rear_panel - pcie_shelf_relief - pcie_insert_relief).clean()

pcie_gpu_stack_height = pcie_bracket_gpu_ear_thickness + pcie_bracket_lift_z
pcie_gpu_proxy = Box(
    pcie_bracket_width_x, pcie_bracket_effective_shelf_depth_y - 2.0,
    pcie_gpu_stack_height, align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((pcie_shelf_center_x, pcie_bracket_effective_shelf_y, pcie_gpu_axis_z)))
pcie_gpu_joints = []
for i, x in enumerate(pcie_gpu_axis_xs):
    j = make_screw_joint_v1(
        size='M3', at=Location((x, pcie_gpu_axis_y, pcie_gpu_axis_z), (180,0,0)),
        through=[(pcie_gpu_proxy, pcie_gpu_stack_height)],
        engage_depth=pcie_bracket_gpu_engagement, into=pcie_bracket,
        head='socket_cap', strategy='auto', termination='through',
        material=material, boss='none', label=f'pcie-gpu-ear:{i}',
    )
    pcie_bracket = (pcie_bracket - j.engage_cuts).clean()
    pcie_gpu_joints.append(j)

pcie_alt_hole_cutters = []
for x in pcie_gpu_alt_axis_xs:
    hole_cut = Cylinder(
        pcie_alt_hole_radius,
        pcie_bracket_shelf_thickness_z + 2*pcie_bracket_alt_slot_z_overcut,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((x, pcie_gpu_alt_axis_y, pcie_bracket_base_z-pcie_bracket_alt_slot_z_overcut)))
    pcie_bracket = (pcie_bracket - hole_cut).clean()
    pcie_alt_hole_cutters.append(hole_cut)

pcie_rear_joints = []
pcie_rear_screw_z = pcie_bracket_base_z + pcie_bracket_rear_screw_z_offset
for i, (pcie_tab_x, pcie_tab_w, _land) in enumerate(pcie_tab_specs):
    tab_proxy = Box(
        pcie_tab_w, pcie_bracket_tab_depth_y, pcie_bracket_tab_height_z - 4.0,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location((pcie_tab_x, pcie_tab_y, pcie_rear_screw_z)))
    j = make_screw_joint_v1(
        size='M3', at=Location((pcie_tab_x, -D/2-pcie_bracket_tab_depth_y, pcie_rear_screw_z), (90,0,0)),
        through=[(tab_proxy, pcie_bracket_tab_depth_y)],
        engage_depth=pcie_bracket_rear_engagement, into=rear_panel,
        head='socket_cap', strategy='auto', termination='blind',
        material=material, boss='auto', label=f'pcie-bracket-rear:{i}',
    )
    pcie_bracket = (pcie_bracket - j.through_cuts[0]).clean()
    rear_panel = (rear_panel + j.bosses - j.engage_cuts).clean()
    pcie_rear_joints.append(j)

pcie_gpu_hardware = Compound(children=[j.hardware for j in pcie_gpu_joints])
pcie_rear_hardware = Compound(children=[j.hardware for j in pcie_rear_joints])
pcie_connection_inventory = {
    'gpu-ears-to-pcie-bracket': 'printed-screw-joint-v1 x2 active',
    'pcie-bracket-alternate-holes': 'free M3 full clearance holes x2 in keyed insert',
    'pcie-bracket-to-rear-panel': 'printed-screw-joint-v1 x2',
}
pcie_overlap = pcie_bracket & rear_panel
pcie_overlap_volume = 0.0 if pcie_overlap is None else sum(s.volume for s in pcie_overlap)
pcie_alt_interpair_pitch = pcie_gpu_alt_axis_xs[1] - pcie_gpu_alt_axis_xs[0]
pcie_alt_to_active_center_spacing = (
    (pcie_bracket_alt_slot_right_x-pcie_bracket_alt_hole_left_shift_x)**2
    + (pcie_bracket_alt_slot_inward_y+pcie_bracket_alt_hole_inward_shift_y)**2
)**0.5
pcie_alt_min_side_wall = min(
    min(pcie_gpu_alt_axis_xs) - pcie_insert_x_min - pcie_alt_hole_radius,
    pcie_insert_x_max - max(pcie_gpu_alt_axis_xs) - pcie_alt_hole_radius,
)
pcie_alt_min_inward_wall = pcie_insert_y_max - pcie_gpu_alt_axis_y - pcie_alt_hole_radius
M3_ACTIVE_SELF_FORMING_R_OUT_MM = 1.809

assert abs(pcie_bracket_alt_hole_left_shift_x - 1.0) < 0.001
assert abs(pcie_bracket_alt_hole_inward_shift_y - 1.0) < 0.001
assert abs(pcie_bracket_alt_slot_diameter - 3.4) < 0.001
assert len(pcie_gpu_joints) == int(pcie_bracket_expected_gpu_screws)
assert len(pcie_alt_hole_cutters) == int(pcie_bracket_expected_alt_slots)
assert len(pcie_rear_joints) == int(pcie_bracket_expected_rear_screws)
assert all(pcie_connection_inventory.values())
assert pcie_bracket.solids().__len__() == 1
assert rear_panel.solids().__len__() == 1
assert pcie_overlap_volume < 0.02
assert all(w >= pcie_bracket_tab_min_width_x for _x,w,_land in pcie_tab_specs)
assert abs(pcie_alt_interpair_pitch - slot_pitch) < 0.001
assert pcie_alt_to_active_center_spacing >= M3_ACTIVE_SELF_FORMING_R_OUT_MM + pcie_alt_hole_radius + 1.5
assert pcie_alt_min_side_wall >= pcie_bracket_insert_side_wall_x - 0.001
assert pcie_alt_min_inward_wall >= pcie_bracket_insert_min_wall_y
assert pcie_insert_y_min < pcie_shelf_inner_edge_y < pcie_insert_y_max

publish('rear_panel', rear_panel, 'Rear with keyed PCIe relief')
publish('pcie_bracket', pcie_bracket, 'Keyed PCIe full-hole bracket')
publish('pcie_gpu_screws', pcie_gpu_hardware, 'Active GPU screws')
publish('pcie_rear_screws', pcie_rear_hardware, 'Raised PCIe rear screws')
print(
    f'PCIE_KEYED_HOLES_PASS: active x={pcie_gpu_axis_xs[0]:.2f}/{pcie_gpu_axis_xs[1]:.2f}, y={pcie_gpu_axis_y:.2f}; '
    f'alternate x={pcie_gpu_alt_axis_xs[0]:.2f}/{pcie_gpu_alt_axis_xs[1]:.2f}, y={pcie_gpu_alt_axis_y:.2f}; '
    f'left/inward shift={pcie_bracket_alt_hole_left_shift_x:.1f}/{pcie_bracket_alt_hole_inward_shift_y:.1f} mm; '
    f'insert depth={pcie_bracket_insert_depth_y:.2f} mm, side/inward wall={pcie_alt_min_side_wall:.2f}/{pcie_alt_min_inward_wall:.2f} mm; '
    f'panel overlap={pcie_overlap_volume:.4f} mm^3.'
)