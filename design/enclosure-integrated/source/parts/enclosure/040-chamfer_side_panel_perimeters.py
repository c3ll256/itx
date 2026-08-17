# Side-panel vertical edges are already rounded by the source shell. Chamfer the
# remaining long top/bottom straight perimeter edges without touching vents.
side_panel_perimeter_chamfer=param('side_panel_perimeter_chamfer',0.30)
side_panel_perimeter_min_length=param('side_panel_perimeter_min_length',200.0)
def side_long_horizontal_edges(shape,min_length):
    result=[]
    for e in shape.edges():
        if e.geom_type!=GeomType.LINE or e.length<min_length: continue
        direction=(e.position_at(1)-e.position_at(0)).normalized()
        if abs(direction.dot(Vector(0,1,0)))>0.99: result.append(e)
    return result
left_perimeter=side_long_horizontal_edges(left_panel,side_panel_perimeter_min_length)
right_perimeter=side_long_horizontal_edges(right_panel,side_panel_perimeter_min_length)
assert len(left_perimeter)>=2 and len(right_perimeter)>=2
left_panel=chamfer(left_perimeter,side_panel_perimeter_chamfer)
right_panel=chamfer(right_perimeter,side_panel_perimeter_chamfer)
assert left_panel.solids().__len__()==1 and right_panel.solids().__len__()==1
publish('left_panel',left_panel,'Deburred left magnetic side'); publish('right_panel',right_panel,'Deburred right magnetic side')
print('SIDE_PANEL_PERIMETER_CHAMFER_PASS:',len(left_perimeter),len(right_perimeter),side_panel_perimeter_chamfer)