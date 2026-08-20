# One 120 mm intake fan in the base, set toward the front in the floor area
# freed by the deleted lower-front motherboard post. The 120 x 120 mm frame,
# the 105 mm hole square and the 25 mm frame depth are fan-standard dimensions.
FAN120_FRAME_MM = 120.0
FAN120_HOLE_SQUARE_MM = 105.0
FAN120_FRAME_DEPTH_MM = 25.0

fan120_aperture_diameter = param('fan120_aperture_diameter', 114.0)
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

fan120_aperture = Cylinder(
    fan120_aperture_diameter / 2.0, fan120_cut_depth,
    align=(Align.CENTER, Align.CENTER, Align.CENTER),
).moved(Location((fan120_center_x, fan120_center_y, base_t / 2.0)))
base = (base - fan120_aperture).clean()
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

# The aperture must be a genuine through hole in the finished base.
fan120_probe = Cylinder(
    fan120_aperture_diameter * 0.4, base_t,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((fan120_center_x, fan120_center_y, 0.0)))
assert fan120_solid_volume(base & fan120_probe) < 0.5

fan120_connection_inventory = {
    'fan-to-base': 'free: M4 fan screw threads into the purchased fan frame through a base clearance hole',
}
assert int(fan120_expected_count) == 1
assert base.solids().__len__() == 1
assert all(fan120_connection_inventory.values())
publish('base', base, 'Base with 120 mm front intake')
print(
    f'BASE_120MM_FAN_PASS: one {FAN120_FRAME_MM:.0f} mm intake at x={fan120_center_x:.1f}, '
    f'y={fan120_center_y:.1f}; {fan120_aperture_diameter:.0f} mm aperture with a '
    f'{FAN120_HOLE_SQUARE_MM:.0f} mm screw square; {fan120_bb.min.Y - fan120_psu_proxy.bounding_box().max.Y:.1f} mm '
    f'clear of the PSU and {D / 2 - panel_t - fan120_bb.max.Y:.1f} mm behind the front panel.'
)
