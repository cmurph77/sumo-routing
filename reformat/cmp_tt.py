import xml.etree.ElementTree as ET
import argparse
import datetime

def parse_axml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    travel_times = {}

    for vehicle in root.findall('vehicle'):
        vehicle_id = vehicle.get('id')
        departure_time = float(vehicle.get('depart'))
        arrival_time = float(vehicle.get('arrival'))
        travel_time = arrival_time - departure_time
        travel_times[vehicle_id] = travel_time

    return travel_times

def compare_travel_times(ue_tt,so_tt):
    diff_array = []
    net_diff = 0
    so_slower = 0
    if len(ue_tt) != len(so_tt):
        print('uneven amount of trips in each file')
        return 
    else:
        sum_diff = 0
        for vehicle_id, travel_time in so_tt.items():
            diff = 0
            so_time = travel_time
            ue_time = ue_tt[vehicle_id]
            net_diff = net_diff + (so_time - ue_time)
            # print('UE TIME: ' + str(ue_time) + " , SO TIME: " + str(so_time))
            if so_time > ue_time:
                
                diff  = so_time - ue_time
                sum_diff = sum_diff + diff
                so_slower = so_slower + 1

    # print('SO SLOWER: ' + str(so_slower))
    avg_so_diff = round((sum_diff/so_slower),3)
    so_slower_percent = round(((so_slower/len(so_tt)) * 100),3)
    return so_slower_percent, avg_so_diff, diff_array, net_diff

def extract_travel_times(trip_count, network):
    filename = "out/so_simple_out/"+network+"_output_files/cr_"+str(trip_count)+"tr.out.xml"
    so_tt = parse_axml(filename)
    filename = "out/ue_simple_out/"+network+"_output_files/cr_"+str(trip_count)+"tr.out.xml"
    ue_tt = parse_axml(filename)
    return so_tt, ue_tt

def log_results(filename, network, tripcount,so_slower, avg_so_diff)  :
    # """Append a new line to a text file."""
    current_time = datetime.datetime.now()
    current_time = '[' + str(current_time) + '] , '
    line = str(current_time) + "Network: " + network + ", Trip Size: " + str(tripcount)+ ", SO Slower: " + str(round(so_slower,2)) + '% , Avg Diff:' + str(avg_so_diff) 
    with open(filename, 'a') as file:
        file.write(line + '\n')

def log_final_results(filename, network, trip_start, trip_end,so_slower_avg, mean_avg_so_diff ,mean_net_diff)  :
    # """Append a new line to a text file."""
    current_time = datetime.datetime.now()
    current_time = '[' + str(current_time) + '] , '
    line = str(current_time) + "Network: " + network + ", start_trip_count: " + str(trip_start)+ ", end_trip_count " + str(trip_end) + ", SO Slower Avg: " + str(round(so_slower_avg,2)) + '% , Avg Diff:' + str(mean_avg_so_diff) + 's , Avg Net Diff:' + str(mean_net_diff) 
    with open(filename, 'a') as file:
        file.write(line + '\n')

def cmp_all(network, start, end):
    so_slower_total = 0
    total_diff = 0
    total_net_diff = 0
    for i in range(start,end):
        so_tt, ue_tt = extract_travel_times(i, network)
        # print(i)
        so_slower_percent,avg_so_diff, diff_array ,net_diff = compare_travel_times(ue_tt,so_tt)
        so_slower_total = so_slower_total + so_slower_percent
        total_diff = total_diff + avg_so_diff
        total_net_diff = total_net_diff + net_diff
        # log_results('tt_cmp_log.txt',network,i,so_slower_percent,avg_so_diff)
        i = i + 1
    
    
    so_slower_average = so_slower_total/(i-start)
    mean_avg_so_diff = total_diff/(i-start)
    mean_net_diff = (total_net_diff/(i-start))/1000

    # so_slower_average_percentage = (so_slower_average/len(so_tt))*100   

    print('SO SLOWER AVERAGE (%): ' + str(so_slower_average) + '%')
    log_final_results('tt_cmp_log.txt',network,start,end,so_slower_average,mean_avg_so_diff, mean_net_diff)


# parser = argparse.ArgumentParser(description="Description of your script.")
# # Define arguments
# parser.add_argument("arg2", help="set the trip count")
# parser.add_argument("arg1", help="set the network")
# args = parser.parse_args()
# trip_count = args.arg1
# network = args.arg2

# so_tt, ue_tt = extract_travel_times(trip_count, network)
# slower = compare_travel_times(so_tt, ue_tt)
# print(str(slower))

x = 49


cmp_all('rand_20', 501,500 + x)
cmp_all('rand_20', 1001,1000 + x)
cmp_all('rand_20', 2001,2000 + x)
cmp_all('grid_10', 100,100 + x)
cmp_all('grid_10', 250,250 + x)
cmp_all('grid_10', 500,500 + x)

# print(result)
