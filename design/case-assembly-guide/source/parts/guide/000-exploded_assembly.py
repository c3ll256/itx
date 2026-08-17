# Visual-only exploded assembly guide; these are the real enclosure part classes, not hardware placeholders.
# This document is excluded from manufacturing export. The manufacturing model remains document 'main'.
W,D,H=146.0,190.0,225.0
connections={
 'shell_panels':'free_M3',
 'top_cap':'free_M3',
 'tray':'free_tongue_slot',
 'psu_cradle':'free_rear_slide_four_M3',
 'gpu_support':'free_M3_tabs_clamps'
}
assert len(connections)==5 and all(v.startswith('free_') for v in connections.values())
# STEP 1 — base and four posts stay at the origin.
base=Box(W,D,3,align=(Align.CENTER,Align.CENTER,Align.MIN))
posts=None
for x in (-65.6,65.6):
  for y in (-89.6,89.6):
    p=Box(10,10,H-6,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,3)))
    posts=p if posts is None else posts+p
base_frame=base+posts
# STEP 2 — rear-slide 1U PSU cradle shown 85 mm behind the case.
psu_x=31.0
psu_y=-85.0
psu_shelf=Box(46,166,3,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((psu_x,psu_y,4)))
psu_left=Box(3,166,84,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((9.5,psu_y,4)))
psu_right=Box(3,166,84,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((52.5,psu_y,4)))
psu_stop=Box(46,3,84,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((psu_x,psu_y+81.5,4)))
psu_cradle=psu_shelf+psu_left+psu_right+psu_stop
# STEP 3 — central tray shown 70 mm above its final slot.
tray_z=70.0
tray=Box(2.4,174,195,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((4,0,15+tray_z)))
tray=tray+Box(3,168,12,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((4,0,3+tray_z)))
tray=tray+Box(3,168,12,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((4,0,210+tray_z)))
# Four actual mounting bosses retained on the exploded tray.
standoffs=None
for y in (-80,80):
  for z in (25,195):
    s=Cylinder(3.8,7,align=(Align.CENTER,Align.CENTER,Align.MIN)).rotate(Axis.Y,-90).moved(Location((2.8,y,z+tray_z)))
    standoffs=s if standoffs is None else standoffs+s
tray=tray+standoffs
# STEP 4 — GPU support module shown 65 mm to the right of its installed position.
gpu_dx=65.0
riser=Box(50,78,4,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31+gpu_dx,18,92)))
rail1=Box(5,178,5,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((13+gpu_dx,-1,92)))
rail2=Box(5,178,5,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((49+gpu_dx,-1,92)))
rear_frame=Box(54,6,126,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31+gpu_dx,-89,92)))
rear_frame=rear_frame-Box(42,10,114,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31+gpu_dx,-91,98)))
front_frame=Box(54,6,126,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31+gpu_dx,87,92)))
front_frame=front_frame-Box(42,10,114,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31+gpu_dx,85,98)))
gpu_support=riser+rail1+rail2+rear_frame+front_frame
# STEP 5 — shell panels moved along their removal normals.
top=Box(W,D,3,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,0,H+75)))
left_panel=Box(2.4,D-12,H-12,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((-W/2-55,0,6)))
right_panel=Box(2.4,D-12,H-12,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((W/2+55,0,6)))
front_panel=Box(W-12,2.4,H-12,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,D/2+65,6)))
rear_panel=Box(W-12,2.4,H-12,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,-D/2-65,6)))
# Large directional arrows: PSU forward, tray downward, GPU left, panels inward.
def arrow_z(x,y,z0,length):
  return Cylinder(2.5,length,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,z0)))+Cone(7,0,14,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,z0-14)))
def arrow_y(x,y,z,length,positive=True):
  shaft=Box(4,length,4,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,z)))
  head=Cone(7,0,14,align=(Align.CENTER,Align.CENTER,Align.MIN)).rotate(Axis.X,-90 if positive else 90).moved(Location((x,y+(length/2 if positive else -length/2),z-5)))
  return shaft+head
def arrow_x(x,y,z,length,positive=True):
  shaft=Box(length,4,4,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,z)))
  head=Cone(7,0,14,align=(Align.CENTER,Align.CENTER,Align.MIN)).rotate(Axis.Y,90 if positive else -90).moved(Location((x+(length/2 if positive else -length/2),y,z-5)))
  return shaft+head
tray_arrow=arrow_z(-10,0,235,38)
psu_arrow=arrow_y(31,-112,48,42,positive=True)
gpu_arrow=arrow_x(76,0,150,36,positive=False)
publish('step1_base_frame',base_frame,'1 — Place printable base/frame')
publish('step2_psu_cradle',psu_cradle,'2 — Slide 1U PSU cradle forward from rear and screw from below')
publish('step3_motherboard_tray',tray,'3 — Lower central tray tongues into base slot')
publish('step4_gpu_support',gpu_support,'4 — Bolt riser/GPU support to tray and frame')
publish('step5_top_cap',top,'5 — Lower top cap last')
publish('step5_left_panel',left_panel,'5 — Fit left panel inward')
publish('step5_right_panel',right_panel,'5 — Fit right panel inward')
publish('step5_front_panel',front_panel,'5 — Fit front panel inward')
publish('step5_rear_panel',rear_panel,'5 — Fit rear panel inward')
publish('tray_down_arrow',tray_arrow,'Lower tray vertically into locating slots')
publish('psu_forward_arrow',psu_arrow,'Slide PSU cradle from rear toward front')
publish('gpu_left_arrow',gpu_arrow,'Move GPU support toward central tray')
print('Guide sequence: base -> rear-slide PSU cradle -> top-load tray -> side-load GPU support -> exterior panels -> top cap.')