
class Country:
    def __init__(self, raw):
        self.population = 0
        self.name = raw[3]
        self.latitude = raw[5]
        self.longitude = raw[6]
        self.confirmed = raw[7]
        self.deaths = raw[8]
        self.recovered = raw[9]
        self.active = raw[10]
        self.combined_key = raw[11]
        self.incident_rate = raw[12]
        self.case_fatality_ratio = raw[13]
