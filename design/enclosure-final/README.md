# CAD Review Brief — final Mini-ITX screw-layout model

Review this exact three-cell source model against `product/artifact-contract.json`.

1. All legacy/duplicate holes are absent; final axes are: top X=±58/Y=±78; Mini-ITX offsets 6.35/163.83; PSU X=16/46,Y=±72; riser tray Y=-14/50; riser slots X=22/40; GPU-tail slots X=16/46; GPU bracket pitch 20.32; GPU side clamps Y=±70/Z=110 mm.
2. Sixteen 15 × 10 × 4 mm countersunk magnet flats each have one centered 2.6 mm diameter × 4.6 mm deep printed M3 pilot; perimeter panels themselves have no screw holes.
3. Top view shows only the four new top-cap holes; bottom view shows only the new four-hole PSU pattern.
4. Purchased screws, inserts, magnets and power switch are BOM hardware and excluded from printable solids; required holes, pockets, flats and clearances remain modeled.
5. Source cells `shell`, `motherboard_psu`, and `gpu_riser` contain all geometry and assertions; their final count assertion covers 40 screw axes across nine interfaces.
