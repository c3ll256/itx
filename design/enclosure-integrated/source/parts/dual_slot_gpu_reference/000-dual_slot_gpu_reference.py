# Envelope proxy for the user's dual-slot Colorful RTX 3060 NB DUO 12G V3 L-V.
# User-measured: the card body without the PCIe bracket is 241 mm long and the
# bracket plate is 106 mm high. The metal bracket baseline follows the active
# PCIe opening lower edge at Z=97 mm; a later cell applies the measured 7.5 mm
# body-only extension below this fixed bracket datum.
COLORFUL_BODY_LENGTH_Y = 241.0
COLORFUL_L_EAR_PROJECTION_Y = 8.8
COLORFUL_OFFICIAL_OVERALL_LENGTH_Y = COLORFUL_BODY_LENGTH_Y + COLORFUL_L_EAR_PROJECTION_Y
COLORFUL_BODY_REAR_Y = -125.2
COLORFUL_L_EAR_REAR_Y = COLORFUL_BODY_REAR_Y - COLORFUL_L_EAR_PROJECTION_Y
COLORFUL_BODY_FRONT_Y = COLORFUL_BODY_REAR_Y + COLORFUL_BODY_LENGTH_Y
COLORFUL_HEIGHT_Z = 132.5
COLORFUL_THICKNESS_X = 41.0
CURRENT_PCIE_OPENING_BOTTOM_Z_MM = 97.0
COLORFUL_BOTTOM_Z = CURRENT_PCIE_OPENING_BOTTOM_Z_MM
COLORFUL_BRACKET_HEIGHT_Z = 106.0
assert abs(COLORFUL_OFFICIAL_OVERALL_LENGTH_Y - 249.8) < 0.01

gpu_ref_center_x = param('gpu_ref_center_x', -31.0)
gpu_ref_shroud = Box(
    COLORFUL_THICKNESS_X, COLORFUL_BODY_LENGTH_Y, COLORFUL_HEIGHT_Z,
    align=(Align.CENTER, Align.MIN, Align.MIN),
).moved(Location((gpu_ref_center_x, COLORFUL_BODY_REAR_Y, COLORFUL_BOTTOM_Z)))
publish('gpu_shroud', gpu_ref_shroud, 'Colorful GPU body')

colorful_pcb_thickness_x = param('colorful_pcb_thickness_x', 1.6)
colorful_pcb_length_y = param('colorful_pcb_length_y', 232.6)
colorful_pcb_height_z = param('colorful_pcb_height_z', 118.0)
gpu_ref_pcb = Box(
    colorful_pcb_thickness_x, colorful_pcb_length_y, colorful_pcb_height_z,
    align=(Align.MAX, Align.MIN, Align.MIN),
).moved(Location((
    gpu_ref_center_x + COLORFUL_THICKNESS_X / 2 - 2.0,
    COLORFUL_BODY_REAR_Y + 3.0,
    COLORFUL_BOTTOM_Z + 7.0,
)))
publish('gpu_pcb', gpu_ref_pcb, 'Colorful GPU PCB')

colorful_bracket_width_x = param('colorful_bracket_width_x', 39.0)
colorful_bracket_depth_y = param('colorful_bracket_depth_y', 1.0)
colorful_mount_ear_depth_y = param('colorful_mount_ear_depth_y', 8.0)
colorful_mount_ear_thickness_z = param('colorful_mount_ear_thickness_z', 0.8)
colorful_mount_ear_overlap_y = param('colorful_mount_ear_overlap_y', 0.2)
gpu_ref_bracket_plate = Box(
    colorful_bracket_width_x, colorful_bracket_depth_y, COLORFUL_BRACKET_HEIGHT_Z,
    align=(Align.CENTER, Align.MAX, Align.MIN),
).moved(Location((gpu_ref_center_x, -126.0, COLORFUL_BOTTOM_Z)))
gpu_ref_mount_ear = Box(
    colorful_bracket_width_x,
    colorful_mount_ear_depth_y + colorful_mount_ear_overlap_y,
    colorful_mount_ear_thickness_z,
    align=(Align.CENTER, Align.MAX, Align.MAX),
).moved(Location((gpu_ref_center_x, -126.0 + colorful_mount_ear_overlap_y, COLORFUL_BOTTOM_Z)))
gpu_ref_bracket = (gpu_ref_bracket_plate + gpu_ref_mount_ear).clean()
publish('gpu_rear_bracket', gpu_ref_bracket, 'Flipped dual-slot bracket')

