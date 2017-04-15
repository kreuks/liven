import datetime
import requests
import random

from bot.stories.base import Story
from bot.constants import Context, Intent, RESPONSES, LOGGER, Weather
from bot.util import get_result_story
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


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
        return (
            lat, lng
        )

    def get_json_data(self, city, type_req):
        url_json = self.URLapi.format(type_req, city, self.keyAPI)
        data_json = requests.get(url_json)
        if data_json.status_code == 200:
            return data_json.status_code, data_json.json()
        else:
            return data_json.status_code, 'ERROR'

    @staticmethod
    def time_frase_conversion(frase_time):
        LOGGER.info(
            '[WEATHER] time_frase_conversion : {}'.format(frase_time)
        )
        now = datetime.datetime.now()
        if 'besok' in frase_time:
            temp_time = now + datetime.timedelta(days=1)
        elif ('kemarin' in frase_time) or ('kemaren' in frase_time):
            temp_time = now + datetime.timedelta(days=-1)
        else:
            temp_time = now
        adj_time_componen = [k for k, v in Weather.ADJ_TIME_FRASE.items() if k in frase_time]
        if len(adj_time_componen) != 0:
            requested_time = datetime.datetime(temp_time.year, temp_time.month, temp_time.day,
                                               Weather.ADJ_TIME_FRASE[adj_time_componen[0]], 0, 0, 0)
        else:
            requested_time = datetime.datetime(temp_time.year, temp_time.month, temp_time.day,
                                               12, 0, 0, 0)
        return (
            requested_time.strftime("%Y-%m-%d %H:%M:%S")
        )

    def run_story(self, context):
        result = get_result_story()
        # Handle no Location problem and get lat long value
        if Context.LOCATION not in context:
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
            key_time = self.time_frase_conversion(Context.TODAY_TIME_ADJ)
            type_weather_request = 'weather'
        # Get JSON Rock !!!!
        respond_code, data_json = self.get_json_data(context[Context.LOCATION], type_weather_request)
        if respond_code != 200:
            result['context'] = context
            result['response'] = 'Lagi ada masalah cuy: {}, coba lagi ya...'.format(respond_code)
            return result
        # Parse the data
        main_weather, summary_weather, humidity_value = parse_json(data_json, type_weather_request, key_time)
        # Return Response
        if type_weather_request == 'forecast':                          # Enter 1'st layer response (time type)
            response = RESPONSES[Weather.WEATHER_FORECAST]
        else:
            response = RESPONSES[Weather.WEATHER_TODAY]
        choose_resp_type = random.randint(0, len(response) - 1)
        response = response[Weather.RESP_VARIATION[choose_resp_type]]   # Enter 2'nd layer response (param amount)
        response = response[random.randint(0, len(response) - 1)]       # Enter 3'rd layer response (resp Variety)
        if choose_resp_type == 0:
            result['response'] = response.format(main_weather)
        elif choose_resp_type == 1:
            result['response'] = response.format(main_weather, humidity_value)
        else:
            result['response'] = response.format(main_weather, summary_weather)
        # Remove unused context
        result['context'] = {
            k: v for k, v in context.items() if (
                k != Context.WEATHER_KEY and v != Intent.WEATHER_FORECAST and k != Context.FUT_TIME_ADJ
            )
        }
        return result


def parse_json(data_json, request_type, time_value=None):
    LOGGER.info(
        '[WEATHER] Parse Json'
    )
    weather_var = {}
    if request_type == 'weather':
        weather_var['main_weather'] = data_json[request_type][0]['main']
        weather_var['summary_weather'] = data_json[request_type][0]['description']
        weather_var['humidity_value'] = data_json['main']['humidity']
    elif request_type == 'forecast':
        data_in_time = [i for i in data_json['list'] if i['dt_txt'] == time_value]
        weather_var['main_weather'] = data_in_time[0]['weather'][0]['main']
        weather_var['summary_weather'] = data_in_time[0]['weather'][0]['description']
        weather_var['humidity_value'] = data_in_time[0]['main']['humidity']
    return (
        weather_var['main_weather'], weather_var['summary_weather'], weather_var['humidity_value']
    )
