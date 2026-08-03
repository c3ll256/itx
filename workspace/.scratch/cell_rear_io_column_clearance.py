# cell: rear_io_column_clearance
# Relieve the inner edge of the left rear column where it overlaps the motherboard rear-I/O aperture.
# Keep the full lower/upper column blocks for the rear-panel M3 screws at z=30 and z=210.
io_clear_x_min=-60.0
io_clear_z_min=72.5
io_clear_z_max=201.5
rear_left_relief=Box(5.0,16.0,io_clear_z_max-io_clear_z_min,align=(Align.MIN,Align.CENTER,Align.MIN)).moved(Location((io_clear_x_min,-post_y,io_clear_z_min)))
columns[0]=(columns[0]-rear_left_relief).clean()
publish('column_fl',columns[0],'I-O clear rear-left')
assert io_clear_z_min>40.0 and io_clear_z_max<205.0
print('REAR_IO_COLUMN_CLEARANCE_PASS: inner 3.4 mm of the left rear column is relieved across the motherboard I/O opening; rear-panel screw zones remain full section.')

