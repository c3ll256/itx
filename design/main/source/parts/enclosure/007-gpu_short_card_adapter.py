# Adjustable tail support for the user-image compact single-fan dual-slot GPU.
# Rear bracket remains fixed; tail saddle adjusts for approximately 130-180 mm card lengths.
short_card_min_y=40.0
short_card_max_y=84.0
nominal_tail_y=60.0
# Add two printed adjustment rails alongside the existing GPU lower rails.
adjust_rail_a=Box(9,58,5,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((13,short_card_min_y+29,92)))
adjust_rail_b=Box(9,58,5,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((49,short_card_min_y+29,92)))
# Long M3 adjustment slots through the added rails.
for x in (13,49):
  slot=Box(3.4,44,8,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,(short_card_min_y+short_card_max_y)/2,90)))
  adjust_rail_a=adjust_rail_a-slot if x==13 else adjust_rail_a
  adjust_rail_b=adjust_rail_b-slot if x==49 else adjust_rail_b
gpu_riser_adjusted=gpu_riser+adjust_rail_a+adjust_rail_b
# Compact U-shaped saddle supports the card tail without a full-height airflow-blocking frame.
base_bar=Box(46,8,8,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,nominal_tail_y,97)))
left_ear=Box(6,8,22,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((11,nominal_tail_y,97)))
right_ear=Box(6,8,22,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((51,nominal_tail_y,97)))
# Two M3 clearance holes clamp the saddle at any point in the adjustment slots.
for x in (13,49):
  hole=Cylinder(m3_clear,12,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,nominal_tail_y,90)))
  base_bar=base_bar-hole
adjustable_saddle=base_bar+left_ear+right_ear
assert short_card_max_y-short_card_min_y>=40
assert nominal_tail_y>=short_card_min_y and nominal_tail_y<=short_card_max_y
publish('gpu_riser_shelf',gpu_riser_adjusted,'GPU riser shelf with 44 mm tail-support adjustment slots')
publish('gpu_front_support',adjustable_saddle,'Adjustable low-profile tail saddle for compact single-fan dual-slot GPU')
print(f'GPU tail support changed from fixed full-height frame to adjustable saddle; travel y={short_card_min_y:.0f}..{short_card_max_y:.0f} mm, nominal y={nominal_tail_y:.0f} mm.')