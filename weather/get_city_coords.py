import requests
from Constants import YANDEX_GEOCODER_API_TOKEN

GEO_CODE_URL = 'https://geocode-maps.yandex.ru/1.x'

def get_coords(cityName: str):
    # дополнительные query параметры смотри здесь
    # https://yandex.ru/dev/maps/geocoder/doc/desc/concepts/input_params.html
    PARAMS = {
        "apikey": YANDEX_GEOCODER_API_TOKEN,
        "geocode": cityName,
        "format": "json"
    }

    response = requests.get(url=GEO_CODE_URL, params=PARAMS)
    data = response.json()['response']

    # Проверяем, что запрос был успешным
    if response.status_code == 200 and \
            data['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found'] != '0':
        # Получаем координаты из ответа
        coordinates = data['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')
        longitude, latitude = coordinates[0], coordinates[1]
        return latitude, longitude
    else:
        # Обработка ошибок, если город не найден или запрос не удался
        print(f'Ошибка при получении координат. Код ошибки: {response.status_code}')
        return None

def get_city(coords):

    PARAMS = {
        "apikey": YANDEX_GEOCODER_API_TOKEN,
        "geocode": f'{coords[0]},{coords[1]}',
        "format": "json",
        "kind": "locality"
    }

    response = requests.get(url=GEO_CODE_URL, params=PARAMS)
    data = response.json()['response']

    if response.status_code == 200 and \
            data['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found'] != '0':
        # Получаем название города из ответа
        city_name = data['GeoObjectCollection']['featureMember'][0]['GeoObject']['name']
        return city_name
    else:
        # Обработка ошибок, если город не найден или запрос не удался
        print(f'Ошибка при получении координат. Код ошибки: {response.status_code}')
        return None