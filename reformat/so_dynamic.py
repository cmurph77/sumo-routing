import traci as t
import traci
import xml.etree.ElementTree as ET
import csv
import set_sumocgf
import random
import argparse
import average_time
import numpy as np
import math

import datetime

last_step = 0

def log_results(filename, network, algorithm, trip_size, ct,avg_tt,increase_factor, max_density, network_total_dist):
    """Append a new line to a text file."""
    current_time = datetime.datetime.now()
    current_time = '[' + str(current_time) + '] , '
    line = str(current_time) + "Network: " + network + ", Trip Size: " + str(trip_size)+ ", Average Time: " + str(avg_tt)  + ", Increase factor: "  +str(increase_factor)+ ", max_density: " + str(max_density) +', Maxspeed: ' + str(max_vspeed) + ', sim_time: ' + str(last_step)
    with open(filename, 'a') as file:
        file.write(line + '\n')
    with open('density_log.txt', 'a') as file:
        file.write(alg_name + "--" +line + '\n')
    with open('overall_density_log.txt', 'a') as file:
        file.write(alg_name + "--" +line + '\n')


# write a dictionary to a txt file
def write_new_line(filename, network, algorithm, trip_size, ct,avg_tt):
    """Append a new line to a text file."""
    current_time = datetime.datetime.now()
    current_time = '[' + str(current_time) + '] , '
    line = str(current_time) + "Network: " + network + ", Trip Size: " + str(trip_size)+ ", Average Time: " + str(avg_tt)  + ", Algo: "  +algorithm+ ", Congestion T: " + str(ct)
    with open(filename, 'a') as file:
        file.write(line + '\n')

def get_network_edges(net_file):
    return traci.edge.getIDList()   # gets a list of edges in the network

# creates a dict with { edge_id : edge_length }
def get_edge_length_dict(network_edges):
    edge_lengths = {}
    for edge_id in network_edges:
        edge_lengths[edge_id] = traci.lane.getLength(edge_id)

    return edge_lengths


# creates a dict with { edge_id : current_vehicles_on_edge }
def create_edges_current_vehicles(active_vehicles, step):
    edges_current_vehicles = {}
    for edge in network_edges:
        vehicles_on_edge = traci.edge.getLastStepVehicleIDs(edge)
        edges_current_vehicles[edge] = vehicles_on_edge

        # print ("step: " + str(step)+ " | On edge: " + edge + ", there are " + str(len(vehicles_on_edge)))

#  creates a dict with {edge_id : current_traveltime}
def create_edges_current_traveltime(network_edges):
    edges_current_traveltime = {}
    # print(network_edges)
    for edge in network_edges:
        current_traveltime = traci.edge.getTraveltime(edge)
        # print(current_traveltime)
        edges_current_traveltime[edge] = current_traveltime

    return edges_current_traveltime

# returns a congestion disctionary with { edge_id :  current_tt/ baseline_traveltime}
def create_congestion_dict(current_travel_times,baseline_edges_traveltime):
    congestion_dict = {}
    for edge_id, current_tt in current_travel_times.items():
        congestion_dict[edge_id] = round(current_tt / baseline_edges_traveltime[edge_id], 3)

    return congestion_dict

# extracts distances from net file in the form { edge_id : distance }

