from screwjoint import make_screw_joint_v1

# Exact local replica of the detachable lower-front motherboard mount from
# enclosure-integrated build 348. Assembly coordinates are translated only so
# the original foot underside sits on Z=0 for direct slicing.
mount_web_depth_x = param('mount_web_depth_x', 4.0)
mount_web_width_y = param('mount_web_width_y', 10.0)
mount_total_height_z = param('mount_total_height_z', 79.85)
mount_foot_depth_x = param('mount_foot_depth_x', 12.0)
mount_foot_width_y = param('mount_foot_width_y', 14.0)
mount_foot_height_z = param('mount_foot_height_z', 7.0)
mount_standoff_height_x = param('mount_standoff_height_x', 6.35)
mount_standoff_diameter = param('mount_standoff_diameter', 8.0)
mount_standoff_fuse_overlap_x = param('mount_standoff_fuse_overlap_x', 0.6)
mount_board_hole_below_top_z = param('mount_board_hole_below_top_z', 5.0)
mount_board_screw_engagement_x = param('mount_board_screw_engagement_x', 6.0)
mount_base_screw_engagement_z = param('mount_base_screw_engagement_z', 5.0)
mount_detachable_anchor_x = param('mount_detachable_anchor_x', -2.0)

PCB_THICKNESS_MM = 1.6  # Mini-ITX PCB reference thickness used by the enclosure.
BOARD_PROXY_SIZE_MM = 8.0
ORIGINAL_BASE_THICKNESS_MM = 3.0
BOARD_FACE_X_MM = -2.15
MATERIAL = 'PLA'

foot_z0 = ORIGINAL_BASE_THICKNESS_MM
mount_hole_z = foot_z0 + mount_total_height_z - mount_board_hole_below_top_z
initial_anchor_x = BOARD_FACE_X_MM - mount_foot_depth_x / 2
board_plane_x = BOARD_FACE_X_MM + mount_standoff_height_x
board_screw_outer_x = board_plane_x + PCB_THICKNESS_MM

web = Box(
    mount_web_depth_x,
    mount_web_width_y,
    mount_total_height_z,
    align=(Align.MAX, Align.CENTER, Align.MIN),
).moved(Location((BOARD_FACE_X_MM, 0, foot_z0)))
foot = Box(
    mount_foot_depth_x,
    mount_foot_width_y,
    mount_foot_height_z,
    align=(Align.MAX, Align.CENTER, Align.MIN),
).moved(Location((BOARD_FACE_X_MM, 0, foot_z0)))
post = Cylinder(
    mount_standoff_diameter / 2,
    mount_standoff_height_x + mount_standoff_fuse_overlap_x,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((
    BOARD_FACE_X_MM - mount_standoff_fuse_overlap_x,
    0,
    mount_hole_z,
), (0, 90, 0)))
mount = (web + foot + post).clean()

board_proxy = Box(
    PCB_THICKNESS_MM,
    BOARD_PROXY_SIZE_MM,
    BOARD_PROXY_SIZE_MM,
    align=(Align.MIN, Align.CENTER, Align.CENTER),
).moved(Location((board_plane_x, 0, mount_hole_z)))
board_joint = make_screw_joint_v1(
    size='M3',
    at=Location((board_screw_outer_x, 0, mount_hole_z), (0, 90, 0)),
    through=[(board_proxy, PCB_THICKNESS_MM)],
    engage_depth=mount_board_screw_engagement_x,
    into=mount,
    head='socket_cap',
    strategy='auto',
    material=MATERIAL,
    boss='none',
    label='motherboard-lower-front:test',
)
mount = (mount - board_joint.engage_cuts).clean()

# Retain both stages present in the current enclosure source: the original
# lower-arm engagement at the foot centre and the later service anchor at X=-2.
base_proxy = Box(
    mount_foot_depth_x + 16.0,
    mount_foot_width_y + 6.0,
    ORIGINAL_BASE_THICKNESS_MM,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((0, 0, 0)))
initial_base_joint = make_screw_joint_v1(
    size='M3',
    at=Location((initial_anchor_x, 0, 0), (180, 0, 0)),
    through=[(base_proxy, ORIGINAL_BASE_THICKNESS_MM)],
    engage_depth=mount_base_screw_engagement_z,
    into=mount,
    head='socket_cap',
    strategy='auto',
    material=MATERIAL,
    boss='none',
    label='lower-arm-base-initial:test',
)
mount = (mount - initial_base_joint.engage_cuts).clean()

detachable_base_joint = make_screw_joint_v1(
    size='M3',
    at=Location((mount_detachable_anchor_x, 0, 0), (180, 0, 0)),
    through=[(base_proxy, ORIGINAL_BASE_THICKNESS_MM)],
    engage_depth=mount_base_screw_engagement_z,
    into=mount,
    head='socket_cap',
    strategy='auto',
    material=MATERIAL,
    boss='auto',
    label='detachable-lower-front-mb-mount:test',
)
mount = (mount + detachable_base_joint.bosses - detachable_base_joint.engage_cuts).clean()

# Put the original foot underside on the slicer build plane.
mount = mount.moved(Location((0, 0, -ORIGINAL_BASE_THICKNESS_MM)))

assert mount.solids().__len__() == 1
assert abs(mount.bounding_box().size.X - 18.35) < 0.02
assert abs(mount.bounding_box().size.Y - 14.0) < 0.02
assert abs(mount.bounding_box().size.Z - 79.85) < 0.02
assert board_joint.screw_length_mm == 8
assert initial_base_joint.screw_length_mm == 8
assert detachable_base_joint.screw_length_mm == 8

connection_inventory = {
    'motherboard-to-test-mount': 'printed-screw-joint-v1',
    'initial-foot-interface': 'printed-screw-joint-v1',
    'detachable-service-anchor': 'printed-screw-joint-v1',
}
assert all(connection_inventory.values())

publish('mount_coupon', mount, 'Lower front mount')
print(f'MITX_MOUNT_COUPON_PASS: bbox={mount.bounding_box().size}; board M3={board_joint.screw_length_mm} mm; service M3={detachable_base_joint.screw_length_mm} mm.')