# The apparent step is the required Mini-ITX rear-lower mounting ear; preserve it unchanged.
rr_mount_ear_preserve_clearance=param('rr_mount_ear_preserve_clearance',0.0)
rr_column=current_top_targets[2]
current_top_targets[2]=rr_column
publish('column_fr',rr_column,'Rear-right support with MB ear')
print('REAR_RIGHT_MB_EAR_PRESERVED: the marked feature is the required Mini-ITX mounting ear at the end of the rear support arm; no geometry is trimmed.')