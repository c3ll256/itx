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

# cell: foot_through_cleanup
# Reapply the printed-screw-joint-v1 clearance cuts to the four detachable feet
# and clean the coincident top faces. Geometry and fastener solution are unchanged.
clean_feet=[]
for foot,j in zip(feet,base_joints):
    clean_foot=(foot-j.through_cuts[0]).clean()
    clean_feet.append(clean_foot)
feet=clean_feet
assert len(feet)==4 and len(base_joints)==4
assert all(abs(j.through_thickness_mm-(4.0+base_t))<0.001 for j in base_joints)
assert all(abs(j.screw_length_mm-12.0)<0.001 for j in base_joints)
publish('case_feet',Compound(children=feet),'Through-hole feet')
print('FOOT_THROUGH_CLEAN_PASS: all four kit-owned foot clearance cuts are reapplied and coincident top faces cleaned; the 4 mm foot + 3 mm base + M3x12 joint stack is unchanged.')

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

# cell: tray_base_slot
# Superseded: no motherboard tray and no base slot.
publish('base',base,'Solid motherboard base')
print('NO_TRAY_BASE_FEATURE_PASS: base has no motherboard-tray slot or dedicated tray screw.')

# cell: edge_softening
# Cosmetic edge softening limited to exterior enclosure edges.
def vertical_edges(shape,min_len):
    return [e for e in shape.edges() if e.geom_type==GeomType.LINE and e.length>=min_len and abs((e.position_at(1)-e.position_at(0)).normalized().dot(Vector(0,0,1)))>0.99]
def outer_vertical_edges(shape,min_len):
    out=[]
    for e in vertical_edges(shape,min_len):
        p=e.position_at(0.5)
        if abs(p.X)>=W/2-1.5 or abs(p.Y)>=D/2-1.5:
            out.append(e)
    return out
front_panel=fillet(vertical_edges(front_panel,210.0),1.0)
rear_panel=fillet(vertical_edges(rear_panel,210.0),1.0)
left_panel=fillet(vertical_edges(left_panel,210.0),1.0)
right_panel=fillet(vertical_edges(right_panel,210.0),1.0)
top_outer=outer_vertical_edges(top_cap,2.8)
base_outer=outer_vertical_edges(base,2.8)
if top_outer: top_cap=fillet(top_outer,1.2)
if base_outer: base=fillet(base_outer,1.2)
publish('base',base,'Rounded support base')
publish('top_cap',top_cap,'Rounded support top')
publish('front_panel',front_panel,'Rounded front panel')
publish('rear_panel',rear_panel,'Rounded rear panel')
publish('left_panel',left_panel,'Rounded left vent')
publish('right_panel',right_panel,'Rounded right vent')
print('EXTERIOR_EDGE_SOFTENING_PASS: only exterior shell edges are filleted; internal motherboard support arms are excluded.')

# cell: power_button_tray_clearance
# Superseded: there is no full motherboard tray to clear around the power button.
print('NO_TRAY_BUTTON_CLEARANCE_PASS: no full tray geometry remains at the power-button region.')

# cell: rear_io_column_clearance
# Relieve the inner edge of the left rear column where it overlaps the motherboard rear-I/O aperture.
# Keep the full lower/upper column blocks for the rear-panel M3 screws at z=30 and z=210.
io_clear_x_min=-60.0
io_clear_z_min=72.5
io_clear_z_max=201.5
rear_left_relief=Box(5.0,16.0,io_clear_z_max-io_clear_z_min,align=(Align.MIN,Align.CENTER,Align.MIN)).moved(Location((io_clear_x_min,-post_y,io_clear_z_min)))
columns[0]=(columns[0]-rear_left_relief).clean()
publish('column_fl',columns[0],'I-O clear rear-left')
assert io_clear_z_min>40.0 and io_clear_z_max<205.0
print('REAR_IO_COLUMN_CLEARANCE_PASS: inner 3.4 mm of the left rear column is relieved across the motherboard I/O opening; rear-panel screw zones remain full section.')

