# Final one-piece base: four feet are fused directly to the bottom panel.
integrated_foot_diameter=param('integrated_foot_diameter',16.0)
integrated_foot_height=param('integrated_foot_height',4.0)
integrated_foot_overlap=param('integrated_foot_overlap',0.4)
integrated_base_width=param('case_width',152.0)
integrated_base_depth=param('case_depth',256.0)
integrated_base_thickness=param('base_thickness',3.0)
assert len(post_xy)==4 and len(base_joints)==4
integrated_base=base; integrated_foot_pads=[]
for (x,y),joint in zip(post_xy,base_joints):
    pad=Cylinder(integrated_foot_diameter/2,integrated_foot_height+integrated_foot_overlap,align=(Align.CENTER,Align.CENTER,Align.MAX)).moved(Location((x,y,integrated_foot_overlap)))
    integrated_base=(integrated_base+pad).clean()
    integrated_base=(integrated_base-joint.through_cuts[0]-joint.through_cuts[1]).clean()
    integrated_foot_pads.append(pad)
base=integrated_base.clean()
assert base.solids().__len__()==1
assert abs(base.bounding_box().size.X-integrated_base_width)<0.001
assert abs(base.bounding_box().size.Y-integrated_base_depth)<0.001
assert abs(base.bounding_box().min.Z+integrated_foot_height)<0.001
assert abs(base.bounding_box().max.Z-integrated_base_thickness)<0.001
publish('base',base,'Integrated-foot base')
print('INTEGRATED_FEET_ONLY: all four feet are fused into the base; retired individual foot component IDs are removed.')