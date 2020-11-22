from datetime import timedelta, datetime

import pandas as pd
import requests

from helper.covid_csv_data import CovidData
from helper.response_data import JsonConverter

COVID_DATA_BASE_URL = 'https://corona-api.com'
COVID_DATA_ALL_COUNTRY = '/countries'
COVID_DAILY_CSV = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{}.csv'
COUNTRY_DATA_URL = 'https://api.ipgeolocationapi.com/countries'
TIME_OUT = 5


class CovidRestAPI:

    def __init__(self):
        self.headers = self.header_init()
        self.country_population = {}
        self.all_country = self.get(self, COUNTRY_DATA_URL).json()

    @classmethod
    def header_init(cls):
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

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

    # def get_data_in_range(self, dayFrom, dayTo):

    def get_covid_data(self):
        csv_data_list = []
        for raw in self.get_latest_data().values:
            # country = Country(raw)
            # if country.name in self.covid_country_data:
            #     cu = self.covid_country_data[country.name]
            #     cu.confirmed = cu.confirmed + country.confirmed
            #     cu.deaths = cu.confirmed + country.confirmed
            #     cu.recovered = cu.confirmed + country.confirmed
            #     cu.active = cu.confirmed + country.confirmed

            csv_data_list.append(CovidData(raw))
        return csv_data_list

    @classmethod
    def get_latest_data(cls, day_delay=0):
        day = datetime.now()
        try:
            data = cls.read_csv_data(day, day_delay)
        except:
            day_delay = day_delay - 1
            data = cls.get_latest_data(day_delay)
        return data

        # data = None
        # response = self.get(self, COVID_DAILY_CSV.format(day.strftime("%m-%d-%Y")))
        # if response.status_code != 200:
        #     data = pd.read_csv(COVID_DAILY_CSV.format((day + timedelta(days=-1)).strftime("%m-%d-%Y")), header=None)
        # else:
        #     data = pd.read_csv(COVID_DAILY_CSV.format(day.strftime("%m-%d-%Y")), header=None)
        # print(data)
        # d = pd.read_csv(COVID_DAILY_CSV.format((day + timedelta(days=-1)).strftime("%m-%d-%Y")), header=None,
        #                 delimiter=',')
        # list_of_rows = [list(row) for row in d.values]
        # covid_data = []
        # for row in d.values:
        #     covid_data.append(CovidData(row))
        #
        # response_json = response.json()
        # return JsonConverter(response_json).response_data

    @classmethod
    def read_csv_data(cls, day, day_delay):
        return pd.read_csv(COVID_DAILY_CSV.format((day + timedelta(days=day_delay)).strftime("%m-%d-%Y")),
                           skiprows=1, header=None)
