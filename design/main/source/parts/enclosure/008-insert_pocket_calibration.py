# Structural M3 pockets synchronized to inset corner-post coordinates.
insert_hole_r=2.25
for x in (-post_x,post_x):
  for y in (-post_y,post_y):
    main_frame=main_frame-Cylinder(insert_hole_r,11,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,H-cap_t-11)))
for y in (-80,80):
  for z in (25,195):
    motherboard_tray=motherboard_tray-Cylinder(insert_hole_r,10,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location((0.0,y,z+1)))
publish('base_and_frame',main_frame,'Inset-post frame with synchronized top insert pockets')
publish('motherboard_tray',motherboard_tray,'Tray with four calibrated motherboard insert pockets')
print(f'Top insert pockets moved to inset post axes X=±{post_x:.1f}, Y=±{post_y:.1f}; motherboard pockets unchanged.')