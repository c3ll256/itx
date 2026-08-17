# Motherboard tray, PSU cradle and feet; all screw interfaces come from the shared kit helper.
tray=Box(2.4,174,195,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((tray_x,0,15)))
tray=tray+Box(3.0,168,12,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((tray_x,0,3)))
tray=tray+Box(3.0,168,12,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((tray_x,0,210)))
tray=tray-Box(8,56,44,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((tray_x,-48,82)))
tray=tray-Box(8,56,44,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((tray_x,48,82)))
motherboard_tray=tray

# Standard Mini-ITX 157.48 mm square pattern. The board is a 1.6 mm through-stack;
# the printed M3 engagement bosses are generated directly by the kit.
board_y0,board_z0=-85.0,25.0
mitx_offsets=(6.35,163.83)
board_mount_axes=[(board_y0+dy,board_z0+dz) for dy in mitx_offsets for dz in mitx_offsets]
board_thickness=1.6
board_mouth_x=-6.2
board_proxy=Box(board_thickness,170,170,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((board_mouth_x+board_thickness/2,0,110)))
board_joints=[]
for i,(y,z) in enumerate(board_mount_axes):
    joint=require_kit_joint(
        f"motherboard:{i}", size="M3", at=Location((board_mouth_x,y,z),(0,-90,0)),
        through=[(board_proxy,board_thickness)], head="socket_cap", strategy="auto", boss="auto"
    )
    motherboard_tray=motherboard_tray+joint.bosses-joint.engage_cuts
    board_joints.append(joint)

# Two printed riser-tab joints. The tray is the through side; kit bosses are consumed by the GPU cell.
riser_tab_y=(-14.0,50.0)
riser_joints=[]
for i,y in enumerate(riser_tab_y):
    joint=require_kit_joint(
        f"riser-tab:{i}", size="M3", at=Location((tray_x-1.2,y,91),(0,-90,0)),
        through=[(motherboard_tray,2.4)], head="socket_cap", strategy="auto", boss="auto"
    )
    motherboard_tray=motherboard_tray-joint.through_cuts[0]
    riser_joints.append(joint)

# 160 x 80 x 40 mm PSU cradle. The four joints were solved in the shell cell so
# screw length includes the base; their kit bosses and engagement cuts terminate here.
psu_x=31.0
shelf=Box(46,166,3,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((psu_x,0,4)))
left_wall=Box(3,166,84,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((9.5,0,4)))
right_wall=Box(3,166,84,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((52.5,0,4)))
front_stop=Box(46,3,84,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((psu_x,81.5,4)))
psu_tabs=None
for x,y in psu_mount_axes:
    tab=Box(14,14,3,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,3)))
    psu_tabs=tab if psu_tabs is None else psu_tabs+tab
one_u_cradle=shelf+left_wall+right_wall+front_stop+psu_tabs
for joint in psu_joints:
    one_u_cradle=one_u_cradle+joint.bosses-joint.engage_cuts

assert len(board_mount_axes)==4 and len(board_joints)==4 and len(riser_joints)==2
assert abs(board_mount_axes[2][0]-board_mount_axes[0][0]-157.48)<0.001
assert abs(board_mount_axes[1][1]-board_mount_axes[0][1]-157.48)<0.001
assert free_connection_ids==set()
assert intended_connection_ids==kit_connection_ids and len(kit_connection_ids)==34
publish('motherboard_tray',motherboard_tray,'Kit-fastened ITX tray')
publish('psu_cradle',one_u_cradle,'Kit-fastened PSU cradle')
publish('case_feet',case_feet,'Four kit-fastened feet')
print(f"BOARD_PSU_KIT_PASS: {len(kit_connection_ids)} cumulative kit joints; Mini-ITX, riser-tab, PSU and foot screw holes are kit-owned.")