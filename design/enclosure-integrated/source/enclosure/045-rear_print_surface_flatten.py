# Flatten the printable rear-panel envelope: remove the two top-edge patch ears
# and the exterior fused PCIe shelf while preserving all inward-facing supports.
rear_print_clip_width_x = param('rear_print_clip_width_x', 152.0)
rear_print_clip_depth_y = param('rear_print_clip_depth_y', 32.0)
rear_print_clip_height_z = param('rear_print_clip_height_z', 246.0)
rear_print_disabled_sfx_patch_diameter = param('rear_print_disabled_sfx_patch_diameter', 8.0)
rear_print_visual_red_hole_count = param('rear_print_visual_red_hole_count', 1)

rear_print_clip = Box(
    rear_print_clip_width_x,
    rear_print_clip_depth_y,
    rear_print_clip_height_z,
    align=(Align.CENTER, Align.MIN, Align.MIN),
).moved(Location((0, -D/2, base_t)))
rear_panel = (rear_panel & rear_print_clip).clean()

# Visual annotation: close only the lower-right SFX hole; retain the other
# three green-circled points. The list follows the visual rear-view order.
rear_print_disabled_sfx_points = [sfx_mount_points[1]]
for x, z in rear_print_disabled_sfx_points:
    patch = Cylinder(
        rear_print_disabled_sfx_patch_diameter/2,
        panel_t,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.X, 90).moved(Location((x, rear_y, z)))
    rear_panel = (rear_panel + patch).clean()

assert len(rear_print_disabled_sfx_points) == int(rear_print_visual_red_hole_count)
assert rear_panel.solids().__len__() == 1
publish('rear_panel', rear_panel, 'Flat printable rear')
print('REAR_PRINT_FLATTEN_PASS: removed two top ears and fused PCIe shelf; closed only the visually marked lower-right SFX hole and retained the three green-circled holes.')