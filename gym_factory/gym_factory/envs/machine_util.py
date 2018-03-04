def initalize_factory(machine_map):
    """initalize factory machine's capa"""
    capa = {}
    
    for machine_type in machine_map.keys():
        capa[machine_type] = [machine_map[machine_type][1]]
        for _ in range(1, machine_map[machine_type][0]):
            capa[machine_type].append(machine_map[machine_type][1])
    return capa