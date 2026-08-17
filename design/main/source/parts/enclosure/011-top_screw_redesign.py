# Completely replace the top-cap hole pattern while keeping purchased inserts/screws out of print geometry.
old_top_xy=[(-post_x,-post_y),(-post_x,post_y),(post_x,-post_y),(post_x,post_y)]
top_screw_xy=[(-58.0,-78.0),(-58.0,78.0),(58.0,-78.0),(58.0,78.0)]
for x,y in old_top_xy:
    main_frame=main_frame+Cylinder(2.35,11.0,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,H-cap_t-11.0)))
    top_cap=top_cap+Cylinder(3.25,5.0,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,H-5.0)))
for x,y in top_screw_xy:
    column=Cylinder(6.5,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,base_t)))
    main_frame=main_frame+column
    main_frame=main_frame-Cylinder(2.25,8.0,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,H-cap_t-8.0)))
    top_cap=top_cap-Cylinder(1.70,7.0,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,H-6.0)))
    top_cap=top_cap-Cylinder(3.20,1.6,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,H-1.6)))
assert set(top_screw_xy).isdisjoint(set(old_top_xy))
publish('base_and_frame',main_frame,'Frame with four reinforced inboard top-screw columns')
publish('top_cap',top_cap,'Top cap with redesigned four-hole pattern')
print('Top screw geometry remains X=+-58/Y=+-78; purchased inserts and M3x8 screws are BOM items, not exported solids.')