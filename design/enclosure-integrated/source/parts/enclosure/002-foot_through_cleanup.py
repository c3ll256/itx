# Reapply kit clearance cuts to construction-only feet for downstream base fusion.
foot_cleanup_expected_count=param('foot_cleanup_expected_count',4)
foot_cleanup_stack_height=param('foot_cleanup_stack_height',7.0)
clean_feet=[]
for foot,j in zip(feet,base_joints):
    clean_feet.append((foot-j.through_cuts[0]).clean())
feet=clean_feet
assert len(feet)==foot_cleanup_expected_count and len(base_joints)==foot_cleanup_expected_count
assert all(abs(j.through_thickness_mm-foot_cleanup_stack_height)<0.001 for j in base_joints)
assert all(abs(j.screw_length_mm-12.0)<0.001 for j in base_joints)
print('FOOT_CLEANUP_SOURCE_ONLY: kit-owned foot cuts retained for fusion; no separate foot component is published.')