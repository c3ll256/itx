# Relocate only the four rear-facing magnet seats out of the rear I/O apertures.
# Existing rear seats are filled, then rebuilt in the solid outer border strips.
rear_old_x=post_outer_x-pad_face_w/2       # 62.5 mm in revision 12
rear_pad_w=13.0
rear_new_x=W/2-rear_pad_w/2               # 66.5 mm; pad spans 60..73 mm
rear_pad_y=-(post_outer_y-pad_depth/2)
rear_pocket_y=-(post_outer_y-flat_d/2)
rear_magnet_y=-(post_outer_y-magnet_t/2)
rear_mouth_y=-post_outer_y
rear_open_left=(-59.0,-11.0)
rear_open_right=(7.0,55.0)
assert -rear_new_x+rear_pad_w/2 <= rear_open_left[0]-1.0
assert rear_new_x-rear_pad_w/2 >= rear_open_right[1]+5.0
rear_relocated_joints=[]
for sx in (-1,1):
    old_x=sx*rear_old_x
    new_x=sx*rear_new_x
    for z in end_z:
        # Restore the former local pad, pocket and engagement cut to plain material.
        old_fill=Box(pad_face_w,pad_depth,pad_h,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((old_x,rear_pad_y,z)))
        main_frame=main_frame+old_fill
        # Rebuild a narrower pad wholly behind the rear panel's solid edge strip.
        new_pad=Box(rear_pad_w,pad_depth,pad_h,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((new_x,rear_pad_y,z)))
        main_frame=main_frame+new_pad
        new_pocket=Box(flat_w,flat_d,flat_h,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((new_x,rear_pocket_y,z)))
        main_frame=main_frame-new_pocket
        magnet_proxy=Box(magnet_w,magnet_t,magnet_h,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((new_x,rear_magnet_y,z)))
        joint=make_screw_joint_v1(
            size="M3", at=Location((new_x,rear_mouth_y,z),(90,0,0)),
            through=[(magnet_proxy,magnet_t)], head="countersunk", strategy="auto",
            material=SCREW_MATERIAL, boss="none", available_depth=pad_available_depth,
            label=f"magnet-rear-relocated:{sx}:{z}"
        )
        main_frame=main_frame-joint.engage_cuts
        rear_relocated_joints.append(joint)

# The outward-shifted rear pads occupy the case corner strip; notch only the
# rear-most 15 mm of each perforated side panel around those four pads.
for sx in (-1,1):
    relief_x=sx*(W/2-panel_t/2)
    for z in end_z:
        relief=Box(panel_t+1.0,pad_depth+1.2,pad_h+1.0,align=(Align.CENTER,Align.CENTER,Align.CENTER)).moved(Location((relief_x,rear_pad_y,z)))
        if sx<0:
            left_panel=left_panel-relief
        else:
            right_panel=right_panel-relief

assert len(rear_relocated_joints)==4
publish('base_and_frame',main_frame,'Rear-clearance slim frame')
publish('left_panel',left_panel,'Left vent panel')
publish('right_panel',right_panel,'Right vent panel')
print('REAR_OPENING_CLEARANCE_PASS: four rear magnet seats relocated to x=+-66.5; left and right I/O apertures receive zero frame-pad overlap.')