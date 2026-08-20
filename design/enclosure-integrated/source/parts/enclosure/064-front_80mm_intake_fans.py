# Two 80 mm intake fans on the board side of the front panel, in the free
# cavity ahead of the Mini-ITX board. The 80 x 80 mm frame, the 71.5 mm hole
# square and the 25 mm frame depth are fan-standard dimensions, not user choices.
FAN80_FRAME_MM = 80.0
FAN80_HOLE_SQUARE_MM = 71.5
FAN80_FRAME_DEPTH_MM = 25.0

fan80_aperture_diameter = param('fan80_aperture_diameter', 76.0)
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
fan80_aperture_radius = fan80_aperture_diameter / 2.0
fan80_hole_offset = FAN80_HOLE_SQUARE_MM / 2.0

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
for fan80_z in fan80_centers_z:
    aperture = Cylinder(
        fan80_aperture_radius, fan80_cut_depth,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.X, 90).moved(Location((fan80_center_x, front_inner_y, fan80_z)))
    front_panel = (front_panel - aperture).clean()
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
    # Each aperture must be a genuine through hole in the finished panel.
    fan80_probe = Box(
        fan80_aperture_diameter * 0.5, panel_t, fan80_aperture_diameter * 0.5,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location((fan80_center_x, front_inner_y + panel_t / 2, fan80_bb.center().Z)))
    assert fan_solid_volume(front_panel & fan80_probe) < 0.5

fan80_gap_z = abs(fan80_upper_center_z - fan80_lower_center_z) - fan80_aperture_diameter
assert len(fan80_bodies) == int(fan80_expected_count)
assert fan80_gap_z >= 5.0
assert front_panel.solids().__len__() == 1
assert all(fan80_connection_inventory.values())
publish('front_panel', front_panel, 'Front with dual 80 mm intakes')
print(
    f'FRONT_80MM_FANS_PASS: two {FAN80_FRAME_MM:.0f} mm fan positions on the board side at '
    f'x={fan80_center_x:.1f}, z={fan80_lower_center_z:.0f} and {fan80_upper_center_z:.0f}; '
    f'{fan80_aperture_diameter:.0f} mm apertures with {FAN80_HOLE_SQUARE_MM:.1f} mm screw squares; '
    f'{fan80_gap_z:.1f} mm web between apertures; every frame clears the card, cradle and board.'
)
