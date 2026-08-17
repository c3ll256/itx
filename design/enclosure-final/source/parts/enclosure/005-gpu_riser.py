# GPU/riser printed supports. Adjustable hand-cut slots are replaced by fixed kit-owned joints.
riser_plate=Box(50,78,4,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,18,92)))
riser_tabs=None
for y in riser_tab_y:
    tab=Box(9,16,10,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((8.5,y,86)))
    riser_tabs=tab if riser_tabs is None else riser_tabs+tab
rail_a=Box(5,178,5,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((13,-1,92)))
rail_b=Box(5,178,5,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((49,-1,92)))
tail_slot_x=(16.0,46.0)  # retained as nominal fixed joint X positions
tail_rails=None
for x in tail_slot_x:
    rail=Box(9,58,5,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,69,92)))
    tail_rails=rail if tail_rails is None else tail_rails+rail
gpu_riser=riser_plate+riser_tabs+rail_a+rail_b+tail_rails
for joint in riser_joints:
    gpu_riser=gpu_riser+joint.bosses-joint.engage_cuts

# Two removable receiver clamp bars: four fixed M3 joints replace the old capsule slots.
receiver_joint_x=(22.0,40.0)
receiver_bar_y=(0.0,36.0)
clamp_bars=None
for y in receiver_bar_y:
    bar=Box(34,8,3,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,y,97)))
    clamp_bars=bar if clamp_bars is None else clamp_bars+bar
receiver_joints=[]
for y in receiver_bar_y:
    for x in receiver_joint_x:
        joint=require_kit_joint(
            f"receiver-clamp:{x}:{y}", size="M3", at=Location((x,y,100)),
            through=[(clamp_bars,3.0)], head="socket_cap", strategy="auto", boss="auto"
        )
        clamp_bars=clamp_bars-joint.through_cuts[0]
        gpu_riser=gpu_riser+joint.bosses-joint.engage_cuts
        receiver_joints.append(joint)

# Compact GPU tail saddle: two fixed kit joints replace the old long slots.
saddle=Box(46,8,8,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,62,97)))
saddle=saddle+Box(6,8,22,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((11,62,97)))
saddle=saddle+Box(6,8,22,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((51,62,97)))
tail_joints=[]
for x in tail_slot_x:
    joint=require_kit_joint(
        f"gpu-tail:{x}", size="M3", at=Location((x,62,105)),
        through=[(saddle,8.0)], head="socket_cap", strategy="auto", boss="auto"
    )
    saddle=saddle-joint.through_cuts[0]
    gpu_riser=gpu_riser+joint.bosses-joint.engage_cuts
    tail_joints.append(joint)

# Rear dual-slot frame with exact 20.32 mm bracket pitch. Metal bracket is the through stack;
# the kit adds reinforced printed engagement bosses to the frame.
rear_frame=Box(54,6,126,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,-89,92)))
rear_frame=rear_frame-Box(42,10,114,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,-91,98)))
bracket_x=(20.84,41.16)
bracket_thickness=1.5
gpu_bracket_proxy=Box(54,bracket_thickness,10,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((31,-92.75,212)))
rear_joints=[]
for i,x in enumerate(bracket_x):
    joint=require_kit_joint(
        f"gpu-rear:{i}", size="M3", at=Location((x,-93.5,212),(90,0,0)),
        through=[(gpu_bracket_proxy,bracket_thickness)], head="socket_cap", strategy="auto", boss="auto"
    )
    rear_frame=rear_frame+joint.bosses-joint.engage_cuts
    rear_joints.append(joint)

# Two coaxial side clamps. Existing 14 mm receiver blocks provide 12 mm of
# engagement-side depth, satisfying the kit's entry, thread and blind-relief contract.
clamp_y=(-70.0,70.0)
clamp_bosses=None
clamps=None
side_clamp_joints=[]
for i,y in enumerate(clamp_y):
    receiver=Box(14,14,22.2,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((50,y,96.8)))
    block=Box(7,14,16,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((58.5,y,102)))
    joint=require_kit_joint(
        f"gpu-side-clamp:{i}", size="M3", at=Location((62,y,110),(0,90,0)),
        through=[(block,7.0)], head="socket_cap", strategy="auto",
        boss="none", available_depth=12.0
    )
    block=block-joint.through_cuts[0]
    receiver=receiver-joint.engage_cuts
    clamp_bosses=receiver if clamp_bosses is None else clamp_bosses+receiver
    clamps=block if clamps is None else clamps+block
    side_clamp_joints.append(joint)
gpu_riser=gpu_riser+clamp_bosses

assert abs(bracket_x[1]-bracket_x[0]-20.32)<0.001
assert len(receiver_joints)==4 and len(tail_joints)==2 and len(rear_joints)==2 and len(side_clamp_joints)==2
assert free_connection_ids==set()
assert intended_connection_ids==kit_connection_ids and len(kit_connection_ids)==44
assert len(joint_bom_lines)==44 and len(screw_hardware_by_connection)==44
publish('gpu_riser_shelf',gpu_riser,'Kit-fastened GPU shelf')
publish('riser_clamp_bars',clamp_bars,'Kit-fastened clamp bars')
publish('gpu_tail_saddle',saddle,'Kit-fastened tail saddle')
publish('gpu_rear_frame',rear_frame,'Kit-fastened rear frame')
publish('gpu_side_clamps',clamps,'Kit-fastened side clamps')
print('SCREW_CONNECTION_INVENTORY_PASS: intended=44, kit=44, free=0, hand-modeled screw holes=0.')
print(f'KIT_BOM_LINES_PASS: {len(joint_bom_lines)} solved screw selections for material={SCREW_MATERIAL}.')