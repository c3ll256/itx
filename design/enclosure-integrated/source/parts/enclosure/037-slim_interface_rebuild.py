# Post-process rebuild: remove legacy thick carriers/blocks, then add slim interfaces.
from screwjoint import make_screw_joint_v1 as _slim_make_screw_joint_v1
slim2_corner_width_x=param('slim2_corner_width_x',12.0); slim2_corner_depth_y=param('slim2_corner_depth_y',12.0); slim2_corner_height_z=param('slim2_corner_height_z',10.0)
slim2_corner_panel_overlap=param('slim2_corner_panel_overlap',0.50); slim2_corner_engagement=param('slim2_corner_engagement',4.2)
slim2_corner_screw_x_inset=param('slim_corner_screw_x_inset',9.6); slim2_corner_screw_y_inset=param('slim_corner_screw_y_inset',10.6)
magnet10_rebuild_width_y=param('magnet10_width_y',10.0); magnet10_rebuild_height_z=param('magnet10_height_z',10.0); magnet10_rebuild_depth_x=param('magnet10_depth_x',3.0)
magnet10_rebuild_clearance=param('magnet10_pocket_clearance',0.20); magnet10_rebuild_back_wall=param('magnet10_back_wall',1.20)
magnet10_rebuild_carrier_width_y=param('magnet10_rebuild_carrier_width_y',13.0); magnet10_rebuild_carrier_height_z=param('magnet10_rebuild_carrier_height_z',13.0)
magnet10_rebuild_station_inset_y=param('magnet10_station_inset_y',8.0); magnet10_rebuild_expected=param('magnet10_carrier_expected',8)
legacy_corner_relief_width_x=param('legacy_corner_relief_width_x',18.5); legacy_corner_relief_depth_y=param('legacy_corner_relief_depth_y',16.0); legacy_corner_relief_height_z=param('legacy_corner_relief_height_z',18.0)
legacy_magnet_relief_width_x=param('legacy_magnet_relief_width_x',18.5); legacy_magnet_relief_depth_y=param('legacy_magnet_relief_depth_y',16.0); legacy_magnet_relief_height_z=param('legacy_magnet_relief_height_z',24.0)
frame_outer_x=W/2-panel_t-param('side_panel_inner_clearance',0.40)
front_rebuilt=front_panel; rear_rebuilt=rear_panel
# Remove interior portions of all legacy corner pads and magnet carriers while preserving panel skins.
for sy in (-1,1):
    rebuilt=front_rebuilt if sy>0 else rear_rebuilt
    relief_y=sy*(D/2-panel_t-legacy_corner_relief_depth_y/2-0.2)
    for sx in (-1,1):
        relief_x=sx*(frame_outer_x-legacy_corner_relief_width_x/2)
        for zc in (base_t+legacy_corner_relief_height_z/2,H-(cap_t+cap_inner_t)-legacy_corner_relief_height_z/2):
            relief=Box(legacy_corner_relief_width_x,legacy_corner_relief_depth_y,legacy_corner_relief_height_z,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((relief_x,relief_y,zc)))
            rebuilt=(rebuilt-relief).clean()
        for zc in (side_station_z_low,side_station_z_high):
            relief=Box(legacy_magnet_relief_width_x,legacy_magnet_relief_depth_y,legacy_magnet_relief_height_z,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((relief_x,relief_y,zc)))
            rebuilt=(rebuilt-relief).clean()
    if sy>0: front_rebuilt=rebuilt
    else: rear_rebuilt=rebuilt
# Add slim 12x12x10 corner blocks with 0.5 mm panel overlap.
slim2_corner_blocks=[]
for sy in (-1,1):
    rebuilt=front_rebuilt if sy>0 else rear_rebuilt
    block_y=sy*(D/2-panel_t-slim2_corner_depth_y/2+slim2_corner_panel_overlap)
    for sx in (-1,1):
        block_x=sx*(frame_outer_x-slim2_corner_width_x/2)
        lower=Box(slim2_corner_width_x,slim2_corner_depth_y,slim2_corner_height_z,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((block_x,block_y,base_t)))
        upper=Box(slim2_corner_width_x,slim2_corner_depth_y,slim2_corner_height_z,align=(Align.CENTER,Align.CENTER,Align.MAX)).moved(Location((block_x,block_y,H-cap_t-cap_inner_t)))
        rebuilt=(rebuilt+lower+upper).clean(); slim2_corner_blocks.extend((lower,upper))
    if sy>0: front_rebuilt=rebuilt
    else: rear_rebuilt=rebuilt
