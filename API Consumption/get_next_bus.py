"""
-Program to find how long it is until the next bus on “BUS ROUTE” leaving from “BUS STOP NAME”
going “DIRECTION” using the api defined at http://svc.metrotransit.org/ .
-“BUS ROUTE” will be a substring of the bus route name which is only in one bus
route.
-“BUS STOP NAME” will be a substring of the bus stop name which is only in one bus
stop on that route.
-“DIRECTION” will be “north” “east” “west” or “south”.

 Usage: get_next_bus.py bus_route stop_name direction
 ex: get_next_bus.py "METRO Blue Line" "Target Field Station Platform 1" south

 Author:mathewjose09@gmail.com
"""

import sys
import datetime, pytz
import requests


def get_route_info(route_base_url, value_to_search, search_key, return_key):
    """
    Generic function to retrieve some uniq id's from the metro API based on the keys passed.
    :param route_base_url: URL to which API call to be made
    :param value_to_search: Value to be searched within the json response from the API call
    :param search_key: dictionary key to be checked in the json response for matching the value against value_to_search
    :param return_key: dictionary key to be used for returning the value if a match found for the value_to_search in search_key.
    :return: ID based on the return_key provided .It can be route_id,stop_id etc.
    """
    # Retrieve the data from the URL provided
    response = requests.get(route_base_url + "?format=json")
    if response.status_code != 200:
        print("There was some issue with the call for ,GET {0}.Return code is {1}.".format(route_base_url, response.status_code))
        sys.exit(1)

    # Initialize info_id with the default value of -1 for marking not found
    info_id = -1
    route_data = response.json()
    for route_info in route_data:
        # check if the search_key's value is matching with value_to_search .Search will be case insensitive.
        if route_info[search_key].lower().find(value_to_search.lower()) != -1:
            info_id = route_info[return_key]
            # No need to search further .So break from the loop.
            break

    return info_id


def main():
    base_url = "http://svc.metrotransit.org/"
    time_zone_to_use = 'US/Central'

    # Check for the arguments to the program
    if len(sys.argv) != 4:
        print("Usage is: " + sys.argv[0] + " bus_route stop_name direction")
        sys.exit(1)

    # Initialize the variables based on the values from command line
    bus_route = sys.argv[1]
    stop_name = sys.argv[2]
    direction = sys.argv[3]

    # Get the route id from the route name received
    route_id = get_route_info(base_url + "NexTrip/Routes", bus_route, "Description", "Route")
    # Exit if the route identification was unsuccessful
    if route_id == -1:
        print("Unable to find the details for the Route name ({0}) entered!!!. ".format(bus_route))
        sys.exit(1)

    # Get the direction id for the route entered and direction chosen by user
    direction_id = get_route_info(base_url + "NexTrip/Directions/" + str(route_id), direction, "Text", "Value")
    # Exit if the direction identification was unsuccessful
    if direction_id == -1:
        print("Unable to find the direction ({0}) for the Route name ({1}) entered!!!. ".format(direction, bus_route))
        sys.exit(1)

    # Get the bus stop id
    stop_id = get_route_info(base_url + "NexTrip/Stops/" + str(route_id) + "/" + str(direction_id), stop_name, "Text", "Value")
    # Exit if the stop identification was unsuccessful
    if stop_id == -1:
        print("Unable to find the stop ({0}) for the Route name ({1}) for the direction ({2}) entered!!!. ".format(stop_name, bus_route, direction))
        sys.exit(1)

    # Get the departure timestamp for the stop_id in the given direction
    departure_time_stamp = get_route_info(base_url + "NexTrip/" + str(route_id) + "/" + str(direction_id) + "/" + str(stop_id), direction, "RouteDirection", "DepartureTime")

    # Proceed further only if we gets a valid timestamp for the stop
    if len(str(departure_time_stamp)) != 2:
        # Take the epoch time in seconds from the time stamp received from the api call
        departure_time_stamp = int(departure_time_stamp[6:16])
        day_in_departure = int(datetime.datetime.fromtimestamp(departure_time_stamp).strftime('%d'))
        current_day = datetime.datetime.now(tz=pytz.timezone(time_zone_to_use)).date().day
        current_time_stamp = int(str(datetime.datetime.now(tz=pytz.timezone(time_zone_to_use)).timestamp())[:10])
        # check if the departure date falls today or current time already crossed departure time,
        # then return, as the last bus for today is already left
        if current_time_stamp > departure_time_stamp or current_day != day_in_departure:
            return
        # Find the minutes till departure from the difference of the timestamps in seconds
        mins_till_departure = (departure_time_stamp - current_time_stamp) // 60
        print(str(mins_till_departure) + " Minutes")


if __name__ == "__main__":
    main()
