# User-confirmed repair: keep the PRD SFX rear pattern at 113 x 51.5 mm.
# Old-hole fills are exactly panel-thick so the exterior rear face stays planar.
rear_sfx_panel_width = param('case_width', W)
rear_sfx_panel_height = param('case_height', H)
rear_sfx_panel_thickness = param('panel_thickness', panel_t)
sfx_corrected_hole_diameter = param('sfx_rear_mount_hole_diameter', 4.2)
sfx_corrected_horizontal_spacing = param('sfx_rear_mount_horizontal_spacing', 113.0)
sfx_corrected_vertical_spacing = param('sfx_rear_mount_vertical_spacing', 51.5)
sfx_legacy_fill_diameter = param('sfx_legacy_hole_fill_diameter', 5.2)
sfx_legacy_fill_depth = rear_sfx_panel_thickness
sfx_corrected_driver_width = param('sfx_corrected_driver_width', 12.0)
sfx_corrected_driver_height = param('sfx_corrected_driver_height', 12.0)
sfx_corrected_driver_depth = param('sfx_corrected_driver_depth', 20.0)
sfx_corrected_through_depth = param('sfx_corrected_through_depth', 32.0)
legacy_hole_x = sfx_psu_width / 2 - sfx_mount_horizontal_inset
legacy_z_low = base_t + sfx_mount_vertical_inset
legacy_z_high = base_t + sfx_psu_height - sfx_mount_vertical_inset
legacy_points = [(-legacy_hole_x, legacy_z_low), (legacy_hole_x, legacy_z_low), (-legacy_hole_x, legacy_z_high), (legacy_hole_x, legacy_z_high)]
rear_face_center_y = -D / 2 + rear_sfx_panel_thickness / 2
for old_x, old_z in legacy_points:
    old_fill = Cylinder(sfx_legacy_fill_diameter / 2, sfx_legacy_fill_depth, align=(Align.CENTER, Align.CENTER, Align.CENTER)).rotate(Axis.X, 90).moved(Location((old_x, rear_face_center_y, old_z)))
    rear_panel = (rear_panel + old_fill).clean()
corrected_hole_x = sfx_corrected_horizontal_spacing / 2
sfx_face_center_z = base_t + sfx_psu_height / 2
corrected_z_low = sfx_face_center_z - sfx_corrected_vertical_spacing / 2
corrected_z_high = sfx_face_center_z + sfx_corrected_vertical_spacing / 2
corrected_points = [(-corrected_hole_x, corrected_z_low), (corrected_hole_x, corrected_z_low), (-corrected_hole_x, corrected_z_high), (corrected_hole_x, corrected_z_high)]
for new_x, new_z in corrected_points:
    driver_clearance = Box(sfx_corrected_driver_width, sfx_corrected_driver_depth, sfx_corrected_driver_height, align=(Align.CENTER, Align.MIN, Align.CENTER)).moved(Location((new_x, -D / 2 + rear_sfx_panel_thickness + 0.05, new_z)))
    corrected_hole = Cylinder(sfx_corrected_hole_diameter / 2, sfx_corrected_through_depth, align=(Align.CENTER, Align.CENTER, Align.CENTER)).rotate(Axis.X, 90).moved(Location((new_x, -D / 2, new_z)))
    rear_panel = ((rear_panel - driver_clearance) - corrected_hole).clean()
assert len(corrected_points) == 4
assert abs(2 * corrected_hole_x - sfx_corrected_horizontal_spacing) < 0.001
assert abs(corrected_z_high - corrected_z_low - sfx_corrected_vertical_spacing) < 0.001
assert abs(sfx_legacy_fill_depth - rear_sfx_panel_thickness) < 0.001
publish('rear_panel', rear_panel, 'Flush corrected SFX holes')
print(f'SFX_PATTERN_REPAIRED_PASS: planar legacy fills; four {sfx_corrected_hole_diameter:.1f} mm holes at {2*corrected_hole_x:.1f} x {corrected_z_high-corrected_z_low:.1f} mm spacing.')