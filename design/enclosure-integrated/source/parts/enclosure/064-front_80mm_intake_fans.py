import math
# Two 80 mm intake positions on the board side of the front panel. Replace the
# former full circular apertures with parallel stadium-slot grilles: every air
# opening has fully rounded ends, while continuous printable ribs protect the
# fan blades and stiffen the panel. The 80 mm frame, 71.5 mm hole square and
# 25 mm frame depth are purchased-fan standard dimensions.
FAN80_FRAME_MM = 80.0
FAN80_HOLE_SQUARE_MM = 71.5
FAN80_FRAME_DEPTH_MM = 25.0

fan80_grille_diameter = param('fan80_grille_diameter', 76.0)
fan80_grille_outer_rim = param('fan80_grille_outer_rim', 4.0)
fan80_grille_slot_width = param('fan80_grille_slot_width', 6.0)
fan80_grille_web = param('fan80_grille_web', 3.0)
fan80_screw_hole_diameter = param('fan80_screw_hole_diameter', 4.4)
fan80_center_x = param('fan80_center_x', 23.0)
fan80_lower_center_z = param('fan80_lower_center_z', 76.0)
fan80_upper_center_z = param('fan80_upper_center_z', 161.0)
fan80_min_clearance = param('fan80_min_clearance', 3.0)
fan80_expected_count = param('fan80_expected_count', 2)

def fan_solid_volume(shape):
    if shape is None:
        return 0.0
    return sum(s.volume for s in shape.solids())

front_inner_y = D / 2.0 - panel_t
fan80_cut_depth = panel_t + 2 * fan80_min_clearance
fan80_centers_z = (fan80_lower_center_z, fan80_upper_center_z)
fan80_hole_offset = FAN80_HOLE_SQUARE_MM / 2.0
fan80_slot_pitch = fan80_grille_slot_width + fan80_grille_web
fan80_open_radius = fan80_grille_diameter / 2.0 - fan80_grille_outer_rim
fan80_slot_half_span_limit = fan80_open_radius - fan80_grille_slot_width / 2.0

assert fan80_grille_web >= 2.5
assert fan80_grille_outer_rim >= 3.0
assert fan80_slot_half_span_limit > 0.0

# Every solid already standing in the front cavity, measured before the cuts.
fan80_panel_before = front_panel
fan80_board_proxy = Box(
    mitx_board_height, mitx_board_width, mitx_board_height,
    align=(Align.MIN, Align.MIN, Align.MIN),
).moved(Location((board_plane_x, mitx_board_rear_edge_y, mitx_board_z_min)))
fan80_obstacles = {
    'front-panel interior features': fan80_panel_before,
    'gpu cradle': front_gpu_cradle,
    'gpu envelope': front_gpu_reference_proxy,
    'motherboard envelope': fan80_board_proxy,
}

