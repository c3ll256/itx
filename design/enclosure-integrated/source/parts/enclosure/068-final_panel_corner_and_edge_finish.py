# Final local-interface cleanup after all panel reinforcement has replayed.
# Rebuild only the final adhesive-magnet pockets here so the 5 mm skin
# lamination cannot copy any obsolete carrier cross-sections.
final_magnet_width_y = param('final_glued_magnet_width_y', 5.0)
final_magnet_height_z = param('final_glued_magnet_height_z', 10.0)
final_magnet_depth_x = param('final_glued_magnet_depth_x', 2.0)
final_magnet_install_clearance = param('final_glued_magnet_install_clearance', 0.50)
final_magnet_depth_clearance = param('final_glued_magnet_depth_clearance', 0.0)
final_magnet_wall = param('final_glued_magnet_wall', 1.20)
final_magnet_panel_overlap = param('final_glued_magnet_panel_overlap', 0.50)
final_magnet_side_inset = param('final_glued_magnet_side_inset', 0.40)
final_magnet_cleanup_width_x = param('final_glued_magnet_cleanup_width_x', 20.0)
final_magnet_cleanup_depth_y = param('final_glued_magnet_cleanup_depth_y', 22.0)
final_magnet_cleanup_height_z = param('final_glued_magnet_cleanup_height_z', 24.0)
final_magnet_cleanup_skin_inset = param('final_glued_magnet_cleanup_skin_inset', 0.0)
final_rear_edge_flap_trim_width_x = param('final_rear_edge_flap_trim_width_x', 0.80)
final_rear_edge_flap_trim_depth_y = param('final_rear_edge_flap_trim_depth_y', 5.40)
final_rear_edge_flap_trim_height_z = param('final_rear_edge_flap_trim_height_z', 256.0)
final_rear_edge_flap_trim_gap_x = param('final_rear_edge_flap_trim_gap_x', 0.001)
final_strike_thickness_x = param('final_glued_strike_thickness_x', 1.0)
final_strike_depth_clearance = param('final_glued_strike_depth_clearance', 0.15)
final_strike_patch_width_y = param('final_glued_strike_patch_width_y', 20.0)
final_strike_patch_height_z = param('final_glued_strike_patch_height_z', 22.0)
final_strike_repair_overlap_x = param('final_glued_strike_repair_overlap_x', 0.20)

# The user's 0.5 mm allowance applies across the 10 x 5 mm plan only.
# Keep the 2 mm depth exact so a magnet bonded against the floor finishes flush
# with the carrier opening instead of sitting 0.5 mm below it.
final_magnet_pocket_width = final_magnet_width_y + final_magnet_install_clearance
final_magnet_pocket_height = final_magnet_height_z + final_magnet_install_clearance
final_magnet_pocket_depth = final_magnet_depth_x + final_magnet_depth_clearance
final_magnet_carrier_width = final_magnet_pocket_width + 2 * final_magnet_wall
final_magnet_carrier_height = final_magnet_pocket_height + 2 * final_magnet_wall
final_magnet_carrier_depth = final_magnet_pocket_depth + final_magnet_wall

assert final_magnet_install_clearance == 0.50
assert final_magnet_depth_clearance == 0.0
assert final_magnet_pocket_width == 5.50
assert final_magnet_pocket_height == 10.50
assert final_magnet_pocket_depth == 2.00
assert final_magnet_wall >= 1.20
assert final_magnet_carrier_width <= 7.90 + 0.01
assert final_magnet_carrier_height <= 12.90 + 0.01
assert final_magnet_carrier_depth <= 3.20 + 0.01
assert final_magnet_cleanup_skin_inset == 0.0
assert final_magnet_side_inset >= end_panel_vertical_chamfer
assert final_rear_edge_flap_trim_width_x > final_magnet_side_inset
assert final_rear_edge_flap_trim_depth_y > rear_target_thickness
assert final_rear_edge_flap_trim_height_z >= H
assert final_rear_edge_flap_trim_gap_x > 0.0
assert final_strike_repair_overlap_x > 0

# Derive the true inner faces after the late 5 mm panel reinforcement.
front_final_outer_y = front_panel.bounding_box().max.Y
rear_final_outer_y = rear_panel.bounding_box().min.Y
front_final_inner_y = front_final_outer_y - rear_target_thickness
rear_final_inner_y = rear_final_outer_y + rear_target_thickness
final_side_interface_x = W / 2 - panel_t
# The end-panel vertical edges are chamfered by 0.35 mm. Recess the complete
# carrier and pocket by 0.40 mm so no carrier edge can project beyond that side.
final_carrier_center_x_abs = final_side_interface_x - final_magnet_side_inset - final_magnet_carrier_depth / 2
final_pocket_center_x_abs = final_side_interface_x - final_magnet_side_inset - final_magnet_pocket_depth / 2
final_front_station_y = front_final_inner_y - final_magnet_carrier_width / 2 + final_magnet_panel_overlap
final_rear_station_y = rear_final_inner_y + final_magnet_carrier_width / 2 - final_magnet_panel_overlap

