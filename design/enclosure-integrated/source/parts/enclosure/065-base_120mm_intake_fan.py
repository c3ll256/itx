import math
# One 120 mm intake fan in the base, set toward the front in the floor area
# freed by the deleted lower-front motherboard post. Replace the former full
# circle with a built-in stadium-slot grille: the openings have fully rounded
# ends, continuous ribs protect the fan, and the base stays one printable solid.
# The 120 mm frame, 105 mm hole square and 25 mm depth are fan-standard values.
FAN120_FRAME_MM = 120.0
FAN120_HOLE_SQUARE_MM = 105.0
FAN120_FRAME_DEPTH_MM = 25.0

fan120_grille_diameter = param('fan120_grille_diameter', 114.0)
fan120_grille_outer_rim = param('fan120_grille_outer_rim', 5.0)
fan120_grille_slot_width = param('fan120_grille_slot_width', 7.0)
fan120_grille_web = param('fan120_grille_web', 3.2)
fan120_screw_hole_diameter = param('fan120_screw_hole_diameter', 4.4)
fan120_center_x = param('fan120_center_x', 0.0)
fan120_center_y = param('fan120_center_y', 58.0)
fan120_min_clearance = param('fan120_min_clearance', 3.0)
fan120_expected_count = param('fan120_expected_count', 1)

def fan120_solid_volume(shape):
    if shape is None:
        return 0.0
    return sum(s.volume for s in shape.solids())

fan120_cut_depth = base_t + foot_height + 2 * fan120_min_clearance
fan120_hole_offset = FAN120_HOLE_SQUARE_MM / 2.0
fan120_slot_pitch = fan120_grille_slot_width + fan120_grille_web
fan120_open_radius = fan120_grille_diameter / 2.0 - fan120_grille_outer_rim
fan120_slot_half_span_limit = fan120_open_radius - fan120_grille_slot_width / 2.0

assert fan120_grille_web >= 2.5
assert fan120_grille_outer_rim >= 4.0
assert fan120_slot_half_span_limit > 0.0

# Symmetric horizontal rows in the base plane. SlotOverall creates semicircular
# ends directly, and the chord-derived length preserves a circular outer rim.
fan120_row_offset = 0.0
fan120_row_offsets = [0.0]
while fan120_row_offset + fan120_slot_pitch <= fan120_slot_half_span_limit + 0.001:
    fan120_row_offset += fan120_slot_pitch
    fan120_row_offsets.extend((-fan120_row_offset, fan120_row_offset))
fan120_row_offsets = sorted(fan120_row_offsets)

fan120_slot_count = 0
fan120_open_area = 0.0
fan120_slot_centers = []
for row_y in fan120_row_offsets:
    chord_half = math.sqrt(max(0.0, fan120_open_radius ** 2 - row_y ** 2))
    slot_length = 2.0 * chord_half
    if slot_length < fan120_grille_slot_width + 0.5:
        continue
    slot_profile = SlotOverall(slot_length, fan120_grille_slot_width)
    slot_cutter = extrude(slot_profile, fan120_cut_depth / 2.0, both=True)
    slot_cutter = slot_cutter.moved(Location((fan120_center_x, fan120_center_y + row_y, base_t / 2.0)))
    base = (base - slot_cutter).clean()
    fan120_slot_count += 1
    fan120_slot_centers.append((fan120_center_x, fan120_center_y + row_y, slot_length))
    fan120_open_area += (
        (slot_length - fan120_grille_slot_width) * fan120_grille_slot_width
        + math.pi * (fan120_grille_slot_width / 2.0) ** 2
    )

for fan120_sx in (-1, 1):
    for fan120_sy in (-1, 1):
        fan120_screw_hole = Cylinder(
            fan120_screw_hole_diameter / 2.0, fan120_cut_depth,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((
            fan120_center_x + fan120_sx * fan120_hole_offset,
            fan120_center_y + fan120_sy * fan120_hole_offset,
            base_t / 2.0,
        )))
        base = (base - fan120_screw_hole).clean()

# The fan body stands on the inside floor and must clear every internal solid.
fan120_body = Box(
    FAN120_FRAME_MM, FAN120_FRAME_MM, FAN120_FRAME_DEPTH_MM,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((fan120_center_x, fan120_center_y, base_t)))
fan120_bb = fan120_body.bounding_box()

fan120_psu_proxy = Box(
    sfx_psu_width, sfx_psu_depth, sfx_psu_height,
    align=(Align.CENTER, Align.MIN, Align.MIN),
).moved(Location((0.0, -D / 2 + panel_t + 0.8, base_t)))
fan120_obstacles = {
    'sfx psu envelope': fan120_psu_proxy,
    'gpu cradle': front_gpu_cradle,
    'gpu envelope': front_gpu_reference_proxy,
    'front panel features': front_panel,
    'rear panel features': rear_panel,
    'lower 80 mm fan frame': fan80_bodies[0],
}
for fan120_obstacle_name, fan120_obstacle in fan120_obstacles.items():
    assert fan120_solid_volume(fan120_body & fan120_obstacle) < 0.01, fan120_obstacle_name

# Frame inside the case floor, and the fixings around it must stay in material.
assert fan120_bb.min.X >= -W / 2 + panel_t + fan120_min_clearance
assert fan120_bb.max.X <= W / 2 - panel_t - fan120_min_clearance
assert fan120_bb.max.Y <= D / 2 - panel_t - fan120_min_clearance
assert fan120_bb.min.Y >= fan120_psu_proxy.bounding_box().max.Y + fan120_min_clearance

# Probe every rounded slot to prove it is a true through opening.
for slot_x, slot_y, slot_length in fan120_slot_centers:
    slot_probe = Box(
        max(1.0, slot_length - fan120_grille_slot_width),
        fan120_grille_slot_width * 0.5,
        base_t,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((slot_x, slot_y, 0.0)))
    assert fan120_solid_volume(base & slot_probe) < 0.5

fan120_nominal_circle_area = math.pi * (fan120_grille_diameter / 2.0) ** 2
fan120_open_ratio = fan120_open_area / fan120_nominal_circle_area
fan120_connection_inventory = {
    'fan-to-base': 'free: M4 fan screw threads into the purchased fan frame through a base clearance hole',
}
assert int(fan120_expected_count) == 1
assert fan120_slot_count >= 9
assert fan120_open_ratio >= 0.40
assert base.solids().__len__() == 1
assert all(fan120_connection_inventory.values())
publish('base', base, 'Base rounded fan grille')
print(
    f'BASE_120MM_GRILLE_PASS: one {FAN120_FRAME_MM:.0f} mm intake at '
    f'x={fan120_center_x:.1f}, y={fan120_center_y:.1f}; {fan120_slot_count} rounded slots, '
    f'width={fan120_grille_slot_width:.1f} mm, web={fan120_grille_web:.1f} mm, '
    f'rim={fan120_grille_outer_rim:.1f} mm, open ratio={fan120_open_ratio:.1%}; '
    f'{fan120_bb.min.Y - fan120_psu_proxy.bounding_box().max.Y:.1f} mm clear of the PSU.'
)