# A 180-degree card roll mirrors the rear I/O features vertically.
COLORFUL_PORT_CENTER_Z_FLIPPED = 169.0
COLORFUL_VENT_CENTER_Z_FLIPPED = 124.0
colorful_port_width_x = param('colorful_port_width_x', 8.0)
colorful_port_depth_y = param('colorful_port_depth_y', 3.0)
colorful_port_height_z = param('colorful_port_height_z', 16.0)
colorful_port_pitch_x = param('colorful_port_pitch_x', 9.5)
colorful_port_first_offset_x = -14.0
gpu_ref_ports = [
    Box(
        colorful_port_width_x, colorful_port_depth_y, colorful_port_height_z,
        align=(Align.CENTER, Align.MAX, Align.CENTER),
    ).moved(Location((
        gpu_ref_center_x + colorful_port_first_offset_x + i * colorful_port_pitch_x,
        -126.0,
        COLORFUL_PORT_CENTER_Z_FLIPPED,
    )))
    for i in range(4)
]
publish('gpu_display_ports', Compound(children=gpu_ref_ports), 'Flipped HDMI and DP')

colorful_vent_width_x = param('colorful_vent_width_x', 2.8)
colorful_vent_depth_y = param('colorful_vent_depth_y', 2.0)
colorful_vent_height_z = param('colorful_vent_height_z', 38.0)
colorful_vent_pitch_x = param('colorful_vent_pitch_x', 5.2)
colorful_vent_first_offset_x = -13.0
gpu_ref_vents = [
    Box(
        colorful_vent_width_x, colorful_vent_depth_y, colorful_vent_height_z,
        align=(Align.CENTER, Align.MAX, Align.CENTER),
    ).moved(Location((
        gpu_ref_center_x + colorful_vent_first_offset_x + i * colorful_vent_pitch_x,
        -126.5,
        COLORFUL_VENT_CENTER_Z_FLIPPED,
    )))
    for i in range(6)
]
publish('gpu_rear_vents', Compound(children=gpu_ref_vents), 'Flipped rear vents')

colorful_fan_diameter = param('colorful_fan_diameter', 91.0)
colorful_fan_hub_diameter = param('colorful_fan_hub_diameter', 28.0)
colorful_fan_ring_width = param('colorful_fan_ring_width', 2.5)
colorful_fan_thickness_x = param('colorful_fan_thickness_x', 1.2)
colorful_fan_pitch_y = param('colorful_fan_pitch_y', 102.0)
colorful_fan_center_y = param('colorful_fan_center_y', 1.5)
colorful_fan_center_z = COLORFUL_BOTTOM_Z + COLORFUL_HEIGHT_Z / 2
colorful_fan_face_x = gpu_ref_center_x - COLORFUL_THICKNESS_X / 2 - 0.6
gpu_ref_fans = []
for y in (
    colorful_fan_center_y - colorful_fan_pitch_y / 2,
    colorful_fan_center_y + colorful_fan_pitch_y / 2,
):
    outer = Cylinder(
        colorful_fan_diameter / 2, colorful_fan_thickness_x,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.Y, 90).moved(Location((colorful_fan_face_x, y, colorful_fan_center_z)))
    inner = Cylinder(
        (colorful_fan_diameter - 2 * colorful_fan_ring_width) / 2,
        colorful_fan_thickness_x + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.Y, 90).moved(Location((colorful_fan_face_x, y, colorful_fan_center_z)))
    hub = Cylinder(
        colorful_fan_hub_diameter / 2, colorful_fan_thickness_x,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.Y, 90).moved(Location((colorful_fan_face_x, y, colorful_fan_center_z)))
    gpu_ref_fans.extend([outer - inner, hub])
publish('gpu_fan', Compound(children=gpu_ref_fans), 'Outward dual fans')

