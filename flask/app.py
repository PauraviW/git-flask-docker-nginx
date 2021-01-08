# python
from datetime import date, datetime
import requests
import copy
import requests_cache
# flask
from flask import Flask, jsonify, abort, request
from flask_restful import Resource, Api
from flask_caching import Cache
from flask_cors import CORS

# custom
from utils.utils import check_if_within_range, get_locations

# create the app
app = Flask(__name__, instance_relative_config=True)
CORS(app)
app.config.from_pyfile('config.py')
api = Api(app)
cache = Cache(app)


# application related data
api_key =  app.config['API_KEY']
requests_cache.install_cache(cache_name='openWeather_cache', backend='sqlite', expire_after=10000)
open_weather_api_endpoint = app.config['OPEN_WEATHER_API']
param_dict = app.config['PARAM_DICT']
todays_date = date.today().isoformat()
location_file_path = app.config['LOCATION_FILE']


@cache.cached(key_prefix='all_locations')
def get_all_locations():
    locations = get_locations(location_file_path)
    return locations

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def wrong_data(e):
    return jsonify(error=str(e)), 500

class SuggestParks(Resource):

    def get(self,latitude, longitude):
        """
        This method retrieves the information regarding the best park that the user should visit.

        :param latitude: request parameter indicating user's latitude
        :param longitude: request parameter indicating user's longitude
        :param radius: request parameter indicating the maximum distance the user wishes to travel
        :param weather: request parameter indicating user's favourite weather
        :return: A list of dictionaries containing the park information
        """

        final_parks = []
        parks = get_all_locations()

        # if the user enters invalid request parameters
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            radius = float(request.args['radius'])
            weather = request.args['weather']
        except:
            abort(400, "Invalid request parameters!")
        #
        # get probable locations
        probable_locations = []
        for park in parks:
            dist, within_range = check_if_within_range(latitude, longitude, radius, park['lat'], park['lng'])
            park['distance'] = int(dist)
            if within_range:
                probable_locations.append(park)


        # # filter based on weather and date.
        for park in probable_locations:
            # generate parameters for the request
            param_dict['lat'] = float(park['lat'])
            param_dict['lon'] = float(park['lng'])
            param_dict['exclude'] = 'current,minutely,hourly,alerts'
            try:
                import  time
                response = requests.get(open_weather_api_endpoint, params=param_dict)
                if response.status_code != 200:
                    abort(500, description="Sorry! Try Again After Some time")

                else:
                    data = response.json()
                    park['lat'] = data['lat']
                    park['lon'] = data['lon']

                    # segregate based on favourite weather
                    for day_info in data['daily']:
                        if day_info['weather'][0]['main'].lower() == weather.lower():
                            park['mainWeather'] = day_info['weather'][0]['main']
                            park['desc'] = day_info['weather'][0]['description']
                            park['temp_day'] = day_info['temp']['day']
                            park['temp_night'] = day_info['temp']['night']
                            park['feels_day'] = day_info['feels_like']['day']
                            park['feels_night'] = day_info['feels_like']['night']
                            park['idate'] = date.fromtimestamp(day_info['dt']).strftime("%A %d. %B %Y")

                            final_parks.append(copy.deepcopy(park))


            except:
                abort(500, "Sorry Could not retrieve the data! Try again after some time!")

        # sort based on distance
        final_parks = sorted(final_parks, key=lambda i: (datetime.strptime(i['idate'], "%A %d. %B %Y"), i['distance']))

        return jsonify({'parks': final_parks})

class Hello(Resource):

    def get(self):
        return 'hello'
# add the api resource
api.add_resource(SuggestParks, '/api/v1.0/parks/latitude/<latitude>/longitude/<longitude>')

api.add_resource(Hello, '/')


if __name__ == '__main__':
    app.run(debug=True)


