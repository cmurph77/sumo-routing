def trip_gen():
    # Open file in write mode ('w' mode)
    with open("write_bash_out.txt", "w") as file:
        # Write "Hello, world!" to the file

        iterations = 45
        start_iter = 0
        trip_gen_line = 'python3 /opt/homebrew/share/sumo/tools/randomTrips.py -n ../../rand_20.net.xml -e 1000 --random\n'
        trip_filecount = 1006
        for i in range(0,iterations):
            file.write(trip_gen_line)
            file.write("mv trips.trips.xml "+str(trip_filecount)+"tr_rand_20.trips.xml\n\n")
            trip_filecount = trip_filecount + 1

def sim_gen1():
    # Open file in write mode ('w' mode)
    with open("write_bash_out.txt", "w") as file:
        # Write "Hello, world!" to the file
        iterations = 50
        start_iter = 0
        trip_filecount = 2000
        for i in range(0,iterations):
            file.write('python3 so_simple.py     '+str(trip_filecount)+' net_001 3 15.00 1.01\n')
            file.write('python3 ue_simple.py '+str(trip_filecount)+' net_001 3 15.00\n')
            trip_filecount = trip_filecount + 1


def sim_gen2():
    'python3 so_simple.py 500 tree_23_tl 3 5 1.01'
    with open("write_bash_out.txt", "w") as file:
        # Write "Hello, world!" to the file
        iterations = 50
        start_iter = 0
        factor = 1
        for i in range(0,iterations):
            file.write('python3 so_simple.py 500 tree_23_tl 3 5 ' + str(round(factor,3))+ '\n')
            factor = factor + 0.001

def gen_trips():
    with open("write_bash_out.txt", "w") as file:
            # Write "Hello, world!" to the file
            iterations = 50
            start_iter = 0
            trip_filecount = 2000
            for i in range(0,iterations):
                file.write('python3 /opt/homebrew/share/sumo/tools/randomTrips.py -n /Users/cianmurphy/code_directories/sumo-routing/reformat/sim_files/net_001.net.xml  -e 500 --random --period 0.25\n')
                file.write('mv trips.trips.xml '+str(trip_filecount)+'tr_net_001.trips.xml\n')
                trip_filecount = trip_filecount + 1

if __name__ == "__main__":
    sim_gen2()
