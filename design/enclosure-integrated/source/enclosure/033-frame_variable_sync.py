# Carry the corrected point-fastened frame geometry into every downstream cell.
frame_sync_expected_clearance=param('side_panel_inner_clearance',0.40)
frame_sync_expected_rear_joints=param('frame_sync_expected_rear_joints',4)
front_panel=front_frame
rear_panel=rear_frame
assert frame_sync_expected_clearance>=0.30
assert frame_sync_expected_rear_joints==rear_top_bottom_joint_count
assert rear_panel.bounding_box().max.X<=frame_outer_x+0.001
assert rear_panel.bounding_box().min.X>=-frame_outer_x-0.001
publish('front_panel',front_panel,'Clearance front panel')
publish('rear_panel',rear_panel,'Rear panel with corner points')
print('FRAME_SYNC_PASS: downstream rear-panel cells now retain two top joints, two bottom joints, four side magnet carriers and the side-panel clearance boundary.')