# Direct AXP120-X67 side intake centred on the project's cooler reference.
# The circular cut replaces the masked portion of the generic perforation field;
# an integral cross grille restores panel continuity without broad masked sectors.
intake_case_width=param('case_width',W)
intake_case_depth=param('case_depth',D)
intake_case_height=param('case_height',H)
intake_panel_thickness=param('panel_thickness',panel_t)
axp_intake_center_y=param('axp_intake_center_y',-42.0)
axp_intake_center_z=param('axp_intake_center_z',169.0)
axp_intake_reference_fan_plane_x=param('axp_intake_reference_fan_plane_x',72.8)
axp_intake_fan_diameter=param('axp_intake_fan_diameter',120.0)
axp_intake_radial_clearance=param('axp_intake_radial_clearance',6.0)
axp_intake_ring_width=param('axp_intake_ring_width',2.8)
axp_intake_spoke_width=param('axp_intake_spoke_width',3.2)
axp_intake_hub_diameter=param('axp_intake_hub_diameter',36.0)
axp_intake_fuse_overlap=param('axp_intake_fuse_overlap',0.5)
axp_intake_cut_overtravel=param('axp_intake_cut_overtravel',1.0)
axp_intake_radius=axp_intake_fan_diameter/2+axp_intake_radial_clearance
axp_intake_panel_x=W/2-panel_t/2
axp_intake_axis_depth=panel_t+2*axp_intake_cut_overtravel
axp_intake_outer_radius=axp_intake_radius+axp_intake_fuse_overlap
axp_intake_clear_radius=axp_intake_radius-axp_intake_ring_width
axp_intake_cut=Cylinder(axp_intake_radius,axp_intake_axis_depth,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location((axp_intake_panel_x,axp_intake_center_y,axp_intake_center_z)))
right_panel=(right_panel-axp_intake_cut).clean()
axp_intake_outer=Cylinder(axp_intake_outer_radius,panel_t,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location((axp_intake_panel_x,axp_intake_center_y,axp_intake_center_z)))
axp_intake_inner=Cylinder(axp_intake_clear_radius,panel_t+0.4,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location((axp_intake_panel_x,axp_intake_center_y,axp_intake_center_z)))
axp_intake_ring=(axp_intake_outer-axp_intake_inner).clean()
axp_intake_hub=Cylinder(axp_intake_hub_diameter/2,panel_t,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location((axp_intake_panel_x,axp_intake_center_y,axp_intake_center_z)))
axp_intake_y_spoke=Box(panel_t,2*axp_intake_outer_radius,axp_intake_spoke_width,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((axp_intake_panel_x,axp_intake_center_y,axp_intake_center_z)))
axp_intake_z_spoke=Box(panel_t,axp_intake_spoke_width,2*axp_intake_outer_radius,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((axp_intake_panel_x,axp_intake_center_y,axp_intake_center_z)))
axp_intake_clip=Cylinder(axp_intake_outer_radius,panel_t+0.4,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location((axp_intake_panel_x,axp_intake_center_y,axp_intake_center_z)))
axp_intake_grille=(axp_intake_ring+axp_intake_hub+((axp_intake_y_spoke+axp_intake_z_spoke)&axp_intake_clip)).clean()
right_panel=(right_panel+axp_intake_grille).clean()
axp_intake_top_margin=(H-cap_t)-(axp_intake_center_z+axp_intake_outer_radius)
axp_intake_rear_margin=(axp_intake_center_y-axp_intake_outer_radius)-(-D/2+panel_t)
axp_intake_clear_diameter=2*axp_intake_clear_radius
axp_fan_plane_to_panel_gap=(W/2-panel_t)-axp_intake_reference_fan_plane_x
assert right_panel.solids().__len__()==1
assert axp_intake_clear_diameter>=axp_intake_fan_diameter+2.0
assert axp_intake_top_margin>=12.0
assert axp_intake_rear_margin>=15.0
assert axp_fan_plane_to_panel_gap>=1.0
publish('right_panel',right_panel,'Right panel AXP intake')
print(f'AXP120_DIRECT_INTAKE_PASS: clear diameter={axp_intake_clear_diameter:.1f} mm, fan={axp_intake_fan_diameter:.1f} mm, top margin={axp_intake_top_margin:.1f} mm, rear margin={axp_intake_rear_margin:.1f} mm, fan-plane gap={axp_fan_plane_to_panel_gap:.1f} mm.')