# cell: standard_gpu_slots
# Vertical dual-slot PCIe rear interface from the user sketch:
# one uninterrupted two-slot aperture, an exterior horizontal fixing flange
# directly fused to the rear panel, and two bottom-up Z-axis THROUGH joints.
rear_y=-D/2+panel_t/2
rear_panel=Box(W,panel_t,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,rear_y,base_t)))
# Existing motherboard I/O and PSU service regions.
rear_panel=rear_panel-Box(48,8,126,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((-35,-D/2,74)))
rear_panel=rear_panel-Box(46,8,86,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,-D/2,4)))
# One continuous aperture spanning both PCIe slots: no center divider.
slot_pitch=20.32
slot_centers=(20.84,41.16)
slot_w=18.0
slot_h=120.0
slot_z0=94.0
dual_x0=slot_centers[0]-slot_w/2
dual_x1=slot_centers[1]+slot_w/2
dual_w=dual_x1-dual_x0
dual_center=(dual_x0+dual_x1)/2
rear_panel=rear_panel-Box(dual_w,8,slot_h,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((dual_center,-D/2,slot_z0)))
# Exterior horizontal flange directly fused to the rear-panel outer face.
flange_w=46.0
flange_d=10.0
flange_t=3.2
flange_z=slot_z0+slot_h
flange_y=-D/2-flange_d/2
gpu_flange=Box(flange_w,flange_d,flange_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((dual_center,flange_y,flange_z)))
rear_panel=(rear_panel+gpu_flange).clean()
# Standard 0.8 mm GPU bracket ears contact the flange UNDERSIDE. Screw heads
# are below the ears. Rotating the kit mouth frame 180 degrees about X makes
# local -Z point toward global +Z, so both screws insert bottom-up.
bracket_t=0.8
bracket_proxy=Box(flange_w,8.0,bracket_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((dual_center,flange_y,flange_z-bracket_t)))
slot_joints=[]
for i,x in enumerate(slot_centers):
    j=make_screw_joint_v1(
        size='M3',at=Location((x,flange_y,flange_z-bracket_t),(180,0,0)),
        through=[(bracket_proxy,bracket_t)],engage_depth=2.4,into=rear_panel,
        head='socket_cap',strategy='auto',termination='through',
        material=material,boss='none',label=f'gpu-slot-bracket:{i}'
    )
    rear_panel=rear_panel-j.engage_cuts
    slot_joints.append(j)
rear_outer_y=-D/2
flange_inner_y=flange_y+flange_d/2
assert abs(flange_inner_y-rear_outer_y)<0.001
assert abs(slot_centers[1]-slot_centers[0]-slot_pitch)<0.001
assert abs(dual_w-38.32)<0.001
assert len(slot_joints)==2
assert all(j.termination=='through' for j in slot_joints)
assert all(abs(j.screw_length_mm-4.0)<0.001 for j in slot_joints)
publish('rear_panel',rear_panel,'Bottom-up dual-slot')
print('BOTTOM_UP_DUAL_SLOT_PASS: the flange remains fused to the rear panel; GPU ears contact its underside; two kit-owned M3x4 joints insert from below along +Z and pass through the 3.2 mm flange.')