fan80_bodies = []
fan80_slot_count_total = 0
fan80_open_area_total = 0.0
fan80_slot_centers = []
for fan80_z in fan80_centers_z:
    # Symmetric horizontal rows. Slot length follows the circular fan field,
    # leaving a constant outer rim; SlotOverall supplies semicircular ends.
    row_offset = 0.0
    row_offsets = [0.0]
    while row_offset + fan80_slot_pitch <= fan80_slot_half_span_limit + 0.001:
        row_offset += fan80_slot_pitch
        row_offsets.extend((-row_offset, row_offset))
    row_offsets = sorted(row_offsets)
    for row_z in row_offsets:
        chord_half = math.sqrt(max(0.0, fan80_open_radius ** 2 - row_z ** 2))
        slot_length = 2.0 * chord_half
        if slot_length < fan80_grille_slot_width + 0.5:
            continue
        slot_profile = SlotOverall(slot_length, fan80_grille_slot_width)
        slot_cutter = extrude(slot_profile, fan80_cut_depth / 2.0, both=True).rotate(Axis.X, 90)
        slot_cutter = slot_cutter.moved(Location((fan80_center_x, front_inner_y, fan80_z + row_z)))
        front_panel = (front_panel - slot_cutter).clean()
        fan80_slot_count_total += 1
        fan80_slot_centers.append((fan80_center_x, fan80_z + row_z, slot_length))
        fan80_open_area_total += (
            (slot_length - fan80_grille_slot_width) * fan80_grille_slot_width
            + math.pi * (fan80_grille_slot_width / 2.0) ** 2
        )
    for fan80_sx in (-1, 1):
        for fan80_sz in (-1, 1):
            screw_hole = Cylinder(
                fan80_screw_hole_diameter / 2.0, fan80_cut_depth,
                align=(Align.CENTER, Align.CENTER, Align.CENTER),
            ).rotate(Axis.X, 90).moved(Location((
                fan80_center_x + fan80_sx * fan80_hole_offset,
                front_inner_y,
                fan80_z + fan80_sz * fan80_hole_offset,
            )))
            front_panel = (front_panel - screw_hole).clean()
    fan80_bodies.append(Box(
        FAN80_FRAME_MM, FAN80_FRAME_DEPTH_MM, FAN80_FRAME_MM,
        align=(Align.CENTER, Align.MAX, Align.CENTER),
    ).moved(Location((fan80_center_x, front_inner_y, fan80_z))))

# The screws thread into each purchased fan's own frame, so the printed panel
# carries clearance holes only and this connection is deliberately free.
fan80_connection_inventory = {
    'fan-to-front-panel': 'free: M4 fan screw threads into the purchased fan frame through a panel clearance hole',
}

for fan80_body in fan80_bodies:
    fan80_bb = fan80_body.bounding_box()
    assert fan80_bb.min.X >= -W / 2 + panel_t + fan80_min_clearance
    assert fan80_bb.max.X <= W / 2 - panel_t - fan80_min_clearance
    assert fan80_bb.min.Z >= base_t + fan80_min_clearance
    assert fan80_bb.max.Z <= H - cap_t - cap_inner_t - fan80_min_clearance
    for fan80_obstacle_name, fan80_obstacle in fan80_obstacles.items():
        assert fan_solid_volume(fan80_body & fan80_obstacle) < 0.01, fan80_obstacle_name

# Probe the centre of every stadium slot to prove it passes through the panel.
for slot_x, slot_z, slot_length in fan80_slot_centers:
    slot_probe = Box(
        max(1.0, slot_length - fan80_grille_slot_width),
        panel_t,
        fan80_grille_slot_width * 0.5,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location((slot_x, front_inner_y + panel_t / 2.0, slot_z)))
    assert fan_solid_volume(front_panel & slot_probe) < 0.5

fan80_gap_z = abs(fan80_upper_center_z - fan80_lower_center_z) - fan80_grille_diameter
fan80_nominal_circle_area = len(fan80_centers_z) * math.pi * (fan80_grille_diameter / 2.0) ** 2
fan80_open_ratio = fan80_open_area_total / fan80_nominal_circle_area
assert len(fan80_bodies) == int(fan80_expected_count)
assert fan80_slot_count_total >= 14
assert fan80_open_ratio >= 0.35
assert fan80_gap_z >= 5.0
assert front_panel.solids().__len__() == 1
assert all(fan80_connection_inventory.values())
publish('front_panel', front_panel, 'Front rounded fan grilles')
print(
    f'FRONT_80MM_GRILLES_PASS: two {FAN80_FRAME_MM:.0f} mm fan positions at '
    f'x={fan80_center_x:.1f}, z={fan80_lower_center_z:.0f}/{fan80_upper_center_z:.0f}; '
    f'{fan80_slot_count_total} rounded slots total, width={fan80_grille_slot_width:.1f} mm, '
    f'web={fan80_grille_web:.1f} mm, rim={fan80_grille_outer_rim:.1f} mm, '
    f'open ratio={fan80_open_ratio:.1%}.'
)
