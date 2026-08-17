# Rear-panel clearance holes for the standard four-point SFX PSU mounting face.
sfx_mount_hole_diameter=param('sfx_mount_hole_diameter',4.2)
sfx_mount_horizontal_inset=param('sfx_mount_horizontal_inset',3.0)
sfx_mount_vertical_inset=param('sfx_mount_vertical_inset',5.5)
sfx_mount_cut_depth=param('sfx_mount_cut_depth',8.0)
sfx_face_z0=base_t
sfx_hole_x=sfx_psu_width/2-sfx_mount_horizontal_inset
sfx_hole_z_low=sfx_face_z0+sfx_mount_vertical_inset
sfx_hole_z_high=sfx_face_z0+sfx_psu_height-sfx_mount_vertical_inset
sfx_mount_points=[(-sfx_hole_x,sfx_hole_z_low),(sfx_hole_x,sfx_hole_z_low),(-sfx_hole_x,sfx_hole_z_high),(sfx_hole_x,sfx_hole_z_high)]
for x,z in sfx_mount_points:
    cut=Cylinder(sfx_mount_hole_diameter/2,sfx_mount_cut_depth,align=(Align.CENTER,Align.CENTER,Align.CENTER)).rotate(Axis.X,90).moved(Location((x,-D/2,z)))
    rear_panel=rear_panel-cut
assert len(sfx_mount_points)==4
assert sfx_hole_x>psu_cut_w/2+sfx_mount_hole_diameter/2
assert sfx_hole_z_low>base_t and sfx_hole_z_high<H-cap_t
publish('rear_panel',rear_panel,'Four-hole SFX rear')
print(f'SFX_REAR_MOUNT_PASS: four {sfx_mount_hole_diameter:.1f} mm clearance holes at x=±{sfx_hole_x:.1f}, z={sfx_hole_z_low:.1f}/{sfx_hole_z_high:.1f} mm surround the reduced service opening.')