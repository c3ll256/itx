# Width-linked unified motherboard-side rear support.
# It follows board_side, so moving the Mini-ITX board to +X also moves this structural support to the right rear.
legacy_profile_x_min=param('left_rear_profile_x_min',-73.0)
legacy_profile_x_max=param('left_rear_profile_x_max',-59.0)
rear_profile_y_min=param('left_rear_profile_y_min',-125.4)
rear_profile_y_max=param('left_rear_profile_y_max',-111.4)
rear_spine_z_min=param('left_rear_spine_z_min',70.0)
rear_spine_z_max=param('left_rear_spine_z_max',259.0)
rear_arm_inner_x=abs(param('left_rear_arm_x_max',0.0))
rear_arm_height=param('left_rear_arm_height',12.0)
rear_leg_z_min=param('left_rear_leg_z_min',3.0)
rear_leg_z_max=param('left_rear_leg_z_max',82.0)
rear_foot_sfx_clearance=param('rear_foot_sfx_clearance',0.3)
profile_x_min=-outer_x if board_side<0 else outer_x-post
profile_x_max=-outer_x+post if board_side<0 else outer_x
profile_d=rear_profile_y_max-rear_profile_y_min
profile_y=(rear_profile_y_min+rear_profile_y_max)/2
aligned_spine=Box(profile_x_max-profile_x_min,profile_d,rear_spine_z_max-rear_spine_z_min,align=(Align.MIN,Align.CENTER,Align.MIN)).moved(Location((profile_x_min,profile_y,rear_spine_z_min)))
arm_x_min=profile_x_min if board_side<0 else rear_arm_inner_x
arm_x_max=-rear_arm_inner_x if board_side<0 else profile_x_max
aligned_arm=Box(arm_x_max-arm_x_min,profile_d,rear_arm_height,align=(Align.MIN,Align.CENTER,Align.MIN)).moved(Location((arm_x_min,profile_y,rear_spine_z_min)))
if board_side<0:
    leg_x_min=-outer_x
    leg_x_max=-(sfx_psu_width/2+rear_foot_sfx_clearance)
    column_index=0
    column_id='column_fl'
    column_label='Unified left-rear support'
else:
    leg_x_min=sfx_psu_width/2+rear_foot_sfx_clearance
    leg_x_max=outer_x
    column_index=2
    column_id='column_fr'
    column_label='Unified right-rear support'
outer_leg=Box(leg_x_max-leg_x_min,profile_d,rear_leg_z_max-rear_leg_z_min,align=(Align.MIN,Align.CENTER,Align.MIN)).moved(Location((leg_x_min,profile_y,rear_leg_z_min)))
rear_integrated=(columns[column_index]+lower_mount_parts[0]+aligned_spine+aligned_arm+outer_leg).clean()
rear_integrated=(rear_integrated-base_joints[column_index].engage_cuts).clean()
# Compatibility alias retained for later magnet/alignment cells.
left_rear_integrated=rear_integrated
hole_x=post_xy[column_index][0]
left_margin=hole_x-leg_x_min
right_margin=leg_x_max-hole_x
assert rear_integrated.solids().__len__()==1
assert rear_integrated.bounding_box().min.Z<=base_t+0.001
assert left_margin>=3.0 and right_margin>=3.0
assert (leg_x_max<=-sfx_psu_width/2) if board_side<0 else (leg_x_min>=sfx_psu_width/2)
publish(column_id,rear_integrated,column_label)
print(f'MOTHERBOARD_REAR_WIDTH_PASS: side={"right" if board_side>0 else "left"}; W={W:.1f}; foot x={leg_x_min:.1f}..{leg_x_max:.1f}; screw axis x={hole_x:.1f}; margins {left_margin:.1f}/{right_margin:.1f} mm.')