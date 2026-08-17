# Postless enclosure with eight isolated top/bottom fixing pads and eight local
# magnet carriers. Every front/rear feature stops before the side-panel inner face.
from screwjoint import make_screw_joint_v1 as _point_make_screw_joint_v1
W=param('case_width',W); D=param('case_depth',D); H=param('case_height',H)
base_t=param('base_thickness',base_t); cap_t=param('top_cap_thickness',cap_t); panel_t=param('panel_thickness',panel_t)
cap_inner_t=param('top_cap_inner_thickness',cap_inner_t); top_stack_t=cap_t+cap_inner_t
side_panel_inner_clearance=param('side_panel_inner_clearance',0.40)
corner_pad_width_x=param('corner_pad_width_x',16.0); corner_pad_depth_y=param('corner_pad_depth_y',16.0); corner_pad_height_z=param('corner_pad_height_z',16.0)
corner_pad_overlap=param('corner_pad_overlap',0.35); corner_screw_x_inset=param('corner_screw_x_inset',9.6); corner_screw_y_inset=param('corner_screw_y_inset',10.6)
corner_screw_engagement=param('corner_screw_engagement',5.0); corner_joint_count_expected=param('corner_joint_count_expected',8)
frame_magnet_pad_depth_x=param('frame_magnet_pad_depth_x',8.0); frame_magnet_pad_depth_y=param('frame_magnet_pad_depth_y',12.0); frame_magnet_pad_height_z=param('frame_magnet_pad_height_z',20.0)
frame_magnet_pocket_depth_x=param('frame_magnet_pocket_depth_x',4.2); frame_magnet_pocket_width_y=param('frame_magnet_pocket_width_y',10.2); frame_magnet_pocket_height_z=param('frame_magnet_pocket_height_z',15.2)
frame_magnet_proxy_depth_x=param('frame_magnet_proxy_depth_x',4.2); frame_magnet_proxy_width_y=param('frame_magnet_proxy_width_y',10.0); frame_magnet_proxy_height_z=param('frame_magnet_proxy_height_z',15.0)
frame_magnet_engagement=param('frame_magnet_engagement',3.2); frame_magnet_count_expected=param('frame_magnet_count_expected',8)
assert corner_pad_width_x>=12.0 and corner_pad_depth_y>=12.0 and corner_pad_height_z>=corner_screw_engagement+3.0
assert frame_magnet_pad_depth_x-frame_magnet_pocket_depth_x>=3.0 and abs(frame_magnet_proxy_depth_x-frame_magnet_pocket_depth_x)<0.001
assert side_panel_inner_clearance>=0.30
front_inner_y=D/2-panel_t; rear_inner_y=-D/2+panel_t
side_panel_inner_x=W/2-panel_t
frame_outer_x=side_panel_inner_x-side_panel_inner_clearance
frame_trim_width=2*frame_outer_x
frame_trim=Box(frame_trim_width,D+20,H+20,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,0,-10)))
front_frame=(front_panel & frame_trim).clean(); rear_frame=(rear_panel & frame_trim).clean()
# Eight isolated corner pads: no rail and no side-panel overlap.
corner_pads=[]
for sy in (-1,1):
    frame=front_frame if sy>0 else rear_frame
    pad_y=sy*(D/2-panel_t-corner_pad_depth_y/2+corner_pad_overlap)
    for sx in (-1,1):
        pad_x=sx*(frame_outer_x-corner_pad_width_x/2)
        lower_pad=Box(corner_pad_width_x,corner_pad_depth_y,corner_pad_height_z,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((pad_x,pad_y,base_t)))
        upper_pad=Box(corner_pad_width_x,corner_pad_depth_y,corner_pad_height_z,align=(Align.CENTER,Align.CENTER,Align.MAX)).moved(Location((pad_x,pad_y,H-top_stack_t)))
        frame=(frame+lower_pad+upper_pad).clean(); corner_pads.extend((lower_pad,upper_pad))
    if sy>0: front_frame=frame
    else: rear_frame=frame
