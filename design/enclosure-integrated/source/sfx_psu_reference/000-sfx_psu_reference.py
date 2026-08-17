# Standard SFX mechanical reference; not a claim of a specific retail PSU.
# The PSU rear face remains planar; no decorative mounting rings are published through the case holes.
sfx_ref_width_x = param('sfx_ref_width_x', 125.0)
sfx_ref_depth_y = param('sfx_ref_depth_y', 100.0)
sfx_ref_height_z = param('sfx_ref_height_z', 63.5)
sfx_ref_rear_clearance_y = param('sfx_ref_rear_clearance_y', 0.8)
sfx_ref_rear_y = param('sfx_ref_rear_y', -125.2)
sfx_ref_bottom_z = param('sfx_ref_bottom_z', 3.0)
sfx_ref_mount_hole_diameter = param('sfx_ref_mount_hole_diameter', 4.2)
sfx_ref_mount_spacing_x = param('sfx_ref_mount_spacing_x', 113.0)
sfx_ref_mount_spacing_z = param('sfx_ref_mount_spacing_z', 51.5)
sfx_ref_mount_cut_depth_y = param('sfx_ref_mount_cut_depth_y', 8.0)
sfx_ref_mount_cut_center_offset_y = param('sfx_ref_mount_cut_center_offset_y', 2.0)
sfx_ref_chassis = Box(sfx_ref_width_x, sfx_ref_depth_y, sfx_ref_height_z, align=(Align.CENTER, Align.MIN, Align.MIN)).moved(Location((0, sfx_ref_rear_y, sfx_ref_bottom_z)))
sfx_ref_face_center_z = sfx_ref_bottom_z + sfx_ref_height_z / 2
sfx_ref_mount_points = [
    (-sfx_ref_mount_spacing_x / 2, sfx_ref_face_center_z - sfx_ref_mount_spacing_z / 2),
    ( sfx_ref_mount_spacing_x / 2, sfx_ref_face_center_z - sfx_ref_mount_spacing_z / 2),
    (-sfx_ref_mount_spacing_x / 2, sfx_ref_face_center_z + sfx_ref_mount_spacing_z / 2),
    ( sfx_ref_mount_spacing_x / 2, sfx_ref_face_center_z + sfx_ref_mount_spacing_z / 2),
]
for sfx_ref_hole_x, sfx_ref_hole_z in sfx_ref_mount_points:
    sfx_ref_hole = Cylinder(sfx_ref_mount_hole_diameter / 2, sfx_ref_mount_cut_depth_y, align=(Align.CENTER, Align.CENTER, Align.CENTER)).rotate(Axis.X, 90).moved(Location((sfx_ref_hole_x, sfx_ref_rear_y + sfx_ref_mount_cut_center_offset_y, sfx_ref_hole_z)))
    sfx_ref_chassis = sfx_ref_chassis - sfx_ref_hole
publish('sfx_chassis', sfx_ref_chassis.clean(), 'SFX chassis reference')

sfx_ref_fan_outer_diameter = param('sfx_ref_fan_outer_diameter', 92.0)
sfx_ref_fan_hub_diameter = param('sfx_ref_fan_hub_diameter', 27.0)
sfx_ref_fan_grille_thickness_z = param('sfx_ref_fan_grille_thickness_z', 1.0)
sfx_ref_fan_center_y = param('sfx_ref_fan_center_y', sfx_ref_rear_y + sfx_ref_depth_y / 2)
sfx_ref_fan_z = param('sfx_ref_fan_z', sfx_ref_bottom_z + sfx_ref_height_z)
sfx_ref_fan_ring_2_diameter = param('sfx_ref_fan_ring_2_diameter', 74.0)
sfx_ref_fan_ring_3_diameter = param('sfx_ref_fan_ring_3_diameter', 56.0)
sfx_ref_fan_ring_4_diameter = param('sfx_ref_fan_ring_4_diameter', 38.0)
sfx_ref_fan_ring_width = param('sfx_ref_fan_ring_width', 2.0)
sfx_ref_fan_cut_extra_z = param('sfx_ref_fan_cut_extra_z', 0.3)
sfx_ref_fan_cut_offset_z = param('sfx_ref_fan_cut_offset_z', 0.1)
sfx_ref_fan_rings = []
for sfx_ref_fan_d in (sfx_ref_fan_outer_diameter, sfx_ref_fan_ring_2_diameter, sfx_ref_fan_ring_3_diameter, sfx_ref_fan_ring_4_diameter):
    sfx_ref_fan_ring_outer = Cylinder(sfx_ref_fan_d / 2, sfx_ref_fan_grille_thickness_z, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, sfx_ref_fan_center_y, sfx_ref_fan_z)))
    sfx_ref_fan_ring_inner = Cylinder((sfx_ref_fan_d - sfx_ref_fan_ring_width) / 2, sfx_ref_fan_grille_thickness_z + sfx_ref_fan_cut_extra_z, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, sfx_ref_fan_center_y, sfx_ref_fan_z - sfx_ref_fan_cut_offset_z)))
    sfx_ref_fan_rings.append(sfx_ref_fan_ring_outer - sfx_ref_fan_ring_inner)
