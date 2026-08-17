# Internal structural interfaces; rear perimeter panel is magnetic and unthreaded.
tray_x=4.0
bottom_slot=Box(3.2,176,8,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((tray_x,0,0)))
top_blind_groove=Box(3.2,176,2.2,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((tray_x,0,H-cap_t-2.1)))
main_frame=main_frame-bottom_slot
top_cap=top_cap-top_blind_groove
for x in (14,48):
  for y in (-70,70):
    main_frame=main_frame-Cylinder(m3_clear,8,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,-1)))
# Rebuild rear panel without screw holes, countersinks or bosses.
rear_panel=Box(W,panel_t,H-base_t-cap_t,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,rear_y,base_t)))
rear_panel=rear_panel-Box(48,8,126,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((-35,-D/2,74)))
rear_panel=rear_panel-Box(48,8,122,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,-D/2,96)))
rear_panel=rear_panel-Box(46,8,86,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((31,-D/2,4)))
publish('base_and_frame',main_frame,'Structural frame with magnetic-panel locating lips')
publish('top_cap',top_cap,'Continuous top cap with concealed tray groove')
publish('rear_io_panel',rear_panel,'Tool-less magnetic rear service panel without screw interfaces')
print('Removed rear-panel screw holes, countersinks and threaded bosses; service apertures remain unchanged.')