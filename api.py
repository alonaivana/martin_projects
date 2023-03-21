import requests
import json
from settings import URL_TOKEN, URL_DATA, API_PASSWORD, API_USER


# Получение токена для получения доступа к данным
def get_token():
    try:
        url = URL_TOKEN
        payload = json.dumps({
            "username": API_USER,
            "password": API_PASSWORD
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response1 = requests.request("POST",
                                     url,
                                     headers=headers,
                                     data=payload).json()
        access_token = response1["access_token"]
        return access_token
    except BaseException:
        return None


# Получение данных (суточного отчёта)
def get_data(access_token, d):
    try:
        url = URL_DATA
        payload = {}
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        size = 1000
        response2 = requests.request("GET",
                                     url,
                                     headers=headers,
                                     data=payload,
                                     params={'date': d,
                                             'page[size]': size,
                                             'page[number]': 0}).json()
        data = response2.get('data')
        row_count = response2.get('rowcount')
        if row_count > size:
            pages = (row_count//size)
            for i in range(1, pages+1):
                response2 = requests.request("GET",
                                             url,
                                             headers=headers,
                                             data=payload,
                                             params={'date': d,
                                                     'page[size]': size,
                                                     'page[number]': i}).json()
                extra = response2.get('data')
                for visit in extra:
                    data.append(visit)
        return data
    except BaseException:
        return None
