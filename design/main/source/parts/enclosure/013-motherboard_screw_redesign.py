# Standard 170 mm Mini-ITX four-hole grid; purchased inserts remain BOM hardware only.
board_y0=-85.0
board_z0=25.0
mitx_offsets=(6.35,163.83)
board_mount_axes=[(board_y0+dy,board_z0+dz) for dy in mitx_offsets for dz in mitx_offsets]
board_insert_r=2.25
new_standoffs=None
for y,z in board_mount_axes:
    foot=Cone(5.0,3.8,2.0,align=(Align.CENTER,Align.CENTER,Align.MIN)).rotate(Axis.Y,-90).moved(Location((tray_x-1.2,y,z)))
    shank=Cylinder(3.8,7.0,align=(Align.CENTER,Align.CENTER,Align.MIN)).rotate(Axis.Y,-90).moved(Location((tray_x-1.2,y,z)))
    pocket=Cylinder(board_insert_r,9.0,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location((tray_x-4.2,y,z)))
    standoff=(foot+shank)-pocket
    new_standoffs=standoff if new_standoffs is None else new_standoffs+standoff
motherboard_tray=tray+new_standoffs
assert len(board_mount_axes)==4
assert abs(board_mount_axes[2][0]-board_mount_axes[0][0]-157.48)<0.001
assert abs(board_mount_axes[1][1]-board_mount_axes[0][1]-157.48)<0.001
publish('motherboard_tray',motherboard_tray,'Tray with standard Mini-ITX four-hole grid')
print('Mini-ITX pockets remain on the 157.48 mm standard grid; four purchased M3 inserts are defined in hardware/bom.json.')