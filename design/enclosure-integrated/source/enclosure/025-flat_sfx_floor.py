# Monolithic base follows the enclosure width/depth parameters; no PSU recess, rail, stop or patch seam.
flat_base_width=param('flat_base_width',152.0)
flat_base_depth=param('flat_base_depth',256.0)
flat_base_thickness=param('flat_base_thickness',3.0)
base=Box(W,D,flat_base_thickness,align=(Align.CENTER,Align.CENTER,Align.MIN))
# Reapply the four exact foot/column screw clearances from the current width-dependent screw-joint kit results.
for j in base_joints:
    base=base-j.through_cuts[1]
rear_floor_anchor_mag=abs(param('rear_floor_anchor_x',-67.0))
front_floor_anchor_mag=abs(param('front_floor_anchor_x',2.0))
rear_floor_anchor_x=board_side*rear_floor_anchor_mag
front_floor_anchor_x=-board_side*front_floor_anchor_mag
flat_floor_anchor_engagement=param('flat_floor_anchor_engagement',5.0)
rear_anchor_joint=make_screw_joint_v1(size='M3',at=Location((rear_floor_anchor_x,lower_mount_ys[0],0),(180,0,0)),through=[(base,flat_base_thickness)],engage_depth=flat_floor_anchor_engagement,into=left_rear_integrated,head='socket_cap',strategy='auto',material=material,boss='auto',label='flat-base-rear-support')
base=base-rear_anchor_joint.through_cuts[0]
front_anchor_joint=make_screw_joint_v1(size='M3',at=Location((front_floor_anchor_x,lower_mount_ys[1],0),(180,0,0)),through=[(base,flat_base_thickness)],engage_depth=flat_floor_anchor_engagement,into=lower_mount_parts[1],head='socket_cap',strategy='auto',material=material,boss='auto',label='flat-base-front-support')
base=base-front_anchor_joint.through_cuts[0]
base=base.clean()
assert abs(flat_base_thickness-base_t)<0.001
assert len(base_joints)==4
assert base.bounding_box().size.Z<=base_t+0.01
assert board_side*rear_floor_anchor_x>0 and board_side*front_floor_anchor_x<0
publish('base',base,'Width-linked flat base')
print(f'WIDTH_LINKED_BASE_PASS: board side={"right" if board_side>0 else "left"}; base follows case dimensions {W:.1f} x {D:.1f} mm; motherboard floor anchors mirror with the board side.')