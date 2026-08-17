# Remove the non-printable 0.5 mm web below the SFX service opening.
# The opening now terminates at the rear-panel bottom edge; the four PSU mounting
# holes and the two outer corner fixing zones remain unchanged.
rear_sfx_edge_opening_width_x = param('rear_sfx_edge_opening_width_x', psu_cut_w)
rear_sfx_edge_opening_bottom_z = param('rear_sfx_edge_opening_bottom_z', base_t)
rear_sfx_edge_opening_top_z = param('rear_sfx_edge_opening_top_z', psu_cut_z)
rear_sfx_edge_opening_depth_y = param('rear_sfx_edge_opening_depth_y', cut_depth)
rear_sfx_edge_boolean_overcut = param('rear_sfx_edge_boolean_overcut', 0.10)

rear_sfx_edge_web_height = rear_sfx_edge_opening_top_z - rear_sfx_edge_opening_bottom_z
assert rear_sfx_edge_web_height > 0.0
assert rear_sfx_edge_web_height < 1.2

rear_sfx_edge_cutter = Box(
    rear_sfx_edge_opening_width_x + 2 * rear_sfx_edge_boolean_overcut,
    rear_sfx_edge_opening_depth_y,
    rear_sfx_edge_web_height + 2 * rear_sfx_edge_boolean_overcut,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((
    psu_cut_x,
    -D / 2,
    rear_sfx_edge_opening_bottom_z - rear_sfx_edge_boolean_overcut,
)))
rear_panel = (rear_panel - rear_sfx_edge_cutter).clean()

rear_sfx_edge_void_probe = Box(
    rear_sfx_edge_opening_width_x - 2 * rear_sfx_edge_boolean_overcut,
    panel_t,
    rear_sfx_edge_web_height,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((psu_cut_x, rear_y, rear_sfx_edge_opening_bottom_z)))
rear_sfx_edge_residual = rear_panel & rear_sfx_edge_void_probe
rear_sfx_edge_residual_volume = sum(s.volume for s in rear_sfx_edge_residual)

assert rear_sfx_edge_residual_volume < 0.02
assert rear_panel.solids().__len__() == 1
publish('rear_panel', rear_panel, 'Rear with open SFX edge')
print(f'REAR_SFX_EDGE_OPEN_PASS: removed {rear_sfx_edge_web_height:.2f} mm bottom web across {rear_sfx_edge_opening_width_x:.1f} mm; residual={rear_sfx_edge_residual_volume:.4f} mm^3.')