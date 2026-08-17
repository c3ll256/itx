# Colorful RTX 3060 fit audit using the correct length datum.
# Official 253.4 mm is the overall dimension from the rear L-ear to the card
# nose; the cooler body starts 8.8 mm forward of that ear and is 244.6 mm long.
COLORFUL_GPU_OFFICIAL_OVERALL_MM = 253.4
COLORFUL_GPU_L_EAR_PROJECTION_MM = 8.8
COLORFUL_GPU_BODY_LENGTH_MM = COLORFUL_GPU_OFFICIAL_OVERALL_MM - COLORFUL_GPU_L_EAR_PROJECTION_MM
COLORFUL_GPU_BODY_REAR_Y_MM = -125.2
COLORFUL_GPU_L_EAR_REAR_Y_MM = COLORFUL_GPU_BODY_REAR_Y_MM - COLORFUL_GPU_L_EAR_PROJECTION_MM
COLORFUL_GPU_HEIGHT_MM = 132.5
COLORFUL_GPU_THICKNESS_MM = 41.0

gpu_min_length_clearance = param('gpu_min_length_clearance', 0.5)
gpu_height_clearance = param('gpu_height_clearance', 4.0)
gpu_thickness_clearance = param('gpu_thickness_clearance', 4.0)

front_inner_y = D / 2.0 - panel_t
body_front_y = COLORFUL_GPU_BODY_REAR_Y_MM + COLORFUL_GPU_BODY_LENGTH_MM
body_front_clearance = front_inner_y - body_front_y
overall_from_l_ear = body_front_y - COLORFUL_GPU_L_EAR_REAR_Y_MM
inner_width_x = W - 2 * (panel_t + clearance)
inner_height_z = H - base_t - cap_t

assert 256.0 - 0.001 <= D <= 260.0 + 0.001
assert abs(COLORFUL_GPU_BODY_LENGTH_MM - 244.6) < 0.01
assert abs(overall_from_l_ear - COLORFUL_GPU_OFFICIAL_OVERALL_MM) < 0.01
assert body_front_clearance >= gpu_min_length_clearance
assert inner_width_x >= COLORFUL_GPU_THICKNESS_MM + gpu_thickness_clearance
assert inner_height_z >= COLORFUL_GPU_HEIGHT_MM + gpu_height_clearance

publish('base', base, 'Correct GPU datum base')
publish('top_cap', top_cap, 'Correct GPU datum top')
publish('front_panel', front_panel, 'Correct GPU datum front')
publish('rear_panel', rear_panel, 'Correct GPU datum rear')
publish('left_panel', left_panel, 'Correct GPU datum left')
publish('right_panel', right_panel, 'Correct GPU datum right')
print(
    f'COLORFUL_GPU_DATUM_PASS: official overall={COLORFUL_GPU_OFFICIAL_OVERALL_MM:.1f} mm '
    f'from L-ear y={COLORFUL_GPU_L_EAR_REAR_Y_MM:.1f} to nose y={body_front_y:.1f}; '
    f'body={COLORFUL_GPU_BODY_LENGTH_MM:.1f} mm; front-inner={front_inner_y:.1f}; '
    f'body clearance={body_front_clearance:.1f} mm.'
)