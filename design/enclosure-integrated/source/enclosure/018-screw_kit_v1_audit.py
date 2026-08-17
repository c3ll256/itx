# Legacy screw-joint audit. Mount shapes are construction-only and are fused later.
expected_joint_count=param('expected_screw_joint_count',38)
actual_joint_count=magnet_joint_count+len(base_joints)+len(top_joints)+len(board_screw_lengths)+len(plate_screw_lengths)+len(slot_joints)+len(rear_screw_joints)
kit_joint_groups=base_joints+top_joints+slot_joints+rear_screw_joints
assert magnet_joint_count==16 and len(base_joints)==4 and len(top_joints)==4
assert len(board_screw_lengths)==4 and len(plate_screw_lengths)==4
assert len(slot_joints)==2 and len(rear_screw_joints)==4 and actual_joint_count==expected_joint_count
assert all(j.strategy=='self_forming' for j in kit_joint_groups)
assert all(j.hole_profile.sides==4 and j.engage_depth_mm>0 for j in kit_joint_groups)
publish('base',base,'Kit-audited base'); publish('top_cap',top_cap,'Kit-audited top'); publish('rear_panel',rear_panel,'Kit-audited rear')
print(f'SCREW_KIT_V1_AUDIT_PASS: {actual_joint_count} legacy kit joints replayed; motherboard support shapes are construction-only and not separate components.')