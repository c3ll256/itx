# Obsolete motherboard-tray locator system removed.
# The authoritative shell now creates a continuous two-layer top cap directly,
# so no tray-slot cut, tongue groove, locator channel, or compensating fill is
# created here. Front and rear panels likewise carry no tray guide grooves.
publish('top_cap',top_cap,'Slotless top cap')
publish('front_panel',front_panel,'Slotless front panel')
publish('rear_panel',rear_panel,'Slotless rear panel')
print('NO_TRAY_GROOVES_PASS: no tray slots are cut and no historical fill solids are required.')