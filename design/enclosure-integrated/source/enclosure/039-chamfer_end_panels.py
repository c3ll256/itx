# Chamfer only the long exterior vertical edges of the front and rear panels.
end_panel_vertical_chamfer=param('end_panel_vertical_chamfer',0.35)
end_panel_vertical_min_length=param('end_panel_vertical_min_length',200.0)
def long_vertical_edges(shape,min_length):
    result=[]
    for e in shape.edges():
        if e.geom_type!=GeomType.LINE or e.length<min_length: continue
        direction=(e.position_at(1)-e.position_at(0)).normalized()
        if abs(direction.dot(Vector(0,0,1)))>0.99: result.append(e)
    return result
front_vertical=long_vertical_edges(front_panel,end_panel_vertical_min_length)
rear_vertical=long_vertical_edges(rear_panel,end_panel_vertical_min_length)
assert len(front_vertical)>=2 and len(rear_vertical)>=2
front_panel=chamfer(front_vertical,end_panel_vertical_chamfer)
rear_panel=chamfer(rear_vertical,end_panel_vertical_chamfer)
assert front_panel.solids().__len__()==1 and rear_panel.solids().__len__()==1
publish('front_panel',front_panel,'Chamfered slim front'); publish('rear_panel',rear_panel,'Chamfered slim rear')
print('END_PANEL_CHAMFER_PASS:',len(front_vertical),len(rear_vertical),end_panel_vertical_chamfer)