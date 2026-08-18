# Mini-ITX mount construction from the standard asymmetric four-hole pattern.
# Figure 3 uses 157.48 mm across the I/O-edge axis. These are external
# standard dimensions, so they are constants rather than user parameters.
# Board rear edge = rear-panel inner face + 1 mm stamped I/O shield (see the
# mini_itx_reference sandwich note); -125.0 puts the four standard holes 1 mm
# farther forward than the earlier -126.0 estimate.
mitx_board_width=param('mitx_board_width',170.0); mitx_board_height=param('mitx_board_height',170.0); mitx_board_rear_edge_y=param('mitx_board_rear_edge_y',-125.0)
# Fixed enclosure interface datum: the user's printed rear-I/O aperture fits at this board position.
MITX_BOARD_BOTTOM_Z_MM=71.50
mitx_board_z_min=MITX_BOARD_BOTTOM_Z_MM
MITX_REAR_UPPER_FROM_REAR_MM=33.02
MITX_FRONT_UPPER_FROM_REAR_MM=165.10
MITX_REAR_LOWER_FROM_REAR_MM=10.16
MITX_FRONT_LOWER_FROM_REAR_MM=165.10
MITX_LOWER_FROM_BOTTOM_MM=6.35
MITX_UPPER_FROM_BOTTOM_MM=163.83
mitx_rear_upper_from_rear=MITX_REAR_UPPER_FROM_REAR_MM; mitx_front_upper_from_rear=MITX_FRONT_UPPER_FROM_REAR_MM; mitx_rear_lower_from_rear=MITX_REAR_LOWER_FROM_REAR_MM; mitx_front_lower_from_rear=MITX_FRONT_LOWER_FROM_REAR_MM
mitx_lower_from_bottom=MITX_LOWER_FROM_BOTTOM_MM; mitx_upper_from_bottom=MITX_UPPER_FROM_BOTTOM_MM
legacy_square_rear=param('mitx_mount_rear_offset',6.35); legacy_square_front=param('mitx_mount_front_offset',163.83)
legacy_square_lower=param('mitx_mount_lower_offset',6.35); legacy_square_upper=param('mitx_mount_upper_offset',163.83)
board_face_x=param('mitx_board_face_x',-2.15)
arm_depth_x=param('mitx_arm_depth_x',4.0); arm_width_y=param('mitx_arm_width_y',10.0); legacy_motherboard_engagement=param('mitx_screw_engagement',2.4)
foot_depth_x=param('mitx_foot_depth_x',12.0); foot_width_y=param('mitx_foot_width_y',14.0); foot_height_z=param('mitx_foot_height_z',7.0)
front_lower_anchor_mag=abs(param('mitx_lower_anchor_x',2.0)); rear_lower_anchor_mag=abs(param('mitx_rear_lower_anchor_x',-67.0)); upper_anchor_mag=abs(param('mitx_upper_anchor_x',-1.5))
lower_plate_engagement=param('mitx_lower_anchor_engagement',5.0); upper_cap_stack=cap_t+param('mitx_upper_cap_extra_stack',2.0); upper_plate_engagement=param('mitx_upper_anchor_engagement',3.0)
board_proxy_thickness=param('mitx_board_proxy_thickness',1.6); board_proxy_size=param('mitx_board_proxy_size',8.0)
rear_bridge_z0=param('mitx_rear_bridge_z0',70.5); rear_bridge_height=param('mitx_rear_bridge_height',6.0); rear_side_leg_width=param('mitx_rear_side_leg_width',5.0)
mitx_standoff_height=param('mitx_integrated_standoff_height',6.35); mitx_standoff_diameter=param('mitx_integrated_standoff_diameter',8.0); mitx_standoff_fuse_overlap=param('mitx_standoff_fuse_overlap',0.6); mitx_standoff_engagement=param('mitx_integrated_standoff_engagement',6.0); motherboard_engagement=mitx_standoff_engagement
board_side=1.0; arm_align_x=Align.MAX; proxy_align_x=Align.MIN
board_plane_x=board_face_x+board_side*mitx_standoff_height; board_screw_outer_x=board_plane_x+board_side*board_proxy_thickness; board_screw_rotation_y=90.0*board_side
corrected_foot_anchor_x=board_face_x-foot_depth_x/2
front_lower_screw_x=corrected_foot_anchor_x; rear_lower_screw_x=board_side*rear_lower_anchor_mag; upper_screw_x=corrected_foot_anchor_x
board_top_z=mitx_board_z_min+mitx_board_height
lower_mount_z=mitx_board_z_min+mitx_lower_from_bottom; upper_mount_z=mitx_board_z_min+mitx_upper_from_bottom
lower_mount_ys=(mitx_board_rear_edge_y+mitx_rear_lower_from_rear,mitx_board_rear_edge_y+mitx_front_lower_from_rear)
upper_mount_ys=(mitx_board_rear_edge_y+mitx_rear_upper_from_rear,mitx_board_rear_edge_y+mitx_front_upper_from_rear)
lower_mount_parts=[]; upper_mount_parts=[]; board_screw_lengths=[]; plate_screw_lengths=[]
def add_integrated_standoff(host,yy,zz,label):
    start_x=board_face_x-board_side*mitx_standoff_fuse_overlap
    post=Cylinder(mitx_standoff_diameter/2,mitx_standoff_height+mitx_standoff_fuse_overlap,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((start_x,yy,zz),(0,90.0*board_side,0)))
    host=(host+post).clean()
    board_proxy=Box(board_proxy_thickness,board_proxy_size,board_proxy_size,align=(proxy_align_x,Align.CENTER,Align.CENTER)).moved(Location((board_plane_x,yy,zz)))
    joint=make_screw_joint_v1(size='M3',at=Location((board_screw_outer_x,yy,zz),(0,board_screw_rotation_y,0)),through=[(board_proxy,board_proxy_thickness)],engage_depth=mitx_standoff_engagement,into=host,head='socket_cap',strategy='auto',material=material,boss='none',label=label)
    return (host-joint.engage_cuts).clean(),joint
