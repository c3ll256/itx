# Replace all four provisional PSU-cradle/base holes with one datum-driven rectangular pattern.
old_psu_axes=[(14.0,-70.0),(14.0,70.0),(48.0,-70.0),(48.0,70.0)]
psu_mount_axes=[(16.0,-72.0),(16.0,72.0),(46.0,-72.0),(46.0,72.0)]
# Close old base holes only within the 3 mm base plate, then cut the new pattern.
for x,y in old_psu_axes:
    main_frame=main_frame+Cylinder(1.85,base_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,0)))
for x,y in psu_mount_axes:
    main_frame=main_frame-Cylinder(m3_clear,base_t+2.0,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,-1.0)))
# Rebuild the cradle from clean shelf/wall/stop solids so no old tab hole survives.
new_psu_tabs=None
for x,y in psu_mount_axes:
    tab=Box(14,14,3,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,3)))
    tab=tab-Cylinder(m3_clear,8,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,1)))
    new_psu_tabs=tab if new_psu_tabs is None else new_psu_tabs+tab
one_u_cradle=shelf+left_wall+right_wall+front_stop+new_psu_tabs
assert len(psu_mount_axes)==4 and set(psu_mount_axes).isdisjoint(set(old_psu_axes))
assert min(x-9.5 for x,y in psu_mount_axes)>=6.5 and min(52.5-x for x,y in psu_mount_axes)>=6.5
publish('base_and_frame',main_frame,'Frame with rebuilt four-hole PSU base pattern')
publish('one_u_psu_cradle',one_u_cradle,'PSU cradle with new 30x144 mm four-hole pattern')
print('PSU mounting holes replaced: old x=14/48,y=+-70 closed; new x=16/46,y=+-72 cut through both cradle tabs and base.')