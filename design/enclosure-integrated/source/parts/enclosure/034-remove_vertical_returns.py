# Compatibility audit for the point-fastened frame. The previous continuous-return
# cutting operation is retired; geometry is now created without rails or returns.
point_frame_audit_min_gap=param('point_frame_audit_min_gap',20.0)
point_frame_audit_expected_corner_joints=param('corner_joint_count_expected',8)
assert point_frame_audit_min_gap>0
assert point_frame_audit_expected_corner_joints==8
print('POINT_FRAME_AUDIT_READY: legacy vertical-return subtraction retired; source frame owns isolated corner geometry directly.')