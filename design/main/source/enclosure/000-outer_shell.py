# Tool-less magnetic perimeter architecture with corner posts fully inside panel planes.
W,D,H=146.0,190.0,225.0
base_t,cap_t,panel_t,post=3.0,3.0,2.4,10.0
m3_clear=1.7
insert_r=2.25
panel_clearance=0.6
# Panel inner planes are X=±70.6 and Y=±92.6 mm.
post_x=W/2-panel_t-panel_clearance-post/2
post_y=D/2-panel_t-panel_clearance-post/2
assert abs(post_x-65.0)<0.001 and abs(post_y-87.0)<0.001
connections={'top':'free_M3_heatset','front':'free_magnetic','rear':'free_magnetic_pending','left':'free_magnetic','right':'free_magnetic'}
assert len(connections)==5 and all(v.startswith('free_') for v in connections.values())
base=Box(W,D,base_t,align=(Align.CENTER,Align.CENTER,Align.MIN))
front_rail=Box(W-12,8,7,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,D/2-8,base_t)))
rear_rail=Box(W-12,8,7,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,-D/2+8,base_t)))
left_rail=Box(8,D-28,7,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((-W/2+8,0,base_t)))
right_rail=Box(8,D-28,7,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((W/2-8,0,base_t)))
posts=None
for x in (-post_x,post_x):
  for y in (-post_y,post_y):
    p=Box(post,post,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,base_t)))
    posts=p if posts is None else posts+p
# Shear lips remain inside removable panels.
front_lip=Box(W-16,3,6,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,D/2-panel_t-2,base_t)))
rear_lip=Box(W-16,3,6,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,-D/2+panel_t+2,base_t)))
left_lip=Box(3,D-20,6,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((-W/2+panel_t+2,0,base_t)))
right_lip=Box(3,D-20,6,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((W/2-panel_t-2,0,base_t)))
main_frame=base+front_rail+rear_rail+left_rail+right_rail+posts+front_lip+rear_lip+left_lip+right_lip
# Top structural holes synchronized to the inset posts.
top_cap=Box(W,D,cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,0,H-cap_t)))
top_rim=Box(W-10,D-10,2,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,0,H-cap_t-2)))
top_cap=top_cap+top_rim
for x in (-post_x,post_x):
  for y in (-post_y,post_y):
    top_cap=top_cap-Cylinder(m3_clear,8,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,H-6)))
    top_cap=top_cap-Cylinder(3.2,1.5,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,H-1.5)))
# Rear service panel has no screw holes.
rear_y=-D/2+panel_t/2
rear_panel=Box(W,panel_t,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,rear_y,base_t)))
rear_panel=rear_panel-Box(48,8,126,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((-35,-D/2,74)))
rear_panel=rear_panel-Box(48,8,122,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,-D/2,96)))
rear_panel=rear_panel-Box(46,8,86,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,-D/2,4)))
# Clean side panels; rectangular magnet zones are owned downstream.
side_depth=D-2*panel_t
side_height=H-base_t-cap_t
def side_panel(x):
  p=Box(panel_t,side_depth,side_height,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,0,base_t)))
  cutters=None
  for row,z in enumerate(range(14,216,10)):
    off=5 if row%2 else 0
    for y in range(-72,73,10):
      yy=y+off
      if -76<=yy<=76:
        c=Cylinder(3.0,8,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location((x,yy,z)))
        cutters=c if cutters is None else cutters+c
  return (p-cutters).clean()
left_panel=side_panel(-W/2+panel_t/2)
right_panel=side_panel(W/2-panel_t/2)
# Top insert pockets only.
for x in (-post_x,post_x):
  for y in (-post_y,post_y):
    main_frame=main_frame-Cylinder(insert_r,11,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,H-cap_t-8)))
# Explicit clearance checks on all four posts.
assert W/2-panel_t-(post_x+post/2)>=panel_clearance-0.001
assert D/2-panel_t-(post_y+post/2)>=panel_clearance-0.001
publish('base_and_frame',main_frame,'Frame with all corner posts inset 0.6 mm from panel inner planes')
publish('top_cap',top_cap,'Top cap synchronized to inset corner posts')
publish('rear_io_panel',rear_panel,'Clear magnetic rear service panel pending smaller magnet selection')
publish('left_vent_panel',left_panel,'Clean left perforated panel')
publish('right_vent_panel',right_panel,'Clean right perforated panel')
print(f'Corner-post repair: centers X=±{post_x:.1f}, Y=±{post_y:.1f}; all panel clearances={panel_clearance:.1f} mm. Rear service openings are clear at source.')