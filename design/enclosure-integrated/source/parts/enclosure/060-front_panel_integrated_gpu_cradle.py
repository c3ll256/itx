# Internal far-end retaining cradle for the user-measured Colorful RTX 3060.
# The GPU body bottom is measured 7.5 mm below the active PCIe opening lower
# edge. The previous 8-pin power-corridor notch is intentionally removed per
# the user's physical fit check. Two vertical side plates locate the card in X
# while remaining open along Y so the front panel can slide off the GPU end.
COLORFUL_GPU_BODY_LENGTH_MM = 241.0
COLORFUL_GPU_L_EAR_PROJECTION_MM = 8.8
COLORFUL_GPU_OFFICIAL_OVERALL_MM = COLORFUL_GPU_BODY_LENGTH_MM + COLORFUL_GPU_L_EAR_PROJECTION_MM
COLORFUL_GPU_THICKNESS_MM = 41.0
COLORFUL_GPU_HEIGHT_MM = 132.5
COLORFUL_GPU_BODY_REAR_Y_MM = -125.2

front_gpu_cradle_center_x = slot_center_x
front_gpu_cradle_bottom_offset_from_pcie_z = param('front_gpu_cradle_bottom_offset_from_pcie_z', 7.5)
front_gpu_cradle_end_engagement_y = param('front_gpu_cradle_end_engagement_y', 5.0)
front_gpu_cradle_shelf_width_x = param('front_gpu_cradle_shelf_width_x', 41.0)
front_gpu_cradle_shelf_thickness_z = param('front_gpu_cradle_shelf_thickness_z', 3.0)
front_gpu_side_clearance_x = param('front_gpu_side_clearance_x', 1.0)
front_gpu_sidewall_thickness_x = param('front_gpu_sidewall_thickness_x', 3.0)
front_gpu_sidewall_height_z = param('front_gpu_sidewall_height_z', 12.0)
front_gpu_cradle_rib_thickness_x = param('front_gpu_cradle_rib_thickness_x', 3.0)
front_gpu_cradle_rib_depth_y = param('front_gpu_cradle_rib_depth_y', 18.0)
front_gpu_cradle_rib_height_z = param('front_gpu_cradle_rib_height_z', 14.0)
front_gpu_cradle_rib_edge_inset_x = param('front_gpu_cradle_rib_edge_inset_x', 5.0)
front_gpu_cradle_root_overlap_z = param('front_gpu_cradle_root_overlap_z', 0.6)
front_gpu_panel_overlap_y = param('front_gpu_panel_overlap_y', 0.4)

assert front_gpu_cradle_bottom_offset_from_pcie_z > 0.0
assert front_gpu_cradle_shelf_width_x >= COLORFUL_GPU_THICKNESS_MM
assert front_gpu_cradle_shelf_thickness_z >= 3.0
assert front_gpu_side_clearance_x >= 0.8
assert front_gpu_sidewall_thickness_x >= 2.0
assert front_gpu_sidewall_height_z >= 8.0
assert front_gpu_cradle_rib_thickness_x >= 3.0
assert front_gpu_cradle_rib_height_z >= 10.0
assert front_gpu_panel_overlap_y >= 0.3

front_inner_y = D / 2.0 - panel_t
front_gpu_reference_end_y = COLORFUL_GPU_BODY_REAR_Y_MM + COLORFUL_GPU_BODY_LENGTH_MM
front_gpu_body_to_panel_clearance_y = front_inner_y - front_gpu_reference_end_y
assert front_gpu_body_to_panel_clearance_y >= 5.0

# User measurement: GPU bottom/support plane is 7.5 mm below the PCIe opening.
front_gpu_cradle_reference_bottom_z = slot_z0 - front_gpu_cradle_bottom_offset_from_pcie_z
front_gpu_shelf_top_z = front_gpu_cradle_reference_bottom_z
front_gpu_shelf_bottom_z = front_gpu_shelf_top_z - front_gpu_cradle_shelf_thickness_z
front_gpu_channel_start_y = front_gpu_reference_end_y - front_gpu_cradle_end_engagement_y
front_gpu_channel_end_y = front_inner_y + front_gpu_panel_overlap_y
front_gpu_channel_depth_y = front_gpu_channel_end_y - front_gpu_channel_start_y

# The floor spans beneath both side plates. The named shelf width remains the
# GPU bearing width; clearance and wall stock grow outward from it.
front_gpu_sidewall_inner_gap_x = front_gpu_cradle_shelf_width_x + 2.0 * front_gpu_side_clearance_x
front_gpu_tray_outer_width_x = front_gpu_sidewall_inner_gap_x + 2.0 * front_gpu_sidewall_thickness_x
front_gpu_shelf = Box(
    front_gpu_tray_outer_width_x,
    front_gpu_channel_depth_y,
    front_gpu_cradle_shelf_thickness_z,
    align=(Align.CENTER, Align.MIN, Align.MIN),
).moved(Location((front_gpu_cradle_center_x, front_gpu_channel_start_y, front_gpu_shelf_bottom_z)))

