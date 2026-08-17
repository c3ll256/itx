# User-requested simplification: remove the complete inner thickening layer from the top cap.
# Retain only the parametric outer cap plate (z = H-cap_t .. H), including its existing
# four kit-generated M3 openings and exterior edge treatment.
thin_cap_envelope=Box(W,D,cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,0,H-cap_t)))
top_cap=top_cap.intersect(thin_cap_envelope).clean()
publish('top_cap',top_cap,'Thin top cap')
assert top_cap.bounding_box().min.Z >= H-cap_t-0.01
assert top_cap.bounding_box().max.Z <= H+0.01
print('TOP_CAP_THICKENING_REMOVED_PASS: inner thickening removed completely; cap occupies only the outer cap thickness and no longer overlaps column tops.')