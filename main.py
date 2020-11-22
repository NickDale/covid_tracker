import math

import folium
import requests

from covid_api import CovidRestAPI
from ui.view import create_popup

if __name__ == '__main__':
    covid_rest = CovidRestAPI()

    # covid_rest.

    data = covid_rest.get_all_countries()
    map = folium.Map(location=[38.58, -99.09], zoom_start=7)

    fg = folium.FeatureGroup(name="MAP")
    # fg.add_child(folium.Marker(location=[38.2, -99.1], popup="TEST", icon=folium.Icon(color='green')))
    # fg.add_child(folium.Marker(location=[38.2, -97.1], popup="TEST_3", icon=folium.Icon(color='red')))

    # for cords in [[38.5, -99.5],[38.5, -97.5]]:
    #     fg.add_child(folium.Marker(cords, popup="TEST_3", icon=folium.Icon(color='purple')))

    popup_html = open('ui/popup.html', 'r').read()
    covid_data = covid_rest.get_covid_data()

    # for cd in covid_data:
    #     if cd.Country_Region == 'US':
    #         continue
    #     if not math.isnan(cd.Lat) and cd.Lat is not None and not math.isnan(cd.Long_) and cd.Long_ is not None:
    #         fg.add_child(folium.Marker(location=[cd.Lat, cd.Long_],
    #                                    popup=create_popup_usa(popup_html, cd),
    #                                    icon=folium.Icon(color='pink')))
    #
    # for i in data:
    #     if i.name == 'USA':
    #         fg.add_child(folium.Marker(location=[i.coordinates['latitude'], i.coordinates['longitude']],
    #                                    popup=create_popup(popup_html, i),
    #                                    icon=folium.Icon(color='blue')))

    for i in data:
        _latitude = i.coordinates['latitude']
        _longitude = i.coordinates['longitude']
        # if not i.latest_data.recovered and not i.latest_data.critical:
        #     continue
        # formatted_popup = html % (i.name, i.population, i.today['deaths'], i.latest_data.deaths,
        #                           i.today['confirmed'], i.latest_data.confirmed,
        #                           i.latest_data.recovered, i.latest_data.critical,
        #                           i.latest_data.calculated['death_rate'], i.latest_data.calculated['recovery_rate']
        #                           )
        # iframe = branca.element.IFrame(html=formatted_popup, width=500, height=300)
        # popup = folium.Popup(iframe, max_width=350)
        _population = i.population
        if not _latitude and not _longitude:
            print(i.code, i.name, i)
            d = covid_rest.get_country_data(i.code)
            _latitude = d['geo']['latitude']
            _longitude = d['geo']['longitude']

        if _latitude is not None and not math.isnan(_latitude) \
                and _longitude is not None and not math.isnan(_longitude):
            fg.add_child(folium.Marker(location=[_latitude, _longitude],
                                       popup=create_popup(popup_html, i),
                                       icon=folium.Icon(color='pink')))

        # for d in covid_data:
        #     if d.Country_Region == 'US' and (d.Long_ and d.Lat):
        #         fg.add_child(folium.Marker(location=[d.Lat, d.Long_],
        #                                    popup=create_popup_usa(popup_html, d),
        #                                    icon=folium.Icon(color='blue')))

    population = requests.get(
        'https://raw.githubusercontent.com/MinnPost/simple-map-d3/master/example-data/world-population.geo.json').json()
    fg.add_child(folium.GeoJson(data=population,
                                style_function=lambda x:
                                {'fillColor': 'green' if float(x['properties']['POP2005']) < 10000000
                                else 'orange' if 10000000 <= float(x['properties']['POP2005']) < 20000000 else 'red'}
                                ))

    # fg.add_child(folium.GeoJson(data=countries_geo_json))
    map.add_child(fg)
    map.save("ui/map.html")
