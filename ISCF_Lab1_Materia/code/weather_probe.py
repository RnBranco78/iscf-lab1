import requests

key = "https://api.openweathermap.org/data/2.5/weather?lat=38.661&lon=-9.2056&appid=94346c4f808479f8cf360666c2c5c3f4"

def get_weather_data(key):
    response = requests.get(key)
    data = response.json()
    country = data["sys"]["country"]
    city = data["name"]
    temperature = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    temp_min = data["main"]["temp_min"]
    temp_max = data["main"]["temp_max"]
    return {
        "Country": country,
        "City": city,
        "Current Temperature": temperature,
        "Feels Like": feels_like,
        "Minimum Temperature": temp_min,
        "Maximum Temperature": temp_max
    }

if __name__ == "__main__":
    weather_data = get_weather_data(key)
    print(weather_data)
