# Integrated bottom support and column relief for a standard SFX 125 x 100 x 63.5 mm envelope.
sfx_psu_width=param('sfx_psu_width',125.0)
sfx_psu_depth=param('sfx_psu_depth',100.0)
sfx_psu_height=param('sfx_psu_height',63.5)
sfx_psu_rear_clearance=param('sfx_psu_rear_clearance',0.8)
sfx_guide_side_clearance=param('sfx_guide_side_clearance',0.8)
sfx_guide_width=param('sfx_guide_width',3.0)
sfx_guide_height=param('sfx_guide_height',10.0)
sfx_guide_overrun=param('sfx_guide_overrun',1.0)
sfx_front_stop_depth=param('sfx_front_stop_depth',3.0)
sfx_front_stop_height=param('sfx_front_stop_height',4.0)
sfx_column_side_clearance=param('sfx_column_side_clearance',1.5)
sfx_column_top_clearance=param('sfx_column_top_clearance',2.0)
sfx_column_notch_depth=param('sfx_column_notch_depth',18.0)
sfx_lower_screw_access_width=param('sfx_lower_screw_access_width',12.0)
sfx_lower_screw_access_height=param('sfx_lower_screw_access_height',12.0)
sfx_lower_screw_access_depth=param('sfx_lower_screw_access_depth',24.0)
sfx_mount_horizontal_inset=param('sfx_mount_horizontal_inset',3.0)
sfx_mount_vertical_inset=param('sfx_mount_vertical_inset',5.5)
psu_y0=-D/2+panel_t+sfx_psu_rear_clearance
psu_y1=psu_y0+sfx_psu_depth
psu_z0=base_t
psu_z1=psu_z0+sfx_psu_height
guide_inner_x=sfx_psu_width/2+sfx_guide_side_clearance
guide_center_x=guide_inner_x+sfx_guide_width/2
guide_length=sfx_psu_depth+2*sfx_guide_overrun
guide_center_y=(psu_y0+psu_y1)/2
left_guide=Box(sfx_guide_width,guide_length,sfx_guide_height,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((-guide_center_x,guide_center_y,base_t)))
right_guide=Box(sfx_guide_width,guide_length,sfx_guide_height,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((guide_center_x,guide_center_y,base_t)))
front_stop=Box(2*guide_inner_x,sfx_front_stop_depth,sfx_front_stop_height,align=(Align.CENTER,Align.MIN,Align.MIN)).moved(Location((0,psu_y1,base_t)))
base=(base+left_guide+right_guide+front_stop).clean()
notch_half_x=sfx_psu_width/2+sfx_column_side_clearance
notch_h=sfx_psu_height+sfx_column_top_clearance
left_notch=Box(notch_half_x+post_x,sfx_column_notch_depth,notch_h,align=(Align.MAX,Align.CENTER,Align.MIN)).moved(Location((-notch_half_x,-post_y,base_t)))
right_notch=Box(notch_half_x+post_x,sfx_column_notch_depth,notch_h,align=(Align.MIN,Align.CENTER,Align.MIN)).moved(Location((notch_half_x,-post_y,base_t)))
columns[0]=(columns[0]-left_notch).clean(); columns[2]=(columns[2]-right_notch).clean()
# Rectangular tool-access notches align to the lower SFX holes and open the remaining outer spines.
sfx_lower_hole_x=sfx_psu_width/2-sfx_mount_horizontal_inset
sfx_lower_hole_z=base_t+sfx_mount_vertical_inset
left_access=Box(sfx_lower_screw_access_width,sfx_lower_screw_access_depth,sfx_lower_screw_access_height,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((-sfx_lower_hole_x,-post_y,sfx_lower_hole_z)))
right_access=Box(sfx_lower_screw_access_width,sfx_lower_screw_access_depth,sfx_lower_screw_access_height,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((sfx_lower_hole_x,-post_y,sfx_lower_hole_z)))
columns[0]=columns[0]-left_access
columns[2]=columns[2]-right_access
inner_half_width=W/2-panel_t-clearance
assert psu_z1<mitx_board_z_min
assert inner_half_width-(guide_center_x+sfx_guide_width/2)>=4.0
assert sfx_lower_screw_access_width>param('sfx_mount_hole_diameter',4.2)+4.0
publish('base',base,'Base with SFX guides')
publish('column_fl',columns[0],'SFX screw-clear left')
publish('column_fr',columns[2],'SFX screw-clear right')
print(f'SFX_SCREW_ACCESS_PASS: lower holes at x=±{sfx_lower_hole_x:.1f}, z={sfx_lower_hole_z:.1f} mm have {sfx_lower_screw_access_width:.1f} x {sfx_lower_screw_access_height:.1f} mm access notches.')