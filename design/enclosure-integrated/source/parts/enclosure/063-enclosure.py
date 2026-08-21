# Preserve the printable open lower edge of the SFX service aperture, then
# reinforce the front and rear skins outward. The service cavity, fan seats,
# GPU cradle, SFX insertion path, columns and side interfaces stay fixed.
rear_sfx_edge_opening_width_x = param('rear_sfx_edge_opening_width_x', psu_cut_w)
rear_sfx_edge_opening_bottom_z = param('rear_sfx_edge_opening_bottom_z', base_t)
rear_sfx_edge_opening_top_z = param('rear_sfx_edge_opening_top_z', psu_cut_z)
rear_sfx_edge_opening_depth_y = param('rear_sfx_edge_opening_depth_y', cut_depth)
rear_sfx_edge_boolean_overcut = param('rear_sfx_edge_boolean_overcut', 0.10)
front_panel_outer_reinforcement = param('front_panel_outer_reinforcement', 1.0)
rear_panel_outer_reinforcement = param('rear_panel_outer_reinforcement', 1.0)

rear_sfx_edge_web_height = rear_sfx_edge_opening_top_z - rear_sfx_edge_opening_bottom_z
assert rear_sfx_edge_web_height > 0.0
assert rear_sfx_edge_web_height < 1.2
assert front_panel_outer_reinforcement > 0.0
assert rear_panel_outer_reinforcement > 0.0

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

front_before_bb = front_panel.bounding_box()
rear_before_bb = rear_panel.bounding_box()
front_before_volume = sum(s.volume for s in front_panel.solids())
rear_before_volume = sum(s.volume for s in rear_panel.solids())

front_outer_layer = front_panel.moved(Location((0.0, front_panel_outer_reinforcement, 0.0)))
rear_outer_layer = rear_panel.moved(Location((0.0, -rear_panel_outer_reinforcement, 0.0)))
front_panel = (front_panel + front_outer_layer).clean()
rear_panel = (rear_panel + rear_outer_layer).clean()

front_after_bb = front_panel.bounding_box()
rear_after_bb = rear_panel.bounding_box()
front_after_volume = sum(s.volume for s in front_panel.solids())
rear_after_volume = sum(s.volume for s in rear_panel.solids())

assert front_panel.solids().__len__() == 1
assert rear_panel.solids().__len__() == 1
assert abs(front_after_bb.min.Y - front_before_bb.min.Y) < 0.01
assert abs(front_after_bb.max.Y - (front_before_bb.max.Y + front_panel_outer_reinforcement)) < 0.01
assert abs(rear_after_bb.max.Y - rear_before_bb.max.Y) < 0.01
assert abs(rear_after_bb.min.Y - (rear_before_bb.min.Y - rear_panel_outer_reinforcement)) < 0.01
assert front_after_volume > front_before_volume
assert rear_after_volume > rear_before_volume
assert abs(base_t - cap_t) < 0.01

publish('front_panel', front_panel, '3 mm reinforced front')
publish('rear_panel', rear_panel, '3 mm reinforced rear')
print(
    f'PANEL_REINFORCEMENT_PASS: SFX lower web removed ({rear_sfx_edge_web_height:.2f} mm, '
    f'residual {rear_sfx_edge_residual_volume:.4f} mm^3); front/rear reinforced outward by '
    f'{front_panel_outer_reinforcement:.1f}/{rear_panel_outer_reinforcement:.1f} mm; '
    f'base/top outer skins {base_t:.1f}/{cap_t:.1f} mm.'
)