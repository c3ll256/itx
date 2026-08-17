# Close obsolete anchor paths, keep the lower-front Mini-ITX support detachable, and fuse only the two upper supports.
retired_anchor_patch_radius=param('retired_anchor_patch_radius',4.5); retired_anchor_patch_margin=param('retired_anchor_patch_margin',0.2)
lower_front_fuse_overlap=param('lower_front_fuse_overlap',0.6)
base_panel_width=param('case_width',W); base_panel_depth=param('case_depth',D); base_panel_thickness=param('base_thickness',base_t)
top_panel_width=param('case_width',W); top_panel_depth=param('case_depth',D); top_panel_stack=param('top_cap_thickness',cap_t)+param('top_cap_inner_thickness',cap_inner_t)
lower_front_detachable_engagement=param('lower_front_detachable_engagement',5.0)
# Retire only the old rear floor path; the front path remains the service fastener for the detachable mount.
rear_patch=Cylinder(retired_anchor_patch_radius,base_panel_thickness,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((rear_lower_screw_x,lower_mount_ys[0],0)))
base=(base+rear_patch).clean()
lower_front_mount=lower_mount_parts[1]
detachable_front_joint=make_screw_joint_v1(size='M3',at=Location((front_floor_anchor_x,lower_mount_ys[1],0),(180,0,0)),through=[(base,base_panel_thickness)],engage_depth=lower_front_detachable_engagement,into=lower_front_mount,head='socket_cap',strategy='auto',material=material,boss='auto',label='detachable-lower-front-mb-mount')
base=(base-detachable_front_joint.through_cuts[0]).clean(); lower_front_mount=(lower_front_mount+detachable_front_joint.bosses-detachable_front_joint.engage_cuts).clean()
# Retire old upper anchor paths and fuse both upper supports to the top panel.
for y in upper_mount_ys:
    patch=Cylinder(retired_anchor_patch_radius,top_panel_stack,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((upper_screw_x,y,H-top_panel_stack)))
    top_cap=(top_cap+patch).clean()
top_cap=(top_cap+upper_mount_parts[0]+upper_mount_parts[1]).clean()
mount_connection_inventory={'lower-front-to-base':'printed-screw-joint-v1 detachable underside M3','upper-rear-to-top':'free monolithic fuse','upper-front-to-top':'free monolithic fuse','motherboard-fasteners':'printed-screw-joint-v1'}
assert base.solids().__len__()==1 and top_cap.solids().__len__()==1 and lower_front_mount.solids().__len__()==1
assert detachable_front_joint.screw_length_mm==8 and len(mount_connection_inventory)==4
publish('base',base,'Base for detachable ITX mount'); publish('top_cap',top_cap,'Top with ITX mounts')
print('DETACHABLE_FRONT_MB_PREP_PASS: lower-front Mini-ITX support remains separate and is retained by one underside M3x8 screw; upper supports remain fused to the top.')