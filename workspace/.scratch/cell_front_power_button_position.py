# cell: front_power_button_position
# Rebuild the simple front panel so the previous upper-center power-button hole
# is removed, then place the 12.2 mm opening at the exterior-view lower right.
# In the front-panel exterior/back camera view, model -X appears on screen right.
power_x=-50.0
power_z=25.0
front_panel=Box(W,panel_t,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,front_y,base_t)))
front_panel=front_panel-Cylinder(6.1,8,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.X,90).moved(Location((power_x,front_y,power_z)))
front_edges=vertical_edges(front_panel,210.0)
if front_edges:
    front_panel=fillet(front_edges,1.0)
assert W/2-abs(power_x)-6.1>15.0
assert power_z-base_t-6.1>15.0
publish('front_panel',front_panel,'Lower-right power panel')
print('FRONT_POWER_LOWER_RIGHT_PASS: the old upper-center hole is removed; the 12.2 mm power-button opening is at model x=-50 mm, z=25 mm, which is the exterior-view lower right, with more than 15 mm material to the side and bottom edges.')
