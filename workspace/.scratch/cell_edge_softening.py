# cell: edge_softening
# Cosmetic edge softening limited to exterior enclosure edges.
def vertical_edges(shape,min_len):
    return [e for e in shape.edges() if e.geom_type==GeomType.LINE and e.length>=min_len and abs((e.position_at(1)-e.position_at(0)).normalized().dot(Vector(0,0,1)))>0.99]
def outer_vertical_edges(shape,min_len):
    out=[]
    for e in vertical_edges(shape,min_len):
        p=e.position_at(0.5)
        if abs(p.X)>=W/2-1.5 or abs(p.Y)>=D/2-1.5:
            out.append(e)
    return out
front_panel=fillet(vertical_edges(front_panel,210.0),1.0)
rear_panel=fillet(vertical_edges(rear_panel,210.0),1.0)
left_panel=fillet(vertical_edges(left_panel,210.0),1.0)
right_panel=fillet(vertical_edges(right_panel,210.0),1.0)
top_outer=outer_vertical_edges(top_cap,2.8)
base_outer=outer_vertical_edges(base,2.8)
if top_outer: top_cap=fillet(top_outer,1.2)
if base_outer: base=fillet(base_outer,1.2)
publish('base',base,'Rounded support base')
publish('top_cap',top_cap,'Rounded support top')
publish('front_panel',front_panel,'Rounded front panel')
publish('rear_panel',rear_panel,'Rounded rear panel')
publish('left_panel',left_panel,'Rounded left vent')
publish('right_panel',right_panel,'Rounded right vent')
print('EXTERIOR_EDGE_SOFTENING_PASS: only exterior shell edges are filleted; internal motherboard support arms are excluded.')

