class CovidData:

    def __init__(self, raw):
        self.FIPS = raw[0]
        self.Admin2 = raw[1]
        self.Province_State = raw[2]
        self.Country_Region = raw[3]
        self.Last_Update = raw[4]
        self.Lat = raw[5]
        self.Long_ = raw[6]
        self.Confirmed = raw[7]
        self.Deaths = raw[8]
        self.Recovered = raw[9]
        self.Active = raw[10]
        self.Combined_Key = raw[11]
        self.Incident_Rate = raw[12]
        self.Case_Fatality_Ratio = raw[13]
