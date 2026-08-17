# Final keep-out for straight SFX insertion. Remove every base-attached feature
# above the floor that enters the PSU envelope; preserve the floor, outer guides,
# and the front stop beyond the 100 mm body depth.
base_sfx_clear_width = param('base_sfx_clear_width', sfx_psu_width + 2*sfx_guide_side_clearance)
base_sfx_clear_depth = param('base_sfx_clear_depth', sfx_psu_depth + sfx_psu_rear_clearance)
base_sfx_clear_height = param('base_sfx_clear_height', sfx_psu_height + sfx_column_top_clearance)
base_sfx_clear_rear_y = param('base_sfx_clear_rear_y', -D/2 + panel_t)
base_sfx_floor_preserve_z = param('base_sfx_floor_preserve_z', base_t)
base_sfx_expected_residual_volume = param('base_sfx_expected_residual_volume', 0.02)

sfx_insertion_corridor = Box(
    base_sfx_clear_width,
    base_sfx_clear_depth,
    base_sfx_clear_height,
    align=(Align.CENTER, Align.MIN, Align.MIN),
).moved(Location((0, base_sfx_clear_rear_y, base_sfx_floor_preserve_z)))
base = (base - sfx_insertion_corridor).clean()
sfx_residual_items = base & sfx_insertion_corridor
sfx_residual_volume = sum(s.volume for s in sfx_residual_items)
assert base.solids().__len__() == 1
assert sfx_residual_volume < base_sfx_expected_residual_volume
publish('base', base, 'Base with clear SFX bay')
print(f'SFX_INSERTION_CLEAR_PASS: {base_sfx_clear_width:.1f} x {base_sfx_clear_depth:.1f} x {base_sfx_clear_height:.1f} mm corridor is clear above the {base_sfx_floor_preserve_z:.1f} mm floor; residual={sfx_residual_volume:.4f} mm^3.')