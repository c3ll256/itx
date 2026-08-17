# Standard Mini-ITX mechanical reference, not a claim of a specific retail motherboard.
# Corrected installation: PCB at x=4.2 mm, mounting support on -X, components and cooler toward +X.
# Mount coordinates come from the standard asymmetric Figure 3 pattern; those
# external dimensions are constants rather than user-editable parameters.
mitx_pcb_thickness = param('mitx_pcb_thickness', 1.6)
mitx_pcb_width_y = param('mitx_pcb_width_y', 170.0)
mitx_pcb_height_z = param('mitx_pcb_height_z', 170.0)
mitx_pcb_mount_hole_diameter = param('mitx_pcb_mount_hole_diameter', 3.96)
mitx_pcb_plane_x = param('mitx_pcb_plane_x', 4.2)
mitx_pcb_rear_edge_y = param('mitx_pcb_rear_edge_y', -126.0)
mitx_pcb_bottom_z = param('mitx_pcb_bottom_z', 71.5)
MITX_REAR_LOWER_FROM_REAR_MM = 10.16
MITX_FRONT_LOWER_FROM_REAR_MM = 165.10
MITX_REAR_UPPER_FROM_REAR_MM = 33.02
MITX_FRONT_UPPER_FROM_REAR_MM = 165.10
MITX_LOWER_FROM_TOP_MM = 163.83
MITX_UPPER_FROM_TOP_MM = 6.35
mitx_pcb_rear_lower_from_rear = MITX_REAR_LOWER_FROM_REAR_MM
mitx_pcb_front_lower_from_rear = MITX_FRONT_LOWER_FROM_REAR_MM
mitx_pcb_rear_upper_from_rear = MITX_REAR_UPPER_FROM_REAR_MM
mitx_pcb_front_upper_from_rear = MITX_FRONT_UPPER_FROM_REAR_MM
mitx_pcb_lower_from_top = MITX_LOWER_FROM_TOP_MM
mitx_pcb_upper_from_top = MITX_UPPER_FROM_TOP_MM
mitx_pcb = Box(mitx_pcb_thickness, mitx_pcb_width_y, mitx_pcb_height_z, align=(Align.MIN, Align.MIN, Align.MIN)).moved(Location((mitx_pcb_plane_x, mitx_pcb_rear_edge_y, mitx_pcb_bottom_z)))
mitx_pcb_top_z = mitx_pcb_bottom_z + mitx_pcb_height_z
mitx_pcb_component_face_x = mitx_pcb_plane_x + mitx_pcb_thickness
mitx_pcb_holes_yz = [
    (mitx_pcb_rear_edge_y + mitx_pcb_rear_lower_from_rear, mitx_pcb_top_z - mitx_pcb_lower_from_top),
    (mitx_pcb_rear_edge_y + mitx_pcb_front_lower_from_rear, mitx_pcb_top_z - mitx_pcb_lower_from_top),
    (mitx_pcb_rear_edge_y + mitx_pcb_rear_upper_from_rear, mitx_pcb_top_z - mitx_pcb_upper_from_top),
    (mitx_pcb_rear_edge_y + mitx_pcb_front_upper_from_rear, mitx_pcb_top_z - mitx_pcb_upper_from_top),
]
for mitx_hole_y, mitx_hole_z in mitx_pcb_holes_yz:
    mitx_hole = Cylinder(mitx_pcb_mount_hole_diameter / 2, mitx_pcb_thickness + 2.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)).rotate(Axis.Y, 90).moved(Location((mitx_pcb_plane_x + mitx_pcb_thickness / 2, mitx_hole_y, mitx_hole_z)))
    mitx_pcb = mitx_pcb - mitx_hole
publish('mitx_pcb', mitx_pcb.clean(), 'Mini-ITX PCB reference')

mitx_mount_rings_outer_diameter = param('mitx_mount_rings_outer_diameter', 7.0)
mitx_mount_rings_inner_diameter = param('mitx_mount_rings_inner_diameter', 3.96)
mitx_mount_rings_thickness_x = param('mitx_mount_rings_thickness_x', 0.25)
mitx_mount_rings_plane_x = param('mitx_mount_rings_plane_x', 4.2)
mitx_mount_rings = []
for mitx_ring_y, mitx_ring_z in mitx_pcb_holes_yz:
    mitx_ring_outer = Cylinder(mitx_mount_rings_outer_diameter / 2, mitx_mount_rings_thickness_x, align=(Align.CENTER, Align.CENTER, Align.CENTER)).rotate(Axis.Y, 90).moved(Location((mitx_mount_rings_plane_x - mitx_mount_rings_thickness_x / 2, mitx_ring_y, mitx_ring_z)))
    mitx_ring_inner = Cylinder(mitx_mount_rings_inner_diameter / 2, mitx_mount_rings_thickness_x + 0.4, align=(Align.CENTER, Align.CENTER, Align.CENTER)).rotate(Axis.Y, 90).moved(Location((mitx_mount_rings_plane_x - mitx_mount_rings_thickness_x / 2, mitx_ring_y, mitx_ring_z)))
    mitx_mount_rings.append(mitx_ring_outer - mitx_ring_inner)
publish('mitx_mount_rings', Compound(children=mitx_mount_rings), 'Four mounting rings')

mitx_rear_io_depth_y = param('mitx_rear_io_depth_y', 12.0)
mitx_rear_io_height_z = param('mitx_rear_io_height_z', 44.45)
mitx_rear_io_width_x = param('mitx_rear_io_width_x', 34.0)
mitx_rear_io_bottom_z = param('mitx_rear_io_bottom_z', 88.0)
mitx_rear_io_base_x = param('mitx_rear_io_base_x', 5.8)
mitx_rear_io_port_gap_z = param('mitx_rear_io_port_gap_z', 1.5)
mitx_rear_io_port_count = 4
mitx_rear_io_port_h = (mitx_rear_io_height_z - mitx_rear_io_port_gap_z * (mitx_rear_io_port_count - 1)) / mitx_rear_io_port_count
mitx_rear_io_ports = []
for mitx_port_i in range(mitx_rear_io_port_count):
    mitx_rear_io_ports.append(Box(mitx_rear_io_width_x, mitx_rear_io_depth_y, mitx_rear_io_port_h, align=(Align.MIN, Align.MAX, Align.MIN)).moved(Location((mitx_rear_io_base_x, mitx_pcb_rear_edge_y, mitx_rear_io_bottom_z + mitx_port_i * (mitx_rear_io_port_h + mitx_rear_io_port_gap_z)))))
publish('mitx_rear_io', Compound(children=mitx_rear_io_ports), 'Rear I-O envelope')

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

# Required Thermalright AXP120-X67 mechanical envelope on the corrected +X component side.
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
assert mitx_axp120x67_base_x > -11.0
assert mitx_axp120x67_base_x + mitx_axp120x67_depth_x < 74.0
print('MINI_ITX_STANDARD_PATTERN_PASS: PCB and four mounts use the standard asymmetric 157.48 mm I/O-edge-axis spacing; components and AXP120-X67 face +X.')