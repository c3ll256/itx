# Final local-interface cleanup after all panel reinforcement has replayed.
# Rebuild only the final adhesive-magnet pockets here so the 5 mm skin
# lamination cannot copy any obsolete carrier cross-sections.
final_magnet_width_y = param('final_glued_magnet_width_y', 5.0)
final_magnet_height_z = param('final_glued_magnet_height_z', 10.0)
final_magnet_depth_x = param('final_glued_magnet_depth_x', 2.0)
final_magnet_install_clearance = param('final_glued_magnet_install_clearance', 0.50)
final_magnet_wall = param('final_glued_magnet_wall', 1.20)
final_magnet_panel_overlap = param('final_glued_magnet_panel_overlap', 0.50)
final_magnet_cleanup_width_x = param('final_glued_magnet_cleanup_width_x', 20.0)
final_magnet_cleanup_depth_y = param('final_glued_magnet_cleanup_depth_y', 22.0)
final_magnet_cleanup_height_z = param('final_glued_magnet_cleanup_height_z', 24.0)
final_magnet_cleanup_skin_inset = param('final_glued_magnet_cleanup_skin_inset', 0.35)
final_strike_thickness_x = param('final_glued_strike_thickness_x', 1.0)
final_strike_depth_clearance = param('final_glued_strike_depth_clearance', 0.15)
final_strike_patch_width_y = param('final_glued_strike_patch_width_y', 20.0)
final_strike_patch_height_z = param('final_glued_strike_patch_height_z', 22.0)

final_magnet_pocket_width = final_magnet_width_y + final_magnet_install_clearance
final_magnet_pocket_height = final_magnet_height_z + final_magnet_install_clearance
final_magnet_pocket_depth = final_magnet_depth_x + final_magnet_install_clearance
final_magnet_carrier_width = final_magnet_pocket_width + 2 * final_magnet_wall
final_magnet_carrier_height = final_magnet_pocket_height + 2 * final_magnet_wall
final_magnet_carrier_depth = final_magnet_pocket_depth + final_magnet_wall

assert final_magnet_install_clearance == 0.50
assert final_magnet_pocket_width == 5.50
assert final_magnet_pocket_height == 10.50
assert final_magnet_pocket_depth == 2.50
assert final_magnet_wall >= 1.20
assert final_magnet_carrier_width <= 7.90 + 0.01
assert final_magnet_carrier_height <= 12.90 + 0.01
assert final_magnet_carrier_depth <= 3.70 + 0.01

# Derive the true inner faces after the late 5 mm panel reinforcement.
front_final_outer_y = front_panel.bounding_box().max.Y
rear_final_outer_y = rear_panel.bounding_box().min.Y
front_final_inner_y = front_final_outer_y - rear_target_thickness
rear_final_inner_y = rear_final_outer_y + rear_target_thickness
final_side_interface_x = W / 2 - panel_t
final_carrier_center_x_abs = final_side_interface_x - final_magnet_carrier_depth / 2
final_pocket_center_x_abs = final_side_interface_x - final_magnet_pocket_depth / 2
final_front_station_y = front_final_inner_y - final_magnet_carrier_width / 2 + final_magnet_panel_overlap
final_rear_station_y = rear_final_inner_y + final_magnet_carrier_width / 2 - final_magnet_panel_overlap

# Remove every legacy carrier, copied lamination strip, and repair flange at the
# eight end-panel stations. The cleanup enters the final skin by 0.35 mm; the
# new carrier overlaps by 0.50 mm, leaving a clean 0.15 mm fused safety overlap.
for sy, station_y in ((1, final_front_station_y), (-1, final_rear_station_y)):
    rebuilt = front_panel if sy > 0 else rear_panel
    inner_y = front_final_inner_y if sy > 0 else rear_final_inner_y
    cleanup_total_depth = final_magnet_cleanup_depth_y + final_magnet_cleanup_skin_inset
    for sx in (-1, 1):
        cleanup_x = sx * (final_side_interface_x - final_magnet_cleanup_width_x / 2)
        for zz in (side_station_z_low, side_station_z_high):
            if sy > 0:
                cleanup = Box(
                    final_magnet_cleanup_width_x,
                    cleanup_total_depth,
                    final_magnet_cleanup_height_z,
                    align=(Align.CENTER, Align.MAX, Align.CENTER),
                ).moved(Location((cleanup_x, inner_y + final_magnet_cleanup_skin_inset, zz)))
            else:
                cleanup = Box(
                    final_magnet_cleanup_width_x,
                    cleanup_total_depth,
                    final_magnet_cleanup_height_z,
                    align=(Align.CENTER, Align.MIN, Align.CENTER),
                ).moved(Location((cleanup_x, inner_y - final_magnet_cleanup_skin_inset, zz)))
            rebuilt = (rebuilt - cleanup).clean()

            carrier_x = sx * final_carrier_center_x_abs
            pocket_x = sx * final_pocket_center_x_abs
            carrier = Box(
                final_magnet_carrier_depth,
                final_magnet_carrier_width,
                final_magnet_carrier_height,
                align=(Align.CENTER, Align.CENTER, Align.CENTER),
            ).moved(Location((carrier_x, station_y, zz)))
            pocket = Box(
                final_magnet_pocket_depth,
                final_magnet_pocket_width,
                final_magnet_pocket_height,
                align=(Align.CENTER, Align.CENTER, Align.CENTER),
            ).moved(Location((pocket_x, station_y, zz)))
            rebuilt = (rebuilt + carrier - pocket).clean()
    if sy > 0:
        front_panel = rebuilt
    else:
        rear_panel = rebuilt