# Two continuous plates capture lateral motion without a top bridge. Because
# they run along Y and are open toward the card, front-panel removal remains a
# straight slide along the GPU length.
front_gpu_sidewall_total_height_z = front_gpu_cradle_shelf_thickness_z + front_gpu_sidewall_height_z
front_gpu_sidewall_offset_x = front_gpu_sidewall_inner_gap_x / 2.0 + front_gpu_sidewall_thickness_x / 2.0
front_gpu_sidewall_xs = (
    front_gpu_cradle_center_x - front_gpu_sidewall_offset_x,
    front_gpu_cradle_center_x + front_gpu_sidewall_offset_x,
)
front_gpu_sidewalls = [
    Box(
        front_gpu_sidewall_thickness_x,
        front_gpu_channel_depth_y,
        front_gpu_sidewall_total_height_z,
        align=(Align.CENTER, Align.MIN, Align.MIN),
    ).moved(Location((wall_x, front_gpu_channel_start_y, front_gpu_shelf_bottom_z)))
    for wall_x in front_gpu_sidewall_xs
]

# Three full-depth ribs stiffen the now-continuous floor and its front-panel root.
front_gpu_rib_y0 = front_inner_y - front_gpu_cradle_rib_depth_y
front_gpu_rib_actual_depth_y = front_gpu_channel_end_y - front_gpu_rib_y0
front_gpu_rib_top_z = front_gpu_shelf_bottom_z + front_gpu_cradle_root_overlap_z
front_gpu_rib_bottom_z = front_gpu_rib_top_z - front_gpu_cradle_rib_height_z
front_gpu_rib_offset_x = front_gpu_tray_outer_width_x / 2.0 - front_gpu_cradle_rib_edge_inset_x
front_gpu_rib_xs = (
    front_gpu_cradle_center_x - front_gpu_rib_offset_x,
    front_gpu_cradle_center_x,
    front_gpu_cradle_center_x + front_gpu_rib_offset_x,
)
front_gpu_ribs = [
    Box(
        front_gpu_cradle_rib_thickness_x,
        front_gpu_rib_actual_depth_y,
        front_gpu_cradle_rib_height_z,
        align=(Align.CENTER, Align.MIN, Align.MIN),
    ).moved(Location((rib_x, front_gpu_rib_y0, front_gpu_rib_bottom_z)))
    for rib_x in front_gpu_rib_xs
]
front_gpu_cradle = (
    front_gpu_shelf
    + front_gpu_sidewalls[0]
    + front_gpu_sidewalls[1]
    + front_gpu_ribs[0]
    + front_gpu_ribs[1]
    + front_gpu_ribs[2]
).clean()

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

front_gpu_actual_side_clearance_x = (front_gpu_sidewall_inner_gap_x - COLORFUL_GPU_THICKNESS_MM) / 2.0
assert front_gpu_rib_actual_depth_y >= 8.0
assert abs(front_gpu_cradle_reference_bottom_z - (slot_z0 - 7.5)) < 0.01
assert abs(front_gpu_shelf_top_z - 89.5) < 0.01
assert abs(front_gpu_actual_side_clearance_x - front_gpu_side_clearance_x) < 0.01
assert front_gpu_actual_side_clearance_x >= 0.8
assert front_gpu_cradle.solids().__len__() == 1
assert (front_gpu_cradle & front_panel).volume > 10.0
assert (front_panel & front_gpu_reference_proxy).volume < 0.01
assert (front_gpu_cradle & front_gpu_reference_proxy).volume < 0.01
assert abs(front_gpu_cradle.bounding_box().max.Z - (front_gpu_shelf_top_z + front_gpu_sidewall_height_z)) < 0.01
assert front_gpu_cradle.bounding_box().min.X >= -W / 2 + panel_t
assert front_gpu_cradle.bounding_box().max.X <= W / 2 - panel_t

front_panel = (front_panel + front_gpu_cradle).clean()
assert front_panel.solids().__len__() == 1
assert front_panel.bounding_box().max.Y <= D / 2.0 + 0.01
publish('front_panel', front_panel, 'GPU retaining cradle')
print(
    f'COLORFUL_GPU_RETAINING_CRADLE_PASS: measured body={COLORFUL_GPU_BODY_LENGTH_MM:.1f} mm; '
    f'support top z={front_gpu_shelf_top_z:.1f}, {front_gpu_cradle_bottom_offset_from_pcie_z:.1f} mm below PCIe opening; '
    f'continuous floor={front_gpu_tray_outer_width_x:.1f} x {front_gpu_channel_depth_y:.1f} x '
    f'{front_gpu_cradle_shelf_thickness_z:.1f} mm; two {front_gpu_sidewall_height_z:.1f} mm side plates; '
    f'{front_gpu_actual_side_clearance_x:.1f} mm clearance per side; front clearance={front_gpu_body_to_panel_clearance_y:.1f} mm.'
)