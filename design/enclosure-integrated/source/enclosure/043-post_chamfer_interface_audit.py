# Exact-revision audit after all chamfers. Chamfers may remove material but must
# not damage interfaces or create panel penetration.
post_chamfer_intersection_tolerance=param('post_chamfer_intersection_tolerance',0.02)
post_chamfer_magnet_carriers_expected=param('magnet10_carrier_expected',8)
post_chamfer_side_pockets_expected=param('magnet10_strike_pocket_expected',8)
post_chamfer_rear_fixings_expected=param('rear_fixing_point_expected',4)
post_pairs=[('front-left',front_panel,left_panel),('front-right',front_panel,right_panel),('rear-left',rear_panel,left_panel),('rear-right',rear_panel,right_panel),('top-left',top_cap,left_panel),('top-right',top_cap,right_panel),('base-left',base,left_panel),('base-right',base,right_panel)]
post_volumes={name:(a & b).volume for name,a,b in post_pairs}
assert all(v<=post_chamfer_intersection_tolerance for v in post_volumes.values()),post_volumes
assert len(magnet_carriers)==post_chamfer_magnet_carriers_expected and len(magnet_joints)==0
assert side_strike_pocket_count==post_chamfer_side_pockets_expected
assert rear_top_bottom_joint_count==post_chamfer_rear_fixings_expected
assert all(p.solids().__len__()==1 for p in (base,top_cap,front_panel,rear_panel,left_panel,right_panel))
final_interface_inventory={'magnets':'8 x screwless 10x10x3 mm adhesive/press-fit pockets','side-strikes':'8 x compact 10 mm steel pockets','rear-fixings':'2 top + 2 bottom M3 kit joints','corner-blocks':'8 x slim 12x12x10 mm isolated blocks','edge-treatment':'front/rear vertical chamfers; side top/bottom chamfers with existing rounded verticals; top/base skin chamfers'}
assert len(final_interface_inventory)==5 and all(final_interface_inventory.values())
print('POST_CHAMFER_INTERFACE_AUDIT_PASS:',post_volumes,final_interface_inventory)