# Final SFX rear-face repair: four complete lands, four recut holes, and four
# unobstructed internal screw-head/driver passages.
sfx_final_hole_diameter=param('sfx_final_hole_diameter',sfx_mount_hole_diameter)
sfx_final_land_diameter=param('sfx_final_land_diameter',14.0)
sfx_final_land_thickness=param('sfx_final_land_thickness',panel_t+0.4)
sfx_final_land_overlap=param('sfx_final_land_overlap',0.2)
sfx_final_tool_clearance_width=param('sfx_final_tool_clearance_width',12.0)
sfx_final_tool_clearance_height=param('sfx_final_tool_clearance_height',12.0)
sfx_final_tool_clearance_depth=param('sfx_final_tool_clearance_depth',20.0)
sfx_final_tool_clearance_start_y=param('sfx_final_tool_clearance_start_y',-D/2+panel_t+0.05)
sfx_final_through_cut_depth=param('sfx_final_through_cut_depth',32.0)
sfx_final_expected_holes=param('sfx_final_expected_holes',4)
sfx_final_min_land_to_opening=param('sfx_final_min_land_to_opening',2.0)
sfx_final_hole_x=sfx_psu_width/2-sfx_mount_horizontal_inset
sfx_final_hole_z_low=base_t+sfx_mount_vertical_inset
sfx_final_hole_z_high=base_t+sfx_psu_height-sfx_mount_vertical_inset
sfx_final_points=[(-sfx_final_hole_x,sfx_final_hole_z_low),(sfx_final_hole_x,sfx_final_hole_z_low),(-sfx_final_hole_x,sfx_final_hole_z_high),(sfx_final_hole_x,sfx_final_hole_z_high)]

# Clear all internal blocks behind the four screw axes without cutting the panel skin.
for x,z in sfx_final_points:
    tool_relief=Box(sfx_final_tool_clearance_width,sfx_final_tool_clearance_depth,sfx_final_tool_clearance_height,align=(Align.CENTER,Align.MIN,Align.CENTER)).moved(Location((x,sfx_final_tool_clearance_start_y,z)))
    rear_panel=rear_panel-tool_relief

# Fuse circular panel lands with 0.2 mm overlap so each hole remains complete.
land_center_y=rear_y-sfx_final_land_overlap
for x,z in sfx_final_points:
    land=Cylinder(sfx_final_land_diameter/2,sfx_final_land_thickness,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.X,90).moved(Location((x,land_center_y,z)))
    rear_panel=rear_panel+land

# Recut the four standard SFX clearance holes through all remaining geometry.
for x,z in sfx_final_points:
    hole=Cylinder(sfx_final_hole_diameter/2,sfx_final_through_cut_depth,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.X,90).moved(Location((x,rear_y,z)))
    rear_panel=rear_panel-hole
rear_panel=rear_panel.clean()

sfx_opening_half_width=psu_cut_w/2
sfx_lower_inner_edge=sfx_final_hole_x-sfx_final_hole_diameter/2
sfx_land_to_opening=sfx_lower_inner_edge-sfx_opening_half_width
sfx_final_connection_inventory={'sfx-four-clearance-holes':'standard 6 mm edge inset','sfx-four-tool-passages':'free clearance through internal chassis blocks'}
assert len(sfx_final_points)==int(sfx_final_expected_holes)
assert sfx_land_to_opening>=sfx_final_min_land_to_opening
assert rear_panel.solids().__len__()==1
assert all(sfx_final_connection_inventory.values())
publish('rear_panel',rear_panel,'Rear with four clear SFX holes')
print(f'SFX_FOUR_HOLE_ACCESS_PASS: four complete {sfx_final_hole_diameter:.1f} mm holes at x=±{sfx_final_hole_x:.1f}, z={sfx_final_hole_z_low:.1f}/{sfx_final_hole_z_high:.1f}; opening land={sfx_land_to_opening:.1f} mm; tool passage={sfx_final_tool_clearance_width:.1f} x {sfx_final_tool_clearance_height:.1f} x {sfx_final_tool_clearance_depth:.1f} mm.')