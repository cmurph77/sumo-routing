import datetime

def write_new_line(filename, network, algorithm, trip_size, ct,avg_tt):
    """Append a new line to a text file."""
    current_time = datetime.datetime.now()
    current_time = '[' + str(current_time) + '] , '
    line = str(current_time) + "Network: " + network + ", Trip Size: " + str(trip_size)+ ", Average Time: " + str(avg_tt)  + ", Algo: "  +algorithm+ ", Congestion T: " + str(ct)
    with open(filename, 'a') as file:
        file.write(line + '\n')

write_new_line('simulation_log.txt','net_001','cr',1000,5,67)