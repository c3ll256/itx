# Correct rear-right top-cover connection with the local column ending at the cap's inner underside.
rr_top_restore_width=param('rr_top_restore_width',14.0)
rr_top_restore_depth=param('rr_top_restore_depth',14.0)
rr_top_restore_height=param('rr_top_restore_height',14.0)
rr_top_cap_outer_thickness=param('final_cap_outer_thickness',3.0)
rr_top_cap_inner_thickness=param('final_cap_inner_thickness',2.0)
rr_top_engagement=param('rr_top_engagement',5.0)
rr_top_trim_margin=param('rr_top_trim_margin',2.0)
rr_top_trim_height=param('rr_top_trim_height',12.0)
rr_top_stack=rr_top_cap_outer_thickness+rr_top_cap_inner_thickness
rr_column_top_z=H-rr_top_stack
rr_x,rr_y=post_xy[2]
rr_column=current_top_targets[2]
# Remove every local feature that entered the top-cap stack.
rr_trim=Box(rr_top_restore_width+2*rr_top_trim_margin,rr_top_restore_depth+2*rr_top_trim_margin,rr_top_trim_height,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((rr_x,rr_y,rr_column_top_z)))
rr_column=(rr_column-rr_trim).clean()
# Restore local column material only below the cap underside.
rr_restore=Box(rr_top_restore_width,rr_top_restore_depth,rr_top_restore_height,align=(Align.CENTER,Align.CENTER,Align.MAX)).moved(Location((rr_x,rr_y,rr_column_top_z)))
rr_column=(rr_column+rr_restore).clean()
# Existing 14 mm column provides sufficient wall; boss='none' prevents any reinforcement from entering the cap.
rr_top_joint=make_screw_joint_v1(size='M3',at=Location((rr_x,rr_y,H)),through=[(top_cap,rr_top_stack)],engage_depth=rr_top_engagement,into=rr_column,head='socket_cap',strategy='auto',material=material,boss='none',label='final-rear-right-top-cover-corrected')
top_cap=(top_cap-rr_top_joint.through_cuts[0]).clean()
rr_column=(rr_column-rr_top_joint.engage_cuts).clean()
current_top_targets[2]=rr_column
assert abs(rr_top_joint.through_thickness_mm-rr_top_stack)<0.001
assert rr_top_joint.screw_length_mm>rr_top_stack
publish('top_cap',top_cap,'Rear-right clearance-hole cap')
publish('column_fr',rr_column,'Rear-right under-cap column')
print(f'REAR_RIGHT_TOP_INTERFACE_PASS: local column is trimmed to cap underside z={rr_column_top_z:.1f} mm; M3 clears the {rr_top_stack:.1f} mm cap and engages {rr_top_engagement:.1f} mm below it; no automatic boss is allowed.')