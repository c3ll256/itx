# Standard Mini-ITX mechanical reference, not a claim of a specific retail motherboard.
# PCB outline and C/F/H/J mount coordinates follow the standard asymmetric pattern.
mitx_pcb_thickness = param('mitx_pcb_thickness', 1.6)
mitx_pcb_width_y = param('mitx_pcb_width_y', 170.0)
mitx_pcb_height_z = param('mitx_pcb_height_z', 170.0)
mitx_pcb_mount_hole_diameter = param('mitx_pcb_mount_hole_diameter', 3.96)
mitx_pcb_plane_x = param('mitx_pcb_plane_x', 4.2)
# Rear-panel sandwich: board rear edge = rear-panel inner face + stamped I/O
# shield thickness. The shield is ~1 mm of rolled steel, not the earlier 0.5 mm
# estimate; the user's printed fit confirms the board sits 1 mm farther forward
# (-125.0 instead of -126.0) behind that 1 mm shield.
mitx_pcb_rear_edge_y = param('mitx_pcb_rear_edge_y', -125.0)
# Preserve the current board datum while the mounting-position correction is handled separately.
MITX_PCB_BOTTOM_Z_MM = 71.50
mitx_pcb_bottom_z = MITX_PCB_BOTTOM_Z_MM
MITX_REAR_LOWER_FROM_REAR_MM = 10.16
MITX_FRONT_LOWER_FROM_REAR_MM = 165.10
MITX_REAR_UPPER_FROM_REAR_MM = 33.02
MITX_FRONT_UPPER_FROM_REAR_MM = 165.10
MITX_LOWER_FROM_BOTTOM_MM = 6.35
MITX_UPPER_FROM_BOTTOM_MM = 163.83
mitx_pcb_rear_lower_from_rear = MITX_REAR_LOWER_FROM_REAR_MM
mitx_pcb_front_lower_from_rear = MITX_FRONT_LOWER_FROM_REAR_MM
mitx_pcb_rear_upper_from_rear = MITX_REAR_UPPER_FROM_REAR_MM
mitx_pcb_front_upper_from_rear = MITX_FRONT_UPPER_FROM_REAR_MM
mitx_pcb_lower_from_bottom = MITX_LOWER_FROM_BOTTOM_MM
mitx_pcb_upper_from_bottom = MITX_UPPER_FROM_BOTTOM_MM
mitx_pcb = Box(mitx_pcb_thickness, mitx_pcb_width_y, mitx_pcb_height_z, align=(Align.MIN, Align.MIN, Align.MIN)).moved(Location((mitx_pcb_plane_x, mitx_pcb_rear_edge_y, mitx_pcb_bottom_z)))
mitx_pcb_top_z = mitx_pcb_bottom_z + mitx_pcb_height_z
mitx_pcb_solder_face_x = mitx_pcb_plane_x
mitx_pcb_component_face_x = mitx_pcb_plane_x + mitx_pcb_thickness
mitx_pcb_holes_yz = [
    (mitx_pcb_rear_edge_y + mitx_pcb_rear_lower_from_rear, mitx_pcb_bottom_z + mitx_pcb_lower_from_bottom),
    (mitx_pcb_rear_edge_y + mitx_pcb_front_lower_from_rear, mitx_pcb_bottom_z + mitx_pcb_lower_from_bottom),
    (mitx_pcb_rear_edge_y + mitx_pcb_rear_upper_from_rear, mitx_pcb_bottom_z + mitx_pcb_upper_from_bottom),
    (mitx_pcb_rear_edge_y + mitx_pcb_front_upper_from_rear, mitx_pcb_bottom_z + mitx_pcb_upper_from_bottom),
]
for mitx_hole_y, mitx_hole_z in mitx_pcb_holes_yz:
    mitx_hole = Cylinder(mitx_pcb_mount_hole_diameter / 2, mitx_pcb_thickness + 2.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)).rotate(Axis.Y, 90).moved(Location((mitx_pcb_plane_x + mitx_pcb_thickness / 2, mitx_hole_y, mitx_hole_z)))
    mitx_pcb = mitx_pcb - mitx_hole
