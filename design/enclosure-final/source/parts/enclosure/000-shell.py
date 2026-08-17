from screwjoint import make_screw_joint_v1, ScrewJointNotApplicableV1

# Slim frame: four 10 x 10 mm continuous columns with local magnet pads only.
W,D,H=146.0,190.0,225.0
base_t,cap_t,panel_t=3.0,3.0,2.4
post=10.0
panel_clearance=0.6
SCREW_MATERIAL="PLA"
intended_connection_ids=set()
kit_connection_ids=set()
free_connection_ids=set()
joint_bom_lines=[]
screw_hardware_by_connection={}

def require_kit_joint(label, **kwargs):
    intended_connection_ids.add(label)
    try:
        joint=make_screw_joint_v1(label=label, material=SCREW_MATERIAL, **kwargs)
    except ScrewJointNotApplicableV1 as exc:
        free_connection_ids.add(label)
        raise AssertionError(f"printed-screw-joint-v1 rejected {label}: {exc}")
    kit_connection_ids.add(label)
    joint_bom_lines.append(joint.bom)
    screw_hardware_by_connection[label]=joint.hardware
    return joint

# Keep the outer faces at the prior panel datum while moving the inner faces outward.
post_outer_x=W/2-panel_t-panel_clearance
post_outer_y=D/2-panel_t-panel_clearance
post_x=post_outer_x-post/2
post_y=post_outer_y-post/2
post_xy=[(-post_x,-post_y),(-post_x,post_y),(post_x,-post_y),(post_x,post_y)]
assert abs(post_x-65.0)<0.001 and abs(post_y-87.0)<0.001

base=Box(W,D,base_t,align=(Align.CENTER,Align.CENTER,Align.MIN))
posts=None
for x,y in post_xy:
    column=Box(post,post,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,base_t)))
    posts=column if posts is None else posts+column
main_frame=base+posts
tray_x=4.0

# Top M3 kit joints remain directly in the four column centers.
top_screw_xy=list(post_xy)
top_cap=Box(W,D,cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,0,H-cap_t)))
top_cap=top_cap+Box(W-10,D-10,2,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,0,H-cap_t-2)))
top_cap=top_cap-Box(3.2,176,2.2,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((tray_x,0,H-cap_t-2.1)))
top_joints=[]
for i,(x,y) in enumerate(top_screw_xy):
    joint=require_kit_joint(
        f"top-cap:{i}", size="M3", at=Location((x,y,H)),
        through=[(top_cap,cap_t)], head="socket_cap", strategy="auto",
        boss="none", available_depth=20.0
    )
    top_cap=top_cap-joint.through_cuts[0]
    main_frame=main_frame-joint.engage_cuts
    top_joints.append(joint)

# PSU cradle-to-base joints remain kit-owned through the flat base plate.
psu_mount_axes=[(16.0,-72.0),(16.0,72.0),(46.0,-72.0),(46.0,72.0)]
psu_joints=[]
for i,(x,y) in enumerate(psu_mount_axes):
    joint=require_kit_joint(
        f"psu-base:{i}", size="M3", at=Location((x,y,0),(180,0,0)),
        through=[(main_frame,base_t)], head="socket_cap", strategy="auto", boss="auto"
    )
    main_frame=main_frame-joint.through_cuts[0]
    psu_joints.append(joint)

# 15 x 10 x 4 mm magnet seats use compact local pads instead of thick full-height columns.
# Local 15 mm depth retains the established M3 countersunk kit connection.
magnet_w,magnet_h,magnet_t=10.0,15.0,4.0
flat_w,flat_h,flat_d=10.4,15.4,4.2
pad_face_w,pad_depth,pad_h=15.0,15.0,20.0
pad_available_depth=pad_depth-flat_d
assert (pad_face_w-flat_w)/2>=2.0 and (pad_h-flat_h)/2>=2.0
assert pad_available_depth>=10.5
end_z=(30.0,195.0)
side_z=(58.0,167.0)
magnet_joints=[]

# Front/rear-facing pads are shifted inward in X so they never project into side openings.
end_pad_x=post_outer_x-pad_face_w/2
for sy in (-1,1):
    for sx in (-1,1):
        x=sx*end_pad_x
        for z in end_z:
            pad=Box(pad_face_w,pad_depth,pad_h,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((x,sy*(post_outer_y-pad_depth/2),z)))
            main_frame=main_frame+pad
            pocket=Box(flat_w,flat_d,flat_h,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((x,sy*(post_outer_y-flat_d/2),z)))
            main_frame=main_frame-pocket
            magnet_proxy=Box(magnet_w,magnet_t,magnet_h,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((x,sy*(post_outer_y-magnet_t/2),z)))
            joint=require_kit_joint(
                f"magnet-end:{sy}:{sx}:{z}", size="M3",
                at=Location((x,sy*post_outer_y,z),(-90*sy,0,0)),
                through=[(magnet_proxy,magnet_t)], head="countersunk", strategy="auto",
                boss="none", available_depth=pad_available_depth
            )
            main_frame=main_frame-joint.engage_cuts
            magnet_joints.append(joint)

