import random
from math import atan2, degrees

import openrouteservice
from geopy.distance import Distance, distance
from geopy.point import Point

KLIENT_KEY = "5b3ce3597851110001cf62483c8ebff6b30a492fbebe1540e83f2e95"

client = openrouteservice.Client(key=KLIENT_KEY)  # Specify your personal API key

VELOCITY = 20  # km / h
MSEC_COEFF = 1000 / 3600  # km/h -> m/s
CHECK_TIME_INTERVAL = 10  # sec
CHECK_DISTANCE = Distance(VELOCITY * CHECK_TIME_INTERVAL / 3600)

IND = 1
CHECK_POINT_DICT = {}


def create_poin_entity(point):
    global IND

    CHECK_POINT_DICT[IND] = point
    IND += 1


def calculate_bearing(point_1: list[float], point_2: list[float]):
    x_long_norm = point_2[0] - point_1[0]
    y_lat_norm = point_2[1] - point_1[1]
    rad = atan2(y_lat_norm, x_long_norm)
    x_axe_rel_degrees = degrees(rad)
    return 90 - x_axe_rel_degrees


def split_route_with_check_points(start_point, end_point, remain_distance):
    bearing = calculate_bearing(
        (start_point.longitude, start_point.latitude), (end_point.longitude, end_point.latitude)
    )
    distance_sub_route = distance(start_point, end_point)
    if remain_distance <= distance_sub_route:
        interval_end_point = distance_sub_route.destination(start_point, bearing)
        create_poin_entity(interval_end_point)
        remain_distance = CHECK_DISTANCE
    else:
        return remain_distance - distance_sub_route

    return split_route_with_check_points(interval_end_point, end_point, remain_distance)


def generate_random_end_point(from_point, radius):
    bearing = round(random.uniform(0, 360), 2) - 180
    point = distance(radius).destination(from_point, bearing)
    return point.latitude, point.longitude


def generate_route(from_point: list[float], to_point: list[float] = None, radius: int = None):
    if radius is not None:
        to_point = generate_random_end_point(from_point, radius)

    routes = client.directions((from_point, to_point))
    geometry = routes["routes"][0]["geometry"]

    decoded = openrouteservice.convert.decode_polyline(geometry)
    route_points = decoded.get("coordinates")

    if not route_points or len(route_points) < 2:
        raise ValueError("NO COORDINATES")

    start_point = Point(*route_points[0][::-1])
    remains_distance = CHECK_DISTANCE

    for point in route_points[1:]:
        end_point = Point(*point[::-1])
        remains_distance = split_route_with_check_points(start_point, end_point, remains_distance)
        if remains_distance == 0:
            remains_distance = CHECK_DISTANCE
        start_point = end_point

    return CHECK_POINT_DICT


if __name__ == "__main__":
    coords = ([13.384116, 52.533558], [13.428726, 52.519355])
    generate_route(*coords)
    print(CHECK_POINT_DICT)
