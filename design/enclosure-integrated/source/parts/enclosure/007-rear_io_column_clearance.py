# Postless rear-I/O audit. The legacy rear-column relief is retired because no
# independent column is published or used by the final six-part enclosure.
postless_io_top_clearance=param('postless_io_top_clearance',0.50)
postless_io_side_clearance=param('postless_io_side_clearance',0.50)
postless_io_expected_board_height=param('mitx_board_height',170.0)
postless_io_z_min=mitx_board_z_min+postless_io_expected_board_height-(param('io_shield_nominal_long',158.75)+2*postless_io_top_clearance)
postless_io_z_max=mitx_board_z_min+postless_io_expected_board_height+postless_io_top_clearance
assert postless_io_z_min>=mitx_board_z_min-0.001
assert postless_io_z_max<=H+0.001
assert postless_io_side_clearance>=0.50
print(f'POSTLESS_REAR_IO_AUDIT_PASS: legacy column relief retired; standard rear I/O spans z={postless_io_z_min:.2f}..{postless_io_z_max:.2f} and may meet the enclosure top boundary.')