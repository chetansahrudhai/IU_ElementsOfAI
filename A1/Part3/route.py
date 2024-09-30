#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Manuel Schabel / mschabe
#
# Based on skeleton code by V. Mathur and D. Crandall, Fall 2022
#
import math
from math import *
import time


# Function to read in city locations in dictionary
# Assumes following row-wise format: city,_state longitude latitude \n

def get_city_loc(filename):
    city_dict = dict()
    with open(filename, "r") as f:
        for line in f.readlines():
            city, latitude, longitude = line.split()
            city_dict[city] = float(latitude), float(longitude)

    return city_dict


# Function to read in (pairwise) road segments into dictionary
# Assumes following row-wise format: city1,_state city2,_state length(miles) speed-limit(mph) highway-name \n
# Read-in routine considers both directions for each segment, i.e city1->city2 AND city2->city1

def get_road_segments(filename):
    road_segments_dict = dict()
    with open(filename, "r") as f:
        for line in f.readlines():
            city1, city2, length, speed_limit, highway = line.split()
            road_segments_dict[city1, city2] = int(length), int(speed_limit), highway  # "forward" direction
            road_segments_dict[city2, city1] = int(length), int(speed_limit), highway  # "backward" direction

    return road_segments_dict


# Goal check function
def is_goal(city, goal):
    return city == goal


# Successor function, returns all road-connected cities as key with road segment data as values in dictionary
def successors(city, road_segments):
    select = dict()
    for connection, v in road_segments.items():
        if connection[0] == city:  # Identify all connected cities
            select[connection[1]] = list(v)
    return select


# Valid state check fct --> check if connected city has GPS data
def geoloc_state(city, city_locations):
    return city in city_locations


# Heuristic function: Use haversine formula to calculate "great circle" distance between two cities based on geodata
# Sources:
# 1. http://www.movable-type.co.uk/scripts/latlong.html
# 2. https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points

def h(start_city, end_city, city_locations, cost_type, max_speed_limit):
    # Extract geolocations
    lat_start, lon_start = city_locations[start_city]
    lat_end, lon_end = city_locations[end_city]

    R = 3960  # Earth radius in miles

    # Radians conversion
    lat_start, lon_start, lat_end, lon_end = map(radians, [lat_start, lon_start, lat_end, lon_end])

    # Calculation
    delta_lat = lat_end - lat_start
    delta_lon = lon_end - lon_start
    a = sin(delta_lat / 2) ** 2 + cos(lat_start) * cos(lat_end) * sin(delta_lon / 2) ** 2
    c = 2 * asin(sqrt(a))
    dist = R * c

    if cost_type == "distance":
        return dist
    elif cost_type == "time":
        return (dist / max_speed_limit)
    elif cost_type == "delivery":
        return (dist / max_speed_limit)
    elif cost_type == "segments":
        return 1

    return 0


# !/usr/bin/env python3
import sys


def get_route(start, end, cost):
    # Read in all city geolocations and road segments
    city_locations = get_city_loc("city-gps.txt")
    road_segments = get_road_segments("road-segments.txt")
    max_speed_limit = max([list(road_segments.values())[i][1] for i in range(len(road_segments))])

    # Fringe format: 0. Current city, 1. path_taken, 2. miles, 3. hours, 4. f(s)=h(s)+c(s),
    # 5. delivery_hours, 6. h(s), 7. no. of segments
    fringe = [[start, [], 0, 0, h(start, end, city_locations, cost, max_speed_limit), 0, 0, 0]]
    path_cities_visited = []
    cities_visited = {start: 0}  # Keep track of visited cities to only keep min distance route to city in fringe

    # A* algo with priority queue and heuristic fct.
    while len(fringe) > 0:
        f_temp = [fringe[i][4] for i in range(len(fringe))]  # extract f(s) of all states in fringe
        min_index = f_temp.index(min(f_temp))  # identify index with min f(s)
        fringe_to_pop = fringe.pop(min_index)

        # Goal check (not as part of successor loop below)
        if is_goal(fringe_to_pop[0], end):
            result = {"route-taken": fringe_to_pop[1], "total-segments": fringe_to_pop[7],
                      "total-miles": float(fringe_to_pop[2]), "total-hours": fringe_to_pop[3],
                      "total-delivery-hours": fringe_to_pop[5]}
            return result

        if len(fringe_to_pop[1]) > 0:
            path_cities_visited = [i[0] for i in fringe_to_pop[1]] + \
                                  [start]  # tracking of visited states (per individual path) to speed up runtime

        for new_city, data in successors(fringe_to_pop[0], road_segments).items():
            if new_city not in path_cities_visited:  # avoidance of path-specific loops

                # Segment data
                road_miles, speed_limit = data[:2]
                travel_time = road_miles / speed_limit

                # If city/jct without geodata, simply decrease last h(s) by cost (miles, time etc.) of last segment
                if geoloc_state(new_city, city_locations):
                    hf = h(new_city, end, city_locations, cost, max_speed_limit)
                else:  # h(s) >= 0 !
                    if cost == "distance":
                        hf = max(fringe_to_pop[6] - road_miles, 0)
                    elif cost in ["time", "delivery"]:
                        hf = max(fringe_to_pop[6] - travel_time, 0)
                    elif cost == "segments":
                        hf = fringe_to_pop[6]

                # Delivery cost (p = prob of mistake)
                if speed_limit < 50:
                    p = 0
                elif speed_limit >= 50:
                    p = math.tanh(road_miles / 1000)
                # Cumulated delivery time (i.e. past and current road segments)
                delivery_time = fringe_to_pop[5] + travel_time + 2 * p * (travel_time + fringe_to_pop[3])

                # c(s) -> cost to get to current state
                if cost == "distance":
                    current_cost = fringe_to_pop[2] + road_miles
                elif cost == "time":
                    current_cost = fringe_to_pop[3] + travel_time
                elif cost == "delivery":
                    current_cost = delivery_time
                elif cost == "segments":
                    current_cost = fringe_to_pop[7]

                # Assure that current city (new_city) in fringe is unique AND with min cost
                cities_fringe = [fringe[i][0] for i in range(len(fringe))]  # extract all cities from fringe
                if ((new_city not in cities_visited) or
                    ((new_city in cities_visited) and (current_cost < cities_visited[new_city]))):
                    if new_city in cities_fringe:
                        city_index = cities_fringe.index(new_city)  # identify index with new_city
                        del fringe[city_index]  # Delete city in fringe with greater cost (distance / travel time)

                    cities_visited[new_city] = current_cost  # Add min cost path to dict

                    # Append current city data to fringe
                    fringe.append([new_city,
                                   fringe_to_pop[1] + [(new_city, f"{data[2]} for {road_miles} miles")],  # path info
                                   fringe_to_pop[2] + road_miles,  # total miles
                                   fringe_to_pop[3] + travel_time,  # total hour
                                   current_cost + hf,  # c(s) + h(s) = f(s)
                                   delivery_time,  # Delivery time (in hours)
                                   hf,  # Current h(s)
                                   fringe_to_pop[7] + 1])  # No. of road segments


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


#    route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
#                  ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
#                   ("Indianapolis,_Indiana","IN_37 for 7 miles")]
#
#    return {"total-segments" : len(route_taken),
#            "total-miles" : 51.,
#            "total-hours" : 1.07949,
#            "total-delivery-hours" : 1.1364,
#            "route-taken" : route_taken}


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise (Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])
