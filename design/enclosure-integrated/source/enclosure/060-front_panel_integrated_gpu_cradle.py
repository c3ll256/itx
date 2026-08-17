# Internal far-end U cradle for the corrected Colorful RTX 3060 body length.
# The official 253.4 mm dimension starts at the rear PCIe bracket L-ear;
# the cooler body itself is 244.6 mm and ends 6.6 mm before the front-panel
# inner face. No external nose bulge or front-panel pocket is required.
COLORFUL_GPU_OFFICIAL_OVERALL_MM = 253.4
COLORFUL_GPU_L_EAR_PROJECTION_MM = 8.8
COLORFUL_GPU_BODY_LENGTH_MM = COLORFUL_GPU_OFFICIAL_OVERALL_MM - COLORFUL_GPU_L_EAR_PROJECTION_MM
COLORFUL_GPU_THICKNESS_MM = 41.0
COLORFUL_GPU_HEIGHT_MM = 132.5
COLORFUL_GPU_BODY_REAR_Y_MM = -125.2

front_gpu_cradle_center_x = param('front_gpu_cradle_center_x', -31.0)
front_gpu_cradle_reference_bottom_z = param('front_gpu_cradle_reference_bottom_z', 97.0)
front_gpu_cradle_end_engagement_y = param('front_gpu_cradle_end_engagement_y', 5.0)
front_gpu_cradle_side_clearance_x = param('front_gpu_cradle_side_clearance_x', 1.2)
front_gpu_cradle_pad_gap_z = param('front_gpu_cradle_pad_gap_z', 1.0)
front_gpu_cradle_wall_x = param('front_gpu_cradle_wall_x', 3.0)
front_gpu_cradle_shelf_thickness_z = param('front_gpu_cradle_shelf_thickness_z', 3.0)
front_gpu_cradle_side_height_z = param('front_gpu_cradle_side_height_z', 10.0)
front_gpu_cradle_root_depth_y = param('front_gpu_cradle_root_depth_y', 30.0)
front_gpu_cradle_root_height_z = param('front_gpu_cradle_root_height_z', 15.0)
front_gpu_cradle_root_overlap_z = param('front_gpu_cradle_root_overlap_z', 0.6)
front_gpu_panel_overlap_y = param('front_gpu_panel_overlap_y', 0.4)
front_gpu_power_corridor_width_x = param('front_gpu_power_corridor_width_x', 22.0)
front_gpu_power_corridor_length_y = param('front_gpu_power_corridor_length_y', 24.0)
front_gpu_power_corridor_height_z = param('front_gpu_power_corridor_height_z', 20.0)
front_gpu_power_corridor_center_exact_x = param('front_gpu_power_corridor_center_exact_x', -22.0)
front_gpu_power_corridor_center_y = param('front_gpu_power_corridor_center_y', 106.0)
front_gpu_power_corridor_center_z = param('front_gpu_power_corridor_center_z', 90.0)

assert abs(COLORFUL_GPU_BODY_LENGTH_MM - 244.6) < 0.01
assert front_gpu_cradle_side_clearance_x >= 1.0
assert front_gpu_cradle_pad_gap_z >= 0.8
assert front_gpu_panel_overlap_y >= 0.3

front_inner_y = D / 2.0 - panel_t
front_gpu_reference_end_y = COLORFUL_GPU_BODY_REAR_Y_MM + COLORFUL_GPU_BODY_LENGTH_MM
front_gpu_body_to_panel_clearance_y = front_inner_y - front_gpu_reference_end_y
assert front_gpu_body_to_panel_clearance_y >= 5.0

front_gpu_channel_start_y = front_gpu_reference_end_y - front_gpu_cradle_end_engagement_y
front_gpu_channel_end_y = front_inner_y + front_gpu_panel_overlap_y
front_gpu_channel_depth_y = front_gpu_channel_end_y - front_gpu_channel_start_y
front_gpu_channel_inner_w = COLORFUL_GPU_THICKNESS_MM + 2 * front_gpu_cradle_side_clearance_x
front_gpu_channel_outer_w = front_gpu_channel_inner_w + 2 * front_gpu_cradle_wall_x
front_gpu_shelf_top_z = front_gpu_cradle_reference_bottom_z - front_gpu_cradle_pad_gap_z
front_gpu_shelf_bottom_z = front_gpu_shelf_top_z - front_gpu_cradle_shelf_thickness_z
front_gpu_left_wall_x = front_gpu_cradle_center_x - front_gpu_channel_inner_w / 2 - front_gpu_cradle_wall_x / 2
front_gpu_right_wall_x = front_gpu_cradle_center_x + front_gpu_channel_inner_w / 2 + front_gpu_cradle_wall_x / 2

