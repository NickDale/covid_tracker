from datetime import timedelta, datetime, date

import pandas as pd
import requests

from helper.covid_data import CovidData
from helper.daily_data import DailyData
from helper.response_data import JsonConverter

WORLD_GEO_JSON = 'https://raw.githubusercontent.com/MinnPost/simple-map-d3/master/example-data/world-population.geo.json'
COVID_DATA = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
COVID_DATA_BASE_URL = 'https://corona-api.com'
COVID_DATA_ALL_COUNTRY = '/countries'
COVID_DAILY_CSV = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data' \
                  '/csse_covid_19_daily_reports/{}.csv '
COUNTRY_DATA_URL = 'https://api.ipgeolocationapi.com/countries'
TIME_OUT = 5
RANGE = 30


class CovidRestAPI:

    def __init__(self):
        self.headers = self.header_init()
        self.country_population = {}
        self.all_data = {}
        self.load_all_data(self, COVID_DATA)
        self.all_country = self.get(self, COUNTRY_DATA_URL).json()

    def get_covid_data_by_country(self, country, from_date=date.today() + timedelta(days=-RANGE), to_date=date.today()):
        result = []
        for data in self.all_data.get(country):
            if from_date <= data.date <= to_date:
                result.append(data)
        return result

    @classmethod
    def header_init(cls):
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    @classmethod
    def load_all_data(cls, self, target):
        pd_read_csv = pd.read_csv(target, skiprows=1, header=None).values
        for raw in pd_read_csv:
            covid_data = CovidData(raw)
            country = raw[2]
            data = []
            if country in self.all_data:
                data = self.all_data[country]
            data.append(covid_data)
            self.all_data[country] = data

    @classmethod
    def get(cls, self, target):
        return requests.get(target, headers=self.headers, timeout=TIME_OUT)

    def get_country_data(self, country_code):
        return self.all_country[country_code]

    def get_all_countries(self):
        response_json = self.get(self, COVID_DATA_BASE_URL + COVID_DATA_ALL_COUNTRY).json()
        for i in response_json['data']:
            self.country_population[i['name']] = i['population']
        return JsonConverter(response_json).response_data

    def get_covid_data(self):
        csv_data_list = []
        for raw in self.get_last_data().values:
            csv_data_list.append(DailyData(raw))
        return csv_data_list

    @classmethod
    def get_last_data(cls, day_delay=0):
        day = datetime.now()
        try:
            data = cls.read_last_data_from_csv(day, day_delay)
        except:
            day_delay = day_delay - 1
            data = cls.get_last_data(day_delay)
        return data

    @classmethod
    def read_last_data_from_csv(cls, day, day_delay):
        return pd.read_csv(COVID_DAILY_CSV.format((day + timedelta(days=day_delay)).strftime("%m-%d-%Y")),
                           skiprows=1, header=None)

    def world_population_geo_json(self):
        return self.get(self, WORLD_GEO_JSON).json()
