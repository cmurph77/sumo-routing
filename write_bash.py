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
        trip_filecount = 1000
        for i in range(0,iterations):
            file.write('python3 so_simple.py '+str(trip_filecount)+' grid_10 3 15.00 *need-to-set\n')
            file.write('python3 ue_simple.py '+str(trip_filecount)+' grid_10 3 15.00 \n')
            trip_filecount = trip_filecount + 1

def sim_gen2():
    with open("write_bash_out.txt", "w") as file:
        # Write "Hello, world!" to the file
        iterations = 21
        start_iter = 0
        factor = 1
        for i in range(0,iterations):
            file.write('python3 so_dynamic.py 500 rand_20 ' + str(round(factor,3))+ ' 15.00 1.025\n')
            factor = factor - 0.05

def sim_gen3():
    with open("write_bash_out.txt", "w") as file:
            # Write "Hello, world!" to the file
            iterations = 21
            start_iter = 0
            factor = 1
            for i in range(0,iterations):
                for trip_count in range(1000,1010):
                    file.write('python3 so_simple.py '+str(trip_count)+' grid_10 3 15 ' + str(round(factor,3))+ '\n')
                    trip_count = trip_count + 1
                factor = factor - 0.05

def gen_trips():
    with open("write_bash_out.txt", "w") as file:
            # Write "Hello, world!" to the file
            iterations = 50
            start_iter = 0
            trip_filecount = 1000
            for i in range(0,iterations):
                file.write('python3 /opt/homebrew/share/sumo/tools/randomTrips.py -n ../../grid_10.net.xml -e 1000 --random --period 1\n')
                file.write('mv trips.trips.xml '+str(trip_filecount)+'tr_grid_10.trips.xml\n')
                trip_filecount = trip_filecount + 1

if __name__ == "__main__":
    
    sim_gen2()
