# Final printable-envelope trim after every late SFX land, PCIe support, and
# rear-panel repair. The two lower SFX lands currently extend 1 mm below the
# intended z=base_t edge; trim only that excess while preserving holes and all
# inward-facing structures.
rear_final_trim_width_x=param('rear_final_trim_width_x',W)
rear_final_trim_depth_y=param('rear_final_trim_depth_y',32.0)
rear_final_trim_outward_allowance_y=param('rear_final_trim_outward_allowance_y',1.0)
rear_final_trim_bottom_z=param('rear_final_trim_bottom_z',base_t)
rear_final_trim_top_z=param('rear_final_trim_top_z',H-cap_t)
rear_final_trim_expected_min_z=param('rear_final_trim_expected_min_z',base_t)
rear_final_trim_height_z=rear_final_trim_top_z-rear_final_trim_bottom_z
rear_final_trim=Box(
    rear_final_trim_width_x,
    rear_final_trim_depth_y,
    rear_final_trim_height_z,
    align=(Align.CENTER,Align.MIN,Align.MIN),
).moved(Location((0,-D/2-rear_final_trim_outward_allowance_y,rear_final_trim_bottom_z)))
rear_panel=(rear_panel & rear_final_trim).clean()
assert rear_panel.solids().__len__()==1
assert abs(rear_panel.bounding_box().min.Z-rear_final_trim_expected_min_z)<0.01
assert rear_panel.bounding_box().min.X>=-W/2-0.01 and rear_panel.bounding_box().max.X<=W/2+0.01
publish('rear_panel',rear_panel,'Rear trimmed to case outline')
print(f'REAR_FINAL_OUTLINE_PASS: min z={rear_panel.bounding_box().min.Z:.2f} mm; both lower SFX lands are flush with the {rear_final_trim_bottom_z:.2f} mm rear-panel edge.')