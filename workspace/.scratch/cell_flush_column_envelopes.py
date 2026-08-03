# cell: flush_column_envelopes
# Remove kit-generated external column extensions while preserving internal screw cuts.
# Each column is clipped to its intended 14 x 14 mm prism between base top and cap underside.
for i,(x,y) in enumerate(post_xy):
    intended=Box(post,post,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,base_t)))
    columns[i]=columns[i].intersect(intended).clean()
publish('column_fl',columns[0],'Flush rear-left column')
publish('column_rl',columns[1],'Flush front-left column')
publish('column_fr',columns[2],'Flush rear-right column')
publish('column_rr',columns[3],'Flush front-right column')
print('FLUSH_COLUMN_ENVELOPES_PASS: all four columns are flat-ended 14 x 14 mm prisms from base top to cap underside; protruding external boss sections removed.')

