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

def sim_gen():
    # Open file in write mode ('w' mode)
    with open("write_bash_out.txt", "w") as file:
        # Write "Hello, world!" to the file
        iterations = 50
        start_iter = 0
        trip_filecount = 1000
        for i in range(0,iterations):
            file.write('python3 so_simple.py     '+str(trip_filecount)+' rand_20 3 15.00\n')
            file.write('python3 ue_simple.py '+str(trip_filecount)+' rand_20 3 15.00\n')
            trip_filecount = trip_filecount + 1



if __name__ == "__main__":
    sim_gen()
