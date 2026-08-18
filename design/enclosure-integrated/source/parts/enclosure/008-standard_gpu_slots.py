# Rear interfaces referenced to the actual Mini-ITX PCB and I/O-shield datums.
# The dual-slot GPU is rolled 180 degrees: PCIe fingers are up and its standard
# rear mounting ear is below the I/O plate, so the retaining flange belongs at
# the bottom edge of the dual-slot opening rather than the top edge.
rear_y = -D / 2 + panel_t / 2
rear_panel = Box(
    W, panel_t, H - base_t - cap_t,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((0, rear_y, base_t)))

# ATX-family removable I/O-shield chassis aperture. microATX Interface
# Specification v1.0, Figure 5 (PDF page 13), locates the 1.750-inch aperture
# from 0.150 inch below the component-side PCB surface; it is not flush to a PCB face.
io_shield_nominal_short = param('io_shield_nominal_short', 44.45)
io_shield_nominal_long = param('io_shield_nominal_long', 158.75)
io_shield_edge_clearance = param('io_shield_edge_clearance', 0.20)
IO_APERTURE_BELOW_PCB_COMPONENT_FACE_MM = 3.81
io_pcb_component_face_x = board_plane_x + board_side * board_proxy_thickness
io_shield_lower_x = io_pcb_component_face_x - board_side * IO_APERTURE_BELOW_PCB_COMPONENT_FACE_MM
io_cut_w = io_shield_nominal_short + 2 * io_shield_edge_clearance
io_cut_h = io_shield_nominal_long + 2 * io_shield_edge_clearance
io_inner_edge_x = io_shield_lower_x - board_side * io_shield_edge_clearance
io_cut_x = io_inner_edge_x + board_side * io_cut_w / 2
board_top_z = mitx_board_z_min + mitx_board_height
io_cut_z_max = board_top_z + io_shield_edge_clearance
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

slot_pitch = param('gpu_slot_pitch', 20.32)
slot_center_mag = abs(param('gpu_slot_pair_center_x', 31.0))
slot_center_x = -board_side * slot_center_mag
slot_centers = (slot_center_x - slot_pitch / 2, slot_center_x + slot_pitch / 2)
slot_w = param('gpu_slot_width', 18.0)
slot_h = param('gpu_slot_height', 120.0)
slot_z0 = param('gpu_slot_z0', 112.0)
dual_slot_opening_width = param('gpu_dual_slot_opening_width', 39.0)
rear_panel = rear_panel - Box(
    dual_slot_opening_width, cut_depth, slot_h,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((slot_center_x, -D / 2, slot_z0)))

flange_w = param('gpu_flange_width', 64.0)
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
).moved(Location((slot_center_x, flange_y, flange_z)))
rear_panel = (rear_panel + gpu_flange).clean()

bracket_t = param('gpu_bracket_ear_thickness', 0.8)
bracket_proxy = Box(
    flange_w, flange_d - 2.0, bracket_t,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((slot_center_x, flange_y, flange_z - bracket_t)))
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
side_land = (flange_w - dual_slot_opening_width) / 2
assert dual_slot_opening_width > slot_pitch + slot_w
assert side_land >= 10.0 and len(slot_joints) == 2
assert board_side * io_cut_x > 0 and board_side * slot_center_x < 0
assert abs((io_pcb_component_face_x - io_shield_lower_x) - board_side * IO_APERTURE_BELOW_PCB_COMPONENT_FACE_MM) < 0.001
assert abs(flange_z - slot_z0) < 0.01
publish('rear_panel', rear_panel, 'Flipped GPU rear opening')
print(f'IO_APERTURE_DATUM_PASS: lower short edge is {IO_APERTURE_BELOW_PCB_COMPONENT_FACE_MM:.2f} mm below the component-side PCB surface; cut center x={io_cut_x:.2f} mm.')