# Close the old strike recess footprint and cut one matching 0.5 mm-clearance
# recess at each new front/rear station. These are simple steel strike pockets;
# the magnets themselves remain on the end panels and are installed with glue.
final_strike_depth = final_strike_thickness_x + final_strike_depth_clearance
for sx, side_shape in ((-1, left_panel), (1, right_panel)):
    revised = side_shape
    side_panel_center_x = sx * (W / 2 - panel_t / 2)
    side_inner_x = sx * final_side_interface_x
    strike_center_x = side_inner_x + sx * final_strike_depth / 2
    for station_y in (final_front_station_y, final_rear_station_y):
        for zz in (side_station_z_low, side_station_z_high):
            patch = Box(
                panel_t,
                final_strike_patch_width_y,
                final_strike_patch_height_z,
                align=(Align.CENTER, Align.CENTER, Align.CENTER),
            ).moved(Location((side_panel_center_x, station_y, zz)))
            strike = Box(
                final_strike_depth,
                final_magnet_pocket_width,
                final_magnet_pocket_height,
                align=(Align.CENTER, Align.CENTER, Align.CENTER),
            ).moved(Location((strike_center_x, station_y, zz)))
            revised = (revised + patch - strike).clean()
    if sx < 0:
        left_panel = revised
    else:
        right_panel = revised

assert all(p.solids().__len__() == 1 for p in (front_panel, rear_panel, left_panel, right_panel))

# Final panel-corner finish. Earlier cells already soften shell edges; complete
# the common R10 outline after the local interface cleanup.
case_panel_corner_radius = param('case_panel_corner_radius', 10.0)
case_corner_arc_tolerance = param('case_corner_arc_tolerance', 0.25)
assert case_panel_corner_radius >= 6.0

def _line_parallel(edge, axis):
    if edge.geom_type != GeomType.LINE:
        return False
    d = edge.position_at(1) - edge.position_at(0)
    if d.length < 1e-6:
        return False
    target = {'x': Vector(1,0,0), 'y': Vector(0,1,0), 'z': Vector(0,0,1)}[axis]
    return abs(d.normalized().dot(target)) > 0.99

def _rounded_envelope(shape, thickness_axis, radius):
    bb = shape.bounding_box()
    env = Box(bb.size.X, bb.size.Y, bb.size.Z, align=(Align.MIN, Align.MIN, Align.MIN)).moved(Location((bb.min.X, bb.min.Y, bb.min.Z)))
    corner_edges = [e for e in env.edges() if _line_parallel(e, thickness_axis)]
    assert len(corner_edges) == 4
    env = fillet(corner_edges, radius)
    result = (shape & env).clean()
    assert result.solids().__len__() == 1
    return result

front_panel = _rounded_envelope(front_panel, 'y', case_panel_corner_radius)
rear_panel = _rounded_envelope(rear_panel, 'y', case_panel_corner_radius)
left_panel = _rounded_envelope(left_panel, 'x', case_panel_corner_radius)
right_panel = _rounded_envelope(right_panel, 'x', case_panel_corner_radius)

def _large_corner_arcs(shape):
    return [e for e in shape.edges() if e.geom_type == GeomType.CIRCLE and abs(e.radius - case_panel_corner_radius) < case_corner_arc_tolerance]

top_corner_arcs_final = _large_corner_arcs(top_cap)
base_corner_arcs_final = _large_corner_arcs(base)
front_corner_arcs_final = _large_corner_arcs(front_panel)
rear_corner_arcs_final = _large_corner_arcs(rear_panel)
left_corner_arcs_final = _large_corner_arcs(left_panel)
right_corner_arcs_final = _large_corner_arcs(right_panel)
assert len(top_corner_arcs_final) >= 4
assert len(base_corner_arcs_final) >= 4
assert len(front_corner_arcs_final) >= 4
assert len(rear_corner_arcs_final) >= 4
assert len(left_corner_arcs_final) >= 4
assert len(right_corner_arcs_final) >= 4
assert all(p.solids().__len__() == 1 for p in (front_panel, rear_panel, left_panel, right_panel, top_cap, base))

publish('front_panel', front_panel, 'Clean glued-magnet front')
publish('rear_panel', rear_panel, 'Clean glued-magnet rear')
publish('left_panel', left_panel, 'Clean left strike pockets')
publish('right_panel', right_panel, 'Clean right strike pockets')
publish('top_cap', top_cap, 'Rounded top panel')
publish('base', base, 'Rounded base panel')
print(f'FINAL_MAGNET_CLEAN_PASS: pockets={final_magnet_pocket_height:.1f}x{final_magnet_pocket_width:.1f}x{final_magnet_pocket_depth:.1f} mm for 10x5x2 magnets; total clearance=0.5 mm; wall={final_magnet_wall:.1f} mm; all copied strips removed.')