for idx,yy in enumerate(lower_mount_ys):
    if idx==0:
        web_h=lower_mount_z+5.0-rear_bridge_z0; web=Box(arm_depth_x,arm_width_y,web_h,align=(arm_align_x,Align.CENTER,Align.MIN)).moved(Location((board_face_x,yy,rear_bridge_z0)))
        bridge_near_x=board_face_x-board_side*arm_depth_x; leg_x0=rear_lower_screw_x-rear_side_leg_width/2; leg_x1=rear_lower_screw_x+rear_side_leg_width/2
        bridge_x_min=min(bridge_near_x,leg_x0); bridge_x_max=max(bridge_near_x,leg_x1)
        bridge=Box(bridge_x_max-bridge_x_min,foot_width_y,rear_bridge_height,align=(Align.MIN,Align.CENTER,Align.MIN)).moved(Location((bridge_x_min,yy,rear_bridge_z0)))
        leg=Box(rear_side_leg_width,foot_width_y,rear_bridge_z0+rear_bridge_height-base_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((rear_lower_screw_x,yy,base_t)))
        arm=(web+bridge+leg).clean(); anchor_x=rear_lower_screw_x
    else:
        arm_h=lower_mount_z+5.0-base_t; web=Box(arm_depth_x,arm_width_y,arm_h,align=(arm_align_x,Align.CENTER,Align.MIN)).moved(Location((board_face_x,yy,base_t)))
        foot=Box(foot_depth_x,foot_width_y,foot_height_z,align=(arm_align_x,Align.CENTER,Align.MIN)).moved(Location((board_face_x,yy,base_t))); arm=(web+foot).clean(); anchor_x=front_lower_screw_x
    arm,mj=add_integrated_standoff(arm,yy,lower_mount_z,f'motherboard-lower:{idx}')
    pj=make_screw_joint_v1(size='M3',at=Location((anchor_x,yy,0),(180,0,0)),through=[(base,base_t)],engage_depth=lower_plate_engagement,into=arm,head='socket_cap',strategy='auto',material=material,boss='none',label=f'lower-arm-base:{idx}')
    base=(base-pj.through_cuts[0]).clean(); arm=(arm-pj.engage_cuts).clean(); lower_mount_parts.append(arm); board_screw_lengths.append(mj.screw_length_mm); plate_screw_lengths.append(pj.screw_length_mm)
for idx,yy in enumerate(upper_mount_ys):
    arm_z0=upper_mount_z-5.0; arm_h=H-cap_t-arm_z0; web=Box(arm_depth_x,arm_width_y,arm_h,align=(arm_align_x,Align.CENTER,Align.MIN)).moved(Location((board_face_x,yy,arm_z0)))
    foot=Box(foot_depth_x,foot_width_y,foot_height_z,align=(arm_align_x,Align.CENTER,Align.MAX)).moved(Location((board_face_x,yy,H-cap_t))); arm=(web+foot).clean()
    arm,mj=add_integrated_standoff(arm,yy,upper_mount_z,f'motherboard-upper:{idx}')
    pj=make_screw_joint_v1(size='M3',at=Location((upper_screw_x,yy,H)),through=[(top_cap,upper_cap_stack)],engage_depth=upper_plate_engagement,into=arm,head='socket_cap',strategy='auto',material=material,boss='none',label=f'upper-arm-cap:{idx}')
    top_cap=(top_cap-pj.through_cuts[0]).clean(); arm=(arm-pj.engage_cuts).clean(); upper_mount_parts.append(arm); board_screw_lengths.append(mj.screw_length_mm); plate_screw_lengths.append(pj.screw_length_mm)
assert len(lower_mount_parts)==2 and len(upper_mount_parts)==2
assert abs((lower_mount_ys[1]-lower_mount_ys[0])-154.94)<0.001
assert abs((upper_mount_ys[1]-upper_mount_ys[0])-132.08)<0.001
assert abs((upper_mount_z-lower_mount_z)-157.48)<0.001
assert abs((upper_mount_ys[0]-lower_mount_ys[0])-22.86)<0.001
assert abs(board_plane_x-4.2)<0.001
assert board_plane_x+board_proxy_thickness+67.0<74.0
assert all(v==8 for v in board_screw_lengths) and all(v==8 for v in plate_screw_lengths)
publish('base',base,'Standard ITX base anchors'); publish('top_cap',top_cap,'Standard ITX top anchors')
print(f'MB_STANDARD_PATTERN_PASS: four-hole grid uses 157.48 mm I/O-edge-axis spacing; PCB x={board_plane_x:.2f}, components +X, GPU remains on -X side.')