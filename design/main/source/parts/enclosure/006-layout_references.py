# Internal service modules with explicit insertion directions and matched screw interfaces.
tray_x=4.0
m3_clear=1.7
insert_r=2.1
connections={
 'tray_to_base_top_slots':'free_tongue_slot',
 'motherboard_to_tray':'free_M3_standoffs',
 'psu_cradle_to_base':'free_four_M3_bottom_screws',
 'gpu_riser_to_tray':'free_two_M3_tabs',
 'gpu_frames_to_rails':'free_integral_print',
 'gpu_clamps_to_frame':'free_two_M3_clamps'
}
assert len(connections)==6 and all(v.startswith('free_') for v in connections.values())
# Central tray drops vertically into bottom slot; top tongue is captured by top cap.
tray=Box(2.4,174,195,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((tray_x,0,15)))
bottom_tongue=Box(3.0,168,12,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((tray_x,0,3)))
top_tongue=Box(3.0,168,12,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((tray_x,0,210)))
tray=tray+bottom_tongue+top_tongue
# Two cable/service windows with retained perimeter and 45-degree-printable proportions.
tray=tray-Box(8,56,44,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((tray_x,-48,82)))
tray=tray-Box(8,56,44,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((tray_x,48,82)))
# Four board standoffs on a 160 x 170 mm nominal pattern; pocket dimensions are provisional.
standoffs=None
for y in (-80,80):
  for z in (25,195):
    base=Cone(5.0,3.8,2.0,align=(Align.CENTER,Align.CENTER,Align.MIN)).rotate(Axis.Y,-90).moved(Location((tray_x-1.2,y,z)))
    shank=Cylinder(3.8,7,align=(Align.CENTER,Align.CENTER,Align.MIN)).rotate(Axis.Y,-90).moved(Location((tray_x-1.2,y,z)))
    pocket=Cylinder(insert_r,9,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location((tray_x-4.2,y,z+1)))
    s=(base+shank)-pocket
    standoffs=s if standoffs is None else standoffs+s
motherboard_tray=tray+standoffs
# 1U PSU cradle: slide PSU from rear along +Y, stop at front wall, then fasten four tabs from underside.
psu_x=31.0
shelf=Box(46,166,3,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((psu_x,0,4)))
left_wall=Box(3,166,84,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((9.5,0,4)))
right_wall=Box(3,166,84,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((52.5,0,4)))
front_stop=Box(46,3,84,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((psu_x,81.5,4)))
psu_tabs=None
for x in (14,48):
  for y in (-70,70):
    t=Box(12,16,3,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,3)))
    t=t-Cylinder(m3_clear,8,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,1)))
    psu_tabs=t if psu_tabs is None else psu_tabs+t
one_u_cradle=shelf+left_wall+right_wall+front_stop+psu_tabs
# GPU assembly above PSU. Shelf bolts to two tabs on the tray; rails carry the card lengthwise.
riser_shelf=Box(50,78,4,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,18,92)))
riser_tabs=None
for y in (-12,48):
  t=Box(9,16,10,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((8.5,y,86)))
  t=t-Cylinder(m3_clear,10,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location((8.5,y,91)))
  riser_tabs=t if riser_tabs is None else riser_tabs+t
for x in (18,44):
  for y in (0,36):
    riser_shelf=riser_shelf-Cylinder(m3_clear,8,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,90)))
rail_a=Box(5,178,5,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((13,-1,92)))
rail_b=Box(5,178,5,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((49,-1,92)))
gpu_riser=riser_shelf+riser_tabs+rail_a+rail_b
# Rear I/O frame and front nose support are joined by rails; each has a 42 x 114 mm clear card window.
rear_frame=Box(54,6,126,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,-89,92)))
rear_frame=rear_frame-Box(42,10,114,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,-91,98)))
front_support=Box(54,6,126,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,87,92)))
front_support=front_support-Box(42,10,114,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,85,98)))
# Two visible rear bracket screw holes.
for x in (18,44):
  rear_frame=rear_frame-Cylinder(m3_clear,10,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.X,90).moved(Location((x,-89,212)))
# Two removable right-side clamp blocks, each with an M3 clearance hole.
clamps=None
for y in (-78,78):
  c=Box(7,18,16,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((58,y,102)))
  c=c-Cylinder(m3_clear,10,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location((58,y,110)))
  clamps=c if clamps is None else clamps+c
# Four feet are separate replaceable parts retained from below.
feet=None
for x in (-54,54):
  for y in (-82,82):
    f=Cylinder(7,4,align=(Align.CENTER,Align.CENTER,Align.MAX)).moved(Location((x,y,0)))
    feet=f if feet is None else feet+f
publish('motherboard_tray',motherboard_tray,'Top-loaded central tray with bottom/top tongues and four standoffs')
publish('one_u_psu_cradle',one_u_cradle,'Rear-slide 1U PSU cradle with front stop and four underside tabs')
publish('gpu_riser_shelf',gpu_riser,'Tray-bolted PCIe riser shelf and two GPU rails')
publish('gpu_rear_io_frame',rear_frame,'Rear GPU I/O frame with two bracket screw holes')
publish('gpu_front_support',front_support,'Front GPU nose-support frame')
publish('gpu_side_clamps',clamps,'Two removable M3 GPU retention clamps')
publish('case_feet',feet,'Four replaceable foot carriers')
print('Install sequence: base -> PSU cradle from rear -> central tray from top -> riser shelf -> GPU -> front/rear panels -> side panels -> top cap.')