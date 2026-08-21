# Add 2 mm internal reinforcement to the existing 3 mm skins. The final fan
# slots and screw holes already exist, so shifted skin copies inherit them.
# Purchased fan and PSU envelopes remain on their original 3 mm mounting lands.
front_inner_layer_thickness = param('front_inner_layer_thickness', 2.0)
front_inner_layer_inset = param('front_inner_layer_inset', 5.0)
front_fan_keepout_size = param('front_fan_keepout_size', 82.0)
base_inner_layer_thickness = param('base_inner_layer_thickness', 2.0)
base_inner_layer_inset = param('base_inner_layer_inset', 5.0)
base_fan_keepout_size = param('base_fan_keepout_size', 122.0)
base_psu_keepout_width = param('base_psu_keepout_width', 127.0)
base_psu_keepout_depth = param('base_psu_keepout_depth', 102.0)
rear_rib_depth = param('rear_rib_depth', 2.0)
rear_vertical_rib_width = param('rear_vertical_rib_width', 8.0)
rear_vertical_rib_x = param('rear_vertical_rib_x', -5.0)
rear_vertical_rib_z_min = param('rear_vertical_rib_z_min', 74.0)
rear_vertical_rib_z_max = param('rear_vertical_rib_z_max', 241.0)
rear_horizontal_rib_width = param('rear_horizontal_rib_width', 120.0)
rear_horizontal_rib_height = param('rear_horizontal_rib_height', 8.0)
rear_horizontal_rib_z = param('rear_horizontal_rib_z', 76.0)
reinforcement_overlap = param('reinforcement_overlap', 1.0)

assert front_inner_layer_thickness == 2.0
assert base_inner_layer_thickness == 2.0
assert rear_rib_depth == 2.0
assert reinforcement_overlap == 1.0

# Front layer: isolate the flat 3 mm skin, shift it inward 2 mm (leaving 1 mm
# overlap), inset its perimeter, and leave both fan frames on the 3 mm surface.
front_skin_slab = Box(W + 2.0, 3.4, H, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0.0, D / 2 - 1.5, 0.0)))
front_skin = (front_panel & front_skin_slab).clean()
front_layer_shift = front_inner_layer_thickness
front_inner_layer = front_skin.moved(Location((0.0, -front_layer_shift, 0.0)))
front_inner_layer = front_inner_layer & Box(
    W - 2 * front_inner_layer_inset, 8.0,
    H - base_t - cap_t - 2 * front_inner_layer_inset,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((0.0, D / 2 - 3.5, base_t + front_inner_layer_inset)))
for front_fan_z in (fan80_lower_center_z, fan80_upper_center_z):
    front_fan_keepout = Box(
        front_fan_keepout_size, 9.0, front_fan_keepout_size,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location((fan80_center_x, D / 2 - 3.5, front_fan_z)))
    front_inner_layer = (front_inner_layer - front_fan_keepout).clean()
front_layer_volume = sum(s.volume for s in front_inner_layer.solids())
front_panel = (front_panel + front_inner_layer).clean()

# Base layer: strengthen the open floor fields while preserving the original
# fan mounting plane and the SFX support plane.
base_skin_slab = Box(W + 2.0, D + 2.0, base_t + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0.0, 0.0, -0.2)))
base_skin = (base & base_skin_slab).clean()
base_layer_shift = base_inner_layer_thickness
base_inner_layer = base_skin.moved(Location((0.0, 0.0, base_layer_shift)))
base_inner_layer = base_inner_layer & Box(
    W - 2 * base_inner_layer_inset, D - 2 * base_inner_layer_inset,
    base_t + base_inner_layer_thickness + 1.0,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((0.0, 0.0, 0.0)))
base_psu_keepout = Box(
    base_psu_keepout_width, base_psu_keepout_depth, 8.0,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((0.0, -D / 2 + panel_t + 0.8 + base_psu_keepout_depth / 2, 0.0)))
base_fan_keepout = Box(
    base_fan_keepout_size, base_fan_keepout_size, 8.0,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((fan120_center_x, fan120_center_y, 0.0)))
base_inner_layer = (base_inner_layer - base_psu_keepout - base_fan_keepout).clean()
base_layer_volume = sum(s.volume for s in base_inner_layer.solids())
base = (base + base_inner_layer).clean()

# Rear T-rib: the cross beam sits above the SFX envelope and the vertical leg
# runs through the solid central corridor between GPU and motherboard I/O.
rear_skin_slab = Box(W + 2.0, 3.4, H, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0.0, -D / 2 + 1.5, 0.0)))
rear_skin = (rear_panel & rear_skin_slab).clean()
rear_rib_shift = rear_rib_depth
rear_rib_source = rear_skin.moved(Location((0.0, rear_rib_shift, 0.0)))
rear_vertical_pattern = Box(
    rear_vertical_rib_width, 8.0,
    rear_vertical_rib_z_max - rear_vertical_rib_z_min,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((rear_vertical_rib_x, -D / 2 + 3.5, rear_vertical_rib_z_min)))
rear_horizontal_pattern = Box(
    rear_horizontal_rib_width, 8.0, rear_horizontal_rib_height,
    align=(Align.CENTER, Align.CENTER, Align.CENTER),
).moved(Location((0.0, -D / 2 + 3.5, rear_horizontal_rib_z)))
rear_ribs = (rear_rib_source & (rear_vertical_pattern + rear_horizontal_pattern)).clean()
rear_rib_volume = sum(s.volume for s in rear_ribs.solids())
rear_panel = (rear_panel + rear_ribs).clean()

# Verify local 5 mm thickness away from openings and keepouts.
front_thickness_probe = front_panel & Box(4.0, 9.0, 4.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)).moved(Location((-50.0, D / 2 - 2.5, 220.0)))
base_thickness_probe = base & Box(4.0, 4.0, 9.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)).moved(Location((68.0, 0.0, 2.5)))
rear_thickness_probe = rear_panel & Box(4.0, 9.0, 4.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)).moved(Location((rear_vertical_rib_x, -D / 2 + 2.5, 150.0)))
assert front_layer_volume > 1000.0
assert base_layer_volume > 1000.0
assert rear_rib_volume > 500.0
assert abs(front_thickness_probe.bounding_box().size.Y - 5.0) < 0.01
assert abs(base_thickness_probe.bounding_box().size.Z - 5.0) < 0.01
assert abs(rear_thickness_probe.bounding_box().size.Y - 5.0) < 0.01
assert front_panel.solids().__len__() == 1
assert rear_panel.solids().__len__() == 1
assert base.solids().__len__() == 1

publish('front_panel', front_panel, '5 mm layered front')
publish('rear_panel', rear_panel, '5 mm ribbed rear')
publish('base', base, '5 mm layered base')
print(
    'PANEL_5MM_REINFORCEMENT_PASS: front/base internal layers and rear T-rib; '
    f'local thicknesses={front_thickness_probe.bounding_box().size.Y:.1f}/'
    f'{base_thickness_probe.bounding_box().size.Z:.1f}/'
    f'{rear_thickness_probe.bounding_box().size.Y:.1f} mm.'
)