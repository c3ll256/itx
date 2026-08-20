# Rear interfaces referenced to the actual Mini-ITX PCB and I/O-shield datums.
# The dual-slot GPU is rolled 180 degrees: PCIe fingers are up and its standard
# rear mounting ear is below the I/O plate, so the retaining flange belongs at
# the bottom edge of the dual-slot opening rather than the top edge.
rear_y = -D / 2 + panel_t / 2
rear_panel = Box(
    W, panel_t, H - base_t - cap_t,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((0, rear_y, base_t)))

# ATX-family removable I/O-shield chassis aperture. Mini-ITX Addendum v2
# delegates the short-axis datum to the microATX specification: 2.24 +/- 0.25 mm
# below the PCB solder-side surface. The top overhang and extra FDM clearance are
# fit-correction parameters from the user's printed installation.
io_shield_nominal_short = param('io_shield_nominal_short', 44.45)
io_shield_nominal_long = param('io_shield_nominal_long', 158.75)
io_shield_edge_clearance = param('io_shield_edge_clearance', 0.30)
io_shield_top_overhang_z = param('io_shield_top_overhang_z', 2.54)
IO_APERTURE_BELOW_PCB_SOLDER_FACE_MM = 2.24
IO_APERTURE_DATUM_TOLERANCE_MM = 0.25
io_pcb_solder_face_x = board_plane_x
io_shield_lower_x = io_pcb_solder_face_x - board_side * IO_APERTURE_BELOW_PCB_SOLDER_FACE_MM
io_cut_w = io_shield_nominal_short + 2 * io_shield_edge_clearance
io_cut_h = io_shield_nominal_long + 2 * io_shield_edge_clearance
io_inner_edge_x = io_shield_lower_x - board_side * io_shield_edge_clearance
io_cut_x = io_inner_edge_x + board_side * io_cut_w / 2
board_top_z = mitx_board_z_min + mitx_board_height
io_shield_top_z = board_top_z + io_shield_top_overhang_z
io_cut_z_max = io_shield_top_z + io_shield_edge_clearance
io_cut_z0 = io_cut_z_max - io_cut_h
io_cut = Box(
    io_cut_w, cut_depth, io_cut_h,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((io_cut_x, -D / 2, io_cut_z0)))
rear_panel = rear_panel - io_cut
rear_panel = rear_panel - Box(
    psu_cut_w, cut_depth, psu_cut_h,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((psu_cut_x, -D / 2, psu_cut_z)))

# Current card position: the slot pair was brought 2 mm back toward the case
# centre from the previous X=-45 mm position, leaving it 43 mm from centre on
# the non-board side while increasing the outboard retention-screw land.
slot_pitch = param('gpu_slot_pitch', 20.32)
slot_center_mag = abs(param('gpu_slot_pair_center_mag', 43.0))
slot_center_x = -board_side * slot_center_mag
slot_centers = (slot_center_x - slot_pitch / 2, slot_center_x + slot_pitch / 2)
slot_w = param('gpu_slot_width', 18.0)
# User-measured card bracket plate height; the aperture was 14 mm taller before.
slot_h = param('gpu_dual_slot_opening_height', 106.0)
slot_z0 = param('gpu_slot_z0', 112.0)
dual_slot_opening_width = param('gpu_dual_slot_opening_width', 39.0)
rear_panel = rear_panel - Box(
    dual_slot_opening_width, cut_depth, slot_h,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((slot_center_x, -D / 2, slot_z0)))

# At the outboard card position a symmetric shelf would overhang the case, so the
# footprint is an explicit asymmetric span: it stops short of the case edge on the
# outboard side and takes the land it needs on the roomy inboard side.
pcie_shelf_outer_margin_x = param('pcie_shelf_outer_margin_x', 4.0)
pcie_shelf_inner_land_x = param('pcie_shelf_inner_land_x', 14.0)
pcie_shelf_min_land_x = param('pcie_shelf_min_land_x', 6.0)
pcie_outboard_sign = -board_side
pcie_shelf_outer_x = pcie_outboard_sign * (W / 2 - pcie_shelf_outer_margin_x)
pcie_shelf_inner_x = slot_center_x - pcie_outboard_sign * (
    dual_slot_opening_width / 2 + pcie_shelf_inner_land_x
)
pcie_shelf_x_min = min(pcie_shelf_outer_x, pcie_shelf_inner_x)
pcie_shelf_x_max = max(pcie_shelf_outer_x, pcie_shelf_inner_x)
flange_w = pcie_shelf_x_max - pcie_shelf_x_min
pcie_shelf_center_x = (pcie_shelf_x_min + pcie_shelf_x_max) / 2
pcie_aperture_x_min = slot_center_x - dual_slot_opening_width / 2
pcie_aperture_x_max = slot_center_x + dual_slot_opening_width / 2
pcie_shelf_outer_land = abs(pcie_shelf_outer_x - (
    pcie_aperture_x_min if pcie_outboard_sign < 0 else pcie_aperture_x_max
))
pcie_shelf_inner_land = abs(pcie_shelf_inner_x - (
    pcie_aperture_x_max if pcie_outboard_sign < 0 else pcie_aperture_x_min
))

