# Path name
/Users/cianmurphy/code_directories/final_year_project/experiments/dva/dva_exp1

# Generate Network
link: https://sumo.dlr.de/docs/netgenerate.html
command netgenerate --rand ----rand.iterations 20


# for generating random trips
python3 /opt/homebrew/share/sumo/tools/randomTrips.py -n /Users/cianmurphy/code_directories/final_year_project/experiments/central_routing/cr_exp1/random_20.net.xml -e 50

# for generating routes
duarouter --trip-files=trips.trips.xml --net-file=random_20.net.xml --routing-algorithm astar --output-file=atar-routes.rou.xml
duarouter --trip-files=trips.trips.xml --net-file=random_20.net.xml --routing-algorithm dijkstra --output-file=dijsktra-routes.rou.xml

duarouter --trip-files=trips.trips.xml --net-file=random_20.net.xml --routing-algorithm dijkstra --output-file=dfrouter-routes.rou.xml

# what ive done
1. created a small network of 20 nodes
2. generated 'n' random trips on the network
3. ran the simulation for a varying size of n using both djikstra and astar
4. stored the resulsts in the results directory using 'd' for dijkstra and 'a' for astar
5. the results are compared in the excel workbook