front_gpu_shelf = Box(
    front_gpu_channel_outer_w,
    front_gpu_channel_depth_y,
    front_gpu_cradle_shelf_thickness_z,
    align=(Align.CENTER, Align.MIN, Align.MIN),
).moved(Location((front_gpu_cradle_center_x, front_gpu_channel_start_y, front_gpu_shelf_bottom_z)))
front_gpu_left_rail = Box(
    front_gpu_cradle_wall_x,
    front_gpu_channel_depth_y,
    front_gpu_cradle_side_height_z,
    align=(Align.CENTER, Align.MIN, Align.MIN),
).moved(Location((front_gpu_left_wall_x, front_gpu_channel_start_y, front_gpu_shelf_bottom_z)))
front_gpu_right_rail = Box(
    front_gpu_cradle_wall_x,
    front_gpu_channel_depth_y,
    front_gpu_cradle_side_height_z,
    align=(Align.CENTER, Align.MIN, Align.MIN),
).moved(Location((front_gpu_right_wall_x, front_gpu_channel_start_y, front_gpu_shelf_bottom_z)))

front_gpu_root_y0 = front_inner_y - front_gpu_cradle_root_depth_y
front_gpu_root_depth = front_gpu_channel_end_y - front_gpu_root_y0
front_gpu_root_z0 = front_gpu_shelf_bottom_z - front_gpu_cradle_root_height_z
front_gpu_root_h = front_gpu_cradle_root_height_z + front_gpu_cradle_root_overlap_z
front_gpu_left_root = Box(
    front_gpu_cradle_wall_x,
    front_gpu_root_depth,
    front_gpu_root_h,
    align=(Align.CENTER, Align.MIN, Align.MIN),
).moved(Location((front_gpu_left_wall_x, front_gpu_root_y0, front_gpu_root_z0)))
front_gpu_right_root = Box(
    front_gpu_cradle_wall_x,
    front_gpu_root_depth,
    front_gpu_root_h,
    align=(Align.CENTER, Align.MIN, Align.MIN),
).moved(Location((front_gpu_right_wall_x, front_gpu_root_y0, front_gpu_root_z0)))

front_gpu_cradle_raw = (
    front_gpu_shelf
    + front_gpu_left_rail
    + front_gpu_right_rail
    + front_gpu_left_root
    + front_gpu_right_root
).clean()
# Preserve the user-owned lower 8-pin routing area. The cut ends before the
# front panel, leaving a rear bridge that keeps the cradle one connected body.
front_gpu_power_corridor = Box(
    front_gpu_power_corridor_width_x,
    front_gpu_power_corridor_length_y,
    front_gpu_power_corridor_height_z,
    align=(Align.CENTER, Align.CENTER, Align.CENTER),
).moved(Location((
    front_gpu_power_corridor_center_exact_x,
    front_gpu_power_corridor_center_y,
    front_gpu_power_corridor_center_z,
)))
front_gpu_cradle = (front_gpu_cradle_raw - front_gpu_power_corridor).clean()

front_gpu_reference_proxy = Box(
    COLORFUL_GPU_THICKNESS_MM,
    COLORFUL_GPU_BODY_LENGTH_MM,
    COLORFUL_GPU_HEIGHT_MM,
    align=(Align.CENTER, Align.MIN, Align.MIN),
).moved(Location((
    front_gpu_cradle_center_x,
    COLORFUL_GPU_BODY_REAR_Y_MM,
    front_gpu_cradle_reference_bottom_z,
)))
front_gpu_pad_proxy = Box(
    COLORFUL_GPU_THICKNESS_MM,
    front_gpu_cradle_end_engagement_y,
    front_gpu_cradle_pad_gap_z,
    align=(Align.CENTER, Align.MIN, Align.MIN),
).moved(Location((
    front_gpu_cradle_center_x,
    front_gpu_channel_start_y,
    front_gpu_shelf_top_z,
)))

assert front_gpu_cradle.solids().__len__() == 1
assert (front_gpu_cradle & front_panel).volume > 10.0
assert (front_panel & front_gpu_reference_proxy).volume < 0.01
assert (front_gpu_cradle & front_gpu_reference_proxy).volume < 0.01
assert (front_gpu_pad_proxy & front_gpu_cradle).volume < 0.01
assert (front_gpu_power_corridor & front_gpu_cradle).volume < 0.01

front_panel = (front_panel + front_gpu_cradle).clean()
assert front_panel.solids().__len__() == 1
assert front_panel.bounding_box().max.Y <= D / 2.0 + 0.01
publish('front_panel', front_panel, 'Internal GPU cradle')
print(
    f'COLORFUL_GPU_INTERNAL_CRADLE_PASS: body length={COLORFUL_GPU_BODY_LENGTH_MM:.1f} mm; '
    f'body end={front_gpu_reference_end_y:.1f}; front-inner={front_inner_y:.1f}; '
    f'free gap={front_gpu_body_to_panel_clearance_y:.1f} mm; no external bulge; 8-pin corridor open.'
)