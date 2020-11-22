import branca
import folium

POPUP_HTML_URL = 'templates/popup.html'


def create_popup(html, data):
    if not data.latest_data.recovered and not data.latest_data.critical:
        return
    formatted_popup = html % (data.name, data.population, data.today['deaths'], data.latest_data.deaths,
                              data.today['confirmed'], data.latest_data.confirmed,
                              data.latest_data.recovered, data.latest_data.critical,
                              data.latest_data.calculated['death_rate'], data.latest_data.calculated['recovery_rate'],
                              'N/A'
                              )
    iframe = branca.element.IFrame(html=formatted_popup, width=500, height=300)
    return folium.Popup(iframe, max_width=350)


def read_pop_html():
    return open(POPUP_HTML_URL, 'r').read()


# not used
def create_popup_usa(html, data):
    formatted_popup = html % (data.Country_Region, 'N/A', 'N/A', data.Deaths, 'N/A', data.Confirmed,
                              data.Recovered, 'N/A', data.Case_Fatality_Ratio, 'N/A', data.Incident_Rate
                              )
    iframe = branca.element.IFrame(html=formatted_popup, width=500, height=300)
    return folium.Popup(iframe, max_width=350)
