# Bring the panel skins to a 5 mm structural target. Front and base retain
# their hardware keepouts. The complete rear skin grows outward so the SFX
# insertion and mounting plane remain unchanged.
front_inner_layer_thickness = param('front_inner_layer_thickness', 2.0)
front_inner_layer_inset = param('front_inner_layer_inset', 5.0)
front_fan_keepout_size = param('front_fan_keepout_size', 82.0)
base_inner_layer_thickness = param('base_inner_layer_thickness', 2.0)
base_inner_layer_inset = param('base_inner_layer_inset', 5.0)
base_fan_keepout_size = param('base_fan_keepout_size', 122.0)
base_psu_keepout_width = param('base_psu_keepout_width', 127.0)
base_psu_keepout_depth = param('base_psu_keepout_depth', 102.0)
rear_target_thickness = param('rear_target_thickness', 5.0)
rear_lamination_overlap_min = param('rear_lamination_overlap_min', 0.5)

assert front_inner_layer_thickness == 2.0
assert base_inner_layer_thickness == 2.0
assert rear_target_thickness == 5.0

front_skin_slab = Box(W + 2.0, 3.4, H, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0.0, D / 2 - 1.5, 0.0)))
front_skin = (front_panel & front_skin_slab).clean()
front_inner_layer = front_skin.moved(Location((0.0, -front_inner_layer_thickness, 0.0)))
front_inner_layer = front_inner_layer & Box(W - 2 * front_inner_layer_inset, 8.0, H - base_t - cap_t - 2 * front_inner_layer_inset, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0.0, D / 2 - 3.5, base_t + front_inner_layer_inset)))
for front_fan_z in (fan80_lower_center_z, fan80_upper_center_z):
    keepout = Box(front_fan_keepout_size, 9.0, front_fan_keepout_size, align=(Align.CENTER, Align.CENTER, Align.CENTER)).moved(Location((fan80_center_x, D / 2 - 3.5, front_fan_z)))
    front_inner_layer = (front_inner_layer - keepout).clean()
front_layer_volume = sum(s.volume for s in front_inner_layer.solids())
front_panel = (front_panel + front_inner_layer).clean()

base_skin_slab = Box(W + 2.0, D + 2.0, base_t + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0.0, 0.0, -0.2)))
base_skin = (base & base_skin_slab).clean()
base_inner_layer = base_skin.moved(Location((0.0, 0.0, base_inner_layer_thickness)))
base_inner_layer = base_inner_layer & Box(W - 2 * base_inner_layer_inset, D - 2 * base_inner_layer_inset, base_t + base_inner_layer_thickness + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0.0, 0.0, 0.0)))
base_psu_keepout = Box(base_psu_keepout_width, base_psu_keepout_depth, 8.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0.0, -D / 2 + panel_t + 0.8 + base_psu_keepout_depth / 2, 0.0)))
base_fan_keepout = Box(base_fan_keepout_size, base_fan_keepout_size, 8.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((fan120_center_x, fan120_center_y, 0.0)))
base_inner_layer = (base_inner_layer - base_psu_keepout - base_fan_keepout).clean()
base_layer_volume = sum(s.volume for s in base_inner_layer.solids())
base = (base + base_inner_layer).clean()

# Extract the complete final rear skin, including every existing opening.
rear_skin_slab = Box(W + 2.0, 3.4, H, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0.0, -D / 2 + 1.5, 0.0)))
rear_skin = (rear_panel & rear_skin_slab).clean()
rear_source_probe = rear_skin & Box(4.0, 6.0, 4.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)).moved(Location((-5.0, -D / 2 + 1.0, 150.0)))
rear_source_thickness = rear_source_probe.bounding_box().size.Y
rear_required_extension = rear_target_thickness - rear_source_thickness
rear_half_shift = rear_required_extension / 2.0
assert rear_source_thickness > rear_lamination_overlap_min
assert rear_required_extension > 0.0
assert rear_half_shift < rear_source_thickness - rear_lamination_overlap_min

# Two overlapping copies span the calculated extension. This avoids a gap even
# when earlier face cleanup made the nominal 3 mm source skin locally 2.2 mm.
rear_layer_mid = rear_skin.moved(Location((0.0, -rear_half_shift, 0.0)))
rear_layer_outer = rear_skin.moved(Location((0.0, -rear_required_extension, 0.0)))
rear_full_layer = (rear_layer_mid + rear_layer_outer).clean()
rear_layer_volume = sum(s.volume for s in rear_full_layer.solids())
rear_panel = (rear_panel + rear_full_layer).clean()

front_probe = front_panel & Box(4.0, 9.0, 4.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)).moved(Location((-50.0, D / 2 - 2.5, 220.0)))
base_probe = base & Box(4.0, 4.0, 9.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)).moved(Location((68.0, 0.0, 2.5)))
rear_final_probe_y = -D / 2 + panel_t - rear_target_thickness / 2.0
rear_probe = rear_panel & Box(4.0, 7.0, 4.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)).moved(Location((-5.0, rear_final_probe_y, 150.0)))
front_probe_y = front_probe.bounding_box().size.Y
base_probe_z = base_probe.bounding_box().size.Z
rear_probe_y = rear_probe.bounding_box().size.Y
assert front_layer_volume > 1000.0
assert base_layer_volume > 1000.0
assert rear_layer_volume > 10000.0
assert abs(front_probe_y - 5.0) < 0.01, f'front thickness={front_probe_y:.3f}'
assert abs(base_probe_z - 5.0) < 0.01, f'base thickness={base_probe_z:.3f}'
assert abs(rear_probe_y - rear_target_thickness) < 0.01, f'rear thickness={rear_probe_y:.3f}'
assert front_panel.solids().__len__() == 1
assert rear_panel.solids().__len__() == 1
assert base.solids().__len__() == 1

publish('front_panel', front_panel, '5 mm layered front')
publish('rear_panel', rear_panel, 'Full 5 mm rear')
publish('base', base, '5 mm layered base')
print(f'PANEL_5MM_REINFORCEMENT_PASS: front/base/rear={front_probe_y:.1f}/{base_probe_z:.1f}/{rear_probe_y:.1f} mm; rear source={rear_source_thickness:.1f} mm, outward extension={rear_required_extension:.1f} mm.')