import requests

def get_weather_data(api_key, city):
    url_for_location = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={api_key}&q={city.strip()}"

    try:
        r = requests.get(url_for_location)
        r.raise_for_status()  

        location_data = r.json()
        if not isinstance(location_data, list) or len(location_data) == 0:
            raise Exception(f"Не найден город: {city}")

        location_key = location_data[0]["Key"]

        url_for_weather = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}&details=true"
        weather_response = requests.get(url_for_weather)
        weather_response.raise_for_status()  

        response = weather_response.json()
        if not response or len(response) == 0:
            raise Exception("Нет данных о погоде.")

        weather_data = response[0] 

    except requests.exceptions.RequestException as req_err:
        print(f'Произошла ошибка HTTP: {req_err}')
        return None
    except Exception as e:
        print(f'Произошла ошибка: {e}')
        return None

    data = {
        "temperature": weather_data["Temperature"]["Metric"]["Value"],
        "humidity": weather_data["RelativeHumidity"],
        "wind_speed": weather_data["Wind"]["Speed"]["Metric"]["Value"],
        "precipitation_prob": weather_data["PrecipitationSummary"]["PastHour"]["Metric"]["Value"]
    }

    return data
