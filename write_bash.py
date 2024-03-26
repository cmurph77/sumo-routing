def main():
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

if __name__ == "__main__":
    main()
