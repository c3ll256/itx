# Permanent physical audit for the rolled Colorful GPU and its correct
# bracket-inclusive length datum.
gpu_orientation_tolerance = param('gpu_orientation_tolerance', 0.05)
gpu_orientation_min_fan_outboard = param('gpu_orientation_min_fan_outboard', 0.5)
gpu_orientation_min_pcb_inboard = param('gpu_orientation_min_pcb_inboard', 1.0)
gpu_orientation_finger_top_overlap = param('gpu_orientation_finger_top_overlap', 0.05)
gpu_body_min_nose_inset = param('gpu_body_min_nose_inset', 1.0)

shroud_bb = gpu_ref_shroud.bounding_box()
fan_bb = Compound(children=gpu_ref_fans).bounding_box()
pcb_bb = gpu_ref_pcb.bounding_box()
fins_bb = Compound(children=gpu_ref_fins).bounding_box()
finger_bb = gpu_ref_pcie_fingers.bounding_box()
power_bb = gpu_ref_power_zone.bounding_box()
bracket_plate_bb = gpu_ref_bracket_plate.bounding_box()
mount_ear_bb = gpu_ref_mount_ear.bounding_box()
ports_bb = Compound(children=gpu_ref_ports).bounding_box()
vents_bb = Compound(children=gpu_ref_vents).bounding_box()

assert fan_bb.max.X <= shroud_bb.min.X + gpu_orientation_tolerance
assert shroud_bb.min.X - fan_bb.min.X >= gpu_orientation_min_fan_outboard
assert pcb_bb.min.X >= gpu_ref_center_x + gpu_orientation_min_pcb_inboard
assert finger_bb.min.Z >= shroud_bb.max.Z - gpu_orientation_finger_top_overlap
assert power_bb.max.Z <= shroud_bb.min.Z + gpu_orientation_tolerance
assert mount_ear_bb.max.Z <= bracket_plate_bb.min.Z + gpu_orientation_tolerance
assert ports_bb.center().Z > vents_bb.center().Z

# Longitudinal datum checks: official overall starts at the L-ear, while every
# body feature must stay inside the shorter cooler/shroud envelope.
official_overall_y = shroud_bb.max.Y - mount_ear_bb.min.Y
assert abs(shroud_bb.size.Y - COLORFUL_BODY_LENGTH_Y) < 0.01
assert abs(official_overall_y - COLORFUL_OFFICIAL_OVERALL_LENGTH_Y) < 0.01
assert shroud_bb.max.Y - pcb_bb.max.Y >= gpu_body_min_nose_inset
assert shroud_bb.max.Y - fins_bb.max.Y >= gpu_body_min_nose_inset
assert power_bb.max.Y <= shroud_bb.max.Y + gpu_orientation_tolerance

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
    f'GPU_DATUM_ORIENTATION_PASS: official overall={official_overall_y:.1f} mm from L-ear; '
    f'body={shroud_bb.size.Y:.1f} mm; PCB nose inset={shroud_bb.max.Y-pcb_bb.max.Y:.1f} mm; '
    f'heatsink nose inset={shroud_bb.max.Y-fins_bb.max.Y:.1f} mm; '
    f'fingers up and fans on outer -X face.'
)