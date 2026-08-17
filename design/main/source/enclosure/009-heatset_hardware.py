# Purchased inserts and screws are defined in hardware/bom.json, not exported as printed CAD solids.
# Keep the centered insert constructor available to downstream source that computes mounting interfaces.
from bd_warehouse.fastener import HeatSetNut
insert=HeatSetNut(size='M3-0.5-Standard',fastener_type='McMaster-Carr',simple=True)
bb=insert.bounding_box(); z_mid=(bb.min.Z+bb.max.Z)/2
centered=insert.moved(Location((0,0,-z_mid)))
redesigned_top_xy=[(-58.0,-78.0),(-58.0,78.0),(58.0,-78.0),(58.0,78.0)]
print('Purchased top and motherboard inserts are BOM hardware; only their coaxial pockets remain in manufacturing geometry.')