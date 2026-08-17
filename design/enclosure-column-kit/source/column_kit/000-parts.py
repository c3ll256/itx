from screwjoint import make_screw_joint_v1
W,D,H=146.0,190.0,225.0
base_t,cap_t,panel_t=3.0,3.0,2.4
post=14.0; clearance=0.6; material='PLA'
outer_x=W/2-panel_t-clearance; outer_y=D/2-panel_t-clearance
post_x=outer_x-post/2; post_y=outer_y-post/2
post_xy=[(-post_x,-post_y),(-post_x,post_y),(post_x,-post_y),(post_x,post_y)]
ids=('fl','rl','fr','rr')
base=Box(W,D,base_t,align=(Align.CENTER,Align.CENTER,Align.MIN))
columns=[]; base_joints=[]; top_joints=[]; magnet_joint_count=0
for i,(x,y) in enumerate(post_xy):
    c=Box(post,post,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,base_t)))
    sy=-1 if y<0 else 1
    for z in (30.0,210.0):
        c=c-Box(10.2,3.2,10.2,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((x,sy*(outer_y-1.6),z)))
        proxy=Box(10,3,10,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((x,sy*(outer_y-1.5),z)))
        j=make_screw_joint_v1(size='M3',at=Location((x,sy*outer_y,z),(-90*sy,0,0)),through=[(proxy,3.0)],into=c,head='countersunk',strategy='auto',material=material,boss='auto',label=f'magnet-end:{ids[i]}:{z}')
        c=c+j.bosses-j.engage_cuts; magnet_joint_count+=1
    sx=-1 if x<0 else 1
    for z in (58.0,167.0):
        c=c-Box(3.2,10.2,10.2,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((sx*(outer_x-1.6),y,z)))
        proxy=Box(3,10,10,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((sx*(outer_x-1.5),y,z)))
        j=make_screw_joint_v1(size='M3',at=Location((sx*outer_x,y,z),(0,90*sx,0)),through=[(proxy,3.0)],into=c,head='countersunk',strategy='auto',material=material,boss='auto',label=f'magnet-side:{ids[i]}:{z}')
        c=c+j.bosses-j.engage_cuts; magnet_joint_count+=1
    top_proxy=Box(10,10,cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,H-cap_t)))
    tj=make_screw_joint_v1(size='M3',at=Location((x,y,H)),through=[(top_proxy,cap_t)],into=c,head='socket_cap',strategy='auto',material=material,boss='auto',label=f'column-top:{ids[i]}')
    c=c+tj.bosses-tj.engage_cuts; top_joints.append(tj)
    columns.append(c)
for i,((x,y),c) in enumerate(zip(post_xy,columns)):
    j=make_screw_joint_v1(size='M3',at=Location((x,y,0),(180,0,0)),through=[(base,base_t)],into=c,head='socket_cap',strategy='auto',material=material,boss='auto',label=f'column-base:{ids[i]}')
    base=base-j.through_cuts[0]
    columns[i]=c+j.bosses-j.engage_cuts
    base_joints.append(j)
assert len(columns)==4 and len(base_joints)==4 and len(top_joints)==4 and magnet_joint_count==16
publish('column_base',base,'Column mounting base')
publish('column_fl',columns[0],'Front left column')
publish('column_rl',columns[1],'Rear left column')
publish('column_fr',columns[2],'Front right column')
publish('column_rr',columns[3],'Rear right column')
print('COLUMN_KIT_PASS: four independent columns; four underside M3 kit joints; four top M3 kit joints; sixteen direct 10x10x3 magnet seats.')