publish('mitx_pcb', mitx_pcb.clean(), 'Mini-ITX PCB reference')

mitx_mount_rings_outer_diameter = param('mitx_mount_rings_outer_diameter', 7.0)
mitx_mount_rings_inner_diameter = param('mitx_mount_rings_inner_diameter', 3.96)
mitx_mount_rings_thickness_x = param('mitx_mount_rings_thickness_x', 0.25)
mitx_mount_rings_plane_x = param('mitx_mount_rings_plane_x', 4.2)
# The PCB keeps all four standard holes, but the enclosure intentionally omits
# the lower-front support so the front-bottom intake fan can occupy that floor area.
MITX_RETIRED_FRONT_LOWER_HOLE_INDEX = 1
mitx_active_mount_holes_yz = [
    hole_yz for hole_index, hole_yz in enumerate(mitx_pcb_holes_yz)
    if hole_index != MITX_RETIRED_FRONT_LOWER_HOLE_INDEX
]
mitx_mount_rings = []
for mitx_ring_y, mitx_ring_z in mitx_active_mount_holes_yz:
    mitx_ring_outer = Cylinder(mitx_mount_rings_outer_diameter / 2, mitx_mount_rings_thickness_x, align=(Align.CENTER, Align.CENTER, Align.CENTER)).rotate(Axis.Y, 90).moved(Location((mitx_mount_rings_plane_x - mitx_mount_rings_thickness_x / 2, mitx_ring_y, mitx_ring_z)))
    mitx_ring_inner = Cylinder(mitx_mount_rings_inner_diameter / 2, mitx_mount_rings_thickness_x + 0.4, align=(Align.CENTER, Align.CENTER, Align.CENTER)).rotate(Axis.Y, 90).moved(Location((mitx_mount_rings_plane_x - mitx_mount_rings_thickness_x / 2, mitx_ring_y, mitx_ring_z)))
    mitx_mount_rings.append(mitx_ring_outer - mitx_ring_inner)
publish('mitx_mount_rings', Compound(children=mitx_mount_rings), 'Three mounting rings')

# ATX-family rear I/O chassis-interface proxy used by full-height Mini-ITX.
# The short-axis aperture datum follows microATX v1.2 Figure 4: 2.24 +/- 0.25 mm
# below the PCB solder face. The long-axis top overhang and panel insertion are
# fit-correction parameters based on the user's printed installation; exact
# stamped lips and spring tabs remain motherboard-specific.
MITX_IO_APERTURE_SHORT_X_MM = 44.45
MITX_IO_APERTURE_LONG_Z_MM = 158.75
MITX_IO_APERTURE_BELOW_PCB_SOLDER_FACE_MM = 2.24
MITX_IO_APERTURE_DATUM_TOLERANCE_MM = 0.25
mitx_io_shield_thickness_y = param('mitx_io_shield_thickness_y', 1.00)
mitx_io_shield_top_overhang_z = param('mitx_io_shield_top_overhang_z', 2.54)
mitx_io_shield_x0 = mitx_pcb_solder_face_x - MITX_IO_APERTURE_BELOW_PCB_SOLDER_FACE_MM
mitx_io_shield_top_z = mitx_pcb_top_z + mitx_io_shield_top_overhang_z
mitx_io_shield_z0 = mitx_io_shield_top_z - MITX_IO_APERTURE_LONG_Z_MM
# Sandwich: the stamped shield fills the gap between the rear-panel inner face
# and the board rear edge, so its center sits half its thickness behind the edge.
mitx_io_shield_center_y = mitx_pcb_rear_edge_y - mitx_io_shield_thickness_y / 2
mitx_rear_io = Box(
    MITX_IO_APERTURE_SHORT_X_MM,
    mitx_io_shield_thickness_y,
    MITX_IO_APERTURE_LONG_Z_MM,
    align=(Align.MIN, Align.CENTER, Align.MIN),
).moved(Location((mitx_io_shield_x0, mitx_io_shield_center_y, mitx_io_shield_z0)))
publish('mitx_rear_io', mitx_rear_io, 'ATX I-O fit envelope')

