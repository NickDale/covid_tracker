import math

import folium

from covid_api import CovidRestAPI
from helper.util import read_pop_html, create_popup


def render_new_map():
    covid_rest = CovidRestAPI()

    covid_rest.get_covid_data()
    data = covid_rest.get_all_countries()
    map = folium.Map(location=[46.2833709, 20.0887508], zoom_start=7)
    folium.TileLayer('Stamen Terrain').add_to(map)
    folium.TileLayer('Stamen Toner').add_to(map)
    folium.TileLayer('Stamen Water Color').add_to(map)
    folium.TileLayer('cartodbpositron').add_to(map)
    folium.TileLayer('cartodbdark_matter').add_to(map)

    pickers = folium.FeatureGroup(name="pickers")
    # fg.add_child(folium.Marker(location=[38.2, -99.1], popup="TEST", icon=folium.Icon(color='green')))
    # fg.add_child(folium.Marker(location=[38.2, -97.1], popup="TEST_3", icon=folium.Icon(color='red')))

    # for cords in [[38.5, -99.5],[38.5, -97.5]]:
    #     fg.add_child(folium.Marker(cords, popup="TEST_3", icon=folium.Icon(color='purple')))

    popup_html = read_pop_html()
    # covid_data = covid_rest.get_covid_data()
    for i in data:
        _latitude = i.coordinates['latitude']
        _longitude = i.coordinates['longitude']
        _population = i.population
        if not _latitude and not _longitude:
            d = covid_rest.get_country_data(i.code)
            _latitude = float(d['geo']['latitude_dec'])
            _longitude = float(d['geo']['longitude_dec'])

        if _latitude is not None and not math.isnan(_latitude) \
                and _longitude is not None and not math.isnan(_longitude):
            pickers.add_child(folium.Marker(location=[_latitude, _longitude],
                                            popup=create_popup(popup_html, i),
                                            icon=folium.Icon(color='pink')))

        # for d in covid_data:
        #     if d.Country_Region == 'US' and (d.Long_ and d.Lat):
        #         fg.add_child(folium.Marker(location=[d.Lat, d.Long_],
        #                                    popup=create_popup_usa(popup_html, d),
        #                                    icon=folium.Icon(color='blue')))

    countries_group = folium.FeatureGroup(name="countries", overlay=True)
    countries_group.add_child(folium.GeoJson(data=covid_rest.world_population_geo_json(),
                                             style_function=lambda x:
                                             {'fillColor': 'green' if float(x['properties']['POP2005']) < 10000000
                                             else 'orange' if 10000000 <= float(
                                                 x['properties']['POP2005']) < 20000000 else 'red'}
                                             ))

    # fg.add_child(folium.GeoJson(data=countries_geo_json))
    map.add_child(pickers)
    map.add_child(countries_group)
    map.add_child(folium.LayerControl())
    map.save("templates/map.html")
