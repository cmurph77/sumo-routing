# every simulation step
while current_active_vehicles > 0:

    # step 1: initialise edge weights to currenrt travel tim
    for edge_id in network_edges:
        edge_travel_time = traci.edge.getTraveltime(edge_id)
        traci.setEdgeEffort(edge_id, edge_travel_time) 

    # step 2: update weights according to vehicles 
    for vehicle_id in current_active_vehicles:
        veh_remaing_route = get_remaining_route(vehicle_id) # gets edges left on a vehicles route
        for edge_id in veh_remaing_route:
            current_edge_effort = traci.getEdgeEffort(edge_id)
            new_edge_effort = current_active_vehicles * increase_factor
            traci.setEdgeEffort(edge_id, new_edge_effort) 
        
    # step 3: reroute vehicles according new weights
    for vehicle_id in current_active_vehicles:
        traci.vehicle.rerouteEffort(vehicle_id)