# Add thin 4.4 mm magnet carriers with 13 mm Y/Z envelope and open 10.2x10.2x3.2 pockets.
magnet10_rebuild_pocket_depth=magnet10_rebuild_depth_x+magnet10_rebuild_clearance
magnet10_rebuild_pocket_width=magnet10_rebuild_width_y+magnet10_rebuild_clearance
magnet10_rebuild_pocket_height=magnet10_rebuild_height_z+magnet10_rebuild_clearance
magnet10_rebuild_carrier_depth=magnet10_rebuild_pocket_depth+magnet10_rebuild_back_wall
magnet10_rebuild_station_y=D/2-magnet10_rebuild_station_inset_y
magnet_carriers=[]; magnet_joints=[]
for sy in (-1,1):
    rebuilt=front_rebuilt if sy>0 else rear_rebuilt
    carrier_y=sy*magnet10_rebuild_station_y
    for sx in (-1,1):
        carrier_x=sx*(frame_outer_x-magnet10_rebuild_carrier_depth/2)
        pocket_x=sx*(frame_outer_x-magnet10_rebuild_pocket_depth/2)
        for zc in (side_station_z_low,side_station_z_high):
            carrier=Box(magnet10_rebuild_carrier_depth,magnet10_rebuild_carrier_width_y,magnet10_rebuild_carrier_height_z,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((carrier_x,carrier_y,zc)))
            pocket=Box(magnet10_rebuild_pocket_depth,magnet10_rebuild_pocket_width,magnet10_rebuild_pocket_height,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((pocket_x,carrier_y,zc)))
            rebuilt=(rebuilt+carrier).clean(); rebuilt=(rebuilt-pocket).clean(); magnet_carriers.append(carrier)
    if sy>0: front_rebuilt=rebuilt
    else: rear_rebuilt=rebuilt
# Re-cut kit-owned M3 engagement holes and true conical countersinks in both exterior plates.
slim2_corner_joints=[]; rear_top_bottom_joint_count=0; screw_x=W/2-slim2_corner_screw_x_inset; screw_y=D/2-slim2_corner_screw_y_inset
for sy in (-1,1):
    rebuilt=front_rebuilt if sy>0 else rear_rebuilt
    for sx in (-1,1):
        x=sx*screw_x; y=sy*screw_y
        bj=_slim_make_screw_joint_v1(size='M3',at=Location((x,y,-foot_height),(180,0,0)),through=[(base,base_t+foot_height)],engage_depth=slim2_corner_engagement,into=rebuilt,head='countersunk',strategy='auto',material=material,boss='none',label=f'slim2-bottom:{sy}:{sx}')
        base=(base-bj.through_cuts[0]).clean(); rebuilt=(rebuilt-bj.engage_cuts).clean()
        tj=_slim_make_screw_joint_v1(size='M3',at=Location((x,y,H)),through=[(top_cap,cap_t+cap_inner_t)],engage_depth=slim2_corner_engagement,into=rebuilt,head='countersunk',strategy='auto',material=material,boss='none',label=f'slim2-top:{sy}:{sx}')
        top_cap=(top_cap-tj.through_cuts[0]).clean(); rebuilt=(rebuilt-tj.engage_cuts).clean(); slim2_corner_joints.extend((bj,tj))
        if sy<0: rear_top_bottom_joint_count+=2
    if sy>0: front_rebuilt=rebuilt
    else: rear_rebuilt=rebuilt
front_panel=front_rebuilt; rear_panel=rear_rebuilt
bottom_corner_screw_lengths={j.screw_length_mm for j in slim2_corner_joints[0::2]}
top_corner_screw_lengths={j.screw_length_mm for j in slim2_corner_joints[1::2]}
assert len(slim2_corner_blocks)==8 and len(slim2_corner_joints)==8 and rear_top_bottom_joint_count==4
assert len(magnet_carriers)==magnet10_rebuild_expected and len(magnet_joints)==0
assert bottom_corner_screw_lengths=={12.0} and top_corner_screw_lengths=={10.0}
assert front_panel.solids().__len__()==1 and rear_panel.solids().__len__()==1
publish('base',base,'Conical countersunk bottom'); publish('top_cap',top_cap,'Conical countersunk top'); publish('front_panel',front_panel,'Slim 10 mm magnetic front'); publish('rear_panel',rear_panel,'Slim 10 mm magnetic rear')
print(f'SLIM_INTERFACE_REBUILD_PASS: top uses M3x{next(iter(top_corner_screw_lengths)):.0f} and bottom uses M3x{next(iter(bottom_corner_screw_lengths)):.0f} conical countersunk screws; corner blocks are {slim2_corner_width_x:.0f}x{slim2_corner_depth_y:.0f}x{slim2_corner_height_z:.0f} mm.')