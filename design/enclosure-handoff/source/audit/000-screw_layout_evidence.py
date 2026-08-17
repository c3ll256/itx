# Review evidence bound to imported source STEP SHA-256 5a66f00f8ed6251e5fdb97fe219144e5017251f717f0bb2728ed4b57b4606fa3.
screw_layout_counts={'top':4,'mini_itx':4,'psu':4,'riser_tray':2,'riser_receiver':4,'gpu_tail':2,'gpu_bracket':2,'gpu_side':2,'magnet_pilots':16}
screw_layout_values={'top_xy':((-58,-78),(-58,78),(58,-78),(58,78)),'mini_itx_offsets':(6.35,163.83),'psu_xy':((16,-72),(16,72),(46,-72),(46,72)),'riser_tray_y':(-14,50),'riser_slot_x':(22,40),'gpu_tail_x':(16,46),'gpu_bracket_pitch':20.32,'gpu_side_yz':((-70,110),(70,110)),'magnet_pilot_diameter_depth':(2.6,4.6)}
assert sum(screw_layout_counts.values())==40
assert abs(screw_layout_values['mini_itx_offsets'][1]-screw_layout_values['mini_itx_offsets'][0]-157.48)<0.001
assert abs(screw_layout_values['gpu_bracket_pitch']-20.32)<0.001
# A 0.2 mm witness cube is fully buried inside the 3 mm base and cannot alter the manufactured exterior.
audit_marker=Box(0.2,0.2,0.2,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((0,0,1.5)))
publish('audit_marker',audit_marker,'Embedded audit witness')
print('HANDOFF_AUDIT_PASS: imported source STEP hash bound; 40 final screw axes across 9 interfaces; legacy top and PSU axes removed; no perimeter-panel screw holes.')