# Left/right-facing pads are shifted inward in Y so they never project into end openings.
side_pad_y=post_outer_y-pad_face_w/2
for sx in (-1,1):
    for sy in (-1,1):
        y=sy*side_pad_y
        for z in side_z:
            pad=Box(pad_depth,pad_face_w,pad_h,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((sx*(post_outer_x-pad_depth/2),y,z)))
            main_frame=main_frame+pad
            pocket=Box(flat_d,flat_w,flat_h,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((sx*(post_outer_x-flat_d/2),y,z)))
            main_frame=main_frame-pocket
            magnet_proxy=Box(magnet_t,magnet_w,magnet_h,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((sx*(post_outer_x-magnet_t/2),y,z)))
            joint=require_kit_joint(
                f"magnet-side:{sx}:{sy}:{z}", size="M3",
                at=Location((sx*post_outer_x,y,z),(0,90*sx,0)),
                through=[(magnet_proxy,magnet_t)], head="countersunk", strategy="auto",
                boss="none", available_depth=pad_available_depth
            )
            main_frame=main_frame-joint.engage_cuts
            magnet_joints.append(joint)

# Four replaceable feet remain kit-fastened through the base.
case_feet=None
foot_joints=[]
for i,(x,y) in enumerate(((-54,-82),(-54,82),(54,-82),(54,82))):
    foot=Cylinder(7,4,align=(Align.CENTER,Align.CENTER,Align.MAX)).moved(Location((x,y,0)))
    joint=require_kit_joint(
        f"case-foot:{i}", size="M3", at=Location((x,y,-4),(180,0,0)),
        through=[(foot,4.0)], head="socket_cap", strategy="auto", boss="auto"
    )
    foot=foot-joint.through_cuts[0]
    main_frame=main_frame+joint.bosses-joint.engage_cuts
    case_feet=foot if case_feet is None else case_feet+foot
    foot_joints.append(joint)

# Removable magnetic exterior panels are unchanged.
front_y=D/2-panel_t/2
front_panel=Box(W,panel_t,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,front_y,base_t)))
front_panel=front_panel-Cylinder(6.1,8,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.X,90).moved(Location((0,front_y,211)))
front_panel=front_panel-Cylinder(7,8,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.X,90).moved(Location((0,D/2,base_t)))
rear_y=-D/2+panel_t/2
rear_panel=Box(W,panel_t,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,rear_y,base_t)))
rear_panel=rear_panel-Box(48,8,126,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((-35,-D/2,74)))
rear_panel=rear_panel-Box(48,8,122,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,-D/2,96)))
rear_panel=rear_panel-Box(46,8,86,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,-D/2,4)))
rear_panel=rear_panel-Cylinder(7,8,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.X,90).moved(Location((0,-D/2,base_t)))

def vent_panel(x,is_right):
    panel=Box(panel_t,D-2*panel_t,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,0,base_t)))
    cutters=None
    count=0
    for row,z in enumerate(range(18,216,18)):
        offset=9 if row%2 else 0
        for y in range(-63,64,18):
            yy=y+offset
            if -72<=yy<=72:
                vent=Cylinder(5.0,8,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location((x,yy,z)))
                cutters=vent if cutters is None else cutters+vent
                count+=1
    panel=(panel-cutters).clean()
    panel=panel-Cylinder(7,8,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location(((W/2 if is_right else -W/2),0,base_t)))
    assert count==88
    return panel.clean()
left_panel=vent_panel(-W/2+panel_t/2,False)
right_panel=vent_panel(W/2-panel_t/2,True)

assert len(post_xy)==4 and len(top_joints)==4 and len(psu_joints)==4
assert len(magnet_joints)==16 and len(foot_joints)==4
assert free_connection_ids==set()
assert intended_connection_ids==kit_connection_ids and len(kit_connection_ids)==28
publish('base_and_frame',main_frame,'Slim four-column frame')
publish('top_cap',top_cap,'Four-hole top cap')
publish('front_panel',front_panel,'Magnetic front panel')
publish('rear_panel',rear_panel,'Rear service panel')
publish('left_panel',left_panel,'Left vent panel')
publish('right_panel',right_panel,'Right vent panel')
print('SLIM_FRAME_PASS: four 10 mm continuous columns, local 15 x 15 x 20 mm magnet pads only, M3 magnet kit joints, M3 top kit joints, open spans restored.')