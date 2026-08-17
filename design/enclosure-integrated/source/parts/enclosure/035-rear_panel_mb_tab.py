# Rear-lower Mini-ITX support fused to the rear panel, with the same integrated standoff used by all four board points.
from screwjoint import make_screw_joint_v1 as _rear_tab_make_screw_joint_v1
rear_panel_width=param('case_width',W); rear_panel_height=param('case_height',H); rear_panel_thickness=param('panel_thickness',panel_t)
rear_mb_tab_width_x=param('rear_mb_tab_width_x',8.0); rear_mb_tab_height_z=param('rear_mb_tab_height_z',12.0); rear_mb_tab_end_margin_y=param('rear_mb_tab_end_margin_y',5.0); rear_mb_tab_panel_overlap=param('rear_mb_tab_panel_overlap',0.35)
rear_mb_board_proxy_thickness=param('mitx_board_proxy_thickness',board_proxy_thickness); rear_mb_board_proxy_size=param('mitx_board_proxy_size',board_proxy_size)
rear_mb_standoff_height=param('mitx_integrated_standoff_height',6.35); rear_mb_standoff_diameter=param('mitx_integrated_standoff_diameter',8.0); rear_mb_standoff_fuse_overlap=param('mitx_standoff_fuse_overlap',0.6); rear_mb_screw_engagement=param('mitx_integrated_standoff_engagement',6.0)
rear_mb_mount_y=lower_mount_ys[0]; rear_mb_mount_z=lower_mount_z
rear_panel_inner_y=-D/2+rear_panel_thickness; rear_mb_tab_y0=rear_panel_inner_y-rear_mb_tab_panel_overlap; rear_mb_tab_y1=rear_mb_mount_y+rear_mb_tab_end_margin_y; rear_mb_tab_depth_y=rear_mb_tab_y1-rear_mb_tab_y0
assert rear_mb_tab_width_x>=rear_mb_screw_engagement+1.5 and rear_mb_tab_depth_y>rear_mb_tab_end_margin_y
arm_align=Align.MAX if board_side>0 else Align.MIN; proxy_align=Align.MIN if board_side>0 else Align.MAX
rear_tab=Box(rear_mb_tab_width_x,rear_mb_tab_depth_y,rear_mb_tab_height_z,align=(arm_align,Align.MIN,Align.CENTER)).moved(Location((board_face_x,rear_mb_tab_y0,rear_mb_mount_z)))
rear_mb_post_start_x=board_face_x-board_side*rear_mb_standoff_fuse_overlap
rear_mb_post=Cylinder(rear_mb_standoff_diameter/2,rear_mb_standoff_height+rear_mb_standoff_fuse_overlap,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((rear_mb_post_start_x,rear_mb_mount_y,rear_mb_mount_z),(0,90.0*board_side,0)))
rear_panel=(rear_panel+rear_tab+rear_mb_post).clean()
rear_mb_board_plane_x=board_face_x+board_side*rear_mb_standoff_height; rear_mb_screw_outer_x=rear_mb_board_plane_x+board_side*rear_mb_board_proxy_thickness
board_proxy=Box(rear_mb_board_proxy_thickness,rear_mb_board_proxy_size,rear_mb_board_proxy_size,align=(proxy_align,Align.CENTER,Align.CENTER)).moved(Location((rear_mb_board_plane_x,rear_mb_mount_y,rear_mb_mount_z)))
rear_mb_joint=_rear_tab_make_screw_joint_v1(size='M3',at=Location((rear_mb_screw_outer_x,rear_mb_mount_y,rear_mb_mount_z),(0,board_screw_rotation_y,0)),through=[(board_proxy,rear_mb_board_proxy_thickness)],engage_depth=rear_mb_screw_engagement,into=rear_panel,head='socket_cap',strategy='auto',material=material,boss='none',label='rear-panel-integrated-lower-motherboard')
rear_panel=(rear_panel-rear_mb_joint.engage_cuts).clean()
rear_panel_mount_inventory={'rear-lower-motherboard':'printed-screw-joint-v1 with 6.35 mm integrated standoff'}
assert rear_panel.solids().__len__()==1 and len(rear_panel_mount_inventory)==1 and rear_mb_joint.screw_length_mm==8
publish('rear_panel',rear_panel,'Rear panel ITX standoff')
print(f'REAR_MB_STANDOFF_PASS: rear-lower board axis at y={rear_mb_mount_y:.2f}, z={rear_mb_mount_z:.2f} now uses a {rear_mb_standoff_height:.2f} mm integrated standoff and M3x8 screw.')