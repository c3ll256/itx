# Sixteen 15 x 10 x 4 mm countersunk magnets seat in shallow flats and use centered M3 printed pilots.
magnet_w,magnet_h,magnet_t=10.0,15.0,4.0
flat_w,flat_h,flat_d=10.4,15.4,4.2
pilot_r,pilot_depth=1.30,4.60
end_z=(30.0,195.0)
side_z=(58.0,167.0)
post_outer_x=post_x+post/2
post_outer_y=post_y+post/2
flat_cuts=None
pilot_cuts=None
# Front/rear stations: magnet flat on +/-Y face and coaxial M3 pilot normal to that face.
for sy in (-1,1):
    flat_center_y=sy*(post_outer_y-flat_d/2)
    pilot_center_y=sy*(post_outer_y-flat_d-pilot_depth/2)
    for x in (-post_x,post_x):
        for z in end_z:
            flat=Box(flat_w,flat_d,flat_h,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((x,flat_center_y,z)))
            pilot=Cylinder(pilot_r,pilot_depth,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.X,90).moved(Location((x,pilot_center_y,z)))
            flat_cuts=flat if flat_cuts is None else flat_cuts+flat
            pilot_cuts=pilot if pilot_cuts is None else pilot_cuts+pilot
# Left/right stations: magnet flat on +/-X face and coaxial M3 pilot normal to that face.
for sx in (-1,1):
    flat_center_x=sx*(post_outer_x-flat_d/2)
    pilot_center_x=sx*(post_outer_x-flat_d-pilot_depth/2)
    for y in (-post_y,post_y):
        for z in side_z:
            flat=Box(flat_d,flat_w,flat_h,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((flat_center_x,y,z)))
            pilot=Cylinder(pilot_r,pilot_depth,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location((pilot_center_x,y,z)))
            flat_cuts=flat_cuts+flat
            pilot_cuts=pilot_cuts+pilot
main_frame=main_frame-flat_cuts-pilot_cuts
rear_panel=rear_panel-Cylinder(7,8,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.X,90).moved(Location((0,-D/2,base_t)))
assert 2*2*len(end_z)+2*2*len(side_z)==16
assert post-flat_d>=5.8-0.001
assert min(abs(a-b) for a in end_z for b in side_z)>20.0
assert abs(2*pilot_r-2.6)<0.001 and pilot_depth<=post-flat_d
publish('base_and_frame',main_frame,'Frame with sixteen magnet flats and centered M3 pilots')
publish('rear_io_panel',rear_panel,'Rear magnetic service panel with clear openings')
print('Magnet retention rebuilt: 16 shallow flats, each with one centered 2.6 x 4.6 mm printed M3 pilot; magnets and M3x8 screws remain BOM hardware.')