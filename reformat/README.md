Algorothms

og_cr.py:

so_v1.py:
this is for use on the tree_tl network. It assigns each vehile that enters the path a route. There are four routes defined and an even amount of vehicles are assigned to each route

so_v3.py:
this was copied from og_cr, it only allows vehicele to reroute if they ar ein the top 50% of travel times. Essentially is orders the list of vehicles by traveltime and allows half the vehiceles to reroute that have veen on the netowrk the longest

so_v4.py:
this was copied from so_v3. it sorts active vehicles by distanct left and gives priority to shortest paths left - ie letteing the bottom half of vehicles reroute

so_v5.py:
this was copied from so_v3. it sorts active vehicles by distanct left and gives priority to longest paths left - ie letteing the top half of vehicles reroute. similar to v4 but used a longest first approach
