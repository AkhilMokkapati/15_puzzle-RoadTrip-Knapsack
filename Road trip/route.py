#!/usr/local/bin/python3
#
# Code by: Vivek Shreshta, Akhil Mokkapati, Vijay Sai Kondamadugu  - vivband, akmokka, vikond
#
# Based on skeleton code by D. Crandall, September 2019
#
# The program uses A* search, using desired heuristics, respective to a particular
# case until the desired goal state(Destination city) is reached.
#
# The road-segments.txt is parsed into a dictionary such that each segment has two mappings
# a->b mapping and b->a mapping provided a and b are city names.
# The key would be the city name and the value would be a list of cities and their respective data.
# This way, getting successors for a city would be of almost O(1) time.
#
# The city-gps.txt file too is parsed into a dictionary. The key name would be the city name and the
# value would be the longitude and latitudes. This data is used for calculating the eucledian distances
#
# State space: All the mappings present in the file, road segment
# Edge weights:
# If cost function is segments, then the edge weight is 1
# If the cost function is distance, then the length of the length of the road
# If the cost function is time, then distance/speed of the on the road is the edge weight
# If the cost function is mpg, then distance of the road/(400*v(1− v/150 )^4)/150 is the edge weight

# Goal state: Destination provided by the user

# Heuristic functions:
# SEGMENTS: We take the biggest road length(Calculated during the parsing of road-segments.txt)
# and is divided with the eucledian distance of the successor and the destination city.
# This way, we get the minimum number of segments that can be there between the successor and the destination city.
# DISTANCE: By using the GPS, we calculate the Eucledian distance between the current city and the destination city.
# Since the Eucledian distance is the least amount of distance, this heuristic is admissible.
# TIME: Its calculated by dividing the Eucledian distance from the successor to the destination by the max highway speed,
# we get the Heuristic. The max highway speed is computed during the road-segments.txt.
# This heuiristic is admissible since the time can never go below the distance/(current speed).
# MPG: By calculating the max gas consumed during the parsing of road-segments.txt and dividing it with the current eucledian
# distance to the destination city, we get the admissible heuristic of mpg.
#
# Assumptions and simplifications
#
# If a point in road segments is not in gps file, then the distance is considered as 0.
#
from queue import PriorityQueue
import sys
from math import pow
from copy import deepcopy
from math import sqrt


# return a list of possible successor states
def successors(road_segments, cities_traversed):
    # Things to return
    # new_miles, new_hours, new_gas_gallons, new_path
    # road_segments[cityA] = [(cityB, road_length, speed_limit, name)]
    current_city = cities_traversed[len(cities_traversed) - 1]
    successors_list = []

    for (next_city, road_length, speed_limit, name) in road_segments.get(current_city):
        if next_city not in cities_traversed:
            new_path = deepcopy(cities_traversed)
            new_path.append(next_city)
            successors_list.append((road_length, float(road_length) / float(speed_limit),
                                    calculate_gas_consumption(float(road_length), speed_limit), new_path))
    return successors_list


# This heuristic gives us the least possible gas consumption from the successor to the destination city
def calculate_gas_consumption(road_length, speed_limit):
    return road_length / mpg(speed_limit)


def mpg(speed_limit):
    return pow(1 - float(speed_limit) / 150, 4) * float(speed_limit) * 8 / 3


# check if we've reached the goal
def is_goal(start_city, current_city):
    return start_city == current_city


# Calculates the eucledian distance from the current city(The one we got from the successor) to the destination city
# This is an admissible heuristic since the heuristic never overestimates the distance between two cities
def distance_to_destination(city_gps, current_city, destination_city):
    if city_gps.get(current_city) is None:
        return float(0)
    (latitude1, longitude1) = city_gps.get(current_city)
    (latitude2, longitude2) = city_gps[destination_city]
    return sqrt(pow(float(latitude1) - float(latitude2), 2) + pow(float(longitude1) - float(longitude2), 2))


# The max speed is calculated during the parsing of road-segments.txt. This heuristic never overestimates since the
# max time to the destination city can never be lower than the current time since we're considering the max speed
def time_heuristic(max_speed, city_gps, current_city, destination_city):
    return distance_to_destination(city_gps, current_city, destination_city) / max_speed


def gas_consumption_heuristic(max_mpg, city_gps, current_city, destination_city):
    return distance_to_destination(city_gps, current_city, destination_city) / max_mpg


def segment_heuristic(max_segment_length, city_gps, current_city, destination_city):
    return distance_to_destination(city_gps, current_city, destination_city) / max_segment_length


