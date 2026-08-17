# Chamfer long straight perimeter edges in the base plate skin only.
base_skin_chamfer=param('base_skin_chamfer',0.40)
base_skin_edge_min_length=param('base_skin_edge_min_length',100.0)
base_skin_min_z=param('base_skin_min_z',-0.01)
base_skin_max_z=param('base_skin_max_z',base_t+0.01)
base_skin_edges=[]
for e in base.edges():
    if e.geom_type!=GeomType.LINE or e.length<base_skin_edge_min_length: continue
    z=e.position_at(0.5).Z
    if base_skin_min_z<=z<=base_skin_max_z: base_skin_edges.append(e)
assert len(base_skin_edges)>=4
base=chamfer(base_skin_edges,base_skin_chamfer)
assert base.solids().__len__()==1
publish('base',base,'Chamfered slim bottom')
print('BASE_SKIN_CHAMFER_PASS:',len(base_skin_edges),base_skin_chamfer)