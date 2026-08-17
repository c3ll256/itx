# Final rear-panel hole restoration after all interface and side-swap cells have replayed.
# Lower left/right fixing blocks and panel patches are each 1 mm narrower; upper points remain unchanged.
rear_case_pad_width_x=param('rear_case_pad_width_x',10.2)
rear_case_lower_pad_width_x=param('rear_case_lower_pad_width_x',9.2)
rear_case_pad_depth_y=param('rear_case_pad_depth_y',10.8)
rear_case_pad_height_z=param('rear_case_pad_height_z',10.2)
rear_case_pad_y_offset=param('rear_case_pad_y_offset',5.4)
rear_case_panel_patch_width=param('rear_case_panel_patch_width',8.0)
rear_case_lower_panel_patch_width_x=param('rear_case_lower_panel_patch_width_x',7.0)
rear_case_panel_patch_height=param('rear_case_panel_patch_height',8.0)
rear_case_screw_z_low=param('rear_case_screw_z_low',30.0)
rear_case_screw_z_high=param('rear_case_screw_z_high',247.0)
sfx_final_hole_diameter=param('sfx_final_hole_diameter',4.2)
sfx_final_hole_patch_diameter=param('sfx_final_hole_patch_diameter',8.0)
sfx_final_hole_cut_depth=param('sfx_final_hole_cut_depth',8.0)
rear_case_targets=[current_top_targets[0],current_top_targets[2]]
rear_case_x=(-post_x,post_x)
rear_case_z=(rear_case_screw_z_low,rear_case_screw_z_high)
final_rear_case_joints=[]
for side_i,(x,target) in enumerate(zip(rear_case_x,rear_case_targets)):
    repaired_target=target
    for z in rear_case_z:
        is_lower = z == rear_case_screw_z_low
        pad_width_x = rear_case_lower_pad_width_x if is_lower else rear_case_pad_width_x
        panel_patch_width_x = rear_case_lower_panel_patch_width_x if is_lower else rear_case_panel_patch_width
        target_restore=Box(pad_width_x,rear_case_pad_depth_y,rear_case_pad_height_z,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((x,-outer_y+rear_case_pad_y_offset,z)))
        repaired_target=(repaired_target+target_restore).clean()
        panel_patch=Box(panel_patch_width_x,panel_t,rear_case_panel_patch_height,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((x,rear_y,z)))
        rear_panel=(rear_panel+panel_patch).clean()
        j=make_screw_joint_v1(size='M3',at=Location((x,-D/2,z),(90,0,0)),through=[(rear_panel,panel_t)],into=repaired_target,head='socket_cap',strategy='auto',material=material,boss='auto',label=f'rear-panel:final:{side_i}:{z}')
        rear_panel=rear_panel-j.through_cuts[0]
        repaired_target=(repaired_target+j.bosses-j.engage_cuts).clean()
        final_rear_case_joints.append(j)
    rear_case_targets[side_i]=repaired_target
for x,z in sfx_mount_points:
    sfx_patch=Cylinder(sfx_final_hole_patch_diameter/2,panel_t,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.X,90).moved(Location((x,rear_y,z)))
    rear_panel=(rear_panel+sfx_patch).clean()
    sfx_cut=Cylinder(sfx_final_hole_diameter/2,sfx_final_hole_cut_depth,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.X,90).moved(Location((x,-D/2,z)))
    rear_panel=rear_panel-sfx_cut
current_top_targets[0]=rear_case_targets[0]
current_top_targets[2]=rear_case_targets[1]
assert len(final_rear_case_joints)==4 and len(sfx_mount_points)==4
assert abs(rear_case_pad_width_x-rear_case_lower_pad_width_x-1.0)<0.001
assert abs(rear_case_panel_patch_width-rear_case_lower_panel_patch_width_x-1.0)<0.001
publish('rear_panel',rear_panel,'Narrow lower rear fixing points')
publish('column_fl',current_top_targets[0],'Left rear screw support')
publish('column_fr',current_top_targets[2],'Right rear screw support')
print(f'REAR_PANEL_FINAL_HOLES_PASS: lower fixing blocks narrowed to {rear_case_lower_pad_width_x:.1f} mm and lower panel patches to {rear_case_lower_panel_patch_width_x:.1f} mm; upper points and all M3 kit joints retained.')