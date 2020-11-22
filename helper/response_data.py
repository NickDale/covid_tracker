from collections import namedtuple


class JsonConverter:
    response_data = []
    __country = namedtuple('country', [
        'coordinates',  # dict
        'name',
        'code',
        'population',
        'updated_at',
        'today',  # dict
        'latest_data'
    ])
    __latest_data = namedtuple('latest_data', [
        'deaths',
        'confirmed',
        'recovered',
        'critical',
        'calculated'  # dict
    ])

    def __init__(self, json):
        self.convert(json)

    def convert(self, json):
        for i in json['data']:
            charge_response = self.__country(
                coordinates=i['coordinates'],  # dict
                # coordinate(test['coordinates']['latitude'], test['coordinates']['longitude'])
                name=i['name'],
                code=i['code'],
                population=i['population'],
                updated_at=i['updated_at'],
                today=i['today'],  # dict
                latest_data=self.__latest_data(i['latest_data']['deaths'], i['latest_data']['confirmed'],
                                               i['latest_data']['recovered'], i['latest_data']['critical'],
                                               i['latest_data']['calculated'])
            )
            self.response_data.append(charge_response)
