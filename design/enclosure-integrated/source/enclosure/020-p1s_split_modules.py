# Geometry tracking audit before the final P1S edge-margin trim.
transition_axis_limit=param('transition_axis_limit',260.0)
printable_objects=[base,top_cap,left_panel,right_panel,front_panel,rear_panel,columns[0],columns[1],columns[2],columns[3],feet[0],feet[1],feet[2],feet[3],lower_mount_parts[0],lower_mount_parts[1],upper_mount_parts[0],upper_mount_parts[1]]
for part in printable_objects:
    bb=part.bounding_box(); dims=(bb.size.X,bb.size.Y,bb.size.Z)
    assert max(dims)<=transition_axis_limit+0.001
assert abs(base.bounding_box().size.Y-D)<0.001
assert abs(top_cap.bounding_box().size.Y-D)<0.001
assert left_panel.bounding_box().size.Y<=D-4.0+0.001 and right_panel.bounding_box().size.Y<=D-4.0+0.001
publish('base',base,'Depth-tracking base')
print(f'DEPTH_TRANSITION_PASS: pre-trim base/top depth={D:.1f} mm; side-panel depth={left_panel.bounding_box().size.Y:.1f} mm; final P1S edge trim is applied later.')