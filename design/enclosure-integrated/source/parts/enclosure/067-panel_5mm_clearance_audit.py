# Deterministic clearance audit for the new reinforcement only.
reinforcement_clearance_tolerance_mm3 = param('reinforcement_clearance_tolerance_mm3', 0.01)

def reinforcement_intersection_volume(a, b):
    return sum(s.volume for s in (a & b).solids())

front_fan_reinforcement_intersections = [
    reinforcement_intersection_volume(front_inner_layer, fan_body)
    for fan_body in fan80_bodies
]
base_fan_reinforcement_intersection = reinforcement_intersection_volume(base_inner_layer, fan120_body)
base_psu_reinforcement_intersection = reinforcement_intersection_volume(base_inner_layer, fan120_psu_proxy)
rear_psu_rib_intersection = reinforcement_intersection_volume(rear_ribs, fan120_psu_proxy)
front_gpu_reinforcement_intersection = reinforcement_intersection_volume(front_inner_layer, front_gpu_reference_proxy)

assert max(front_fan_reinforcement_intersections) < reinforcement_clearance_tolerance_mm3
assert base_fan_reinforcement_intersection < reinforcement_clearance_tolerance_mm3
assert base_psu_reinforcement_intersection < reinforcement_clearance_tolerance_mm3
assert rear_psu_rib_intersection < reinforcement_clearance_tolerance_mm3
assert front_gpu_reinforcement_intersection < reinforcement_clearance_tolerance_mm3
print(
    'PANEL_5MM_CLEARANCE_PASS: reinforcement intersections mm3 '
    f'front fans={front_fan_reinforcement_intersections}, '
    f'base fan={base_fan_reinforcement_intersection:.4f}, '
    f'base PSU={base_psu_reinforcement_intersection:.4f}, '
    f'rear PSU={rear_psu_rib_intersection:.4f}, '
    f'front GPU={front_gpu_reinforcement_intersection:.4f}.'
)