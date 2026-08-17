# Historical foot construction retained only for downstream base fusion.
foot_fl_diameter=param('foot_fl_diameter',16.0); foot_rl_diameter=param('foot_rl_diameter',16.0)
foot_fr_diameter=param('foot_fr_diameter',16.0); foot_rr_diameter=param('foot_rr_diameter',16.0)
foot_fl_height=param('foot_fl_height',4.0); foot_rl_height=param('foot_rl_height',4.0)
foot_fr_height=param('foot_fr_height',4.0); foot_rr_height=param('foot_rr_height',4.0)
assert len(feet)==4 and len(base_joints)==4
assert all(j.screw_length_mm>0 for j in base_joints)
print('FOOT_SOURCE_ONLY: four historical foot solids remain construction data and are not published as separate components.')