def solve(city_gps, road_segments, start_city, destination_city, variant, max_speed, max_mpg, max_segment_length):
    if is_goal(start_city, destination_city):
        return '', '', '', []

    visited = []
    # This is a list of all the cities in the path. This list is maintained for each mapping in the fringe for
    # knowing the cities traversed
    path = [start_city]
    fringe = PriorityQueue()
    fringe.put((0, 0, 0, 0, path))

    while not fringe.empty():
        (cost, total_miles, total_hours, total_gas_gallons, path) = fringe.get()
        visited.append(path[len(path) - 1])

        if is_goal(destination_city, path[len(path) - 1]):
            return total_miles, total_hours, total_gas_gallons, path

        for (new_miles, new_hours, new_gas_gallons, new_path) in successors(road_segments, path):
            if new_path[len(new_path) - 1] not in visited:
                if variant == 'segments':
                    fringe.put((len(new_path) + segment_heuristic(max_segment_length, city_gps, new_path[len(new_path) - 1], destination_city),
                                int(total_miles) + int(new_miles), float(total_hours) + float(new_hours),
                                float(total_gas_gallons) + float(new_gas_gallons), new_path))
                elif variant == 'distance':
                    # Distance is found from road_segments and the heuristic is calculated b/n the second city and final city. It should be short
                    fringe.put((int(total_miles) + int(new_miles) + distance_to_destination(city_gps, new_path[len(new_path) - 1], destination_city),
                                int(total_miles) + int(new_miles),
                                float(total_hours) + float(new_hours),
                                float(total_gas_gallons) + float(new_gas_gallons), new_path))
                elif variant == 'time':
                    # Time is found by dividing the distance by velocity.
                    fringe.put((float(total_hours) + float(new_hours) +
                                time_heuristic(max_speed, city_gps, new_path[len(new_path) - 1], destination_city),
                                int(total_miles) + int(new_miles),
                                float(total_hours) + float(new_hours),
                                float(total_gas_gallons) + float(new_gas_gallons), new_path))
                elif variant == 'mpg':
                    # MPG(v)=(8*v(1 − v/150)^4)/3
                    fringe.put((float(total_gas_gallons) + float(new_gas_gallons) +
                                gas_consumption_heuristic(max_mpg, city_gps, new_path[len(new_path) - 1], destination_city),
                                int(total_miles) + int(new_miles),
                                float(total_hours) + float(new_hours),
                                float(total_gas_gallons) + float(new_gas_gallons), new_path))
    return int(0), float(0), float(0), []


# Mapping of a->b in Road-Segments.txt is stored in the dictionary as
# a->b and b->a
# This way, getting the successors of a city can be retrieved in almost O(1) time
def add_city_entry(road_segments, cityA, cityB, road_length, speed_limit, name):
    road_mapping = road_segments.get(cityA)
    if road_mapping is None:
        road_segments[cityA] = [(cityB, road_length, speed_limit, name)]
    else:
        road_mapping.append((cityB, road_length, speed_limit, name))


def is_valid_input_cities(start_city, destination_city, road_segments):
    # checks if start_city and destination_city are present in road segments input and are in the right format -
    # city,_state
    return any(start_city in city for city in road_segments) and any(destination_city in city for city in road_segments) \
           and any(',' in char for char in list(start_city)) and any(',' in char for char in list(destination_city)) \
           and len(list(filter(None, start_city.split(',_')))) == 2 and len(
        list(filter(None, destination_city.split(',_')))) == 2


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise Exception("Error: expected 3 arguments")

    start_city = sys.argv[1]
    destination_city = sys.argv[2]
    variant = sys.argv[3]

    # city_locations is a list of list containing the city name, the longitude and latitude. If the longitude or
    # latitude isn't mentioned for a city, it isn't stored in the HashMap. That would mean, the distance from that
    # city to the final destination while calculating the Heuristic would be infinite. So ideally PriorityQueue would
    # never return this as a route

    # There might be a problem with this assumption. If there's a really short path through this city, we would never
    # consider this path until all the other routes are considered
    city_gps = {}
    with open("city-gps.txt", 'r') as file:
        for line in file:
            elements = line.split()
            if len(elements) == 3:
                city_gps[elements[0]] = (elements[1], elements[2])

    # road_segments is a list of lists containing the two locations of
    # These max speeds, mpg and lengths are calculated for later use in the heuristics
    road_segments = {}
    max_speed = float(0)
    max_mpg = float(0)
    max_segment_length = float(0)
    with open("road-segments.txt", 'r') as file:
        for line in file:
            elements = line.split()
            # first city, second city, length (in miles), speed limit (in miles per hour), name of highway
            if len(elements) == 5:
                add_city_entry(road_segments, elements[0], elements[1], elements[2], elements[3], elements[4])
                add_city_entry(road_segments, elements[1], elements[0], elements[2], elements[3], elements[4])

                if max_speed < float(elements[3]):
                    max_speed = float(elements[3])

                current_mpg = mpg(float(elements[3]))
                if max_mpg < current_mpg:
                    max_mpg = current_mpg

                if max_segment_length < float(elements[2]):
                    max_segment_length = float(elements[2])

    if is_valid_input_cities(start_city, destination_city, road_segments):
        print("Solving...")
        result = solve(city_gps, road_segments, start_city, destination_city, variant, max_speed, max_mpg, max_segment_length)

        if result == ('', '', '', []):
            # when start and destination city are same
            print("Inf")
        else:
            # total_miles, total_hours, total_gas_gallons, path
            if (len(result[3]) - 1) < 1:
                print("Inf")
            else:
                print(str((len(result[3]) - 1)) + " " + str(result[0]) + " " + str(result[1]) + " " + str(result[2]) +
                  " " + " ".join(result[3]))
    else:
        # either of start or destination city not present in roadsegmets
        print("Inf")
