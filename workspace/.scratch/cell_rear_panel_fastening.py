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

