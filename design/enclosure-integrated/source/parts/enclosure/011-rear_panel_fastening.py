# Four M3 kit joints fix the rear panel to the rear-column outer spines.
# The two lower restore blocks are 1 mm narrower than before; upper blocks remain unchanged.
rear_column_indices=(0,2)
rear_screw_z=(end_station_z_low,end_station_z_high)
rear_restore_width_x=param('rear_restore_width_x',10.2)
rear_lower_restore_width_x=param('rear_lower_restore_width_x',9.2)
rear_restore_depth_y=param('rear_restore_depth_y',10.8)
rear_restore_height_z=param('rear_restore_height_z',10.2)
rear_restore_y_offset=param('rear_restore_y_offset',5.4)
rear_screw_joints=[]
for idx in rear_column_indices:
    x,y=post_xy[idx]
    c=columns[idx]
    for z in rear_screw_z:
        restore_width_x = rear_lower_restore_width_x if z == end_station_z_low else rear_restore_width_x
        restore=Box(restore_width_x,rear_restore_depth_y,rear_restore_height_z,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((x,-outer_y+rear_restore_y_offset,z)))
        c=c+restore
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
assert rear_screw_z[0]>base_t and rear_screw_z[1]<H-cap_t
assert abs(rear_restore_width_x-rear_lower_restore_width_x-1.0)<0.001
publish('rear_panel',rear_panel,'Screw-fixed SFX rear')
publish('column_fl',columns[0],'Rear left screw spine')
publish('column_fr',columns[2],'Rear right screw spine')
print(f'REAR_PANEL_SCREW_PASS: lower restore blocks narrowed to {rear_lower_restore_width_x:.1f} mm; upper blocks remain {rear_restore_width_x:.1f} mm; four M3 kit joints retained at z={rear_screw_z}.')