colorful_fin_depth_x = param('colorful_fin_depth_x', 28.0)
colorful_fin_thickness_y = param('colorful_fin_thickness_y', 1.2)
colorful_fin_height_z = param('colorful_fin_height_z', 96.0)
colorful_fin_pitch_y = param('colorful_fin_pitch_y', 7.0)
gpu_ref_fins = []
y = COLORFUL_BODY_REAR_Y + 12.0
while y < COLORFUL_BODY_FRONT_Y - 8.0:
    gpu_ref_fins.append(
        Box(
            colorful_fin_depth_x, colorful_fin_thickness_y, colorful_fin_height_z,
            align=(Align.CENTER, Align.MIN, Align.CENTER),
        ).moved(Location((gpu_ref_center_x + 3.0, y, colorful_fan_center_z)))
    )
    y += colorful_fin_pitch_y
publish('gpu_heatsink', Compound(children=gpu_ref_fins), 'Colorful heatsink fins')

colorful_finger_width_x = param('colorful_finger_width_x', 3.0)
colorful_finger_length_y = param('colorful_finger_length_y', 78.0)
colorful_finger_height_z = param('colorful_finger_height_z', 5.0)
gpu_ref_pcie_fingers = Box(
    colorful_finger_width_x, colorful_finger_length_y, colorful_finger_height_z,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((
    gpu_ref_center_x + 11.0,
    -68.0,
    COLORFUL_BOTTOM_Z + COLORFUL_HEIGHT_Z,
)))
publish('gpu_pcie_fingers', gpu_ref_pcie_fingers, 'Upward PCIe fingers')

colorful_power_width_x = param('colorful_power_width_x', 22.0)
colorful_power_length_y = param('colorful_power_length_y', 24.0)
colorful_power_height_z = param('colorful_power_height_z', 12.0)
# The 8-pin zone belongs to the card: it stays 9 mm inboard of the card centre
# and 13.4 mm behind the card nose whatever the card length or position is.
colorful_power_center_x = gpu_ref_center_x + 9.0
colorful_power_center_y = COLORFUL_BODY_FRONT_Y - 13.4
gpu_ref_power_zone = Box(
    colorful_power_width_x, colorful_power_length_y, colorful_power_height_z,
    align=(Align.CENTER, Align.CENTER, Align.MAX),
).moved(Location((colorful_power_center_x, colorful_power_center_y, COLORFUL_BOTTOM_Z)))
publish('gpu_power_zone', gpu_ref_power_zone, 'Lower inverted 8-pin zone')

shroud_bb = gpu_ref_shroud.bounding_box()
fan_bb = Compound(children=gpu_ref_fans).bounding_box()
finger_bb = gpu_ref_pcie_fingers.bounding_box()
ear_bb = gpu_ref_mount_ear.bounding_box()
power_bb = gpu_ref_power_zone.bounding_box()
assert abs(shroud_bb.size.Y - COLORFUL_BODY_LENGTH_Y) < 0.01
assert abs(shroud_bb.max.Y - ear_bb.min.Y - COLORFUL_OFFICIAL_OVERALL_LENGTH_Y) < 0.01
assert fan_bb.max.X <= shroud_bb.min.X + 0.05
assert finger_bb.min.Z >= shroud_bb.max.Z - 0.05
assert ear_bb.max.Z <= COLORFUL_BOTTOM_Z + 0.05
assert power_bb.max.Y <= shroud_bb.max.Y + 0.01
assert COLORFUL_PORT_CENTER_Z_FLIPPED > COLORFUL_VENT_CENTER_Z_FLIPPED
assert COLORFUL_PORT_CENTER_Z_FLIPPED + colorful_port_height_z / 2 <= COLORFUL_BOTTOM_Z + COLORFUL_BRACKET_HEIGHT_Z
print(
    f'COLORFUL_GPU_LENGTH_PASS: measured body={COLORFUL_BODY_LENGTH_Y:.1f} mm without bracket; '
    f'overall={COLORFUL_OFFICIAL_OVERALL_LENGTH_Y:.1f} mm including the {COLORFUL_L_EAR_PROJECTION_Y:.1f} mm L-ear; '
    f'bracket datum={COLORFUL_BOTTOM_Z:.1f} mm; plate={COLORFUL_BRACKET_HEIGHT_Z:.1f} mm; '
    f'body nose y={shroud_bb.max.Y:.1f}.'
)