# Remove legacy carrier material only from the enclosure interior. The cleanup
# starts exactly at the final inner-panel datum and never enters the panel skin,
# so no broad recess or restorative patch is created around the compact carrier.
for sy, station_y in ((1, final_front_station_y), (-1, final_rear_station_y)):
    rebuilt = front_panel if sy > 0 else rear_panel
    inner_y = front_final_inner_y if sy > 0 else rear_final_inner_y
    for sx in (-1, 1):
        cleanup_x = sx * (final_side_interface_x - final_magnet_cleanup_width_x / 2)
        for zz in (side_station_z_low, side_station_z_high):
            if sy > 0:
                cleanup = Box(
                    final_magnet_cleanup_width_x,
                    final_magnet_cleanup_depth_y,
                    final_magnet_cleanup_height_z,
                    align=(Align.CENTER, Align.MAX, Align.CENTER),
                ).moved(Location((cleanup_x, inner_y, zz)))
            else:
                cleanup = Box(
                    final_magnet_cleanup_width_x,
                    final_magnet_cleanup_depth_y,
                    final_magnet_cleanup_height_z,
                    align=(Align.CENTER, Align.MIN, Align.CENTER),
                ).moved(Location((cleanup_x, inner_y, zz)))
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

# The old skin guards were copied by the late 5 mm lamination and survived as
# narrow edge flaps beside the front and rear magnet carriers. Continue the same
# 0.40 mm recess along both complete vertical edges of both end panels. This is
# subtractive only; a 0.001 mm gap leaves every compact carrier untouched.
carrier_side_x_abs = final_carrier_center_x_abs + final_magnet_carrier_depth / 2
for sy in (1, -1):
    edge_panel = front_panel if sy > 0 else rear_panel
    edge_trim_y = (
        (front_final_outer_y + front_final_inner_y) / 2
        if sy > 0
        else (rear_final_outer_y + rear_final_inner_y) / 2
    )
    for sx in (-1, 1):
        if sx > 0:
            edge_trim = Box(
                final_rear_edge_flap_trim_width_x,
                final_rear_edge_flap_trim_depth_y,
                final_rear_edge_flap_trim_height_z,
                align=(Align.MIN, Align.CENTER, Align.CENTER),
            )
        else:
            edge_trim = Box(
                final_rear_edge_flap_trim_width_x,
                final_rear_edge_flap_trim_depth_y,
                final_rear_edge_flap_trim_height_z,
                align=(Align.MAX, Align.CENTER, Align.CENTER),
            )
        edge_trim_x = sx * (carrier_side_x_abs + final_rear_edge_flap_trim_gap_x)
        cutter = edge_trim.moved(Location((edge_trim_x, edge_trim_y, H / 2)))
        edge_panel = (edge_panel - cutter).clean()
    if sy > 0:
        front_panel = edge_panel
    else:
        rear_panel = edge_panel

# Restore only the old oversized strike recesses from the inner face of each
# side panel, never through the full panel thickness. Then cut the final compact
# 5.5 x 10.5 x 1.15 mm strike pocket. This removes the old rectangular ghost
# while preserving the outer face, perimeter chamfer, and panel outline.
final_strike_depth = final_strike_thickness_x + final_strike_depth_clearance
final_strike_repair_depth = final_strike_depth + final_strike_repair_overlap_x
assert final_strike_repair_depth < panel_t
for sx, side_shape in ((-1, left_panel), (1, right_panel)):
    revised = side_shape
    side_inner_x = sx * final_side_interface_x
    repair_center_x = side_inner_x + sx * final_strike_repair_depth / 2
    strike_center_x = side_inner_x + sx * final_strike_depth / 2
    for station_y in (final_front_station_y, final_rear_station_y):
        for zz in (side_station_z_low, side_station_z_high):
            inner_repair = Box(
                final_strike_repair_depth,
                final_strike_patch_width_y,
                final_strike_patch_height_z,
                align=(Align.CENTER, Align.CENTER, Align.CENTER),
            ).moved(Location((repair_center_x, station_y, zz)))
            strike = Box(
                final_strike_depth,
                final_magnet_pocket_width,
                final_magnet_pocket_height,
                align=(Align.CENTER, Align.CENTER, Align.CENTER),
            ).moved(Location((strike_center_x, station_y, zz)))
            revised = (revised + inner_repair - strike).clean()
    if sx < 0:
        left_panel = revised
    else:
        right_panel = revised

assert all(p.solids().__len__() == 1 for p in (front_panel, rear_panel, left_panel, right_panel))

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

publish('front_panel', front_panel, 'Front magnets without edge flaps')
publish('rear_panel', rear_panel, 'Rear magnets without edge flaps')
publish('left_panel', left_panel, 'Compact strike pockets on restored inner skin')
publish('right_panel', right_panel, 'Compact strike pockets on restored inner skin')
publish('top_cap', top_cap, 'Rounded top panel')
publish('base', base, 'Rounded base panel')
print(f'FLUSH_MAGNET_PASS: pocket={final_magnet_pocket_height:.1f}x{final_magnet_pocket_width:.1f}x{final_magnet_pocket_depth:.1f} mm for 10x5x2 magnets; wall={final_magnet_wall:.1f} mm; side inset={final_magnet_side_inset:.2f} mm; front and rear edge flaps removed without moving carriers.')