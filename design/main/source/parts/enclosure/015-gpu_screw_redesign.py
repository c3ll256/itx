# Final GPU/riser printed geometry; all purchased screws are represented by coaxial holes and the BOM, not exported solids.
riser_tab_y=(-14.0,50.0)
riser_plate=Box(50,78,4,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,18,92)))
riser_tabs_new=None
for y in riser_tab_y:
    tab=Box(9,16,10,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((8.5,y,86)))
    axis_cut=Cylinder(m3_clear,14,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location((8.5,y,91)))
    tab=tab-axis_cut
    motherboard_tray=motherboard_tray-axis_cut
    riser_tabs_new=tab if riser_tabs_new is None else riser_tabs_new+tab
receiver_slot_x=(22.0,40.0)
for x in receiver_slot_x:
    slot=Box(3.4,44.0,8,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,18,89)))
    slot=slot+Cylinder(1.7,8,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,-4,89)))
    slot=slot+Cylinder(1.7,8,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,40,89)))
    riser_plate=riser_plate-slot
tail_slot_x=(16.0,46.0)
tail_rails=None
for x in tail_slot_x:
    rail=Box(9,58,5,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,69,92)))
    cut=Box(3.4,40.6,8,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,62,90)))
    cut=cut+Cylinder(1.7,8,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,41.7,90)))
    cut=cut+Cylinder(1.7,8,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,82.3,90)))
    rail=rail-cut
    tail_rails=rail if tail_rails is None else tail_rails+rail
clamp_y=(-70.0,70.0)
clamp_bosses=None
clamps_new=None
for y in clamp_y:
    boss=Box(10,14,22.2,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((52,y,96.8)))
    pocket=Cylinder(2.25,9,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location((53,y,110)))
    boss=boss-pocket
    block=Box(7,14,16,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((58.5,y,102)))
    hole=Cylinder(m3_clear,12,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.Y,90).moved(Location((58.5,y,110)))
    block=block-hole
    clamp_bosses=boss if clamp_bosses is None else clamp_bosses+boss
    clamps_new=block if clamps_new is None else clamps_new+block
gpu_riser_new=riser_plate+riser_tabs_new+rail_a+rail_b+tail_rails+clamp_bosses
clamp_bar_y=(0.0,36.0)
receiver_bars=None
for y in clamp_bar_y:
    bar=Box(34,8,3,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,y,97)))
    for x in receiver_slot_x:
        bar=bar-Cylinder(m3_clear,5,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,96)))
    receiver_bars=bar if receiver_bars is None else receiver_bars+bar
nominal_tail_y=62.0
saddle_base=Box(46,8,8,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,nominal_tail_y,97)))
for x in tail_slot_x:
    saddle_base=saddle_base-Cylinder(m3_clear,12,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,nominal_tail_y,90)))
tail_saddle=saddle_base+Box(6,8,22,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((11,nominal_tail_y,97)))+Box(6,8,22,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((51,nominal_tail_y,97)))
rear_frame_new=Box(54,6,126,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,-89,92)))
rear_frame_new=rear_frame_new-Box(42,10,114,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,-91,98)))
bracket_x=(31-10.16,31+10.16)
for x in bracket_x:
    rear_frame_new=rear_frame_new-Cylinder(m3_clear,10,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.X,90).moved(Location((x,-89,212)))
assert abs(bracket_x[1]-bracket_x[0]-20.32)<0.001
assert set(receiver_slot_x).isdisjoint(set(tail_slot_x))
assert set(riser_tab_y).isdisjoint({-12.0,48.0})
publish('motherboard_tray',motherboard_tray,'Mini-ITX tray with redesigned riser-tab axes')
publish('gpu_riser_shelf',gpu_riser_new,'GPU shelf with rebuilt riser and tail-support slots')
publish('riser_clamp_bars',receiver_bars,'Receiver clamp bars on redesigned slot axes')
publish('gpu_front_support',tail_saddle,'Tail saddle on redesigned two-slot pattern')
publish('gpu_rear_io_frame',rear_frame_new,'GPU frame with 20.32 mm dual-slot screw pitch')
publish('gpu_side_clamps',clamps_new,'GPU clamps coaxial with support bosses')
print('GPU/riser screw holes remain fully redesigned; four M3x12 screws are BOM hardware and excluded from printable CAD solids.')