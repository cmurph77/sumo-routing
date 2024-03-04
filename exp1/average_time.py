import xml.etree.ElementTree as ET
import csv
import matplotlib.pyplot as plt
import numpy as np
import argparse


# Strores the overal sim results for each trip size
t1_average_tt = []
t2_average_tt = []
same_route_counts = []
same_tt_counts = []

print_results_to_conole = True



def parse_data(data):
    parsed_data = {}
    for entry in data:
        key = list(entry.keys())[0]
        value = list(entry.values())[0]
        parsed_data[key] = value
    return parsed_data


def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root

def extract_vehicle_data(vehicle):
    depart = float(vehicle.attrib['depart'])
    arrival = float(vehicle.attrib['arrival'])
    travel_time = arrival - depart
    
    vehicle_data = {
        'depart': depart,
        'arrival': arrival,
        'travel_time': travel_time,
       'route': [route.attrib['edges'] for route in vehicle.findall('.//route[@edges]')]
    }
    return vehicle_data

def extract_routes(xml):
    routes = {}
    i = 0
    for vehicle in xml.findall('vehicle'):
        i = i +1
        vehicle_id = int(vehicle.attrib['id'])
        vehicle_id = vehicle.attrib['id']
        try:
            vehicle_id_integer = int(vehicle_id)
            # Now vehicle_id_integer holds the integer value of vehicle_id
        except ValueError:
            print("Error: vehicle_id is not a valid integer")


        routes[vehicle_id] = extract_vehicle_data(vehicle)
    return routes

def func_1(trips1,trips):

        num_trips = len(trips1)
        trip1_tot_tt = 0;
        for i in range(0,(len(trips1))):
            trip1_tt = trips1[str(i)]['travel_time']
            trip1_tot_tt = trip1_tot_tt + trip1_tt;

        # Calculate Average Travel Times
        trip1_avg_tt = trip1_tot_tt/num_trips;

        return trip1_avg_tt

def get_avg(fname):
    xml1 = parse_xml(fname)
    trips1 = extract_routes(xml1)
    return func_1(trips1,1000)


if __name__ == "__main__":
    file = "/Users/cianmurphy/code_directories/final_year_project/experiments/central_routing/cr_exp1/rand_20_output_files/cr_1500tr.out.xml"
    avg = get_avg(file)
    print("----------- AVERAGE: " + str(avg))








    
    