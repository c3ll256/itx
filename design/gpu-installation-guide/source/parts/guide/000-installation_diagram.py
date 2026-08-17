# Visual-only GPU installation guide; excluded from manufacturing export.
riser_shelf=Box(50,78,4,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,20,0)))
for hx in (-13,13):
  for hy in (0,40):
    riser_shelf=riser_shelf-Cylinder(1.7,6,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((hx,hy,-1)))
rail_a=Box(5,184,4,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((-18,0,0)))
rail_b=Box(5,184,4,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((18,0,0)))
riser_base=riser_shelf+rail_a+rail_b
rear_frame=Box(54,5,126,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,-92,0)))
rear_frame=rear_frame-Box(42,9,114,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,-94,6)))
for hx in (-15,15):
  rear_frame=rear_frame-Cylinder(1.7,10,align=(Align.CENTER,Align.CENTER,Align.MIN)).rotate(Axis.X,90).moved(Location((hx,-87,123)))
front_frame=Box(54,5,126,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,90,0)))
front_frame=front_frame-Box(42,9,114,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,88,6)))
# Two physical clamps separated in the exploded view so both are unmistakable.
clamps=None
for y in (-55,55):
  c=Box(5,18,16,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((92,y,12)))
  c=c-Cylinder(1.7,8,align=(Align.CENTER,Align.CENTER,Align.MIN)).rotate(Axis.Y,90).moved(Location((88,y,20)))
  clamps=c if clamps is None else clamps+c
# Guide-only recognizable GPU, offset right/up.
gpu_x,gpu_z=55.0,18.0
gpu_shroud=Box(40,180,115,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((gpu_x,0,gpu_z)))
fan_details=None
for fy in (-45,45):
  cutter=Cylinder(27,5,align=(Align.CENTER,Align.CENTER,Align.MIN)).rotate(Axis.Y,90).moved(Location((gpu_x+17.5,fy,gpu_z+58)))
  gpu_shroud=gpu_shroud-cutter
  ring_outer=Cylinder(25,3,align=(Align.CENTER,Align.CENTER,Align.MIN)).rotate(Axis.Y,90).moved(Location((gpu_x+19,fy,gpu_z+58)))
  ring_inner=Cylinder(20,4,align=(Align.CENTER,Align.CENTER,Align.MIN)).rotate(Axis.Y,90).moved(Location((gpu_x+18.5,fy,gpu_z+58)))
  ring=ring_outer-ring_inner
  hub=Cylinder(6,3.5,align=(Align.CENTER,Align.CENTER,Align.MIN)).rotate(Axis.Y,90).moved(Location((gpu_x+19,fy,gpu_z+58)))
  d=ring+hub
  fan_details=d if fan_details is None else fan_details+d
# Split rear flange into two slot plates with a central gap.
gpu_io_flange=Box(44,5,115,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((gpu_x,-92.5,gpu_z)))
gpu_io_flange=gpu_io_flange-Box(2.5,9,105,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((gpu_x,-94,gpu_z+5)))
pcie_edge=Box(3,64,10,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((gpu_x-18,16,gpu_z-10)))
slide_shaft=Box(38,4,4,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((65,0,145)))
slide_head=Cone(7,0,14,align=(Align.CENTER,Align.CENTER,Align.MIN)).rotate(Axis.Y,-90).moved(Location((39,0,140)))
down_shaft=Cylinder(2.5,30,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,106,24)))
down_head=Cone(0,7,14,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,106,10)))
publish('step1_riser_shelf',riser_base,'1 — Screw the PCIe riser to this shelf')
publish('step2_rear_io_frame',rear_frame,'2 — Slide GPU rear bracket through this frame and use two screws')
publish('step3_front_support',front_frame,'3 — Far end passes through this support frame')
publish('step4_side_clamps',clamps,'4 — Refit both right-side clamps')
publish('guide_gpu_body',gpu_shroud,'Guide-only dual-fan GPU illustration; not manufacturing geometry')
publish('guide_gpu_fans',fan_details,'Guide-only two fan rings')
publish('guide_gpu_io',gpu_io_flange,'Guide-only split dual-slot flange')
publish('guide_gpu_pcie',pcie_edge,'Guide-only PCIe edge connector')
publish('slide_left_arrow',slide_shaft+slide_head,'Slide card left through both frames')
publish('press_down_arrow',down_shaft+down_head,'Press PCIe edge down into riser')
print('Side panel is already removed in this guide; both fans, both slot plates, and both clamps are unobstructed.')