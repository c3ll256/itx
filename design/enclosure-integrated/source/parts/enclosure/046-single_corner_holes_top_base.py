# Restore both historical and current corner-hole envelopes, then reapply only
# the four current printed-screw-joint-v1 through cuts per panel.
top_corner_repair_patch_diameter = param('top_corner_repair_patch_diameter', 12.0)
top_corner_repair_patch_height = param('top_corner_repair_patch_height', cap_t + cap_inner_t)
base_corner_repair_patch_diameter = param('base_corner_repair_patch_diameter', 12.0)
base_corner_repair_patch_height = param('base_corner_repair_patch_height', base_t + foot_height)
corner_repair_legacy_y = param('corner_repair_legacy_y', post_y)
corner_repair_current_y = param('corner_repair_current_y', screw_y)
corner_repair_patch_y = (corner_repair_legacy_y + corner_repair_current_y) / 2
corner_repair_legacy_x = param('corner_repair_legacy_x', post_x)
corner_repair_current_x = param('corner_repair_current_x', screw_x)
corner_repair_patch_x = (corner_repair_legacy_x + corner_repair_current_x) / 2

# Fill the complete double-hole footprint in both printable parts.
for sy in (-1, 1):
    for sx in (-1, 1):
        px = sx * corner_repair_patch_x
        py = sy * corner_repair_patch_y
        top_patch = Cylinder(
            top_corner_repair_patch_diameter / 2,
            top_corner_repair_patch_height,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((px, py, H - top_corner_repair_patch_height)))
        base_patch = Cylinder(
            base_corner_repair_patch_diameter / 2,
            base_corner_repair_patch_height,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((px, py, -foot_height)))
        top_cap = (top_cap + top_patch).clean()
        base = (base + base_patch).clean()

# Reuse the exact kit-generated cuts from the active slim corner joints.
active_bottom_corner_joints = slim2_corner_joints[0::2]
active_top_corner_joints = slim2_corner_joints[1::2]
for joint in active_bottom_corner_joints:
    base = (base - joint.through_cuts[0]).clean()
for joint in active_top_corner_joints:
    top_cap = (top_cap - joint.through_cuts[0]).clean()

assert len(active_bottom_corner_joints) == 4
assert len(active_top_corner_joints) == 4
assert base.solids().__len__() == 1 and top_cap.solids().__len__() == 1
publish('top_cap', top_cap, 'Single-hole top')
publish('base', base, 'Single-hole bottom')
print('SINGLE_CORNER_HOLES_PASS: restored four double-hole envelopes on each panel and reapplied exactly four active kit-owned holes per panel.')