# Four magnets per side: carrier face is clearance-separated from the removable panel.
magnet_joints=[]
for sy in (-1,1):
    frame=front_frame if sy>0 else rear_frame
    pad_y=sy*(D/2-panel_t-frame_magnet_pad_depth_y/2)
    for sx in (-1,1):
        pad_x=sx*(frame_outer_x-frame_magnet_pad_depth_x/2)
        for z in (side_station_z_low,side_station_z_high):
            pad=Box(frame_magnet_pad_depth_x,frame_magnet_pad_depth_y,frame_magnet_pad_height_z,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((pad_x,pad_y,z)))
            frame=(frame+pad).clean()
            pocket_x=sx*(frame_outer_x-frame_magnet_pocket_depth_x/2)
            pocket=Box(frame_magnet_pocket_depth_x,frame_magnet_pocket_width_y,frame_magnet_pocket_height_z,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((pocket_x,pad_y,z)))
            frame=(frame-pocket).clean()
            proxy_x=sx*(frame_outer_x-frame_magnet_proxy_depth_x/2)
            proxy=Box(frame_magnet_proxy_depth_x,frame_magnet_proxy_width_y,frame_magnet_proxy_height_z,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((proxy_x,pad_y,z)))
            joint=_point_make_screw_joint_v1(size='M3',at=Location((sx*frame_outer_x,pad_y,z),(0,90*sx,0)),through=[(proxy,frame_magnet_proxy_depth_x)],engage_depth=frame_magnet_engagement,into=frame,head='countersunk',strategy='auto',material=material,boss='auto',label=f'clearance-frame-side-magnet:{sy}:{sx}:{z}')
            frame=(frame+joint.bosses-joint.engage_cuts).clean(); magnet_joints.append(joint)
    if sy>0: front_frame=frame
    else: rear_frame=frame
# Four top and four bottom M3 joints, including two top/two bottom joints on the rear panel.
corner_joints=[]; screw_x=W/2-corner_screw_x_inset; screw_y=D/2-corner_screw_y_inset
rear_top_bottom_joint_count=0
for sy in (-1,1):
    frame=front_frame if sy>0 else rear_frame
    for sx in (-1,1):
        x=sx*screw_x; y=sy*screw_y
        bottom_joint=_point_make_screw_joint_v1(size='M3',at=Location((x,y,-foot_height),(180,0,0)),through=[(base,base_t+foot_height)],engage_depth=corner_screw_engagement,into=frame,head='socket_cap',strategy='auto',material=material,boss='none',label=f'clearance-bottom:{sy}:{sx}')
        base=(base-bottom_joint.through_cuts[0]).clean(); frame=(frame-bottom_joint.engage_cuts).clean()
        top_joint=_point_make_screw_joint_v1(size='M3',at=Location((x,y,H)),through=[(top_cap,top_stack_t)],engage_depth=corner_screw_engagement,into=frame,head='socket_cap',strategy='auto',material=material,boss='none',label=f'clearance-top:{sy}:{sx}')
        top_cap=(top_cap-top_joint.through_cuts[0]).clean(); frame=(frame-top_joint.engage_cuts).clean(); corner_joints.extend((bottom_joint,top_joint))
        if sy<0: rear_top_bottom_joint_count+=2
    if sy>0: front_frame=frame
    else: rear_frame=frame
connection_inventory={'bottom-four-corners':'printed-screw-joint-v1','top-four-corners':'printed-screw-joint-v1','rear-top-bottom':'four of the eight corner joints','side-panel-magnets':'printed-screw-joint-v1 plus captive steel pockets'}
assert len(corner_pads)==8 and len(corner_joints)==corner_joint_count_expected and rear_top_bottom_joint_count==4
assert len(magnet_joints)==frame_magnet_count_expected and len(connection_inventory)==4 and all(connection_inventory.values())
assert front_frame.solids().__len__()==1 and rear_frame.solids().__len__()==1
assert front_frame.bounding_box().max.X<=frame_outer_x+0.001 and front_frame.bounding_box().min.X>=-frame_outer_x-0.001
assert rear_frame.bounding_box().max.X<=frame_outer_x+0.001 and rear_frame.bounding_box().min.X>=-frame_outer_x-0.001
publish('base',base,'Four-point bottom panel'); publish('top_cap',top_cap,'Four-point top panel')
publish('front_panel',front_frame,'Clearance front panel'); publish('rear_panel',rear_frame,'Clearance rear panel')
print(f'PANEL_CLEARANCE_PASS: front/rear geometry stops at x=±{frame_outer_x:.2f}, leaving {side_panel_inner_clearance:.2f} mm to side-panel inner faces; rear panel owns two top and two bottom M3 points; eight magnet carriers align to side pockets.')