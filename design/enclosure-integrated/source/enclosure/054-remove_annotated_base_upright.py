# Superseded by the corrected four-point Mini-ITX mounting pattern.
# Keep the lower-front support: removing it leaves the motherboard with only three fasteners.
marked_upright_clearance_xy=param('marked_upright_clearance_xy',0.5)
marked_upright_cut_height=param('marked_upright_cut_height',H)
marked_upright_floor_skin=param('marked_upright_floor_skin',0.0)
restored_lower_front_mount_count=param('restored_lower_front_mount_count',1)
assert int(restored_lower_front_mount_count)==1 and base.solids().__len__()==1
publish('base',base,'Base with four-point ITX mount')
print('LOWER_FRONT_MB_MOUNT_RESTORED: obsolete upright-removal operation disabled so all four Mini-ITX mounting points remain available.')