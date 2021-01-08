import os
import json
from geopy import distance as ds

basedir = os.path.abspath(os.path.dirname(__file__))


def get_locations(location_file_path):

    '''
    Function to read the park details.
    :return: list of all the parks with details.
    '''
    data_file = os.path.join(basedir, location_file_path)
    with open(data_file, 'r') as f:
        locations = json.load(f)
        return locations


def check_if_within_range(user_latitude, user_longitude, radius, park_latitude, park_longitude):
    """
    Method to check if distance between 2 places is within the range prescribed by the user
    :param user_latitude: User location - latitude
    :param user_longitude: User Location - longitude
    :param radius: Maximum miles user can travel
    :param park_latitude: Park Location - Latitude
    :param park_longitude: Park Location - Longitude
    :return: boolean - If a park is within the range specified by the user then return true else false.
    """
    lat1 = user_latitude
    lon1 = user_longitude
    lat2 = float(park_latitude)
    lon2 = float(park_longitude)
    dist = ds.distance((lat1, lon1), (lat2, lon2)).miles

    if dist <= float(radius):

        return dist, True
    else:
        return dist, False