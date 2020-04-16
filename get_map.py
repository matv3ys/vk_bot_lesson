from io import BytesIO
import requests
from PIL import Image


def get_coords(city):
    toponym_to_find = city

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        return False

    json_response = response.json()

    if json_response['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found'] == '0':
        return False

    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]

    toponym_coodrinates = toponym["Point"]["pos"]
    lclat, lclon = [float(coord) for coord in toponym['boundedBy']['Envelope']['lowerCorner'].split()]
    uclat, uclon = [float(coord) for coord in toponym['boundedBy']['Envelope']['upperCorner'].split()]
    dlat = str(abs(uclat - lclat))
    dlon = str(abs(uclon - lclon))

    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    # delta = "0.05"

    map_params = {
        "size": "450,450",
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([dlat, dlon]),
    }

    return map_params


def get_map(map_params, type, user_id):
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    im = Image.open(BytesIO(response.content))

    fname = f'{user_id}.png'
    if type == 'sat':
        fname = f'{user_id}.jpg'

    im.save(f'static/{fname}')
    return f'static/{fname}'
