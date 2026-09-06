# The active printed-screw-joint-v1 bottom joints already cut true conical
# countersinks into the integrated feet. Do not add the former cylindrical
# socket-head counterbores here, because they erase the conical seating face.
corner_countersunk_expected_count=param('corner_countersunk_expected_count',4)
corner_countersunk_expected_screw_length=param('corner_countersunk_expected_screw_length',12.0)
corner_countersunk_connection_inventory={
    'bottom-corner-threads':'printed-screw-joint-v1 x4',
    'bottom-corner-head-seats':'kit-owned conical countersinks x4',
}
bottom_countersunk_joints=active_bottom_corner_joints
bottom_countersunk_screw_lengths={j.screw_length_mm for j in bottom_countersunk_joints}
assert len(bottom_countersunk_joints)==int(corner_countersunk_expected_count)
assert bottom_countersunk_screw_lengths=={corner_countersunk_expected_screw_length}
assert base.solids().__len__()==1
assert all(corner_countersunk_connection_inventory.values())
publish('base',base,'Conical countersunk bottom')
print(f'BOTTOM_COUNTERSUNK_PASS: retained {len(bottom_countersunk_joints)} kit-owned conical M3 countersinks for M3x{corner_countersunk_expected_screw_length:.0f} flat-head screws; no cylindrical head recesses remain.')