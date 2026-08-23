# Deterministic clearance audit for the panel reinforcement.
reinforcement_clearance_tolerance_mm3 = param('reinforcement_clearance_tolerance_mm3', 0.01)

def reinforcement_intersection_volume(a, b):
    return sum(s.volume for s in (a & b).solids())

front_fan_reinforcement_intersections = [
    reinforcement_intersection_volume(front_inner_layer, fan_body)
    for fan_body in fan80_bodies
]
base_fan_reinforcement_intersection = reinforcement_intersection_volume(base_inner_layer, fan120_body)
base_psu_reinforcement_intersection = reinforcement_intersection_volume(base_inner_layer, fan120_psu_proxy)
if 'rear_full_layer' in globals():
    rear_reinforcement_shape = rear_full_layer
elif 'rear_inner_layer' in globals():
    rear_reinforcement_shape = rear_inner_layer
else:
    rear_reinforcement_shape = rear_ribs
rear_psu_reinforcement_intersection = reinforcement_intersection_volume(rear_reinforcement_shape, fan120_psu_proxy)
front_gpu_reinforcement_intersection = reinforcement_intersection_volume(front_inner_layer, front_gpu_reference_proxy)

assert max(front_fan_reinforcement_intersections) < reinforcement_clearance_tolerance_mm3, f'front fan reinforcement intersection={front_fan_reinforcement_intersections}'
assert base_fan_reinforcement_intersection < reinforcement_clearance_tolerance_mm3, f'base fan reinforcement intersection={base_fan_reinforcement_intersection:.4f}'
assert base_psu_reinforcement_intersection < reinforcement_clearance_tolerance_mm3, f'base PSU reinforcement intersection={base_psu_reinforcement_intersection:.4f}'
assert rear_psu_reinforcement_intersection < reinforcement_clearance_tolerance_mm3, f'rear PSU reinforcement intersection={rear_psu_reinforcement_intersection:.4f}'
assert front_gpu_reinforcement_intersection < reinforcement_clearance_tolerance_mm3, f'front GPU reinforcement intersection={front_gpu_reinforcement_intersection:.4f}'
print(
    'PANEL_5MM_CLEARANCE_PASS: reinforcement intersections mm3 '
    f'front fans={front_fan_reinforcement_intersections}, '
    f'base fan={base_fan_reinforcement_intersection:.4f}, '
    f'base PSU={base_psu_reinforcement_intersection:.4f}, '
    f'rear PSU={rear_psu_reinforcement_intersection:.4f}, '
    f'front GPU={front_gpu_reinforcement_intersection:.4f}.'
)