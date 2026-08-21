# Final placement correction from the current committed PCIe aperture datum.
# The user's 7.5 mm measurement applies to the cooler/shroud body bottom, not to
# the metal rear bracket. The bracket and its I/O details remain aligned to the
# PCIe opening and retention screws while the body extends 7.5 mm below it.
CURRENT_PCIE_OPENING_BOTTOM_Z_MM = 97.0
gpu_bottom_below_pcie_opening_z = param('gpu_bottom_below_pcie_opening_z', 7.5)
gpu_measured_bottom_z = CURRENT_PCIE_OPENING_BOTTOM_Z_MM - gpu_bottom_below_pcie_opening_z
gpu_body_datum_correction_z = gpu_measured_bottom_z - COLORFUL_BOTTOM_Z
gpu_bracket_datum_correction_z = CURRENT_PCIE_OPENING_BOTTOM_Z_MM - COLORFUL_BOTTOM_Z
gpu_body_correction = Location((0, 0, gpu_body_datum_correction_z))
gpu_bracket_correction = Location((0, 0, gpu_bracket_datum_correction_z))

gpu_ref_shroud = gpu_ref_shroud.moved(gpu_body_correction)
gpu_ref_pcb = gpu_ref_pcb.moved(gpu_body_correction)
gpu_ref_fans = [shape.moved(gpu_body_correction) for shape in gpu_ref_fans]
gpu_ref_fins = [shape.moved(gpu_body_correction) for shape in gpu_ref_fins]
gpu_ref_pcie_fingers = gpu_ref_pcie_fingers.moved(gpu_body_correction)
gpu_ref_power_zone = gpu_ref_power_zone.moved(gpu_body_correction)

gpu_ref_bracket_plate = gpu_ref_bracket_plate.moved(gpu_bracket_correction)
gpu_ref_mount_ear = gpu_ref_mount_ear.moved(gpu_bracket_correction)
gpu_ref_bracket = gpu_ref_bracket.moved(gpu_bracket_correction)
# Ports and vents are already authored in the fixed PCIe-opening coordinate
# system, so they intentionally receive no body-bottom correction.

assert abs(gpu_ref_shroud.bounding_box().min.Z - 89.5) < 0.01
assert abs(CURRENT_PCIE_OPENING_BOTTOM_Z_MM - gpu_ref_shroud.bounding_box().min.Z - 7.5) < 0.01
assert abs(gpu_ref_bracket_plate.bounding_box().min.Z - CURRENT_PCIE_OPENING_BOTTOM_Z_MM) < 0.01
assert abs(gpu_ref_mount_ear.bounding_box().max.Z - CURRENT_PCIE_OPENING_BOTTOM_Z_MM) < 0.01
publish('gpu_shroud', gpu_ref_shroud, 'Colorful GPU body')
publish('gpu_pcb', gpu_ref_pcb, 'Colorful GPU PCB')
publish('gpu_rear_bracket', gpu_ref_bracket, 'Flipped dual-slot bracket')
publish('gpu_display_ports', Compound(children=gpu_ref_ports), 'Flipped HDMI and DP')
publish('gpu_rear_vents', Compound(children=gpu_ref_vents), 'Flipped rear vents')
publish('gpu_fan', Compound(children=gpu_ref_fans), 'Outward dual fans')
publish('gpu_heatsink', Compound(children=gpu_ref_fins), 'Colorful heatsink fins')
publish('gpu_pcie_fingers', gpu_ref_pcie_fingers, 'Upward PCIe fingers')
publish('gpu_power_zone', gpu_ref_power_zone, 'Lower inverted 8-pin zone')
print(
    f'GPU_MEASURED_BOTTOM_DATUM_PASS: PCIe opening bottom={CURRENT_PCIE_OPENING_BOTTOM_Z_MM:.1f} mm; '
    f'body bottom={gpu_measured_bottom_z:.1f} mm; bracket remains at opening datum; '
    f'body offset={gpu_bottom_below_pcie_opening_z:.1f} mm.'
)