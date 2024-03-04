import traci as t
import traci
import xml.etree.ElementTree as ET
import csv
import set_sumocgf
import random
import argparse
import average_time
import numpy as np

import datetime

def log_results(filename, network, algorithm, trip_size, ct,avg_tt):
    """Append a new line to a text file."""
    current_time = datetime.datetime.now()
    current_time = '[' + str(current_time) + '] , '
    line = str(current_time) + "Network: " + network + ", Trip Size: " + str(trip_size)+ ", Average Time: " + str(avg_tt)  + ", Algo: "  +algorithm+ ", Congestion T: " + str(ct)
    with open(filename, 'a') as file:
        file.write(line + '\n')

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
def set_edge_length_dict():
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


# SUMO simulation
def simulation(congestion_threshold, central_route, network_edges,baseline_edges_traveltime):
    run = True
    step = 0
    # vehicle_rerouted = [False] * trip_count
    rerouted_count = 0
    congestion_matrix = []
    live_congestion = {}

    while run:
        t.simulationStep()
        # Get Current Time Step Variables  -------------------------------------------------

        current_active_vehicles = traci.vehicle.getIDList()  # get a list of active vehicles
        active_veh_count = len(current_active_vehicles)
        current_travel_times = create_edges_current_traveltime(network_edges)
        current_congestion = create_congestion_dict(current_travel_times,baseline_edges_traveltime)   # get a congestion dict for time step
        # print(current_congestion)
        # add to congestion matrix
        congestion_matrix.append(current_congestion)
        live_congestion = update_live_congestion(current_congestion, congestion_threshold)  # get live congestion in boolean

        # ----- Analyse Each Vehicle  ------------------------------------------------

        if central_route:
            for vehicle_id in current_active_vehicles:

                # Get Vehcile Details
                veh_location = traci.vehicle.getRoadID(vehicle_id)
                veh_route = traci.vehicle.getRoute(vehicle_id)
                veh_remaing_route = get_remaining_route(
                    veh_location, veh_route)
                
                # print(live_congestion)

                # Check if there is congestion on the route
                if congestion_on_route(veh_remaing_route, live_congestion):
                    # print("rereruoting vehicles")

                    rerouted_count = rerouted_count + 1
                    # print("   veh_id: " + str(vehicle_id) + ", location: " + str(veh_location)+ " | route = " + str(veh_route) + " | left = " + str(veh_remaing_route) )
                    traci.vehicle.rerouteTraveltime(vehicle_id)
                    # vehicle_rerouted[int(vehicle_id)] = True

        # -----------------------------------------------------------------------------
        step += 1
        if t.vehicle.getIDCount() == 0:
            run = False

    return congestion_matrix


def run_sim(congestion_threshold):
    traci.start(["sumo", "-c", config_file])     # Connect to SUMO simulation

    #  Set up Code for measuring congestion
    network_edges = get_network_edges(net_file)                                 # gets a list of edges in the network
    baseline_edges_traveltime = create_edges_current_traveltime(network_edges)  # calculates the travel time for each edge at the start as a baseline
    # baseline_congestion = create_congestion_dict(baseline_edges_traveltime)
    network_distances = get_distances_in_net(path_to_sim_files + net_file)

    # Run the Simulation
    congestion_matrix = simulation(congestion_threshold, central_route, network_edges,baseline_edges_traveltime)

    # Print out results
    output_congestion_matrix(congestion_matrix, congestion_matrix_output_file)

    # Close TraCI connection - End Simulation
    traci.close()

def set_config_file(network,path_to_sim_files,algorithm):
    # Sim input files Files
    config_file = path_to_sim_files + network + ".sumocfg"
    net_file = network + ".net.xml"
    set_sumocgf.set_netfile_value(config_file, net_file)
    set_sumocgf.set_route_file_value(config_file, "../trip_files_"+network+"/" + str(trip_count) + "tr_"+network+".trips.xml")
    set_sumocgf.set_routing_algo_value(config_file, "astar")

    # Sim output files
    output_file = "../"+network+"_output_files/" + algorithm + "_" + str(trip_count) + "tr.out.xml"
    set_sumocgf.set_output_file_value(config_file, output_file)

    return config_file

def read_args():
    parser = argparse.ArgumentParser(description="Description of your script.")
    # Define arguments
    parser.add_argument("arg1", help="set the trip count")
    parser.add_argument("arg2", help="set the network")
    parser.add_argument("arg3", help="set the congestion threshold")
    parser.add_argument("arg4", help="centrally route? Y/N")

    # Parse arguments
    args = parser.parse_args()

    # Accessing arguments
    trip_count = args.arg1
    network = args.arg2
    congestion_threshold = int(args.arg3)
    central_route = args.arg4 == 'Y'  # Convert 'Y' to True, 'N' to False

    # Return parsed arguments
    return trip_count, network, congestion_threshold, central_route

if __name__ == "__main__":

    # Sim Constants - ie to be run before the start of each set up


    # Simulation Parameters
    # trip_count = 1000
    # network = "net_001"
    # congestion_threshold = 5    
    # central_route = False

    trip_count, network, congestion_threshold, central_route = read_args()
    print("Trip count:", trip_count)
    print("Network:", network)
    print("Congestion threshold:", congestion_threshold)
    print("Centrally route:", central_route)    

    # File Details
    if central_route: algorithm = "cr"
    else: algorithm = 'astar'
    path_to_sim_files = "sim_files/"
    net_file = network + ".net.xml"

    
    # set the config files
    config_file = set_config_file(network,path_to_sim_files,algorithm)

    # Output file Locations
    congestion_matrix_output_file = network+"_output_files/congestion_matrices/" + str(trip_count) + "tr_" + algorithm + "_cm.csv"
    rel_path_output_file = network+"_output_files/" + algorithm + "_" + str(trip_count) + "tr.out.xml"

    run_sim(congestion_threshold)
    avg_time = average_time.get_avg(rel_path_output_file)
    log_results('exp1sim_log.txt',network,algorithm,trip_count, congestion_threshold,avg_time)


    # ------------------ RUN WITH MULTIPLE TRIPS --------------------------
    # results = {}
    # results['TRIPS_NO'] = 'AVG_TIME'
    # trip_sizes = [1000,2000,3000,400]
    # # Run Simulation
    # for trip_no in trip_sizes:
    #     congestion_matrix_output_file = network+"_output_files/congestion_matrices/" + str(trip_count) + "tr_" + algorithm + "_cm.csv"
    #     rel_path_output_file = network+"_output_files/" + algorithm + "_" + str(trip_count) + "tr.out.xml"
    #     trip_count = trip_no
    #     congestion_threshold = 5
    #     run_sim(congestion_threshold)
    #     avg_time = average_time.get_avg(rel_path_output_file)
    #     results[str(trip_no)] = str(avg_time)
    #     print("\n\n\n")
    #     write_dict_to_file(results, "net_001_avg_tts.txt")
    #     print(results)

    # print("\n\n\n")
    # # write_dict_to_file(results, "r20_1to100ct_1000tr_.txt")
    # print(results)
