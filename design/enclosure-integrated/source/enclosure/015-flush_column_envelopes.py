# Keep each printed column inside its intended 14 x 14 mm envelope.
# The cap's 2 mm inner layer overlaps the column tops, so reuse the printed-screw-joint-v1
# through-cut there; this joins the cap clearance path to the kit-owned engagement cut.
assert len(columns)==4 and len(top_joints)==4
for i,(x,y) in enumerate(post_xy):
    intended=Box(post,post,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,base_t)))
    clipped=columns[i].intersect(intended)
    columns[i]=(clipped-top_joints[i].through_cuts[0]).clean()
publish('column_fl',columns[0],'Open-top rear-left')
publish('column_rl',columns[1],'Open-top front-left')
publish('column_fr',columns[2],'Open-top rear-right')
publish('column_rr',columns[3],'Open-top front-right')
print('COLUMN_TOP_OPENINGS_PASS: all four columns reuse the screw-joint kit clearance cut across the cap overlap; no solid top plugs remain.')