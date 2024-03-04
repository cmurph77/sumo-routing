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

def graph_results(data1, data2,title,ylabel,labels,file1_name,file2_name):
    # labels = list(data1.keys())
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()

    values1 = [list(entry.values())[0] for entry in data1]
    values2 = [list(entry.values())[0] for entry in data2]


    rects1 = ax.bar(x - width/2, values1, width, label=file1_name)
    rects2 = ax.bar(x + width/2, values2, width, label=file2_name)

    ax.set_xlabel('Trips')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.show()

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

def create_csv(trips1,trips2,output_filename,filename_1,filename_2,trips):
    # Open a CSV file in write mode
    if print_results_to_conole: print("\nComparing " + filename_1 + " & " + filename_2 + " -> output file: " + output_filename)
    with open(output_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        trips1_name = filename_1
        trips2_name = filename_2

        if len(trips1) != len(trips2):
            print("Error: There is not the same number of trips in both files")

        num_trips = len(trips1)
    

        # Write each row of data to the CSV file
        # write in the header row
        writer.writerow(['id',
                         trips1_name+'_dep',
                         trips2_name+'_dep',
                         trips1_name+'_arr',
                         trips2_name+'_arr',
                         trips1_name+'_route',
                         trips2_name+'_route',
                         trips1_name+'_traveltime',
                         trips2_name+'_traveltime',
                         'same_traveltime?',
                         "same_route?",
                        ])
        # size 
        # store the total trip times
        trip1_tot_tt = 0;
        trip2_tot_tt = 0;
        same_route_count = 0
        same_tt_count = 0
    

        for i in range(0,(len(trips1))):
            
            # print("i:" + str(trips1[str(i)]))
            # Load in data from the trips1 and 2
            trip1_rou = trips1[str(i)]['route']
            trip2_rou = trips2[str(i)]['route']
            trip1_tt = trips1[str(i)]['travel_time']
            trip2_tt = trips2[str(i)]['travel_time']

            # Update the total trip times
            trip1_tot_tt = trip1_tot_tt + trip1_tt;
            trip2_tot_tt = trip2_tot_tt + trip2_tt;

            # Check is the trip time is the same
            if trip1_tt == trip2_tt:
                same_time = True
                same_tt_count = same_tt_count + 1
            else :
                same_time = False

            # Check if the route is the same
            if (trip1_rou == trip2_rou):
                same_route = True
                same_route_count = same_route_count + 1
            else: 
                same_route = False

            # Write the data to a new line
            writer.writerow([i,
                             trips1[str(i)]['depart'],
                             trips2[str(i)]['depart'],
                             trips1[str(i)]['arrival'],
                             trips2[str(i)]['arrival'],
                             trips1[str(i)]['route'],
                             trips2[str(i)]['route'],
                             trips1[str(i)]['travel_time'],
                             trips2[str(i)]['travel_time'],
                            same_time,
                            same_route,
                             ])
            
        # store same rout and same time count
        same_route_counts.append({trips:same_route_count})
        same_tt_counts.append({trips:same_tt_count})


        # Calculate Average Travel Times
        trip1_avg_tt = trip1_tot_tt/num_trips;
        t1_average_tt.append({trips:trip1_avg_tt})
        trip2_avg_tt = trip2_tot_tt/num_trips;
        t2_average_tt.append({trips:trip2_avg_tt})
        # speed_up =  (float(t2_average_tt) / float(t1_average_tt))* 100
        if print_results_to_conole:
            print("    " +filename_1 + ' Average Time: ' +  str(trip1_avg_tt))
            print("    " +filename_2 + ' Average Time: ' +  str(trip2_avg_tt))
            print("    Same Route Count: " +str(same_route_count) + "/ " + trips)
            print("    Same Time Count:  " + str(same_tt_count) + "/ " + trips)
            # print("    PERECENTAGE AVG SPEED REDUCTION: " + str(t))

            print("    CSV file " + output_filename+" has been created.\n")

def compare_output_files(output_filename, xml1, xml2,filename_1,filename_2,trips):
    trips1 = extract_routes(xml1)
    trips2 = extract_routes(xml2)
    
    # sort the trips by id
    sorted_trips1 = dict(sorted(trips1.items()))
    sorted_trips2 = dict(sorted(trips2.items()))

    # for i in range (0,len(sorted_trips1)):
    #     print(str(i) + ": " + str(sorted_trips1[str(i)]))

    # print(sorted_trips2)

    create_csv(sorted_trips1,sorted_trips2,output_filename,filename_1,filename_2,trips)

    
def create_overall_csv(out_filename, t1_average_tt, t2_average_tt,same_routes,same_times):
    x_axis_keys = [list(entry.keys())[0] for entry in t1_average_tt]
    t1_average_time_vals =  [list(entry.values())[0] for entry in t1_average_tt]
    t2_average_time_vals =  [list(entry.values())[0] for entry in t2_average_tt]
    same_routes_vals = [list(entry.values())[0] for entry in same_routes]
    same_times_vals = [list(entry.values())[0] for entry in same_times]

    # print(x_axis_keys)
    # print(t1_average_time_vals)
    # print(t2_average_time_vals)
    # print(same_routes_vals)
    # print(same_times_vals)

    combined_data = zip(x_axis_keys, t1_average_time_vals, t2_average_time_vals, same_routes_vals,same_times_vals)
    # Combine arrays into a list of tuples
    # combined_data = list(zip(array1, array2, array3, array4))

    # Transpose the data
    transposed_data = np.array(combined_data).T.tolist()


    # Write data to CSV file
    with open(out_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['Number of Trips', 't1_avg', 't2_avg', 'same_route?', 'same_time'])
        # Write data columns
        writer.writerows(transposed_data)


if __name__ == "__main__":

    # Read in Arguments
    parser = argparse.ArgumentParser(description='Description of your script.')

    # Add arguments
    parser.add_argument('arg1', type=str, help='Description of argument 1')
    # parser.add_argument('arg2', type=str, help='Description of argument 2')

    # Parse arguments
    args = parser.parse_args()
    network = args.arg1

    if network == 'grid_10':     trips_array = [500,1000,1500,2000]
    if network == 'rand_20':     trips_array = [500,1000,1250,1500]
    if network == 'net_001':     trips_array = [1000,2000,3000,4000]

    f1_exp = '1'
    f2_exp = '2'
    f1 = 'cr'
    f2 = 'cr'

    # network = "rand_20"
    print(" \n\n---------- PRINTING RESULTS FOR NETWORK: " + network + "-------------")

    for trip_count in trips_array:
        file1_name = "Exp:"+f1_exp+", Trip Count: " + str(trip_count) + ", Algo: " + f1
        file1 = "exp"+f1_exp+"/"+network+"_output_files/"+f1+"_" + str(trip_count) + "tr.out.xml"
        xml1 = parse_xml(file1)
        file2_name = "Exp:"+f2_exp+", Trip Count: " + str(trip_count) + ", Algo: " + f2
        file2 = "exp"+f2_exp+"/"+network+"_output_files/"+f2+"_" + str(trip_count) + "tr.out.xml"
        xml2 = parse_xml(file2)
        output_file_loc = "exp"+f1_exp+"/"+network+"_output_files/" + str(trip_count) + "tr_crVa.csv"
        compare_output_files(output_file_loc,xml1, xml2,file1_name,file2_name,str(trip_count))




    graph_results(t1_average_tt,t2_average_tt,"Average Travel Time on Netowrk: " + network, "Travel Time (seconds)",trips_array,file1_name,file2_name)







    
    