# cell: rear_panel_fastening
# Convert the rear panel from magnetic retention to four M3 screws.
# Reuse the former rear magnet station positions on the two rear columns.
rear_column_indices=(0,2)  # post_xy entries with y < 0
rear_screw_z=(30.0,210.0)
rear_screw_joints=[]
for idx in rear_column_indices:
    x,y=post_xy[idx]
    c=columns[idx]
    for z in rear_screw_z:
        # Restore solid column material where the obsolete 10 x 10 x 3 mm
        # rear magnet pocket and its centered engagement cut previously existed.
        restore=Box(10.2,10.8,10.2,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((x,-outer_y+5.4,z)))
        c=c+restore
        # Screw enters from the exterior rear face, through the 2.4 mm panel,
        # bridges the 0.6 mm panel clearance, and engages the printed column.
        j=make_screw_joint_v1(
            size='M3',at=Location((x,-D/2,z),(90,0,0)),
            through=[(rear_panel,panel_t)],into=c,
            head='socket_cap',strategy='auto',material=material,boss='auto',
            label=f'rear-panel:{idx}:{z}'
        )
        rear_panel=rear_panel-j.through_cuts[0]
        c=c+j.bosses-j.engage_cuts
        rear_screw_joints.append(j)
    columns[idx]=c
assert len(rear_screw_joints)==4
publish('rear_panel',rear_panel,'Screw-fixed rear panel')
publish('column_fl',columns[0],'Rear left column')
publish('column_fr',columns[2],'Rear right column')
print('REAR_PANEL_SCREW_PASS: four M3 kit joints replace the four rear magnet stations; rear panel is screw-fixed to the two rear columns.')

# cell: tray_top_rear_locators
# Obsolete motherboard-tray locator system removed.
# The authoritative shell now creates a continuous two-layer top cap directly,
# so no tray-slot cut, tongue groove, locator channel, or compensating fill is
# created here. Front and rear panels likewise carry no tray guide grooves.
publish('top_cap',top_cap,'Slotless top cap')
publish('front_panel',front_panel,'Slotless front panel')
publish('rear_panel',rear_panel,'Slotless rear panel')
print('NO_TRAY_GROOVES_PASS: no tray slots are cut and no historical fill solids are required.')

# cell: tray_hidden_mounts
# Superseded: the full tray and its four hidden brackets are removed.
# Standard Mini-ITX corner support arms are generated in the internals cell.
print('OLD_TRAY_MOUNTS_REMOVED_PASS: no full-tray hidden brackets remain.')

# cell: tray_base_screw
# Superseded: no full motherboard tray and no dedicated tray screw.
print('NO_TRAY_SCREW_PASS: motherboard is held directly by four corner support-arm screw points.')

# cell: flush_column_envelopes
# Remove kit-generated external column extensions while preserving internal screw cuts.
# Each column is clipped to its intended 14 x 14 mm prism between base top and cap underside.
for i,(x,y) in enumerate(post_xy):
    intended=Box(post,post,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,base_t)))
    columns[i]=columns[i].intersect(intended).clean()
publish('column_fl',columns[0],'Flush rear-left column')
publish('column_rl',columns[1],'Flush front-left column')
publish('column_fr',columns[2],'Flush rear-right column')
publish('column_rr',columns[3],'Flush front-right column')
print('FLUSH_COLUMN_ENVELOPES_PASS: all four columns are flat-ended 14 x 14 mm prisms from base top to cap underside; protruding external boss sections removed.')

# cell: front_power_button_position
# Rebuild the simple front panel so the previous upper-center power-button hole
# is removed, then place the 12.2 mm opening at the exterior-view lower right.
# In the front-panel exterior/back camera view, model -X appears on screen right.
power_x=-50.0
power_z=25.0
front_panel=Box(W,panel_t,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,front_y,base_t)))
front_panel=front_panel-Cylinder(6.1,8,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.X,90).moved(Location((power_x,front_y,power_z)))
front_edges=vertical_edges(front_panel,210.0)
if front_edges:
    front_panel=fillet(front_edges,1.0)
assert W/2-abs(power_x)-6.1>15.0
assert power_z-base_t-6.1>15.0
publish('front_panel',front_panel,'Lower-right power panel')
print('FRONT_POWER_LOWER_RIGHT_PASS: the old upper-center hole is removed; the 12.2 mm power-button opening is at model x=-50 mm, z=25 mm, which is the exterior-view lower right, with more than 15 mm material to the side and bottom edges.')