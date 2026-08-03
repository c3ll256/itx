# cell: shell_columns
from screwjoint import make_screw_joint_v1 as _make_screw_joint_v1
# Historical API bridge retained for downstream cells; obsolete tray slots are
# no longer created in the authoritative shell geometry.
def make_screw_joint_v1(*args, engage_depth=None, **kwargs):
    if engage_depth is None:
        label=kwargs.get('label','')
        if label.startswith('motherboard-'):
            engage_depth=7.5
        elif label.startswith('gpu-slot-bracket:'):
            engage_depth=2.5
        elif label.startswith('rear-panel:'):
            engage_depth=5.6
        else:
            engage_depth=5.0
    return _make_screw_joint_v1(*args, engage_depth=engage_depth, **kwargs)
W,D,H=146.0,190.0,225.0
base_t,cap_t,panel_t=3.0,3.0,2.4
top_stack_t=cap_t+2.0
post=14.0; clearance=0.6; material='PLA'; tray_x=4.0
outer_x=W/2-panel_t-clearance; outer_y=D/2-panel_t-clearance
post_x=outer_x-post/2; post_y=outer_y-post/2
post_xy=[(-post_x,-post_y),(-post_x,post_y),(post_x,-post_y),(post_x,post_y)]
ids=('fl','rl','fr','rr')
base=Box(W,D,base_t,align=(Align.CENTER,Align.CENTER,Align.MIN))
columns=[]; base_joints=[]; top_joints=[]; magnet_joint_count=0
for i,(x,y) in enumerate(post_xy):
    c=Box(post,post,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,base_t)))
    sy=-1 if y<0 else 1
    for z in (30.0,210.0):
        c=c-Box(10.2,3.2,10.2,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((x,sy*(outer_y-1.6),z)))
        proxy=Box(10,3,10,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((x,sy*(outer_y-1.5),z)))
        j=make_screw_joint_v1(size='M3',at=Location((x,sy*outer_y,z),(-90*sy,0,0)),through=[(proxy,3.0)],into=c,head='countersunk',strategy='auto',material=material,boss='auto',label=f'magnet-end:{ids[i]}:{z}')
        c=c+j.bosses-j.engage_cuts; magnet_joint_count+=1
    sx=-1 if x<0 else 1
    for z in (58.0,167.0):
        c=c-Box(3.2,10.2,10.2,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((sx*(outer_x-1.6),y,z)))
        proxy=Box(3,10,10,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((sx*(outer_x-1.5),y,z)))
        j=make_screw_joint_v1(size='M3',at=Location((sx*outer_x,y,z),(0,90*sx,0)),through=[(proxy,3.0)],into=c,head='countersunk',strategy='auto',material=material,boss='auto',label=f'magnet-side:{ids[i]}:{z}')
        c=c+j.bosses-j.engage_cuts; magnet_joint_count+=1
    # The cap is a 5 mm two-layer stack. Clearance must pass through both
    # layers; 3 mm engagement keeps the existing M3x8 fastener length.
    top_proxy=Box(10,10,top_stack_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,H-top_stack_t)))
    tj=make_screw_joint_v1(size='M3',at=Location((x,y,H)),through=[(top_proxy,top_stack_t)],engage_depth=3.0,into=c,head='socket_cap',strategy='auto',material=material,boss='auto',label=f'column-top:{ids[i]}')
    c=c+tj.bosses-tj.engage_cuts; top_joints.append(tj); columns.append(c)
feet=[]
for i,((x,y),c) in enumerate(zip(post_xy,columns)):
    foot=Cylinder(8,4,align=(Align.CENTER,Align.CENTER,Align.MAX)).moved(Location((x,y,0)))
    j=make_screw_joint_v1(size='M3',at=Location((x,y,-4),(180,0,0)),through=[(foot,4.0),(base,base_t)],into=c,head='socket_cap',strategy='auto',material=material,boss='auto',label=f'foot-base-column:{ids[i]}')
    foot=foot-j.through_cuts[0]; base=base-j.through_cuts[1]
    columns[i]=c+j.bosses-j.engage_cuts; feet.append(foot); base_joints.append(j)
# Continuous two-layer top cap: no tray slot, tongue groove, or guide channel.
top_cap=Box(W,D,cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,0,H-cap_t)))+Box(W-10,D-10,2,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,0,H-cap_t-2)))
for j in top_joints: top_cap=top_cap-j.through_cuts[0]
front_y=D/2-panel_t/2
front_panel=Box(W,panel_t,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,front_y,base_t)))
front_panel=front_panel-Cylinder(6.1,8,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.X,90).moved(Location((0,front_y,211)))
rear_y=-D/2+panel_t/2
rear_panel=Box(W,panel_t,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,rear_y,base_t)))
rear_panel=rear_panel-Box(48,8,126,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((-35,-D/2,74)))-Box(48,8,122,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,-D/2,96)))-Box(46,8,86,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,-D/2,4)))
def vent_panel(x):
    panel=Box(panel_t,D-2*panel_t,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,0,base_t))); cuts=None
    for row,z in enumerate(range(18,216,18)):
        off=9 if row%2 else 0
        for y in range(-63,64,18):
            yy=y+off
            if -72<=yy<=72:
                v=Cylinder(5,8,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location((x,yy,z))); cuts=v if cuts is None else cuts+v
    return (panel-cuts).clean()
left_panel=vent_panel(-W/2+panel_t/2); right_panel=vent_panel(W/2-panel_t/2)
assert len(columns)==4 and len(base_joints)==4 and len(feet)==4 and magnet_joint_count==16
assert len(top_joints)==4
assert all(abs(j.through_thickness_mm-top_stack_t)<0.001 for j in top_joints)
assert all(abs(j.screw_length_mm-8.0)<0.001 for j in top_joints)
publish('base',base,'Detachable column base'); publish('column_fl',columns[0],'Front left column'); publish('column_rl',columns[1],'Rear left column'); publish('column_fr',columns[2],'Front right column'); publish('column_rr',columns[3],'Rear right column')
publish('case_feet',Compound(children=feet),'Coaxial screw feet')
publish('top_cap',top_cap,'Through-hole top cap'); publish('front_panel',front_panel,'Front panel'); publish('rear_panel',rear_panel,'Rear panel'); publish('left_panel',left_panel,'Left vent panel'); publish('right_panel',right_panel,'Right vent panel')
print('TOP_CAP_THROUGH_PASS: all four M3 clearance holes pass through the complete 5 mm top-cap stack; column receiver holes retain 3 mm printed engagement and M3x8 hardware.')

