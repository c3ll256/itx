# Rebuild the one-piece base and all four column connections from the final column axes.
# Old foot/base holes are not reused: each column root is restored, then a fresh kit joint cuts one coaxial path.
coax_base_width=param('case_width',152.0)
coax_base_depth=param('case_depth',256.0)
coax_base_thickness=param('base_thickness',3.0)
coax_foot_diameter=param('integrated_foot_diameter',16.0)
coax_foot_height=param('integrated_foot_height',4.0)
coax_foot_overlap=param('integrated_foot_overlap',0.4)
coax_column_restore_width=param('coax_column_restore_width',14.0)
coax_column_restore_depth=param('coax_column_restore_depth',14.0)
coax_column_restore_height=param('coax_column_restore_height',10.0)
coax_column_engagement=param('coax_column_engagement',5.0)
coax_stack_thickness=coax_base_thickness+coax_foot_height
# Final physical columns in post_xy order: rear-left, front-left, rear-right, front-right.
final_column_targets=[current_top_targets[0],current_top_targets[1],current_top_targets[2],current_top_targets[3]]
coax_base=Box(coax_base_width,coax_base_depth,coax_base_thickness,align=(Align.CENTER,Align.CENTER,Align.MIN))
for x,y in post_xy:
    foot_pad=Cylinder(coax_foot_diameter/2,coax_foot_height+coax_foot_overlap,align=(Align.CENTER,Align.CENTER,Align.MAX)).moved(Location((x,y,coax_foot_overlap)))
    coax_base=(coax_base+foot_pad).clean()
# Preserve the two motherboard-support floor fasteners after rebuilding the base.
rear_anchor_joint=make_screw_joint_v1(size='M3',at=Location((rear_floor_anchor_x,lower_mount_ys[0],0),(180,0,0)),through=[(coax_base,coax_base_thickness)],engage_depth=flat_floor_anchor_engagement,into=left_rear_integrated,head='socket_cap',strategy='auto',material=material,boss='auto',label='coax-base-rear-mb-support')
coax_base=coax_base-rear_anchor_joint.through_cuts[0]
front_anchor_joint=make_screw_joint_v1(size='M3',at=Location((front_floor_anchor_x,lower_mount_ys[1],0),(180,0,0)),through=[(coax_base,coax_base_thickness)],engage_depth=flat_floor_anchor_engagement,into=lower_mount_parts[1],head='socket_cap',strategy='auto',material=material,boss='auto',label='coax-base-front-mb-support')
coax_base=coax_base-front_anchor_joint.through_cuts[0]
coax_column_joints=[]
rebuilt_columns=[]
for i,((x,y),target) in enumerate(zip(post_xy,final_column_targets)):
    root_restore=Box(coax_column_restore_width,coax_column_restore_depth,coax_column_restore_height,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,coax_base_thickness)))
    restored_target=(target+root_restore).clean()
    joint=make_screw_joint_v1(size='M3',at=Location((x,y,-coax_foot_height),(180,0,0)),through=[(coax_base,coax_stack_thickness)],engage_depth=coax_column_engagement,into=restored_target,head='socket_cap',strategy='auto',material=material,boss='auto',label=f'final-coax-base-column:{i}')
    coax_base=(coax_base-joint.through_cuts[0]).clean()
    restored_target=(restored_target+joint.bosses-joint.engage_cuts).clean()
    coax_column_joints.append(joint); rebuilt_columns.append(restored_target)
base=coax_base.clean()
current_top_targets=rebuilt_columns
assert base.solids().__len__()==1 and len(coax_column_joints)==4
assert all(abs(j.through_thickness_mm-coax_stack_thickness)<0.001 for j in coax_column_joints)
assert abs(base.bounding_box().min.Z+coax_foot_height)<0.001 and abs(base.bounding_box().max.Z-coax_base_thickness)<0.001
publish('base',base,'Coaxial integrated-foot base')
publish('column_fl',rebuilt_columns[0],'Coaxial rear-left column')
publish('column_rl',rebuilt_columns[1],'Coaxial front-left column')
publish('column_fr',rebuilt_columns[2],'Coaxial rear-right column')
publish('column_rr',rebuilt_columns[3],'Coaxial front-right column')
print(f'FINAL_COAXIAL_BASE_PASS: four fresh M3 paths run through each integrated foot and base into restored column roots at exact axes {post_xy}; no old foot/base hole is reused.')