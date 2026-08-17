# Chamfer long straight perimeter edges in the top-cap skin only. The Z threshold
# follows the current case height instead of persisting the original 262 mm value.
top_skin_chamfer=param('top_skin_chamfer',0.40)
top_skin_edge_min_length=param('top_skin_edge_min_length',100.0)
top_skin_threshold_margin=param('top_skin_threshold_margin',0.01)
top_skin_min_z=H-cap_t-cap_inner_t-top_skin_threshold_margin
top_skin_edges=[]
for e in top_cap.edges():
    if e.geom_type!=GeomType.LINE or e.length<top_skin_edge_min_length: continue
    if e.position_at(0.5).Z>=top_skin_min_z: top_skin_edges.append(e)
assert len(top_skin_edges)>=4
top_cap=chamfer(top_skin_edges,top_skin_chamfer)
assert top_cap.solids().__len__()==1
publish('top_cap',top_cap,'Chamfered slim top')
print('TOP_SKIN_CHAMFER_PASS:',len(top_skin_edges),top_skin_chamfer,'dynamic_threshold',top_skin_min_z)