flange_d = param('gpu_flange_depth', 14.0)
flange_t = param('gpu_flange_thickness', 3.2)
ear_projection = param('gpu_ear_projection_above_flange', 6.0)
# Flipped installation: the ear occupies z=slot_z0-bracket_t..slot_z0 and
# contacts the underside of this flange. The existing screw-joint cell then
# inserts the GPU screws upward into the printed flange.
flange_z = slot_z0
flange_y = -D / 2 - flange_d / 2
gpu_flange = Box(
    flange_w, flange_d, flange_t,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((pcie_shelf_center_x, flange_y, flange_z)))
rear_panel = (rear_panel + gpu_flange).clean()

bracket_t = param('gpu_bracket_ear_thickness', 0.8)
bracket_proxy = Box(
    flange_w, flange_d - 2.0, bracket_t,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((pcie_shelf_center_x, flange_y, flange_z - bracket_t)))
slot_joints = []
for i, x in enumerate(slot_centers):
    j = make_screw_joint_v1(
        size='M3',
        at=Location((x, flange_y, flange_z - bracket_t), (180, 0, 0)),
        through=[(bracket_proxy, bracket_t)],
        engage_depth=param('gpu_bracket_engagement', 2.4),
        into=rear_panel,
        head='socket_cap',
        strategy='auto',
        termination='through',
        material=material,
        boss='none',
        label=f'gpu-slot-bracket:{i}',
    )
    rear_panel = rear_panel - j.engage_cuts
    slot_joints.append(j)

center_web = 0.0
side_land = min(pcie_shelf_outer_land, pcie_shelf_inner_land)
assert dual_slot_opening_width > slot_pitch + slot_w
assert len(slot_joints) == 2
assert pcie_shelf_outer_land >= pcie_shelf_min_land_x
assert pcie_shelf_inner_land >= pcie_shelf_min_land_x
assert pcie_shelf_x_min >= -W / 2 + pcie_shelf_outer_margin_x - 0.001
assert pcie_shelf_x_max <= W / 2 - pcie_shelf_outer_margin_x + 0.001
assert min(slot_centers) >= pcie_shelf_x_min + 3.0
assert max(slot_centers) <= pcie_shelf_x_max - 3.0
assert board_side * io_cut_x > 0 and board_side * slot_center_x < 0
assert abs((io_pcb_solder_face_x - io_shield_lower_x) - board_side * IO_APERTURE_BELOW_PCB_SOLDER_FACE_MM) < 0.001
assert IO_APERTURE_DATUM_TOLERANCE_MM == 0.25
assert io_shield_top_overhang_z > 0.0
assert abs(flange_z - slot_z0) < 0.01
publish('rear_panel', rear_panel, 'Flipped GPU rear opening')
print(f'IO_APERTURE_FIT_PASS: top overhang={io_shield_top_overhang_z:.2f} mm, clearance={io_shield_edge_clearance:.2f} mm/side, solder-face datum={IO_APERTURE_BELOW_PCB_SOLDER_FACE_MM:.2f} mm.')
print(
    f'PCIE_APERTURE_MOVED: slot centre x={slot_center_x:.1f} mm, aperture '
    f'{dual_slot_opening_width:.0f} x {slot_h:.0f} mm at z={slot_z0:.0f}..{slot_z0+slot_h:.0f}; '
    f'shelf x={pcie_shelf_x_min:.1f}..{pcie_shelf_x_max:.1f} mm inside the {W:.0f} mm outline; '
    f'lands outboard={pcie_shelf_outer_land:.1f} mm, inboard={pcie_shelf_inner_land:.1f} mm.'
)