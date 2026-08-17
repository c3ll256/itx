# Conservative bottom-side M.2_2 reservation for ASUS ROG STRIX Z390-I GAMING.
# The official manual confirms M.2_2 is on the bottom side but does not publish dimensioned coordinates.
# This proxy reserves a central 2280-class SSD/screw region inside the standard board outline.
rog_m2_bottom_depth_x = param('rog_m2_bottom_depth_x', 4.0)
rog_m2_bottom_width_y = param('rog_m2_bottom_width_y', 28.0)
rog_m2_bottom_height_z = param('rog_m2_bottom_height_z', 85.0)
rog_m2_bottom_center_y = param('rog_m2_bottom_center_y', -30.0)
rog_m2_bottom_center_z = param('rog_m2_bottom_center_z', 145.0)
rog_m2_bottom_clearance_to_support_x = param('rog_m2_bottom_clearance_to_support_x', 2.35)
rog_m2_bottom_min_x = mitx_pcb_plane_x - rog_m2_bottom_depth_x
rog_m2_bottom = Box(rog_m2_bottom_depth_x, rog_m2_bottom_width_y, rog_m2_bottom_height_z, align=(Align.MIN, Align.CENTER, Align.CENTER)).moved(Location((rog_m2_bottom_min_x, rog_m2_bottom_center_y, rog_m2_bottom_center_z)))
assert rog_m2_bottom.bounding_box().max.X <= mitx_pcb_plane_x + 0.001
assert rog_m2_bottom.bounding_box().min.X >= mitx_pcb_plane_x - 6.35 + rog_m2_bottom_clearance_to_support_x - 0.001
assert rog_m2_bottom.bounding_box().min.Y >= mitx_pcb_rear_edge_y and rog_m2_bottom.bounding_box().max.Y <= mitx_pcb_rear_edge_y + mitx_pcb_width_y
assert rog_m2_bottom.bounding_box().min.Z >= mitx_pcb_bottom_z and rog_m2_bottom.bounding_box().max.Z <= mitx_pcb_top_z
publish('mitx_m2_bottom', rog_m2_bottom, 'ROG backside M.2 keepout')
print(f'ROG_Z390I_M2_BOTTOM_PASS: conservative {rog_m2_bottom_depth_x:.1f} x {rog_m2_bottom_width_y:.1f} x {rog_m2_bottom_height_z:.1f} mm bottom-side reserve; {rog_m2_bottom_clearance_to_support_x:.2f} mm remains to the 6.35 mm support plane.')