def get_distances_in_net(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    edge_lengths = {}

    for edge in root.findall('edge'):
        edge_id = edge.attrib['id']
        lane = edge.find('lane')
        if lane is not None:
            length = float(lane.attrib['length'])
            edge_lengths[edge_id] = length

    return edge_lengths

# outputs a csv file of the congestion matrix with edge_ids on top row and congestion at each time step below
def output_congestion_matrix(congestion_matrix, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write header
        # header = [list(entry.keys())[0] for entry in congestion_matrix[1]]
        field_headers = congestion_matrix[0].keys()
        # print(field_headers)
        writer.writerow(field_headers)

        # i = 0
        for cong_dict in congestion_matrix:
            # congestion_vals = [list(entry.values())[0] for entry in cong_dict]
            congestion_vals = cong_dict.values()
            writer.writerow(congestion_vals)

# This function produces a dict like { edge_id : Boolean of whether congestion exceeds set congestion threshold}
def update_live_congestion(current_congestion, congestion_threshold):
    live_congestion = {}
    for edge_id, congeestion_level in current_congestion.items():
        # print('congestion level:' , str(congeestion_level))
        # print('congestion t:' , congestion_threshold)

        if congeestion_level > congestion_threshold:
            congested = True
        else:
            congested = f = False
        live_congestion[edge_id] = congested

    return live_congestion

# this function checks if there is congestion on any of the edges on the routs
def congestion_on_route(route, live_congestion):
    for edge_id in route:
        congestion = live_congestion[edge_id]
        # print(congestion)
        if congestion:
            return True

    return False

# takes the vehicles location and route and determines the edges left on it
def get_remaining_route(current_location, routes):
    # Find the index of the current location in the routes list
    try:
        current_index = routes.index(current_location)
    except ValueError:
        # print(f"Error: Current location '{current_location}' not found in the route.")
        return []

    # Extract the remaining route from the current location onwards
    remaining_route = routes[current_index + 1:]

    return remaining_route

# creates a dict with { edge_id : edge_length }
def get_network_length(network_edges):
    net_length = 0
    lanes = traci.lane.getIDList()
    # print(lanes)
    for lane in lanes:
        current_len = traci.lane.getLength(lane)
        net_length = net_length + current_len

    # for edge_id in network_edges:
    #     lanes = traci.lane.getIDList()
    #     print(lanes)
        

    return net_length

def density_function(density,exponent):
    a = 1.05
    b = exponent
    return 2 * math.exp((-1 * exponent ) + 1.05)

# SUMO simulation
def simulation(congestion_threshold, central_route, network_edges,baseline_edges_traveltime,increase_factor,exponent):
    run = True
    step = 0
    # vehicle_rerouted = [False] * trip_count
    rerouted_count = 0
    congestion_matrix = []
    live_congestion = {}
    # increase_factor = 1.02
    network_total_dist = get_network_length(network_edges)
    max_density = 0
    print('net_total_dist: ' + str(network_total_dist))
    # network_density = network_total_dist
    # print('\n\n net_total_dist: ' + str(network_total_dist))
    # edge_legnths = get_edge_length_dict(network_edges)
    # with open('density_log.txt', 'r') as file:
    #     file.close()
    while run:
        t.simulationStep()
        # Get Current Time Step Variables  -------------------------------------------------

        current_active_vehicles = traci.vehicle.getIDList()  # get a list of active vehicles
        # active_veh_count = len(current_active_vehicles)
        # current_travel_times = create_edges_current_traveltime(network_edges)
        # current_congestion = create_congestion_dict(current_travel_times,baseline_edges_traveltime)   # get a congestion dict for time step
        # print(current_congestion)
        # congestion_matrix.append(current_congestion)
        # live_congestion = update_live_congestion(current_congestion, congestion_threshold)  # get live congestion in boolean
        veh_count = t.vehicle.getIDCount()

        if veh_count > 0 : 
            veh_length = traci.vehicle.getLength(current_active_vehicles[0])
            density = (veh_count*veh_length)/network_total_dist

        if density > max_density: max_density = density
        
        with open('density_log.txt', 'a') as file:
            file.write(alg_name + '--  step: ' + str(step) + ", density: " +str(density) +'\n')

        increase_factor = density_function(density,exponent)
        # print('density: ' + str(density))
        # print('net_total_dist: ' + str(network_total_dist))

        # print("increae factor: " + str(increase_factor))

        # step 1: get the travel time on each edge
        edge_efforts = {}
        for edge_id in network_edges:
            edge_travel_time = traci.edge.getTraveltime(edge_id)
            edge_efforts[str(edge_id)] = str(edge_travel_time)

        for vehicle_id in current_active_vehicles:
            # Get Vehcile Details
            veh_location = traci.vehicle.getRoadID(vehicle_id)
            veh_route = traci.vehicle.getRoute(vehicle_id)
            veh_remaing_route = get_remaining_route(veh_location, veh_route)
            for edge_id in veh_remaing_route:
                edge_efforts[str(edge_id)] =  float(edge_efforts[str(edge_id)]) * increase_factor

        for edge_id in network_edges:
            # edge_travel_time = traci.edge.getTraveltime(edge_id)
            traci.edge.setEffort(edge_id, edge_efforts[str(edge_id)])

            

        # ----- Analyse Each Vehicle  ------------------------------------------------
        for vehicle_id in current_active_vehicles:
                traci.vehicle.setMaxSpeed(vehicle_id,max_vspeed)
                traci.vehicle.rerouteEffort(vehicle_id)
        # -----------------------------------------------------------------------------
        step += 1
        # print(step)
        last_step = step

        if t.vehicle.getIDCount() == 0:
            run = False
        


    return congestion_matrix, last_step, max_density, network_total_dist


def run_sim(congestion_threshold,increase_factor,exponent):
    if gui_bool: traci.start(["sumo-gui", "-c", config_file])     # Connect to SUMO simulation
    else: traci.start(["sumo", "-c", config_file])     # Connect to SUMO simulation

    #  Set up Code for measuring congestion
    network_edges = get_network_edges(net_file)                                 # gets a list of edges in the network
    baseline_edges_traveltime = create_edges_current_traveltime(network_edges)  # calculates the travel time for each edge at the start as a baseline
    # baseline_congestion = create_congestion_dict(baseline_edges_traveltime)
    network_distances = get_distances_in_net(path_to_sim_files + net_file)

    # Run the Simulation
    congestion_matrix,last_step, max_density, network_total_dist = simulation(congestion_threshold, central_route, network_edges,baseline_edges_traveltime,increase_factor,exponent)

    # Print out results
    # output_congestion_matrix(congestion_matrix, congestion_matrix_output_file)


    # Close TraCI connection - End Simulation
    traci.close()
    return last_step, max_density, network_total_dist

def set_config_file(network,path_to_sim_files,algorithm):
    # Sim input files Files
    config_file = path_to_sim_files + network + ".sumocfg"
    net_file = network + ".net.xml"
    set_sumocgf.set_netfile_value(config_file, net_file)
    set_sumocgf.set_route_file_value(config_file, "trip_files/trip_files_"+network+"/" + str(trip_count) + "tr_"+network+".trips.xml")
    set_sumocgf.set_routing_algo_value(config_file, "astar")

    # Sim output files
    output_file = "../out/"+alg_name+"_out/"+network+"_output_files/" + algorithm + "_" + str(trip_count) + "tr.out.xml"
    set_sumocgf.set_output_file_value(config_file, output_file)

    return config_file

def read_args():
    parser = argparse.ArgumentParser(description="Description of your script.")
    # Define arguments
    parser.add_argument("arg1", help="set the trip count")
    parser.add_argument("arg2", help="set the network")
    parser.add_argument("arg5", help="max v speed")
    parser.add_argument("arg4", help="gui?")

    # parser.add_argument("arg6", help="increase factor")


    # Parse arguments
    args = parser.parse_args()

    # Accessing arguments
    trip_count = args.arg1
    network = args.arg2
    congestion_threshold = 3
    central_route = True
    max_vspeed = float(args.arg5)
    increase_factor = 1
    
    gui = args.arg4
    if gui == 'Y' : gui_bool = True
    else : gui_bool = False

    # Return parsed arguments
    return trip_count, network, congestion_threshold, central_route,max_vspeed, increase_factor,gui_bool

if __name__ == "__main__":

    # Sim Constants - ie to be run before the start of each set up
    # last_step = 0

    # gui_bool = False
    alg_name = 'so_dynamic'
    out_directory = 'out/'+alg_name+'_out'
    exponent = 1000

    trip_count, network, congestion_threshold, central_route,max_vspeed,increase_factor,gui_bool = read_args()
    print("\nTrip count:", trip_count)
    print("Network:", network)
    print("Congestion threshold:", congestion_threshold)
    print("Max Speed:" + str(max_vspeed))   

    # File Details
    if central_route: algorithm = "cr"
    else: algorithm = 'astar'
    path_to_sim_files = "sim_files/"
    net_file = network + ".net.xml"

    
    # set the config files
    config_file = set_config_file(network,path_to_sim_files,algorithm)

    # Output file Locations
    congestion_matrix_output_file = out_directory+"/"+network+"_output_files/congestion_matrices/" + str(trip_count) + "tr_" + algorithm + "_cm.csv"
    rel_path_output_file = out_directory+"/"+network+"_output_files/" + algorithm + "_" + str(trip_count) + "tr.out.xml"

    print("congifg file:" + config_file)
    last_step,max_density, network_total_dist = run_sim(congestion_threshold,increase_factor,exponent)
    print("printing last ste from main() " + str(last_step))


    avg_time = average_time.get_avg(rel_path_output_file)
    log_file = out_directory+"/"+alg_name+'_sim_log.txt'
    log_results(log_file,network,algorithm,trip_count, congestion_threshold,avg_time,increase_factor, max_density, network_total_dist)


