# Final interface regeneration after width change and side-aware rear structural fusion.
final_cap_outer_thickness=param('final_cap_outer_thickness',3.0)
final_cap_inner_thickness=param('final_cap_inner_thickness',2.0)
final_cap_inset=param('final_cap_inset',5.0)
final_top_engagement=param('final_top_engagement',3.0)
final_upper_mount_engagement=param('final_upper_mount_engagement',3.0)
# Legacy parameters retained for revision compatibility; current rear side stations use the selected 15 x 10 x 4 mm magnet envelope.
legacy_final_magnet_pocket_size=param('final_left_rear_magnet_pocket_size',10.2)
legacy_final_magnet_pocket_depth=param('final_left_rear_magnet_pocket_depth',3.2)
legacy_final_magnet_proxy_size=param('final_left_rear_magnet_proxy_size',10.0)
legacy_final_magnet_proxy_depth=param('final_left_rear_magnet_proxy_depth',3.0)
legacy_final_magnet_edge_offset=param('final_left_rear_magnet_edge_offset',1.6)
legacy_final_magnet_proxy_offset=param('final_left_rear_magnet_proxy_offset',1.5)
legacy_final_magnet_engagement=param('final_left_rear_magnet_engagement',5.0)
rear_magnet_restore_extra_z=param('rear_magnet_restore_extra_z',0.8)
# Resolve physical left/right rear columns independently of which side carries the motherboard.
left_rear_structural=left_rear_integrated if board_side<0 else right_rear_integrated
right_rear_structural=right_rear_integrated if board_side<0 else left_rear_integrated
rear_side_targets=[(-1,left_rear_structural,'left'),(1,right_rear_structural,'right')]
restored_magnet_joints=[]
restored_rear_targets=[]
for sx,target,side_name in rear_side_targets:
    restored=target
    column_center_x=sx*post_x
    for z in (side_station_z_low,side_station_z_high):
        restore_block=Box(post,post,side_magnet_height_z+rear_magnet_restore_extra_z,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((column_center_x,-post_y,z)))
        restored=(restored+restore_block).clean()
        pocket=Box(side_magnet_pocket_depth_x,side_magnet_width_y,side_magnet_height_z,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((sx*(outer_x-side_magnet_edge_offset_x),-post_y,z)))
        restored=restored-pocket
        proxy=Box(side_magnet_proxy_depth_x,side_magnet_proxy_width_y,side_magnet_proxy_height_z,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((sx*(outer_x-side_magnet_proxy_offset_x),-post_y,z)))
        mj=make_screw_joint_v1(size='M3',at=Location((sx*outer_x,-post_y,z),(0,90*sx,0)),through=[(proxy,side_magnet_proxy_depth_x)],engage_depth=side_magnet_engagement,into=restored,head='countersunk',strategy='auto',material=material,boss='auto',label=f'final-{side_name}-rear-magnet:{z}')
        restored=(restored+mj.bosses-mj.engage_cuts).clean(); restored_magnet_joints.append(mj)
    restored_rear_targets.append(restored)
left_rear_final,right_rear_final=restored_rear_targets
top_cap=Box(W,D,final_cap_outer_thickness,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,0,H-final_cap_outer_thickness)))+Box(W-2*final_cap_inset,D-2*final_cap_inset,final_cap_inner_thickness,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,0,H-final_cap_outer_thickness-final_cap_inner_thickness)))
current_top_targets=[left_rear_final,columns[1],right_rear_final,columns[3]]
final_top_joints=[]
for i,((x,y),target) in enumerate(zip(post_xy,current_top_targets)):
    tj=make_screw_joint_v1(size='M3',at=Location((x,y,H)),through=[(top_cap,final_cap_outer_thickness+final_cap_inner_thickness)],engage_depth=final_top_engagement,into=target,head='socket_cap',strategy='auto',material=material,boss='auto',label=f'final-column-top:{i}')
    top_cap=top_cap-tj.through_cuts[0]; current_top_targets[i]=(target+tj.bosses-tj.engage_cuts).clean(); final_top_joints.append(tj)
final_upper_cap_joints=[]
for i,(yy,target) in enumerate(zip(upper_mount_ys,upper_mount_parts)):
    uj=make_screw_joint_v1(size='M3',at=Location((upper_screw_x,yy,H)),through=[(top_cap,final_cap_outer_thickness+final_cap_inner_thickness)],engage_depth=final_upper_mount_engagement,into=target,head='socket_cap',strategy='auto',material=material,boss='auto',label=f'final-upper-mb-cap:{i}')
    top_cap=top_cap-uj.through_cuts[0]; final_upper_cap_joints.append(uj)
assert len(final_top_joints)==4 and len(final_upper_cap_joints)==2 and len(restored_magnet_joints)==4
publish('top_cap',top_cap,'Axis-aligned top cap')
publish('column_fl',current_top_targets[0],'Left rear support')
publish('column_rl',current_top_targets[1],'Front-left column')
publish('column_fr',current_top_targets[2],'Right rear support')
publish('column_rr',current_top_targets[3],'Front-right column')
print(f'FINAL_REAR_MAGNET_PASS: both rear side columns now carry 15 x 10 x 4 mm center-screw magnet stations at z={side_station_z_low:.1f}/{side_station_z_high:.1f}; board side={"right" if board_side>0 else "left"}.')