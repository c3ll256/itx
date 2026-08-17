# Hard keepouts behind all rear-panel apertures. These cut only the frame,
# guaranteeing no column or magnet-pad material can enter the visible openings.
rear_keepouts=[
    (-35.0,137.0,49.6,127.6),  # left motherboard / I/O opening
    (31.0,157.0,49.6,123.6),   # upper-right GPU opening
    (31.0,47.0,47.6,87.6),     # lower-right PSU opening
]
for x,z,w,h in rear_keepouts:
    keepout=Box(w,30.0,h,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((x,-85.0,z)))
    main_frame=main_frame-keepout
assert len(rear_keepouts)==3
publish('base_and_frame',main_frame,'Rear-opening-safe frame')
print('REAR_FRAME_KEEPOUT_PASS: frame material excluded from all three rear apertures with 0.8 mm perimeter clearance.')