mitx_cpu_socket_depth_x = param('mitx_cpu_socket_depth_x', 5.0)
mitx_cpu_socket_width_y = param('mitx_cpu_socket_width_y', 45.0)
mitx_cpu_socket_height_z = param('mitx_cpu_socket_height_z', 45.0)
mitx_cpu_socket_center_y = param('mitx_cpu_socket_center_y', -42.0)
mitx_cpu_socket_center_z = param('mitx_cpu_socket_center_z', 169.0)
mitx_cpu_socket = Box(mitx_cpu_socket_depth_x, mitx_cpu_socket_width_y, mitx_cpu_socket_height_z, align=(Align.MIN, Align.CENTER, Align.CENTER)).moved(Location((mitx_pcb_component_face_x, mitx_cpu_socket_center_y, mitx_cpu_socket_center_z)))
publish('mitx_cpu_socket', mitx_cpu_socket, 'CPU socket envelope')

mitx_dimm_bank_depth_x = param('mitx_dimm_bank_depth_x', 8.0)
mitx_dimm_bank_slot_width_y = param('mitx_dimm_bank_slot_width_y', 5.5)
mitx_dimm_bank_slot_height_z = param('mitx_dimm_bank_slot_height_z', 133.0)
mitx_dimm_bank_pitch_y = param('mitx_dimm_bank_pitch_y', 8.0)
mitx_dimm_bank_first_center_y = param('mitx_dimm_bank_first_center_y', 24.0)
mitx_dimm_bank_bottom_z = param('mitx_dimm_bank_bottom_z', 91.0)
mitx_dimm_slots = []
for mitx_dimm_i in range(2):
    mitx_dimm_slots.append(Box(mitx_dimm_bank_depth_x, mitx_dimm_bank_slot_width_y, mitx_dimm_bank_slot_height_z, align=(Align.MIN, Align.CENTER, Align.MIN)).moved(Location((mitx_pcb_component_face_x, mitx_dimm_bank_first_center_y + mitx_dimm_i * mitx_dimm_bank_pitch_y, mitx_dimm_bank_bottom_z))))
publish('mitx_dimm_bank', Compound(children=mitx_dimm_slots), 'Dual DIMM slots')

mitx_pcie_slot_depth_x = param('mitx_pcie_slot_depth_x', 11.0)
mitx_pcie_slot_length_y = param('mitx_pcie_slot_length_y', 89.0)
mitx_pcie_slot_height_z = param('mitx_pcie_slot_height_z', 11.0)
mitx_pcie_slot_rear_y = param('mitx_pcie_slot_rear_y', -104.0)
mitx_pcie_slot_bottom_z = param('mitx_pcie_slot_bottom_z', 79.0)
mitx_pcie_slot = Box(mitx_pcie_slot_depth_x, mitx_pcie_slot_length_y, mitx_pcie_slot_height_z, align=(Align.MIN, Align.MIN, Align.MIN)).moved(Location((mitx_pcb_component_face_x, mitx_pcie_slot_rear_y, mitx_pcie_slot_bottom_z)))
publish('mitx_pcie_slot', mitx_pcie_slot, 'PCIe x16 slot')

