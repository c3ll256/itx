# Final placement correction from the active rear GPU-opening datum.
# The complete graphics-card assembly moves rigidly: bracket, rear I/O, body,
# cooling hardware and PCIe fingers all follow the opening datum. The card body
# remains 7.5 mm below the metal bracket. Final acceptance compares this GPU
# opening datum with the Mini-ITX rear-I/O chassis opening lower edge.
gpu_opening_bottom_z = param('gpu_opening_bottom_z', 84.99)
gpu_bottom_below_pcie_opening_z = param('gpu_bottom_below_pcie_opening_z', 7.5)
gpu_measured_bottom_z = gpu_opening_bottom_z - gpu_bottom_below_pcie_opening_z
gpu_body_datum_correction_z = gpu_measured_bottom_z - COLORFUL_BOTTOM_Z
gpu_bracket_datum_correction_z = gpu_opening_bottom_z - COLORFUL_BOTTOM_Z
gpu_body_correction = Location((0, 0, gpu_body_datum_correction_z))
gpu_bracket_correction = Location((0, 0, gpu_bracket_datum_correction_z))

gpu_ref_shroud = gpu_ref_shroud.moved(gpu_body_correction)
gpu_ref_pcb = gpu_ref_pcb.moved(gpu_body_correction)
gpu_ref_fans = [shape.moved(gpu_body_correction) for shape in gpu_ref_fans]
gpu_ref_fins = [shape.moved(gpu_body_correction) for shape in gpu_ref_fins]
gpu_ref_pcie_fingers = gpu_ref_pcie_fingers.moved(gpu_body_correction)

gpu_ref_bracket_plate = gpu_ref_bracket_plate.moved(gpu_bracket_correction)
gpu_ref_mount_ear = gpu_ref_mount_ear.moved(gpu_bracket_correction)
gpu_ref_bracket = gpu_ref_bracket.moved(gpu_bracket_correction)
gpu_ref_ports = [shape.moved(gpu_bracket_correction) for shape in gpu_ref_ports]
gpu_ref_vents = [shape.moved(gpu_bracket_correction) for shape in gpu_ref_vents]

assert abs(gpu_opening_bottom_z - gpu_ref_shroud.bounding_box().min.Z - gpu_bottom_below_pcie_opening_z) < 0.01
assert abs(gpu_ref_bracket_plate.bounding_box().min.Z - gpu_opening_bottom_z) < 0.01
assert abs(gpu_ref_mount_ear.bounding_box().max.Z - gpu_opening_bottom_z) < 0.01
publish('gpu_shroud', gpu_ref_shroud, 'Colorful GPU body')
publish('gpu_pcb', gpu_ref_pcb, 'Colorful GPU PCB')
publish('gpu_rear_bracket', gpu_ref_bracket, 'Flipped dual-slot bracket')
publish('gpu_display_ports', Compound(children=gpu_ref_ports), 'Flipped HDMI and DP')
publish('gpu_rear_vents', Compound(children=gpu_ref_vents), 'Flipped rear vents')
publish('gpu_fan', Compound(children=gpu_ref_fans), 'Outward dual fans')
publish('gpu_heatsink', Compound(children=gpu_ref_fins), 'Colorful heatsink fins')
publish('gpu_pcie_fingers', gpu_ref_pcie_fingers, 'Upward PCIe fingers')
print(
    f'GPU_REAR_OPENING_DATUM: opening bottom={gpu_opening_bottom_z:.2f} mm; '
    f'GPU body bottom={gpu_measured_bottom_z:.2f} mm; '
    f'body remains {gpu_bottom_below_pcie_opening_z:.1f} mm below bracket datum.'
)