sfx_ref_fan_hub = Cylinder(sfx_ref_fan_hub_diameter / 2, sfx_ref_fan_grille_thickness_z, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, sfx_ref_fan_center_y, sfx_ref_fan_z)))
sfx_ref_fan_rings.append(sfx_ref_fan_hub)
publish('sfx_fan_grille', Compound(children=sfx_ref_fan_rings), 'SFX fan grille')

sfx_ref_ac_inlet_width_x = param('sfx_ref_ac_inlet_width_x', 27.0)
sfx_ref_ac_inlet_depth_y = param('sfx_ref_ac_inlet_depth_y', 3.0)
sfx_ref_ac_inlet_height_z = param('sfx_ref_ac_inlet_height_z', 31.0)
sfx_ref_ac_inlet_center_x = param('sfx_ref_ac_inlet_center_x', 20.0)
sfx_ref_ac_inlet_bottom_z = param('sfx_ref_ac_inlet_bottom_z', 14.0)
sfx_ref_ac_inlet = Box(sfx_ref_ac_inlet_width_x, sfx_ref_ac_inlet_depth_y, sfx_ref_ac_inlet_height_z, align=(Align.CENTER, Align.MAX, Align.MIN)).moved(Location((sfx_ref_ac_inlet_center_x, sfx_ref_rear_y, sfx_ref_ac_inlet_bottom_z)))
publish('sfx_ac_inlet', sfx_ref_ac_inlet, 'AC inlet reference')

sfx_ref_switch_width_x = param('sfx_ref_switch_width_x', 13.0)
sfx_ref_switch_depth_y = param('sfx_ref_switch_depth_y', 3.0)
sfx_ref_switch_height_z = param('sfx_ref_switch_height_z', 20.0)
sfx_ref_switch_center_x = param('sfx_ref_switch_center_x', 45.0)
sfx_ref_switch_bottom_z = param('sfx_ref_switch_bottom_z', 38.0)
sfx_ref_switch = Box(sfx_ref_switch_width_x, sfx_ref_switch_depth_y, sfx_ref_switch_height_z, align=(Align.CENTER, Align.MAX, Align.MIN)).moved(Location((sfx_ref_switch_center_x, sfx_ref_rear_y, sfx_ref_switch_bottom_z)))
publish('sfx_switch', sfx_ref_switch, 'PSU switch reference')

sfx_ref_modular_bank_width_x = param('sfx_ref_modular_bank_width_x', 92.0)
sfx_ref_modular_bank_depth_y = param('sfx_ref_modular_bank_depth_y', 5.0)
sfx_ref_modular_bank_height_z = param('sfx_ref_modular_bank_height_z', 42.0)
sfx_ref_modular_bank_bottom_z = param('sfx_ref_modular_bank_bottom_z', 13.0)
sfx_ref_front_y = sfx_ref_rear_y + sfx_ref_depth_y
sfx_ref_modular_bank = Box(sfx_ref_modular_bank_width_x, sfx_ref_modular_bank_depth_y, sfx_ref_modular_bank_height_z, align=(Align.CENTER, Align.MIN, Align.MIN)).moved(Location((0, sfx_ref_front_y, sfx_ref_modular_bank_bottom_z)))
publish('sfx_modular_bank', sfx_ref_modular_bank, 'Modular cable bank')

assert abs(sfx_ref_mount_points[1][0] - sfx_ref_mount_points[0][0] - sfx_ref_mount_spacing_x) < 0.001
assert abs(sfx_ref_mount_points[2][1] - sfx_ref_mount_points[0][1] - sfx_ref_mount_spacing_z) < 0.001
assert abs(sfx_ref_rear_y - (-128.0 + 2.0 + sfx_ref_rear_clearance_y)) < 0.001
print('SFX_REFERENCE_PASS: planar rear face, 125x100x63.5 mm body, 113x51.5 mm four-hole pattern; exposed proxy rings removed.')