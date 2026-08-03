# cell: internals
# Four independent Mini-ITX L-brackets. Upper screw axes are shifted left to
# x=-1.5 mm so their complete clearance circles lie outside the longitudinal
# top-cap slot (slot begins at x=2.4 mm). Full 5 mm top-cap stack is cut.
board_y0,board_z0=-85.0,25.0
mitx_offsets=(6.35,163.83)
mount_ys=(board_y0+mitx_offsets[0],board_y0+mitx_offsets[1])
lower_mount_z=board_z0+mitx_offsets[0]
upper_mount_z=board_z0+mitx_offsets[1]
board_face_x=-4.2
arm_depth_x=4.0
arm_width_y=10.0
motherboard_engagement=2.4
foot_depth_x=12.0
foot_width_y=14.0
foot_height_z=7.0
lower_screw_x=2.0
upper_screw_x=-1.5
lower_plate_engagement=5.0
upper_cap_stack=cap_t+2.0
upper_plate_engagement=3.0
top_slot_left_x=tray_x-3.2/2
lower_mount_parts=[]
upper_mount_parts=[]
board_screw_lengths=[]
plate_screw_lengths=[]
for idx,yy in enumerate(mount_ys):
    arm_h=lower_mount_z+5.0-base_t
    web=Box(arm_depth_x,arm_width_y,arm_h,align=(Align.MIN,Align.CENTER,Align.MIN)).moved(Location((board_face_x,yy,base_t)))
    foot=Box(foot_depth_x,foot_width_y,foot_height_z,align=(Align.MIN,Align.CENTER,Align.MIN)).moved(Location((board_face_x,yy,base_t)))
    arm=(web+foot).clean()
    board_proxy=Box(1.6,8.0,8.0,align=(Align.MIN,Align.CENTER,Align.CENTER)).moved(Location((board_face_x-1.6,yy,lower_mount_z)))
    mj=make_screw_joint_v1(size='M3',at=Location((board_face_x-1.6,yy,lower_mount_z),(0,-90,0)),through=[(board_proxy,1.6)],engage_depth=motherboard_engagement,into=arm,head='socket_cap',strategy='auto',material=material,boss='none',label=f'motherboard-lower:{yy}')
    arm=(arm-mj.engage_cuts).clean()
    pj=make_screw_joint_v1(size='M3',at=Location((lower_screw_x,yy,0),(180,0,0)),through=[(base,base_t)],engage_depth=lower_plate_engagement,into=arm,head='socket_cap',strategy='auto',material=material,boss='none',label=f'lower-arm-base:{idx}')
    base=(base-pj.through_cuts[0]).clean(); arm=(arm-pj.engage_cuts).clean()
    lower_mount_parts.append(arm); board_screw_lengths.append(mj.screw_length_mm); plate_screw_lengths.append(pj.screw_length_mm)
for idx,yy in enumerate(mount_ys):
    arm_z0=upper_mount_z-5.0
    arm_h=H-cap_t-arm_z0
    web=Box(arm_depth_x,arm_width_y,arm_h,align=(Align.MIN,Align.CENTER,Align.MIN)).moved(Location((board_face_x,yy,arm_z0)))
    foot=Box(foot_depth_x,foot_width_y,foot_height_z,align=(Align.MIN,Align.CENTER,Align.MAX)).moved(Location((board_face_x,yy,H-cap_t)))
    arm=(web+foot).clean()
    board_proxy=Box(1.6,8.0,8.0,align=(Align.MIN,Align.CENTER,Align.CENTER)).moved(Location((board_face_x-1.6,yy,upper_mount_z)))
    mj=make_screw_joint_v1(size='M3',at=Location((board_face_x-1.6,yy,upper_mount_z),(0,-90,0)),through=[(board_proxy,1.6)],engage_depth=motherboard_engagement,into=arm,head='socket_cap',strategy='auto',material=material,boss='none',label=f'motherboard-upper:{yy}')
    arm=(arm-mj.engage_cuts).clean()
    pj=make_screw_joint_v1(size='M3',at=Location((upper_screw_x,yy,H)),through=[(top_cap,upper_cap_stack)],engage_depth=upper_plate_engagement,into=arm,head='socket_cap',strategy='auto',material=material,boss='none',label=f'upper-arm-cap:{idx}')
    top_cap=(top_cap-pj.through_cuts[0]).clean(); arm=(arm-pj.engage_cuts).clean()
    upper_mount_parts.append(arm); board_screw_lengths.append(mj.screw_length_mm); plate_screw_lengths.append(pj.screw_length_mm)
assert len(lower_mount_parts)==2 and len(upper_mount_parts)==2
assert upper_cap_stack==5.0
assert top_slot_left_x-upper_screw_x>3.5
assert all(v==4 for v in board_screw_lengths)
assert all(v==8 for v in plate_screw_lengths)
publish('base',base,'Base mount holes')
publish('top_cap',top_cap,'Clear top holes')
publish('mb_mount_lower_rear',lower_mount_parts[0],'Lower rear mount')
publish('mb_mount_lower_front',lower_mount_parts[1],'Lower front mount')
publish('mb_mount_upper_rear',upper_mount_parts[0],'Upper rear mount')
publish('mb_mount_upper_front',upper_mount_parts[1],'Upper front mount')
print(f'FULL_TOP_HOLE_PASS: upper axes moved to x={upper_screw_x:.1f} mm, {top_slot_left_x-upper_screw_x:.1f} mm from slot edge; two complete M3 clearance circles cut through full 5 mm cap; M3x8 unchanged.')

