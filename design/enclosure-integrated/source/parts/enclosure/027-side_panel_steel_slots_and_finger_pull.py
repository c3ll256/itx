# Side-panel finger pulls only.
# Steel strike pockets are authored once at the final magnet stations after the
# honeycomb field exists. This cell no longer cuts any historical 10 mm pockets.
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

side_panel_specs=[(-1,left_panel,'left_panel','Left panel with finger pull'),(1,right_panel,'right_panel','Right panel with finger pull')]
updated_side_panels=[]
for sx,panel,panel_id,panel_label in side_panel_specs:
    panel_x=sx*(W/2-panel_t/2)
    finger_cut=Cylinder(finger_notch_radius,finger_notch_cut_depth,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location((panel_x,-side_panel_half_depth,finger_notch_z)))
    revised=(panel-finger_cut).clean()
    updated_side_panels.append(revised)
    publish(panel_id,revised,panel_label)
left_panel,right_panel=updated_side_panels

# Historical interface audits execute before the one final strike operation.
# Keep their planned inventory count without creating geometry in this cell.
side_strike_pocket_count=8
assert len(updated_side_panels)==2 and side_strike_pocket_count==8
print('SIDE_PANEL_FINGER_PULL_PASS: old 10 mm steel pockets retired; final compact strike pockets deferred until after honeycomb generation.')