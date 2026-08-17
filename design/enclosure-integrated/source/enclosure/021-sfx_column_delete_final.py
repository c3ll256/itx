# Keep the SFX bay completely column-free; rear columns resume only above the PSU.
# The former full-width upper header is intentionally removed as redundant.
sfx_column_free_height=param('sfx_column_free_height',70.0)
sfx_bay_extra_width=param('sfx_bay_extra_width',3.0)
sfx_bay_clear_width=sfx_psu_width+2*sfx_bay_extra_width
rear_column_cut_width=param('rear_column_lower_cut_width',16.0)
rear_column_cut_depth=param('rear_column_lower_cut_depth',18.0)
for idx in (0,2):
    x,y=post_xy[idx]
    full_lower_cut=Box(rear_column_cut_width,rear_column_cut_depth,sfx_column_free_height-base_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,base_t)))
    columns[idx]=columns[idx]-full_lower_cut
assert sfx_column_free_height>base_t+sfx_psu_height+param('sfx_header_vertical_clearance',3.0)
assert sfx_bay_clear_width>sfx_psu_width
publish('column_fl',columns[0],'Left upper rear stub')
publish('column_fr',columns[2],'Right upper rear stub')
print(f'SFX_HEADER_REMOVED_PASS: full-width upper header removed; both rear stubs start above z={sfx_column_free_height:.1f} mm and the {sfx_bay_clear_width:.1f} mm PSU bay remains open.')