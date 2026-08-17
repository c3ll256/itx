# Front-panel exterior view is from +Y; positive X appears on the viewer's left.
power_x=param('power_button_x',50.0)
power_z=param('power_button_z',25.0)
power_hole_radius=param('power_button_radius',6.1)
power_cut_depth=param('power_button_cut_depth',8.0)
front_fillet_radius=param('front_panel_fillet_radius',1.0)
front_fillet_min_edge=param('front_panel_fillet_min_edge',210.0)
power_min_edge_clearance=param('power_button_min_edge_clearance',15.0)
front_panel=Box(W,panel_t,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,front_y,base_t)))
front_panel=front_panel-Cylinder(power_hole_radius,power_cut_depth,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.X,90).moved(Location((power_x,front_y,power_z)))
front_edges=vertical_edges(front_panel,front_fillet_min_edge)
if front_edges: front_panel=fillet(front_edges,front_fillet_radius)
assert abs(power_x)>0
assert W/2-abs(power_x)-power_hole_radius>power_min_edge_clearance
assert power_z-base_t-power_hole_radius>power_min_edge_clearance
publish('front_panel',front_panel,'Lower-left power panel')
print(f'FRONT_POWER_POSITION: exterior-front center x={power_x:.1f} mm, z={power_z:.1f} mm; positive X is exterior-view left.')