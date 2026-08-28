# Preserve the printable open lower edge of the SFX service aperture, reinforce
# the front/rear skins outward, then cut final-state PCIe bracket seating pockets.
rear_sfx_edge_opening_width_x = param('rear_sfx_edge_opening_width_x', psu_cut_w)
rear_sfx_edge_opening_bottom_z = param('rear_sfx_edge_opening_bottom_z', base_t)
rear_sfx_edge_opening_top_z = param('rear_sfx_edge_opening_top_z', psu_cut_z)
rear_sfx_edge_opening_depth_y = param('rear_sfx_edge_opening_depth_y', cut_depth)
rear_sfx_edge_boolean_overcut = param('rear_sfx_edge_boolean_overcut', 0.10)
front_panel_outer_reinforcement = param('front_panel_outer_reinforcement', 1.0)
rear_panel_outer_reinforcement = param('rear_panel_outer_reinforcement', 1.0)
pcie_final_pocket_clearance_xz = param('pcie_final_pocket_clearance_xz', 0.25)
pcie_final_pocket_clearance_y = param('pcie_final_pocket_clearance_y', 0.20)

rear_sfx_edge_web_height = rear_sfx_edge_opening_top_z - rear_sfx_edge_opening_bottom_z
assert rear_sfx_edge_web_height > 0.0
assert rear_sfx_edge_web_height < 1.2
assert front_panel_outer_reinforcement > 0.0
assert rear_panel_outer_reinforcement > 0.0
assert pcie_final_pocket_clearance_xz > 0.0
assert pcie_final_pocket_clearance_y > 0.0

rear_sfx_edge_cutter = Box(
    rear_sfx_edge_opening_width_x + 2 * rear_sfx_edge_boolean_overcut,
    rear_sfx_edge_opening_depth_y,
    rear_sfx_edge_web_height + 2 * rear_sfx_edge_boolean_overcut,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((
    psu_cut_x,
    -D / 2,
    rear_sfx_edge_opening_bottom_z - rear_sfx_edge_boolean_overcut,
)))
rear_panel = (rear_panel - rear_sfx_edge_cutter).clean()

rear_sfx_edge_void_probe = Box(
    rear_sfx_edge_opening_width_x - 2 * rear_sfx_edge_boolean_overcut,
    panel_t,
    rear_sfx_edge_web_height,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).moved(Location((psu_cut_x, rear_y, rear_sfx_edge_opening_bottom_z)))
rear_sfx_edge_residual = rear_panel & rear_sfx_edge_void_probe
rear_sfx_edge_residual_volume = sum(s.volume for s in rear_sfx_edge_residual)
assert rear_sfx_edge_residual_volume < 0.02

front_before_bb = front_panel.bounding_box()
rear_before_bb = rear_panel.bounding_box()
front_before_volume = sum(s.volume for s in front_panel.solids())
rear_before_volume = sum(s.volume for s in rear_panel.solids())

front_outer_layer = front_panel.moved(Location((0.0, front_panel_outer_reinforcement, 0.0)))
rear_outer_layer = rear_panel.moved(Location((0.0, -rear_panel_outer_reinforcement, 0.0)))
front_panel = (front_panel + front_outer_layer).clean()
rear_panel = (rear_panel + rear_outer_layer).clean()

