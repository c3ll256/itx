# Source geometry plus an authoritative retired-component publication filter.
_workbench_publish=publish
retired_component_ids={'column_fl','column_rl','column_fr','column_rr','case_feet','foot_front_left','foot_rear_right','foot_front_right','mb_mount_lower_rear'}
def publish(object_id,shape,label):
    if object_id in retired_component_ids: return None
    return _workbench_publish(object_id,shape,label)
from screwjoint import make_screw_joint_v1 as _make_screw_joint_v1
def make_screw_joint_v1(*args,engage_depth=None,**kwargs):
    if engage_depth is None:
        label=kwargs.get('label','')
        if label.startswith('motherboard-'): engage_depth=param('motherboard_default_engagement',7.5)
        elif label.startswith('gpu-slot-bracket:'): engage_depth=param('gpu_default_engagement',2.5)
        elif label.startswith('rear-panel:'): engage_depth=param('rear_panel_default_engagement',5.6)
        else: engage_depth=param('general_default_engagement',5.0)
    return _make_screw_joint_v1(*args,engage_depth=engage_depth,**kwargs)
W=param('case_width',146.0); D=param('case_depth',190.0); H=param('case_height',262.0)
base_t=param('base_thickness',3.0); cap_t=param('top_cap_thickness',3.0); panel_t=param('panel_thickness',2.4)
cap_inner_t=param('top_cap_inner_thickness',2.0); cap_inset=param('top_cap_inner_inset',5.0); top_stack_t=cap_t+cap_inner_t
post=param('column_size',14.0); clearance=param('panel_clearance',0.6); material='PLA'; tray_x=param('legacy_tray_axis_x',4.0)
end_station_z_low=param('end_station_z_low',30.0); end_station_z_high=param('end_station_z_high',210.0)
side_station_z_low=param('side_station_z_low',58.0); side_station_z_high=param('side_station_z_high',167.0)
station_pocket_size=param('station_pocket_size',10.2); station_pocket_depth=param('station_pocket_depth',3.2)
station_proxy_size=param('station_proxy_size',10.0); station_proxy_depth=param('station_proxy_depth',3.0)
station_edge_offset=param('station_edge_offset',1.6); station_proxy_offset=param('station_proxy_offset',1.5)
side_magnet_height_z=param('side_magnet_height_z',15.2); side_magnet_width_y=param('side_magnet_width_y',10.2); side_magnet_pocket_depth_x=param('side_magnet_pocket_depth_x',4.2)
side_magnet_proxy_height_z=param('side_magnet_proxy_height_z',15.0); side_magnet_proxy_width_y=param('side_magnet_proxy_width_y',10.0); side_magnet_proxy_depth_x=param('side_magnet_proxy_depth_x',4.0)
side_magnet_edge_offset_x=param('side_magnet_edge_offset_x',2.1); side_magnet_proxy_offset_x=param('side_magnet_proxy_offset_x',2.0); side_magnet_engagement=param('side_magnet_engagement',6.0)
top_joint_engagement=param('top_joint_engagement',3.0); foot_radius=param('foot_radius',8.0); foot_height=param('foot_height',4.0)
front_button_radius=param('power_button_radius',6.1); cut_depth=param('panel_cut_depth',8.0); initial_button_x=param('initial_button_x',0.0); initial_button_z=param('initial_button_z',211.0)
rear_io_w=param('rear_io_width',48.0); rear_io_h=param('rear_io_height',126.0); rear_io_x=param('rear_io_x',-35.0); rear_io_z=param('rear_io_z',74.0)
rear_aux_w=param('rear_aux_width',48.0); rear_aux_h=param('rear_aux_height',122.0); rear_aux_x=param('rear_aux_x',31.0); rear_aux_z=param('rear_aux_z',96.0)
psu_cut_w=param('sfx_rear_cut_width',125.8); psu_cut_h=param('sfx_rear_cut_height',64.3); psu_cut_x=param('sfx_rear_cut_x',0.0); psu_cut_z=param('sfx_rear_cut_z',3.5)
outer_x=W/2-panel_t-clearance; outer_y=D/2-panel_t-clearance; post_x=outer_x-post/2; post_y=outer_y-post/2
post_xy=[(-post_x,-post_y),(-post_x,post_y),(post_x,-post_y),(post_x,post_y)]; ids=('fl','rl','fr','rr')
base=Box(W,D,base_t,align=(Align.CENTER,Align.CENTER,Align.MIN)); columns=[]; base_joints=[]; top_joints=[]; magnet_joint_count=0
for i,(x,y) in enumerate(post_xy):
    c=Box(post,post,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,base_t))); sy=-1 if y<0 else 1
    for z in (end_station_z_low,end_station_z_high):
        c=c-Box(station_pocket_size,station_pocket_depth,station_pocket_size,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((x,sy*(outer_y-station_edge_offset),z)))
        proxy=Box(station_proxy_size,station_proxy_depth,station_proxy_size,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((x,sy*(outer_y-station_proxy_offset),z)))
        j=make_screw_joint_v1(size='M3',at=Location((x,sy*outer_y,z),(-90*sy,0,0)),through=[(proxy,station_proxy_depth)],into=c,head='countersunk',strategy='auto',material=material,boss='auto',label=f'magnet-end:{ids[i]}:{z}'); c=c+j.bosses-j.engage_cuts; magnet_joint_count+=1
    sx=-1 if x<0 else 1
    for z in (side_station_z_low,side_station_z_high):
        c=c-Box(side_magnet_pocket_depth_x,side_magnet_width_y,side_magnet_height_z,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((sx*(outer_x-side_magnet_edge_offset_x),y,z)))
        proxy=Box(side_magnet_proxy_depth_x,side_magnet_proxy_width_y,side_magnet_proxy_height_z,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((sx*(outer_x-side_magnet_proxy_offset_x),y,z)))
        j=make_screw_joint_v1(size='M3',at=Location((sx*outer_x,y,z),(0,90*sx,0)),through=[(proxy,side_magnet_proxy_depth_x)],engage_depth=side_magnet_engagement,into=c,head='countersunk',strategy='auto',material=material,boss='auto',label=f'magnet-side:{ids[i]}:{z}'); c=c+j.bosses-j.engage_cuts; magnet_joint_count+=1
    top_proxy=Box(station_proxy_size,station_proxy_size,top_stack_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,H-top_stack_t)))
    tj=make_screw_joint_v1(size='M3',at=Location((x,y,H)),through=[(top_proxy,top_stack_t)],engage_depth=top_joint_engagement,into=c,head='socket_cap',strategy='auto',material=material,boss='auto',label=f'column-top:{ids[i]}'); c=c+tj.bosses-tj.engage_cuts; top_joints.append(tj); columns.append(c)
