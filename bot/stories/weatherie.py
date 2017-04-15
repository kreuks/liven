import datetime
import requests
import random

from bot.stories.base import Story
from bot.constants import Context, Intent, RESPONSES, LOGGER, Weather
from bot.util import get_result_story
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# TODO:
# 1. add location procedure to fetch city name
# DONE 2. convert location name to lat long
# 3. Request by API to openweathermap.org or darksky.net/dev/docs (OW-API-KEY : fa7ed6cfa9e8cc674f19ae0e9dddaf45)

class WeatherForecast(Story):
    def __init__(self):
        self.URLlatlong = 'http://www.latlong.net/'
        self.URLapi = 'http://api.openweathermap.org/data/2.5/{}?q={}&APPID={}'
        self.URLapi_latlongnet = 'http://api.openweathermap.org/data/2.5/{}?lat={}&lon={}&APPID={}'
        self.keyAPI = 'fa7ed6cfa9e8cc674f19ae0e9dddaf45'

    def compliance(self, context):
        LOGGER.info(
            'Compliance Stock Price'
        )
        return (
            Intent.WEATHER_FORECAST in context.values() and
            Context.WEATHER_KEY in context
        )

    def get_lat_long(self, city_name):
        # Initiate driver and load the web
        driver = webdriver.Chrome()
        driver.get(self.URLlatlong)
        # Fill the city name checkbox and press key ENTER
        fill = driver.find_element_by_id('gadres')
        fill.send_keys(city_name)
        fill.send_keys(Keys.ENTER)
        # Get latitude and longitude values
        lat = driver.find_element_by_id('lat').get_attribute('value')
        lng = driver.find_element_by_id('lng').get_attribute('value')
        # Close the driver to save memory
        driver.close()
        return lat, lng

    def get_json_data(self, city, type_req):
        url_json = self.URLapi.format(type_req, city, self.keyAPI)
        dataJson = requests.get(url_json)
        if dataJson.status_code == 200:
            return dataJson.status_code, dataJson.json()
        else:
            return dataJson.status_code, 'ERROR'

    def time_frase_conversion(self, frase_time):
        LOGGER.info(
            '[WEATHER] time_frase_conversion : {}'.format(frase_time)
        )
        now = datetime.datetime.now()
        if 'besok' in frase_time:
            temp_time = now + datetime.timedelta(days=1)
        elif ('kemarin' in frase_time) or ('kemaren' in frase_time):
            temp_time = now + datetime.timedelta(days=-1)
        adj_time_componen = [k for k,v in Weather.ADJ_TIME_FRASE.items() if k in frase_time]
        if len(adj_time_componen) != 0:
            requested_time = datetime.datetime(temp_time.year, temp_time.month, temp_time.day,
                                               Weather.ADJ_TIME_FRASE[adj_time_componen[0]], 0, 0, 0)
        else:
            requested_time = datetime.datetime(temp_time.year, temp_time.month, temp_time.day,
                                               12, 0, 0, 0)
        return requested_time.strftime("%Y-%m-%d %H:%M:%S")

    def parse_json(self, data_json, request_type, time_value=None):
        if request_type == 'weather':
            main_weather = data_json[request_type][0]['main']
            summary_weather = data_json[request_type][0]['description']
            humidity_value = data_json['main']['humidity']
        elif request_type == 'forecast':
            data_in_time = [ i for i in data_json['list'] if i['dt_txt'] == time_value ]
            main_weather = data_in_time[0]['weather'][0]['main']
            summary_weather = data_in_time[0]['weather'][0]['description']
            humidity_value = data_in_time[0]['main']['humidity']
        return main_weather, summary_weather, humidity_value

    def run_story(self, context):
        result = get_result_story()
        response = RESPONSES[Weather.WEATHER_RESP]
        response = response[random.randint(0, len(response)-1)]
        # Handle no Location problem and get lat long value
        if Context.LOCATION not in context:
            # TODO : Return context data for the next step and the response
            result['context'] = context
            result['response'] = 'Lokasi nya mana euyy...., yang lengkap lah....'
            return result
        # else :
        #    latitude, longitude = self.get_lat_long(context[Context.LOCATION])
        # Return if contain past time adj
        if Context.PAST_TIME_ADJ in context:
            result['context'] = context
            result['response'] = 'Masa lu lupa kemarin cuacanya gimana... Parah...'
            return result
        elif Context.FUT_TIME_ADJ in context:
            key_time = self.time_frase_conversion(context[Context.FUT_TIME_ADJ])
            type_weather_request = 'forecast'
        else:
            type_weather_request = 'weather'

        # Get JSON Rock !!!!
        respond_code, data_json = self.get_json_data(context[Context.LOCATION], type_weather_request)
        if respond_code == 200:
            #Process the message
        else:
            result['context'] = context
            result['response'] = 'Lagi ada masalah cuy: {}, coba lagi ya...'.format(respond_code)
            return result
        # Parse the data
        main_weather, summary_weather, humidity_value = self.parse_json(data_json, type_weather_request, key_time)
        # Return Response