# Generic dimensional reference for a standard 120 mm PC case fan.
# No exact commercial model was specified and no exact STEP candidate was found,
# so this object represents the standard frame and mounting interface only.
FAN120_FRAME_STANDARD_MM = 120.0
FAN120_HOLE_PITCH_STANDARD_MM = 105.0

fan_ref_thickness = param('base_fan_ref_thickness', 25.0)
fan_ref_corner_radius = param('base_fan_ref_corner_radius', 6.0)
fan_ref_opening_diameter = param('base_fan_ref_opening_diameter', 110.0)
fan_ref_mount_hole_diameter = param('base_fan_ref_mount_hole_diameter', 4.4)
fan_ref_hub_diameter = param('base_fan_ref_hub_diameter', 42.0)
fan_ref_hub_thickness = param('base_fan_ref_hub_thickness', 8.0)
fan_ref_blade_count = param('base_fan_ref_blade_count', 7)
fan_ref_blade_width = param('base_fan_ref_blade_width', 13.0)
fan_ref_blade_thickness = param('base_fan_ref_blade_thickness', 2.0)
fan_ref_strut_width = param('base_fan_ref_strut_width', 5.0)
fan_ref_strut_thickness = param('base_fan_ref_strut_thickness', 2.5)

assert 2.0 <= fan_ref_corner_radius <= 12.0
assert 100.0 <= fan_ref_opening_diameter < FAN120_FRAME_STANDARD_MM
assert 35.0 <= fan_ref_hub_diameter < fan_ref_opening_diameter
assert int(fan_ref_blade_count) >= 5

corner_offset = FAN120_FRAME_STANDARD_MM / 2.0 - fan_ref_corner_radius
frame_outer = Box(
    FAN120_FRAME_STANDARD_MM - 2 * fan_ref_corner_radius,
    FAN120_FRAME_STANDARD_MM,
    fan_ref_thickness,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
frame_outer = frame_outer + Box(
    FAN120_FRAME_STANDARD_MM,
    FAN120_FRAME_STANDARD_MM - 2 * fan_ref_corner_radius,
    fan_ref_thickness,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
for sx in (-1, 1):
    for sy in (-1, 1):
        frame_outer = frame_outer + Cylinder(
            fan_ref_corner_radius,
            fan_ref_thickness,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((sx * corner_offset, sy * corner_offset, 0.0)))

fan_frame = frame_outer - Cylinder(
    fan_ref_opening_diameter / 2.0,
    fan_ref_thickness,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
mount_offset = FAN120_HOLE_PITCH_STANDARD_MM / 2.0
for sx in (-1, 1):
    for sy in (-1, 1):
        fan_frame = fan_frame - Cylinder(
            fan_ref_mount_hole_diameter / 2.0,
            fan_ref_thickness,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((sx * mount_offset, sy * mount_offset, 0.0)))
fan_frame = fan_frame.clean()

rotor_z = fan_ref_thickness / 2.0
fan_hub = Cylinder(
    fan_ref_hub_diameter / 2.0,
    fan_ref_hub_thickness,
    align=(Align.CENTER, Align.CENTER, Align.CENTER),
).moved(Location((0.0, 0.0, rotor_z)))

blade_inner_r = fan_ref_hub_diameter / 2.0 - 1.0
blade_outer_r = fan_ref_opening_diameter / 2.0 - 3.0
blade_length = blade_outer_r - blade_inner_r
blade_center_r = (blade_inner_r + blade_outer_r) / 2.0
fan_blades = []
for i in range(int(fan_ref_blade_count)):
    blade_angle = i * 360.0 / int(fan_ref_blade_count)
    blade = Box(
        blade_length,
        fan_ref_blade_width,
        fan_ref_blade_thickness,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location((blade_center_r, 0.0, rotor_z))).rotate(Axis.Z, blade_angle)
    fan_blades.append(blade)

strut_length = blade_outer_r - fan_ref_hub_diameter / 2.0
strut_center_r = fan_ref_hub_diameter / 2.0 + strut_length / 2.0
fan_struts = []
for strut_angle in (45.0, 135.0, 225.0, 315.0):
    strut = Box(
        strut_length,
        fan_ref_strut_width,
        fan_ref_strut_thickness,
        align=(Align.CENTER, Align.CENTER, Align.MAX),
    ).moved(Location((strut_center_r, 0.0, fan_ref_thickness))).rotate(Axis.Z, strut_angle)
    fan_struts.append(strut)

fan_reference = Compound(children=[fan_frame, fan_hub] + fan_blades + fan_struts)
fan_ref_bb = fan_reference.bounding_box()
assert abs((fan_ref_bb.max.X - fan_ref_bb.min.X) - FAN120_FRAME_STANDARD_MM) < 0.01
assert abs((fan_ref_bb.max.Y - fan_ref_bb.min.Y) - FAN120_FRAME_STANDARD_MM) < 0.01
assert abs((fan_ref_bb.max.Z - fan_ref_bb.min.Z) - fan_ref_thickness) < 0.01
publish('base_fan120_reference', fan_reference, '120 mm fan reference')
print(
    f'BASE_FAN_REFERENCE_READY: generic {FAN120_FRAME_STANDARD_MM:.0f} x '
    f'{FAN120_FRAME_STANDARD_MM:.0f} x {fan_ref_thickness:.0f} mm fan, '
    f'{FAN120_HOLE_PITCH_STANDARD_MM:.0f} mm mounting square; dimensional proxy only.'
)