mitx_atx_power_depth_x = param('mitx_atx_power_depth_x', 12.0)
mitx_atx_power_width_y = param('mitx_atx_power_width_y', 10.0)
mitx_atx_power_height_z = param('mitx_atx_power_height_z', 52.0)
mitx_atx_power_center_y = param('mitx_atx_power_center_y', 39.0)
mitx_atx_power_bottom_z = param('mitx_atx_power_bottom_z', 136.0)
mitx_atx_power = Box(mitx_atx_power_depth_x, mitx_atx_power_width_y, mitx_atx_power_height_z, align=(Align.MIN, Align.CENTER, Align.MIN)).moved(Location((mitx_pcb_component_face_x, mitx_atx_power_center_y, mitx_atx_power_bottom_z)))
publish('mitx_atx_power', mitx_atx_power, '24-pin ATX header')

mitx_eps_power_depth_x = param('mitx_eps_power_depth_x', 12.0)
mitx_eps_power_width_y = param('mitx_eps_power_width_y', 20.0)
mitx_eps_power_height_z = param('mitx_eps_power_height_z', 10.0)
mitx_eps_power_rear_y = param('mitx_eps_power_rear_y', -118.0)
mitx_eps_power_bottom_z = param('mitx_eps_power_bottom_z', 224.0)
mitx_eps_power = Box(mitx_eps_power_depth_x, mitx_eps_power_width_y, mitx_eps_power_height_z, align=(Align.MIN, Align.MIN, Align.MIN)).moved(Location((mitx_pcb_component_face_x, mitx_eps_power_rear_y, mitx_eps_power_bottom_z)))
publish('mitx_eps_power', mitx_eps_power, 'CPU power header')

mitx_chipset_depth_x = param('mitx_chipset_depth_x', 8.0)
mitx_chipset_width_y = param('mitx_chipset_width_y', 36.0)
mitx_chipset_height_z = param('mitx_chipset_height_z', 36.0)
mitx_chipset_center_y = param('mitx_chipset_center_y', -15.0)
mitx_chipset_center_z = param('mitx_chipset_center_z', 111.0)
mitx_chipset = Box(mitx_chipset_depth_x, mitx_chipset_width_y, mitx_chipset_height_z, align=(Align.MIN, Align.CENTER, Align.CENTER)).moved(Location((mitx_pcb_component_face_x, mitx_chipset_center_y, mitx_chipset_center_z)))
publish('mitx_chipset', mitx_chipset, 'Chipset heatsink')

# Required Thermalright AXP120-X67 mechanical envelope on the +X component side.
mitx_axp120x67_depth_x = param('mitx_axp120x67_depth_x', 67.0)
mitx_axp120x67_width_y = param('mitx_axp120x67_width_y', 123.5)
mitx_axp120x67_height_z = param('mitx_axp120x67_height_z', 120.0)
mitx_axp120x67_base_x = param('mitx_axp120x67_base_x', 5.8)
mitx_axp120x67_center_y = param('mitx_axp120x67_center_y', -42.0)
mitx_axp120x67_center_z = param('mitx_axp120x67_center_z', 169.0)
mitx_axp120x67_envelope = Box(mitx_axp120x67_depth_x, mitx_axp120x67_width_y, mitx_axp120x67_height_z, align=(Align.MIN, Align.CENTER, Align.CENTER)).moved(Location((mitx_axp120x67_base_x, mitx_axp120x67_center_y, mitx_axp120x67_center_z)))
publish('mitx_axp120x67_envelope', mitx_axp120x67_envelope, 'AXP120-X67 envelope')

