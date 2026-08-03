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

