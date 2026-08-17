# Four compact steel-strike pockets per removable side panel, aligned to the
# 10x10x3 mm adhesive/press-fit magnets in the front and rear panel carriers.
magnet10_steel_height_z=param('magnet10_steel_height_z',10.0)
magnet10_steel_width_y=param('magnet10_steel_width_y',10.0)
magnet10_steel_thickness_x=param('magnet10_steel_thickness_x',1.0)
magnet10_slot_height_clearance=param('magnet10_slot_height_clearance',0.30)
magnet10_slot_width_clearance=param('magnet10_slot_width_clearance',0.30)
magnet10_slot_thickness_clearance=param('magnet10_slot_thickness_clearance',0.15)
magnet10_station_inset_y=param('magnet10_station_inset_y',8.0)
magnet10_station_z_low=param('side_station_z_low',58.0)
magnet10_station_z_high=param('side_station_z_high',167.0)
finger_notch_radius=param('side_panel_finger_notch_radius',9.0)
finger_notch_z=param('side_panel_finger_notch_z',130.0)
finger_notch_cut_depth=param('side_panel_finger_notch_cut_depth',6.0)
side_panel_half_depth=(D-2*panel_t)/2
magnet10_slot_height=magnet10_steel_height_z+magnet10_slot_height_clearance
magnet10_slot_width=magnet10_steel_width_y+magnet10_slot_width_clearance
magnet10_slot_thickness=magnet10_steel_thickness_x+magnet10_slot_thickness_clearance
magnet10_station_y=D/2-magnet10_station_inset_y
assert magnet10_slot_thickness<panel_t and magnet10_slot_height<12.0
assert magnet10_station_y<side_panel_half_depth
side_panel_specs=[(-1,left_panel,'left_panel','Left 10 mm magnetic panel'),(1,right_panel,'right_panel','Right 10 mm magnetic panel')]
updated_side_panels=[]
side_strike_pocket_count=0
for sx,panel,panel_id,panel_label in side_panel_specs:
    inner_face_x=sx*(W/2-panel_t)
    pocket_center_x=inner_face_x+sx*magnet10_slot_thickness/2
    revised=panel
    for sy in (-1,1):
        station_y=sy*magnet10_station_y
        for z in (magnet10_station_z_low,magnet10_station_z_high):
            captive_pocket=Box(magnet10_slot_thickness,magnet10_slot_width,magnet10_slot_height,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((pocket_center_x,station_y,z)))
            revised=(revised-captive_pocket).clean(); side_strike_pocket_count+=1
    panel_x=sx*(W/2-panel_t/2)
    finger_cut=Cylinder(finger_notch_radius,finger_notch_cut_depth,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location((panel_x,-side_panel_half_depth,finger_notch_z)))
    revised=(revised-finger_cut).clean(); updated_side_panels.append(revised); publish(panel_id,revised,panel_label)
left_panel,right_panel=updated_side_panels
assert len(updated_side_panels)==2 and side_strike_pocket_count==8
print(f'MAGNET10_SIDE_POINTS_PASS: each side panel has four compact {magnet10_slot_height:.1f} x {magnet10_slot_width:.1f} x {magnet10_slot_thickness:.2f} mm inner-face steel pockets aligned to 10x10x3 mm magnets.')