mitx_axp120x67_fan_diameter = param('mitx_axp120x67_fan_diameter', 120.0)
mitx_axp120x67_fan_hub_diameter = param('mitx_axp120x67_fan_hub_diameter', 32.0)
mitx_axp120x67_fan_ring_width = param('mitx_axp120x67_fan_ring_width', 2.0)
mitx_axp120x67_fan_thickness_x = param('mitx_axp120x67_fan_thickness_x', 1.0)
mitx_axp120x67_fan_plane_x = param('mitx_axp120x67_fan_plane_x', 72.8)
mitx_axp120x67_fan_outer = Cylinder(mitx_axp120x67_fan_diameter / 2, mitx_axp120x67_fan_thickness_x, align=(Align.CENTER, Align.CENTER, Align.CENTER)).rotate(Axis.Y, 90).moved(Location((mitx_axp120x67_fan_plane_x, mitx_axp120x67_center_y, mitx_axp120x67_center_z)))
mitx_axp120x67_fan_inner = Cylinder((mitx_axp120x67_fan_diameter - 2 * mitx_axp120x67_fan_ring_width) / 2, mitx_axp120x67_fan_thickness_x + 0.4, align=(Align.CENTER, Align.CENTER, Align.CENTER)).rotate(Axis.Y, 90).moved(Location((mitx_axp120x67_fan_plane_x, mitx_axp120x67_center_y, mitx_axp120x67_center_z)))
mitx_axp120x67_fan_ring = mitx_axp120x67_fan_outer - mitx_axp120x67_fan_inner
mitx_axp120x67_fan_hub = Cylinder(mitx_axp120x67_fan_hub_diameter / 2, mitx_axp120x67_fan_thickness_x, align=(Align.CENTER, Align.CENTER, Align.CENTER)).rotate(Axis.Y, 90).moved(Location((mitx_axp120x67_fan_plane_x, mitx_axp120x67_center_y, mitx_axp120x67_center_z)))
publish('mitx_axp120x67_fan', Compound(children=[mitx_axp120x67_fan_ring, mitx_axp120x67_fan_hub]), 'AXP120-X67 fan')

assert abs(mitx_pcb_plane_x - 4.2) < 0.001
assert abs(mitx_pcb_width_y - 170.0) < 0.001 and abs(mitx_pcb_height_z - 170.0) < 0.001
assert abs((mitx_pcb_holes_yz[1][0] - mitx_pcb_holes_yz[0][0]) - 154.94) < 0.001
assert abs((mitx_pcb_holes_yz[3][0] - mitx_pcb_holes_yz[2][0]) - 132.08) < 0.001
assert abs((mitx_pcb_holes_yz[2][1] - mitx_pcb_holes_yz[0][1]) - 157.48) < 0.001
assert abs((mitx_pcb_holes_yz[2][0] - mitx_pcb_holes_yz[0][0]) - 22.86) < 0.001
assert len(mitx_pcb_holes_yz) == 4
assert len(mitx_active_mount_holes_yz) == 3
assert mitx_pcb_holes_yz[MITX_RETIRED_FRONT_LOWER_HOLE_INDEX] not in mitx_active_mount_holes_yz
assert abs((mitx_pcb_solder_face_x - mitx_io_shield_x0) - MITX_IO_APERTURE_BELOW_PCB_SOLDER_FACE_MM) < 0.001
assert MITX_IO_APERTURE_DATUM_TOLERANCE_MM == 0.25
assert mitx_io_shield_x0 < mitx_pcb_solder_face_x < mitx_pcb_component_face_x
assert abs((mitx_io_shield_z0 + MITX_IO_APERTURE_LONG_Z_MM) - (mitx_pcb_top_z + mitx_io_shield_top_overhang_z)) < 0.001
assert mitx_io_shield_top_overhang_z > 0.0
assert abs((mitx_io_shield_center_y + mitx_io_shield_thickness_y / 2) - mitx_pcb_rear_edge_y) < 0.001
assert 0.8 <= mitx_io_shield_thickness_y <= 1.4
assert mitx_axp120x67_base_x > -11.0
assert mitx_axp120x67_base_x + mitx_axp120x67_depth_x < 74.0
print(
    f'MINI_ITX_THREE_MOUNT_REFERENCE_PASS: PCB retains {len(mitx_pcb_holes_yz)} standard holes; '
    f'enclosure mount reference shows {len(mitx_active_mount_holes_yz)} active rings with the lower-front point retired. '
    f'IO top overhang={mitx_io_shield_top_overhang_z:.2f} mm, shield t={mitx_io_shield_thickness_y:.2f} mm.'
)