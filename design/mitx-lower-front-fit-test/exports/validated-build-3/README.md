# Mini-ITX lower-front mount fit-test STEP

This directory contains the isolated lower-front motherboard mounting arm from `enclosure-integrated` build 348, translated only so its foot underside is on Z=0 for slicing.

- CAD document: `mitx-lower-front-fit-test`
- Build: `3`
- Source hash: `15ad71d7a13400a6991c844a2c4f498db3da789a7c9b6369a31c3ec534a571a3`
- STEP: `mitx-lower-front-mount-fit-test.step`
- STEP SHA-256: `f1f920c7ce32869159182974a0dfe7f00de66e982f12f1861b77838ee706a46e`
- Envelope: `18.35 × 14.00 × 79.85 mm`

Exact-geometry validation compared the STEP with `lower_front_mb_mount` from enclosure build 348 after applying the intended translation. Both directional Boolean differences were `0 mm³`, and both volumes were `4287.78989466239 mm³` within floating-point precision.

The normal CAD handoff exporter was unavailable because its staging/authority path validation rejected this auxiliary document. This file is therefore a validated-build fallback for the requested fit print, not a formal reviewed handoff of the complete enclosure.

For the intended orientation, keep the 18.35 × 14 mm foot on the print bed. Import the STEP into the slicer and retain 100% scale.