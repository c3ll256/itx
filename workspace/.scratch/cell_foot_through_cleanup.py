# cell: foot_through_cleanup
# Reapply the printed-screw-joint-v1 clearance cuts to the four detachable feet
# and clean the coincident top faces. Geometry and fastener solution are unchanged.
clean_feet=[]
for foot,j in zip(feet,base_joints):
    clean_foot=(foot-j.through_cuts[0]).clean()
    clean_feet.append(clean_foot)
feet=clean_feet
assert len(feet)==4 and len(base_joints)==4
assert all(abs(j.through_thickness_mm-(4.0+base_t))<0.001 for j in base_joints)
assert all(abs(j.screw_length_mm-12.0)<0.001 for j in base_joints)
publish('case_feet',Compound(children=feet),'Through-hole feet')
print('FOOT_THROUGH_CLEAN_PASS: all four kit-owned foot clearance cuts are reapplied and coincident top faces cleaned; the 4 mm foot + 3 mm base + M3x12 joint stack is unchanged.')

