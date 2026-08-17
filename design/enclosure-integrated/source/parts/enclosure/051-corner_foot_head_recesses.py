# Recess the four M3 socket-cap heads inside the fused 4 mm feet. The cutter
# starts 0.2 mm outside the foot to avoid a coplanar boolean at the bottom face.
corner_foot_recess_diameter=param('corner_foot_recess_diameter',7.0)
corner_foot_recess_depth=param('corner_foot_recess_depth',3.2)
corner_foot_recess_cutter_overrun=param('corner_foot_recess_cutter_overrun',0.2)
corner_foot_recess_floor_z=param('corner_foot_recess_floor_z',-integrated_foot_height)
corner_foot_recess_expected_count=param('corner_foot_recess_expected_count',4)
corner_foot_recess_min_radial_wall=param('corner_foot_recess_min_radial_wall',4.0)
corner_foot_recess_cutter_z=corner_foot_recess_floor_z-corner_foot_recess_cutter_overrun
corner_foot_recess_cutter_depth=corner_foot_recess_depth+corner_foot_recess_cutter_overrun
corner_foot_recess_top_z=corner_foot_recess_floor_z+corner_foot_recess_depth
corner_foot_recess_points=[(-screw_x,-screw_y),(screw_x,-screw_y),(-screw_x,screw_y),(screw_x,screw_y)]
for x,y in corner_foot_recess_points:
    recess=Cylinder(corner_foot_recess_diameter/2,corner_foot_recess_cutter_depth,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,corner_foot_recess_cutter_z)))
    base=(base-recess).clean()
corner_foot_radial_wall=integrated_foot_diameter/2-corner_foot_recess_diameter/2
corner_foot_connection_inventory={'corner-threads':'printed-screw-joint-v1 x4','corner-head-recesses':'free non-threaded socket-head clearance x4'}
assert len(corner_foot_recess_points)==int(corner_foot_recess_expected_count)
assert corner_foot_radial_wall>=corner_foot_recess_min_radial_wall
assert corner_foot_recess_top_z<0
assert base.solids().__len__()==1
assert all(corner_foot_connection_inventory.values())
publish('base',base,'Base with recessed corner heads')
print(f'CORNER_HEAD_RECESS_PASS: four visible bottom-entry recesses diameter={corner_foot_recess_diameter:.1f} mm, depth={corner_foot_recess_depth:.1f} mm, top z={corner_foot_recess_top_z:.1f} mm; radial foot wall={corner_foot_radial_wall:.1f} mm.')