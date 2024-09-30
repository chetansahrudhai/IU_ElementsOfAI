#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Megha Nagabhushana Reddy (menaga@iu.edu)
#
# Based on skeleton code by V. Mathur and D. Crandall, Fall 2022
#


# !/usr/bin/env python3
import sys
from queue import PriorityQueue
import math
from collections import deque
import time
def get_route(start, end, type_of_cost):
    temporary_start = start.split(',')
    route = []
    altered = end.split(',')
    roadsegment_dict, citygps_dict = build_path_dict()
    fringe = PriorityQueue()
    fringe.put((0, [temporary_start, route, 0], 0))
    visited = []

    while not fringe.empty():
        cost, city, ttrip = fringe.get()
        next_city = city[0]
        route = city[1]
        visited.append(next_city)

        for next in allpaths(roadsegment_dict, next_city, route):
            previouscost = float(city[2])
            if next:
                if next[0][0] + ',' + next[0][1] == end:
                    total_distance = 0.0
                    total_time = 0.0
                    return_total_dhours = 0.0
                    route_taken = []
                    for entry in next[1]:
                        initial_point, startstate, distance, speed, highway = entry
                        total_distance = total_distance + int(distance)
                        ipst = initial_point + ',' + startstate
                        highwayseg = highway + ' for ' + distance + ' miles'
                        hiway = f'"{highwayseg}"'
                        time = float(distance) / float(speed)
                        total_time = total_time + time

                        route_taken.append((ipst, highwayseg))
                        if int(speed) > 50:
                            return_total_dhours += time + ((2 * math.tanh(float(distance) / 1000)) * (time + return_total_dhours))
                        else:
                            return_total_dhours += time


                    return {"total-segments": len(route_taken),
                            "total-miles": total_distance,
                            "total-hours": total_time,
                            "total-delivery-hours": return_total_dhours,
                            "route-taken": route_taken}

                    # return "Found Path"  # return a dummy answer
                else:
                    if next[0] not in visited:
                        time1 = float(next[0][2]) / float(next[0][3])
                        if int(next[0][3]) > 50:
                            new_total_dhours = ttrip + time1 + ((2 * math.tanh(int(next[0][2]) / 1000)) * (ttrip + time1))
                        else:
                            new_total_dhours = ttrip + time1

                        visited.append(next[0])
                        # print("Visited Places after Insert: ", visited_places)
                        if type_of_cost == 'distance':
                            cost_1 = float(next[0][2])
                        elif type_of_cost == 'segments':
                            cost_1 = 1
                        elif type_of_cost == 'time':
                            cost_1 = float(next[0][2]) / float(next[0][3])
                        elif type_of_cost == 'delivery':
                            # Cost to move from
                            cost_1 = new_total_dhours

                        previouscost += cost_1
                        new_cost = astar_heuristic(next[0][0], next[0][1], altered[0], altered[1], citygps_dict, type_of_cost)
                        total_cost = new_cost + previouscost
                        fringe.put((total_cost, [next[0], next[1], previouscost], new_total_dhours))
    
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

 #   route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
 #                  ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
 #                  ("Indianapolis,_Indiana","IN_37 for 7 miles")]
 #   
 #   return {"total-segments" : len(route_taken), 
 #           "total-miles" : 51., 
 #           "total-hours" : 1.07949, 
 #           "total-delivery-hours" : 1.1364, 
 #           "route-taken" : route_taken}

def build_path_dict():
    with open("city-gps.txt", "r") as citygps:
        lines = citygps.read().splitlines()

    City_GPS_Dict = {}

    for entry in lines:
        P1 = entry.split(',')
        city = P1[0]
        P2 = P1[1].split(' ')
        state = P2[0]
        latitude = P2[1]
        long = P2[2]
        City_GPS_Dict[city, state] = [latitude, long]
    # print(CityGPSDict['"Y"_City','_Arkansas'])

    with open("road-segments.txt", "r") as segment:
        segment_lines = segment.read().splitlines()

    roadsegment_dict = {}

    for entry in segment_lines:
        P1Seg = entry.split(',')
        fromCity = P1Seg[0]
        P_2 = P1Seg[1].split(' ')
        fromState = P_2[0]
        toCity = P_2[1]
        remaining_Segments = P1Seg[2].split(' ')
        toState = remaining_Segments[0]
        distance = remaining_Segments[1]
        speed_limit = remaining_Segments[2]
        highway_Name = remaining_Segments[3]

        Key = fromCity + ',' + fromState
        if Key in roadsegment_dict.keys():
            roadsegment_dict[Key].append([toCity, toState, distance, speed_limit, highway_Name])
        else:
            roadsegment_dict[Key] = [[toCity, toState, distance, speed_limit, highway_Name]]

        Key1 = toCity + ',' + toState
        if Key1 in roadsegment_dict.keys():
            roadsegment_dict[Key1].append([fromCity, fromState, distance, speed_limit, highway_Name])
        else:
            roadsegment_dict[Key1] = [[fromCity, fromState, distance, speed_limit, highway_Name]]
    return roadsegment_dict, City_GPS_Dict

def allpaths(roadsegment_dict, next_city, route):
    key_of_city = next_city[0] + ',' + next_city[1]
    for keys in roadsegment_dict.keys():
        if key_of_city.lower() == keys.lower():
            temporary_list = roadsegment_dict[keys]
            temporary_list = [[element, route + [element]] for element in temporary_list]
            return temporary_list
    return []


def astar_heuristic(start_city, start_state, goal_city, goal_state, City_GPS, costtype):


    if ((start_city, start_state) in City_GPS) and ((goal_city, goal_state) in City_GPS):

        latitude1, longitude1 = (City_GPS[start_city, start_state])
        latitude2, longitude2 = City_GPS[goal_city, goal_state]

        latitude1 = float(latitude1)
        longitude1 = float(longitude1)

        latitude2 = float(latitude2)
        longitude2 = float(longitude2)

        radius = 3596
        longitude1, latitude1, longitude2, latitude2 = map(math.radians, [longitude1, latitude1, longitude2, latitude2])
        # haversine formula
        diff_longitude = longitude2 - longitude1
        diff_latitude = latitude2 - latitude1
        a = math.sin(diff_latitude / 2) ** 2 + math.cos(latitude1) * math.cos(latitude2) * math.sin(diff_longitude / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))

        d = radius * c
        if costtype == "distance":
            return d
        elif costtype == "time":
            return (d / 70)
        elif costtype == "segments":
            return 1
        elif costtype == "delivery":
            return (d / 70)

    return 0


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

     # Initialize timer
    start_time = time.time()

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])
      # Display runtime
    print(f"Runtime: {(time.time() - start_time)} seconds")