# The PCIe bracket was collision-free against the original rear skin, but the
# later outward reinforcement duplicated rear material into its shelf and both
# vertical tabs. Cut a shelf slot and two shallow tab mortises after lamination.
pcie_final_overlap_before = rear_panel & pcie_bracket
pcie_final_overlap_before_volume = (
    0.0 if pcie_final_overlap_before is None
    else sum(s.volume for s in pcie_final_overlap_before)
)
rear_reinforced_bb = rear_panel.bounding_box()
pcie_pocket_outer_y = rear_reinforced_bb.min.Y - pcie_final_pocket_clearance_y
pcie_shelf_pocket_inner_y = pcie_shelf_inner_edge_y + pcie_final_pocket_clearance_y
pcie_shelf_pocket_depth_y = pcie_shelf_pocket_inner_y - pcie_pocket_outer_y
pcie_shelf_pocket = Box(
    pcie_bracket_width_x + 2 * pcie_final_pocket_clearance_xz,
    pcie_shelf_pocket_depth_y,
    pcie_bracket_shelf_thickness_z + 2 * pcie_final_pocket_clearance_xz,
    align=(Align.CENTER, Align.MIN, Align.MIN),
).moved(Location((
    pcie_shelf_center_x,
    pcie_pocket_outer_y,
    pcie_bracket_base_z - pcie_final_pocket_clearance_xz,
)))
rear_panel = (rear_panel - pcie_shelf_pocket).clean()

pcie_original_rear_outer_face_y = -D / 2
pcie_tab_pocket_inner_y = pcie_original_rear_outer_face_y + pcie_final_pocket_clearance_y
pcie_tab_pocket_depth_y = pcie_tab_pocket_inner_y - pcie_pocket_outer_y
pcie_tab_pockets = []
for pcie_tab_x, pcie_tab_w, _land in pcie_tab_specs:
    pcie_tab_pocket = Box(
        pcie_tab_w + 2 * pcie_final_pocket_clearance_xz,
        pcie_tab_pocket_depth_y,
        pcie_bracket_tab_height_z + 2 * pcie_final_pocket_clearance_xz,
        align=(Align.CENTER, Align.MIN, Align.MIN),
    ).moved(Location((
        pcie_tab_x,
        pcie_pocket_outer_y,
        pcie_bracket_base_z - pcie_final_pocket_clearance_xz,
    )))
    rear_panel = (rear_panel - pcie_tab_pocket).clean()
    pcie_tab_pockets.append(pcie_tab_pocket)

pcie_final_overlap_after = rear_panel & pcie_bracket
pcie_final_overlap_after_volume = (
    0.0 if pcie_final_overlap_after is None
    else sum(s.volume for s in pcie_final_overlap_after)
)

front_after_bb = front_panel.bounding_box()
rear_after_bb = rear_panel.bounding_box()
front_after_volume = sum(s.volume for s in front_panel.solids())
rear_after_volume = sum(s.volume for s in rear_panel.solids())

assert pcie_final_overlap_before_volume > 0.1
assert pcie_final_overlap_after_volume < 0.02
assert len(pcie_tab_pockets) == 2
assert pcie_shelf_pocket_depth_y > 0.0
assert pcie_tab_pocket_depth_y > 0.0
assert front_panel.solids().__len__() == 1
assert rear_panel.solids().__len__() == 1
assert abs(front_after_bb.min.Y - front_before_bb.min.Y) < 0.01
assert abs(front_after_bb.max.Y - (front_before_bb.max.Y + front_panel_outer_reinforcement)) < 0.01
assert abs(rear_after_bb.max.Y - rear_before_bb.max.Y) < 0.01
assert abs(rear_after_bb.min.Y - (rear_before_bb.min.Y - rear_panel_outer_reinforcement)) < 0.01
assert front_after_volume > front_before_volume
assert rear_after_volume > rear_before_volume
assert abs(base_t - cap_t) < 0.01

publish('front_panel', front_panel, '3 mm reinforced front')
publish('rear_panel', rear_panel, 'Rear with PCIe seating pockets')
print(
    f'FINAL_PCIE_POCKET_PASS: prior overlap {pcie_final_overlap_before_volume:.3f} mm^3; '
    f'final overlap {pcie_final_overlap_after_volume:.4f} mm^3; shelf pocket depth '
    f'{pcie_shelf_pocket_depth_y:.2f} mm; tab pocket depth {pcie_tab_pocket_depth_y:.2f} mm; '
    f'clearance XZ/Y {pcie_final_pocket_clearance_xz:.2f}/{pcie_final_pocket_clearance_y:.2f} mm.'
)