# Recreate the former fused dual-slot shelf as a support-free printable L bracket.
# Two GPU bracket screws retain the card ears; two rear-facing M3 screws retain
# this separate part to solid lands on the rear panel.
pcie_bracket_width_x = param('pcie_bracket_width_x', flange_w)
pcie_bracket_shelf_depth_y = param('pcie_bracket_shelf_depth_y', flange_d)
pcie_bracket_shelf_thickness_z = param('pcie_bracket_shelf_thickness_z', flange_t)
pcie_bracket_tab_width_x = param('pcie_bracket_tab_width_x', 10.0)
pcie_bracket_tab_depth_y = param('pcie_bracket_tab_depth_y', 3.2)
pcie_bracket_tab_height_z = param('pcie_bracket_tab_height_z', 16.0)
pcie_bracket_tab_opening_gap_x = param('pcie_bracket_tab_opening_gap_x', 1.0)
pcie_bracket_rear_screw_z_offset = param('pcie_bracket_rear_screw_z_offset', 10.0)
pcie_bracket_rear_engagement = param('pcie_bracket_rear_engagement', 4.2)
pcie_bracket_gpu_engagement = param('pcie_bracket_gpu_engagement', 2.4)
pcie_bracket_gpu_ear_thickness = param('pcie_bracket_gpu_ear_thickness', bracket_t)
pcie_bracket_expected_gpu_screws = param('pcie_bracket_expected_gpu_screws', 2)
pcie_bracket_expected_rear_screws = param('pcie_bracket_expected_rear_screws', 2)

pcie_shelf = Box(
    pcie_bracket_width_x,
    pcie_bracket_shelf_depth_y,
    pcie_bracket_shelf_thickness_z,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((slot_center_x, flange_y, flange_z)))

pcie_tab_center_offset_x = dual_slot_opening_width/2 + pcie_bracket_tab_opening_gap_x + pcie_bracket_tab_width_x/2
pcie_tab_y = -D/2 - pcie_bracket_tab_depth_y/2
pcie_tabs = []
for sx in (-1, 1):
    tab = Box(
        pcie_bracket_tab_width_x,
        pcie_bracket_tab_depth_y,
        pcie_bracket_tab_height_z,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((slot_center_x + sx*pcie_tab_center_offset_x, pcie_tab_y, flange_z)))
    pcie_tabs.append(tab)
pcie_bracket = (pcie_shelf + pcie_tabs[0] + pcie_tabs[1]).clean()

# Keep the original two vertical GPU bracket-ear attachment axes.
pcie_gpu_proxy = Box(
    pcie_bracket_width_x,
    pcie_bracket_shelf_depth_y - 2.0,
    pcie_bracket_gpu_ear_thickness,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((slot_center_x, flange_y, flange_z - pcie_bracket_gpu_ear_thickness)))
pcie_gpu_joints = []
for i, x in enumerate(slot_centers):
    joint = make_screw_joint_v1(
        size='M3',
        at=Location((x, flange_y, flange_z - pcie_bracket_gpu_ear_thickness), (180, 0, 0)),
        through=[(pcie_gpu_proxy, pcie_bracket_gpu_ear_thickness)],
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

# Screw the separate bracket into the rear panel through the two side tabs.
# The screw-joint kit uses local -Z as insertion; +90 degrees about X points
# local -Z from the rear exterior toward the enclosure interior (+Y).
pcie_rear_joints = []
pcie_rear_screw_z = flange_z + pcie_bracket_rear_screw_z_offset
for i, sx in enumerate((-1, 1)):
    x = slot_center_x + sx*pcie_tab_center_offset_x
    tab_proxy = Box(
        pcie_bracket_tab_width_x,
        pcie_bracket_tab_depth_y,
        pcie_bracket_tab_height_z - 4.0,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location((x, pcie_tab_y, pcie_rear_screw_z)))
    joint = make_screw_joint_v1(
        size='M3',
        at=Location((x, -D/2-pcie_bracket_tab_depth_y, pcie_rear_screw_z), (90, 0, 0)),
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
    'gpu-ears-to-pcie-bracket': 'printed-screw-joint-v1 x2',
    'pcie-bracket-to-rear-panel': 'printed-screw-joint-v1 x2',
}
pcie_overlap = pcie_bracket & rear_panel
assert len(pcie_gpu_joints) == int(pcie_bracket_expected_gpu_screws)
assert len(pcie_rear_joints) == int(pcie_bracket_expected_rear_screws)
assert all(pcie_connection_inventory.values())
assert pcie_bracket.solids().__len__() == 1 and rear_panel.solids().__len__() == 1
assert pcie_overlap is None or pcie_overlap.volume < 0.02
publish('rear_panel', rear_panel, 'Rear with PCIe mounts')
publish('pcie_bracket', pcie_bracket, 'Dual-slot PCIe bracket')
publish('pcie_gpu_screws', pcie_gpu_hardware, 'GPU bracket screws')
publish('pcie_rear_screws', pcie_rear_hardware, 'PCIe rear screws')
print(f'PCIE_BRACKET_SEPARATE_PASS: one printable dual-slot L bracket; GPU screws=2; rear-panel screws=2; rear screw length={pcie_rear_joints[0].screw_length_mm:.0f} mm.')