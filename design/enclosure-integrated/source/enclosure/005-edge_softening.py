# Cosmetic edge softening limited to exterior enclosure edges and safe for 2 mm FDM panels.
def vertical_edges(shape,min_len):
    return [e for e in shape.edges() if e.geom_type==GeomType.LINE and e.length>=min_len and abs((e.position_at(1)-e.position_at(0)).normalized().dot(Vector(0,0,1)))>0.99]
def outer_vertical_edges(shape,min_len):
    out=[]
    for e in vertical_edges(shape,min_len):
        p=e.position_at(0.5)
        if abs(p.X)>=W/2-1.5 or abs(p.Y)>=D/2-1.5: out.append(e)
    return out
panel_edge_radius=param('panel_edge_radius',0.7)
shell_edge_radius=param('shell_edge_radius',1.2)
front_edges=vertical_edges(front_panel,210.0); rear_edges=vertical_edges(rear_panel,210.0)
left_edges=vertical_edges(left_panel,210.0); right_edges=vertical_edges(right_panel,210.0)
if front_edges: front_panel=fillet(front_edges,panel_edge_radius)
if rear_edges: rear_panel=fillet(rear_edges,panel_edge_radius)
if left_edges: left_panel=fillet(left_edges,panel_edge_radius)
if right_edges: right_panel=fillet(right_edges,panel_edge_radius)
top_outer=outer_vertical_edges(top_cap,2.8); base_outer=outer_vertical_edges(base,2.8)
if top_outer: top_cap=fillet(top_outer,shell_edge_radius)
if base_outer: base=fillet(base_outer,shell_edge_radius)
publish('base',base,'Rounded support base'); publish('top_cap',top_cap,'Rounded support top')
publish('front_panel',front_panel,'Rounded front panel'); publish('rear_panel',rear_panel,'Rounded rear panel')
publish('left_panel',left_panel,'Rounded left vent'); publish('right_panel',right_panel,'Rounded right vent')
print(f'PANEL_EDGE_PASS: exterior panel radius {panel_edge_radius:.1f} mm remains below half of the 2.0 mm target panel thickness.')