# Colorful RTX 3060 fit audit against the user-measured card dimensions.
# The card body without the PCIe bracket is 241 mm; the bracket L-ear adds
# 8.8 mm behind it. These are measurements of the physical card.
COLORFUL_GPU_BODY_LENGTH_MM = 241.0
COLORFUL_GPU_L_EAR_PROJECTION_MM = 8.8
COLORFUL_GPU_OFFICIAL_OVERALL_MM = COLORFUL_GPU_BODY_LENGTH_MM + COLORFUL_GPU_L_EAR_PROJECTION_MM
COLORFUL_GPU_BODY_REAR_Y_MM = -125.2
COLORFUL_GPU_L_EAR_REAR_Y_MM = COLORFUL_GPU_BODY_REAR_Y_MM - COLORFUL_GPU_L_EAR_PROJECTION_MM
COLORFUL_GPU_HEIGHT_MM = 132.5
COLORFUL_GPU_THICKNESS_MM = 41.0

gpu_min_length_clearance = param('gpu_min_length_clearance', 0.5)
gpu_height_clearance = param('gpu_height_clearance', 4.0)
gpu_thickness_clearance = param('gpu_thickness_clearance', 4.0)
gpu_min_fan_intake_gap_x = param('gpu_min_fan_intake_gap_x', 6.0)
gpu_min_board_side_gap_x = param('gpu_min_board_side_gap_x', 12.0)

front_inner_y = D / 2.0 - panel_t
body_front_y = COLORFUL_GPU_BODY_REAR_Y_MM + COLORFUL_GPU_BODY_LENGTH_MM
body_front_clearance = front_inner_y - body_front_y
overall_from_l_ear = body_front_y - COLORFUL_GPU_L_EAR_REAR_Y_MM
inner_width_x = W - 2 * (panel_t + clearance)
inner_height_z = H - base_t - cap_t

# The card now sits on the same axis as the moved PCIe aperture.
gpu_body_center_x = slot_center_x
gpu_body_outboard_face_x = gpu_body_center_x - board_side * -COLORFUL_GPU_THICKNESS_MM / 2
gpu_fan_side_face_x = gpu_body_center_x - COLORFUL_GPU_THICKNESS_MM / 2
gpu_board_side_face_x = gpu_body_center_x + COLORFUL_GPU_THICKNESS_MM / 2
side_panel_inner_x = -(W / 2 - panel_t)
gpu_fan_intake_gap_x = gpu_fan_side_face_x - side_panel_inner_x
gpu_board_side_gap_x = board_plane_x - gpu_board_side_face_x

assert 256.0 - 0.001 <= D <= 260.0 + 0.001
assert abs(overall_from_l_ear - COLORFUL_GPU_OFFICIAL_OVERALL_MM) < 0.01
assert body_front_clearance >= gpu_min_length_clearance
assert inner_width_x >= COLORFUL_GPU_THICKNESS_MM + gpu_thickness_clearance
assert inner_height_z >= COLORFUL_GPU_HEIGHT_MM + gpu_height_clearance
assert gpu_fan_intake_gap_x >= gpu_min_fan_intake_gap_x
assert gpu_board_side_gap_x >= gpu_min_board_side_gap_x

publish('base', base, 'Correct GPU datum base')
publish('top_cap', top_cap, 'Correct GPU datum top')
publish('front_panel', front_panel, 'Correct GPU datum front')
publish('rear_panel', rear_panel, 'Correct GPU datum rear')
publish('left_panel', left_panel, 'Correct GPU datum left')
publish('right_panel', right_panel, 'Correct GPU datum right')
print(
    f'COLORFUL_GPU_DATUM_PASS: body={COLORFUL_GPU_BODY_LENGTH_MM:.1f} mm without bracket, '
    f'overall={COLORFUL_GPU_OFFICIAL_OVERALL_MM:.1f} mm from L-ear y={COLORFUL_GPU_L_EAR_REAR_Y_MM:.1f} '
    f'to nose y={body_front_y:.1f}; front gap={body_front_clearance:.1f} mm.'
)
print(
    f'GPU_LATERAL_POSITION: card centre x={gpu_body_center_x:.1f} mm; '
    f'fan-side intake gap={gpu_fan_intake_gap_x:.1f} mm to the side panel; '
    f'board-side gap={gpu_board_side_gap_x:.1f} mm to the motherboard plane.'
)