feet=[]
for i,((x,y),c) in enumerate(zip(post_xy,columns)):
    foot=Cylinder(foot_radius,foot_height,align=(Align.CENTER,Align.CENTER,Align.MAX)).moved(Location((x,y,0)))
    j=make_screw_joint_v1(size='M3',at=Location((x,y,-foot_height),(180,0,0)),through=[(foot,foot_height),(base,base_t)],into=c,head='socket_cap',strategy='auto',material=material,boss='auto',label=f'foot-base-column:{ids[i]}')
    foot=foot-j.through_cuts[0]; base=base-j.through_cuts[1]; columns[i]=c+j.bosses-j.engage_cuts; feet.append(foot); base_joints.append(j)
top_cap=Box(W,D,cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,0,H-cap_t)))+Box(W-2*cap_inset,D-2*cap_inset,cap_inner_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,0,H-cap_t-cap_inner_t)))
for j in top_joints: top_cap=top_cap-j.through_cuts[0]
front_y=D/2-panel_t/2; front_panel=Box(W,panel_t,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,front_y,base_t))); front_panel=front_panel-Cylinder(front_button_radius,cut_depth,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.X,90).moved(Location((initial_button_x,front_y,initial_button_z)))
rear_y=-D/2+panel_t/2; rear_panel=Box(W,panel_t,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,rear_y,base_t)))
rear_panel=rear_panel-Box(rear_io_w,cut_depth,rear_io_h,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((rear_io_x,-D/2,rear_io_z)))-Box(rear_aux_w,cut_depth,rear_aux_h,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((rear_aux_x,-D/2,rear_aux_z)))-Box(psu_cut_w,cut_depth,psu_cut_h,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((psu_cut_x,-D/2,psu_cut_z)))

# Build side panels without the old circular vent pattern
left_panel=Box(panel_t,D-2*panel_t,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((-W/2+panel_t/2,0,base_t)))
right_panel=Box(panel_t,D-2*panel_t,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((W/2-panel_t/2,0,base_t)))

assert len(columns)==4 and len(base_joints)==4 and len(feet)==4 and magnet_joint_count==16 and len(top_joints)==4
publish('base',base,'Source base'); publish('top_cap',top_cap,'Source top'); publish('front_panel',front_panel,'Source front'); publish('rear_panel',rear_panel,'Source rear'); publish('left_panel',left_panel,'Left solid panel'); publish('right_panel',right_panel,'Right solid panel')
print(f'RETIRED_COMPONENT_FILTER_ACTIVE: {len(retired_component_ids)} legacy object IDs are suppressed during the complete target replay.')