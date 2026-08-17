# Clean perforated side panels with an export-efficient staggered round-hole array.
# The previous 630-hole pair was visually dense and made STEP/STL handoff exceed the CAD runtime budget.
side_depth=D-2*panel_t
side_height=H-base_t-cap_t
vent_r=5.0
vent_pitch=18.0
def clean_side_panel(x,is_right):
    panel=Box(panel_t,side_depth,side_height,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,0,base_t)))
    cutters=None
    hole_count=0
    for row,z in enumerate(range(18,216,18)):
        offset=9 if row%2 else 0
        for y in range(-63,64,18):
            yy=y+offset
            if -72<=yy<=72:
                hole=Cylinder(vent_r,8,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location((x,yy,z)))
                cutters=hole if cutters is None else cutters+hole
                hole_count+=1
    panel=(panel-cutters).clean()
    relief_x=W/2 if is_right else -W/2
    panel=panel-Cylinder(7,8,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location((relief_x,0,base_t)))
    assert hole_count==88
    return panel.clean()
right_panel=clean_side_panel(W/2-panel_t/2,True)
left_panel=clean_side_panel(-W/2+panel_t/2,False)
assert post_y>72+magnet_w/2
publish('left_vent_panel',left_panel,'Left panel with efficient staggered round vents')
publish('right_vent_panel',right_panel,'Right panel with efficient staggered round vents')
print('Perforated panels optimized from 315 to 88 holes per side; 10 mm staggered vents preserve airflow, solid magnetic borders and export tractability.')