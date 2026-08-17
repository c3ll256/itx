# Restore eight 15x10x4 mm magnets with centered M3 retention and matching strikes.
from screwjoint import make_screw_joint_v1 as _mag15_make_screw_joint_v1
panel_magnet15_width_y=param('panel_magnet15_width_y',15.0)
panel_magnet15_height_z=param('panel_magnet15_height_z',10.0)
panel_magnet15_depth_x=param('panel_magnet15_depth_x',4.0)
panel_magnet15_pocket_clearance=param('panel_magnet15_pocket_clearance',0.20)
panel_magnet15_back_wall_x=param('panel_magnet15_back_wall_x',3.0)
panel_magnet15_carrier_width_y=param('panel_magnet15_carrier_width_y',19.0)
panel_magnet15_carrier_height_z=param('panel_magnet15_carrier_height_z',14.0)
panel_magnet15_center_screw_engagement=param('panel_magnet15_center_screw_engagement',3.2)
panel_magnet15_expected=param('panel_magnet15_expected',8)
panel_magnet15_station_inset_y=param('panel_magnet15_station_inset_y',10.0)
panel_magnet15_steel_thickness_x=param('panel_magnet15_steel_thickness_x',1.0)
panel_magnet15_steel_clearance=param('panel_magnet15_steel_clearance',0.30)
panel_magnet15_steel_depth_clearance=param('panel_magnet15_steel_depth_clearance',0.15)
panel_magnet15_side_patch_width_y=param('panel_magnet15_side_patch_width_y',16.0)
panel_magnet15_side_patch_height_z=param('panel_magnet15_side_patch_height_z',14.0)
panel_magnet15_pocket_depth=panel_magnet15_depth_x+panel_magnet15_pocket_clearance
panel_magnet15_pocket_width=panel_magnet15_width_y+panel_magnet15_pocket_clearance
panel_magnet15_pocket_height=panel_magnet15_height_z+panel_magnet15_pocket_clearance
panel_magnet15_carrier_depth=panel_magnet15_pocket_depth+panel_magnet15_back_wall_x
panel_magnet15_station_y=D/2-panel_magnet15_station_inset_y
panel_magnet15_joints=[]
for sy in (-1,1):
    panel=front_panel if sy>0 else rear_panel
    station_y=sy*panel_magnet15_station_y
    for sx in (-1,1):
        carrier_x=sx*(frame_outer_x-panel_magnet15_carrier_depth/2)
        pocket_x=sx*(frame_outer_x-panel_magnet15_pocket_depth/2)
        magnet_center_x=sx*(frame_outer_x-panel_magnet15_depth_x/2)
        for zz in (side_station_z_low,side_station_z_high):
            carrier=Box(panel_magnet15_carrier_depth,panel_magnet15_carrier_width_y,panel_magnet15_carrier_height_z,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((carrier_x,station_y,zz)))
            pocket=Box(panel_magnet15_pocket_depth,panel_magnet15_pocket_width,panel_magnet15_pocket_height,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((pocket_x,station_y,zz)))
            panel=(panel+carrier).clean(); panel=(panel-pocket).clean()
            magnet_proxy=Box(panel_magnet15_depth_x,panel_magnet15_width_y,panel_magnet15_height_z,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((magnet_center_x,station_y,zz)))
            joint=_mag15_make_screw_joint_v1(size='M3',at=Location((sx*frame_outer_x,station_y,zz),(0,90.0*sx,0)),through=[(magnet_proxy,panel_magnet15_depth_x)],engage_depth=panel_magnet15_center_screw_engagement,into=panel,head='countersunk',strategy='auto',material=material,label=f'panel-magnet15:{sy}:{sx}:{zz:.1f}')
            panel=(panel+joint.bosses-joint.engage_cuts).clean(); panel_magnet15_joints.append(joint)
    if sy>0: front_panel=panel
    else: rear_panel=panel
assert len(panel_magnet15_joints)==int(panel_magnet15_expected)
panel_magnet15_slot_width=panel_magnet15_width_y+panel_magnet15_steel_clearance
panel_magnet15_slot_height=panel_magnet15_height_z+panel_magnet15_steel_clearance
panel_magnet15_slot_depth=panel_magnet15_steel_thickness_x+panel_magnet15_steel_depth_clearance
panel_magnet15_side_count=0
updated_side_panels=[]
for sx,panel in ((-1,left_panel),(1,right_panel)):
    revised=panel
    panel_x=sx*(W/2-panel_t/2)
    inner_face_x=sx*(W/2-panel_t)
    pocket_center_x=inner_face_x+sx*panel_magnet15_slot_depth/2
    for sy in (-1,1):
        station_y=sy*panel_magnet15_station_y
        for zz in (side_station_z_low,side_station_z_high):
            patch=Box(panel_t,panel_magnet15_side_patch_width_y,panel_magnet15_side_patch_height_z,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((panel_x,station_y,zz)))
            strike=Box(panel_magnet15_slot_depth,panel_magnet15_slot_width,panel_magnet15_slot_height,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((pocket_center_x,station_y,zz)))
            revised=(revised+patch).clean(); revised=(revised-strike).clean(); panel_magnet15_side_count+=1
    updated_side_panels.append(revised)
left_panel,right_panel=updated_side_panels
assert panel_magnet15_side_count==int(panel_magnet15_expected)
assert front_panel.solids().__len__()==1 and rear_panel.solids().__len__()==1
assert left_panel.solids().__len__()==1 and right_panel.solids().__len__()==1
publish('front_panel',front_panel,'Front 15 mm centered-screw magnets')
publish('rear_panel',rear_panel,'Rear 15 mm centered-screw magnets')
publish('left_panel',left_panel,'Left 15 mm strike pockets')
publish('right_panel',right_panel,'Right 15 mm strike pockets')
print('MAGNET15_FINAL_PASS: eight 15x10x4 mm centered-screw pockets and matching side-panel steel pockets.')