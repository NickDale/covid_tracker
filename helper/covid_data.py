from datetime import datetime


class CovidData:

    def __init__(self, raw):
        # self.country = raw[2]
        self.date = datetime.strptime(raw[3], '%Y-%m-%d').date()
        self.total_cases = raw[4]
        self.new_cases = raw[5]
        self.new_cases_smoothed = raw[6]
        self.total_deaths = raw[7]
        self.new_deaths = raw[8]
        self.new_deaths_smoothed = raw[9]
        self.total_cases_per_million = raw[10]
        self.new_cases_per_million = raw[11]
        # self.new_cases_smoothed_per_million = raw[12]
        self.total_deaths_per_million = raw[13]
        self.new_deaths_per_million = raw[14]
        # self.new_deaths_smoothed_per_million = raw[15]
        self.total_tests = raw[25]
        self.new_tests = raw[26]
        self.positive_rate = raw[31]
        self.median_age = raw[37]
        self.aged_65_older = raw[38]
        self.aged_70_older = raw[39]
        self.hospital_beds_per_thousand = raw[47]
        self.life_expectancy = raw[48]
