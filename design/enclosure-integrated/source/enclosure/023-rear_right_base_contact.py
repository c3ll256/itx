# Width-linked rear base foot on the side opposite the motherboard support.
rear_leg_y_min=param('right_rear_leg_y_min',-125.4)
rear_leg_y_max=param('right_rear_leg_y_max',-111.4)
rear_leg_z_min_opposite=param('right_rear_leg_z_min',3.0)
rear_leg_z_max_opposite=param('right_rear_leg_z_max',82.0)
rear_sfx_clearance_opposite=param('right_rear_sfx_clearance',0.3)
if board_side<0:
    opposite_leg_x_min=sfx_psu_width/2+rear_sfx_clearance_opposite
    opposite_leg_x_max=outer_x
    opposite_column_index=2
    opposite_column_id='column_fr'
    opposite_column_label='Base-contact right rear'
else:
    opposite_leg_x_min=-outer_x
    opposite_leg_x_max=-(sfx_psu_width/2+rear_sfx_clearance_opposite)
    opposite_column_index=0
    opposite_column_id='column_fl'
    opposite_column_label='Base-contact left rear'
opposite_leg=Box(opposite_leg_x_max-opposite_leg_x_min,rear_leg_y_max-rear_leg_y_min,rear_leg_z_max_opposite-rear_leg_z_min_opposite,align=(Align.MIN,Align.MIN,Align.MIN)).moved(Location((opposite_leg_x_min,rear_leg_y_min,rear_leg_z_min_opposite)))
opposite_rear_integrated=(columns[opposite_column_index]+opposite_leg).clean()
opposite_rear_integrated=(opposite_rear_integrated-base_joints[opposite_column_index].engage_cuts).clean()
# Compatibility alias retained for the final cap/magnet cell.
right_rear_integrated=opposite_rear_integrated
hole_x=post_xy[opposite_column_index][0]
left_margin=hole_x-opposite_leg_x_min
right_margin=opposite_leg_x_max-hole_x
assert opposite_rear_integrated.solids().__len__()==1
assert opposite_rear_integrated.bounding_box().min.Z<=base_t+0.001
assert left_margin>=3.0 and right_margin>=3.0
assert (opposite_leg_x_min>=sfx_psu_width/2) if board_side<0 else (opposite_leg_x_max<=-sfx_psu_width/2)
publish(opposite_column_id,opposite_rear_integrated,opposite_column_label)
print(f'OPPOSITE_REAR_WIDTH_PASS: side={"right" if board_side<0 else "left"}; W={W:.1f}; foot x={opposite_leg_x_min:.1f}..{opposite_leg_x_max:.1f}; screw axis x={hole_x:.1f}; margins {left_margin:.1f}/{right_margin:.1f} mm.')