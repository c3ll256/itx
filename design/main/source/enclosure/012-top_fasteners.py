# Top M3x8 screws are purchased BOM hardware and are intentionally excluded from printed-part geometry.
top_screw_xy=[(-58.0,-78.0),(-58.0,78.0),(58.0,-78.0),(58.0,78.0)]
assert len(top_screw_xy)==4
print('Top screw axes remain X=+-58/Y=+-78; physical screws are defined in hardware/bom.json and not exported as solids.')