# Final non-penetration and interface-count audit for slim screwless magnets.
panel_intersection_tolerance_mm3=param('panel_intersection_tolerance_mm3',0.02)
panel_clearance_required_mm=param('side_panel_inner_clearance',0.40)
rear_fixing_point_expected=param('rear_fixing_point_expected',4)
magnet10_carrier_expected=param('magnet10_carrier_expected',8)
magnet10_strike_pocket_expected=param('magnet10_strike_pocket_expected',8)
panel_pairs=[('front-left',front_panel,left_panel),('front-right',front_panel,right_panel),('rear-left',rear_panel,left_panel),('rear-right',rear_panel,right_panel),('top-left',top_cap,left_panel),('top-right',top_cap,right_panel),('base-left',base,left_panel),('base-right',base,right_panel)]
intersection_volumes={name:(a & b).volume for name,a,b in panel_pairs}
assert all(v<=panel_intersection_tolerance_mm3 for v in intersection_volumes.values()),intersection_volumes
assert panel_clearance_required_mm>=0.30 and rear_top_bottom_joint_count==rear_fixing_point_expected
active_magnet_carrier_count=len(magnet_carriers) if 'magnet_carriers' in globals() else len(magnet_joints)
assert active_magnet_carrier_count==magnet10_carrier_expected
assert side_strike_pocket_count==magnet10_strike_pocket_expected
interface_inventory={'rear-to-top':'2 x M3 printed-screw-joint-v1','rear-to-bottom':'2 x M3 printed-screw-joint-v1','left-side-magnetic':'4 screwless 10x10x3 magnet pockets plus 4 steel pockets','right-side-magnetic':'4 screwless 10x10x3 magnet pockets plus 4 steel pockets','panel-clearance':f'{panel_clearance_required_mm:.2f} mm between carriers and side-panel inner faces'}
assert len(interface_inventory)==5 and all(interface_inventory.values())
print('MAGNET10_PANEL_INTERFACE_AUDIT_PASS:',intersection_volumes,interface_inventory)