# Replace all framed magnet pads with 10 x 10 x 3 mm pockets cut directly into four columns.
# Reset the screw inventory because this cell supersedes the earlier shell fastening geometry.
intended_connection_ids=set()
kit_connection_ids=set()
free_connection_ids=set()
joint_bom_lines=[]
screw_hardware_by_connection={}

post=14.0
post_outer_x=W/2-panel_t-panel_clearance
post_outer_y=D/2-panel_t-panel_clearance
post_x=post_outer_x-post/2
post_y=post_outer_y-post/2
post_xy=[(-post_x,-post_y),(-post_x,post_y),(post_x,-post_y),(post_x,post_y)]
assert abs(post_x-63.0)<0.001 and abs(post_y-85.0)<0.001

# Plain base plus four uninterrupted rectangular columns: no pad, frame, tower, or collar.
base=Box(W,D,base_t,align=(Align.CENTER,Align.CENTER,Align.MIN))
posts=None
for x,y in post_xy:
    column=Box(post,post,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,base_t)))
    posts=column if posts is None else posts+column
main_frame=base+posts

# Rebuild top cap holes directly over the new column centers.
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

# Preserve PSU and foot fastening interfaces.
psu_mount_axes=[(16.0,-72.0),(16.0,72.0),(46.0,-72.0),(46.0,72.0)]
psu_joints=[]
for i,(x,y) in enumerate(psu_mount_axes):
    joint=require_kit_joint(
        f"psu-base:{i}", size="M3", at=Location((x,y,0),(180,0,0)),
        through=[(main_frame,base_t)], head="socket_cap", strategy="auto", boss="auto"
    )
    main_frame=main_frame-joint.through_cuts[0]
    psu_joints.append(joint)

# User-selected 10 x 10 x 3 mm square magnet, recessed directly in each column face.
magnet_w=10.0
magnet_h=10.0
magnet_t=3.0
pocket_w=10.2
pocket_h=10.2
pocket_d=3.2
magnet_available_depth=post-pocket_d
assert (post-pocket_w)/2>=1.8
assert magnet_available_depth>=10.5
end_z=(30.0,210.0)   # upper rear/front seat clears the tall left rear aperture
side_z=(58.0,167.0)
magnet_joints=[]

# Front and rear faces: pocket center is the column center; no surrounding frame is added.
for sy in (-1,1):
    for x in (-post_x,post_x):
        for z in end_z:
            pocket=Box(pocket_w,pocket_d,pocket_h,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((x,sy*(post_outer_y-pocket_d/2),z)))
            main_frame=main_frame-pocket
            magnet_proxy=Box(magnet_w,magnet_t,magnet_h,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((x,sy*(post_outer_y-magnet_t/2),z)))
            joint=require_kit_joint(
                f"magnet-end:{sy}:{x}:{z}", size="M3",
                at=Location((x,sy*post_outer_y,z),(-90*sy,0,0)),
                through=[(magnet_proxy,magnet_t)], head="countersunk", strategy="auto",
                boss="none", available_depth=magnet_available_depth
            )
            main_frame=main_frame-joint.engage_cuts
            magnet_joints.append(joint)

# Left and right faces: same direct pocket treatment.
for sx in (-1,1):
    for y in (-post_y,post_y):
        for z in side_z:
            pocket=Box(pocket_d,pocket_w,pocket_h,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((sx*(post_outer_x-pocket_d/2),y,z)))
            main_frame=main_frame-pocket
            magnet_proxy=Box(magnet_t,magnet_w,magnet_h,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((sx*(post_outer_x-magnet_t/2),y,z)))
            joint=require_kit_joint(
                f"magnet-side:{sx}:{y}:{z}", size="M3",
                at=Location((sx*post_outer_x,y,z),(0,90*sx,0)),
                through=[(magnet_proxy,magnet_t)], head="countersunk", strategy="auto",
                boss="none", available_depth=magnet_available_depth
            )
            main_frame=main_frame-joint.engage_cuts
            magnet_joints.append(joint)

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

# Restore side panels without the obsolete rear-pad relief notches.
left_panel=vent_panel(-W/2+panel_t/2,False)
right_panel=vent_panel(W/2-panel_t/2,True)

# Hard rear-aperture keepouts remain tied to the rear-panel cuts and trim only hidden column overlap.
rear_keepouts=[
    (-35.0,137.0,49.6,127.6),
    (31.0,157.0,49.6,123.6),
    (31.0,47.0,47.6,87.6),
]
for x,z,w,h in rear_keepouts:
    keepout=Box(w,30.0,h,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((x,-85.0,z)))
    main_frame=main_frame-keepout

assert len(post_xy)==4 and len(top_joints)==4 and len(psu_joints)==4
assert len(magnet_joints)==16 and len(foot_joints)==4
assert free_connection_ids==set()
assert intended_connection_ids==kit_connection_ids and len(kit_connection_ids)==28
publish('base_and_frame',main_frame,'Direct-magnet frame')
publish('top_cap',top_cap,'Four-hole top cap')
publish('left_panel',left_panel,'Left vent panel')
publish('right_panel',right_panel,'Right vent panel')
publish('case_feet',case_feet,'Four kit-fastened feet')
print('DIRECT_MAGNET_PASS: 16 pockets, each 10.2 x 10.2 x 3.2 mm, cut directly into four 14 mm columns; zero magnet frames or pads; M3 center screws remain kit-owned.')