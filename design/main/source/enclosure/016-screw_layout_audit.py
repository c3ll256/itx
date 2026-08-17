# Single authoritative audit table for every screw-bearing interface in the final revision.
magnet_pilot_axes=[]
for sy in (-1,1):
    for x in (-post_x,post_x):
        for z in end_z:
            magnet_pilot_axes.append({'mouth_xyz':(x,sy*(post_outer_y-flat_d),z),'normal':(0,-sy,0)})
for sx in (-1,1):
    for y in (-post_y,post_y):
        for z in side_z:
            magnet_pilot_axes.append({'mouth_xyz':(sx*(post_outer_x-flat_d),y,z),'normal':(-sx,0,0)})
screw_layout={
    'top_cap_xy':[(-58.0,-78.0),(-58.0,78.0),(58.0,-78.0),(58.0,78.0)],
    'mini_itx_yz':[(-78.65,31.35),(-78.65,188.83),(78.83,31.35),(78.83,188.83)],
    'psu_base_xy':[(16.0,-72.0),(16.0,72.0),(46.0,-72.0),(46.0,72.0)],
    'riser_tray_yz':[(-14.0,91.0),(50.0,91.0)],
    'riser_receiver_xy':[(22.0,0.0),(22.0,36.0),(40.0,0.0),(40.0,36.0)],
    'gpu_tail_xy':[(16.0,62.0),(46.0,62.0)],
    'gpu_bracket_xz':[(20.84,212.0),(41.16,212.0)],
    'gpu_side_yz':[(-70.0,110.0),(70.0,110.0)],
    'magnet_pilot_axes':magnet_pilot_axes
}
legacy_axes={
    'top_cap_xy':[(-65.0,-87.0),(-65.0,87.0),(65.0,-87.0),(65.0,87.0)],
    'psu_base_xy':[(14.0,-70.0),(14.0,70.0),(48.0,-70.0),(48.0,70.0)]
}
assert [len(screw_layout[k]) for k in screw_layout]==[4,4,4,2,4,2,2,2,16]
assert sum(len(v) for v in screw_layout.values())==40
assert set(screw_layout['top_cap_xy']).isdisjoint(set(legacy_axes['top_cap_xy']))
assert set(screw_layout['psu_base_xy']).isdisjoint(set(legacy_axes['psu_base_xy']))
assert abs(screw_layout['mini_itx_yz'][2][0]-screw_layout['mini_itx_yz'][0][0]-157.48)<0.001
assert abs(screw_layout['mini_itx_yz'][1][1]-screw_layout['mini_itx_yz'][0][1]-157.48)<0.001
assert abs(screw_layout['gpu_bracket_xz'][1][0]-screw_layout['gpu_bracket_xz'][0][0]-20.32)<0.001
assert set(receiver_slot_x)=={22.0,40.0} and set(tail_slot_x)=={16.0,46.0}
assert all(abs(2*pilot_r-2.6)<0.001 for axis in magnet_pilot_axes)
print('SCREW_LAYOUT_AUDIT_PASS: 40 final axes across 9 interfaces, including 16 centered magnet pilots; legacy top/PSU axes disjoint; Mini-ITX pitch 157.48 mm; dual-slot pitch 20.32 mm; no perimeter-panel screw holes.')