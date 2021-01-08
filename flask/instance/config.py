API_KEY = '2c62ed2633df21a18d7700c436125852'
OPEN_WEATHER_API = 'http://api.openweathermap.org/data/2.5/onecall'
PARAM_DICT = {'appid': API_KEY, 'lat': None, 'lon': None, 'units': 'imperial', 'exclude':'minutely,hourly,current,alerts'}
LOCATION_FILE = "../data/locations.json"
DEBUG= True
CACHE_TYPE= "simple"
CACHE_DEFAULT_TIMEOUT = 5000000