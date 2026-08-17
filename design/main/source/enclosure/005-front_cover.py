# Tool-less solid front panel; purchased switch hardware stays in the BOM, not the printed-part export.
front_y=D/2-panel_t/2
panel=Box(W,panel_t,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,front_y,base_t)))
button_x,button_z=0.0,211.0
panel=panel-Cylinder(6.1,8,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.X,90).moved(Location((button_x,front_y,button_z)))
panel=panel-Cylinder(7,8,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.X,90).moved(Location((0,D/2,base_t)))
publish('front_vent_panel',panel,'Solid front panel with 12.2 mm switch opening')
print('Front panel retains the power-switch opening; purchased switch body is BOM hardware and is intentionally excluded from CAD manufacturing geometry.')