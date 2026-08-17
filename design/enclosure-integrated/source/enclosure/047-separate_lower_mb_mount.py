# Publish and verify the detachable lower-front Mini-ITX mount retained by an underside M3 screw.
base_direct_mb_mount_web_depth_x=param('base_direct_mb_mount_web_depth_x',arm_depth_x); base_direct_mb_mount_width_y=param('base_direct_mb_mount_width_y',arm_width_y)
base_direct_mb_mount_height_z=param('base_direct_mb_mount_height_z',lower_mount_z+5.0-base_t)
base_direct_mb_mount_foot_depth_x=param('base_direct_mb_mount_foot_depth_x',foot_depth_x); base_direct_mb_mount_foot_width_y=param('base_direct_mb_mount_foot_width_y',foot_width_y); base_direct_mb_mount_foot_height_z=param('base_direct_mb_mount_foot_height_z',foot_height_z)
base_direct_mb_mount_hole_z=param('base_direct_mb_mount_hole_z',lower_mount_z)
_active_mb_engagement=mitx_standoff_engagement if 'mitx_standoff_engagement' in globals() else motherboard_engagement
base_direct_mb_mount_hole_engagement=param('base_direct_mb_mount_hole_engagement',_active_mb_engagement); base_direct_mb_mount_expected_count=param('base_direct_mb_mount_expected_count',1)
lower_front_mb_mount=lower_front_mount if 'lower_front_mount' in globals() else lower_mount_parts[1]
base_direct_mb_connection_inventory={'motherboard-to-detachable-arm':'printed-screw-joint-v1','detachable-arm-to-base':'printed-screw-joint-v1 underside M3'}
assert int(base_direct_mb_mount_expected_count)==1 and base.solids().__len__()==1 and lower_front_mb_mount.solids().__len__()==1
assert all(base_direct_mb_connection_inventory.values())
publish('base',base,'Base with detachable ITX mount'); publish('lower_front_mb_mount',lower_front_mb_mount,'Detachable MB mount')
print(f'MB_DETACHABLE_BASE_PASS: lower-front Mini-ITX mount is a separate solid at z={base_direct_mb_mount_hole_z:.2f} mm and is serviced by one underside M3 screw.')