# http://api.weatherapi.com/v1/current.json?key=c809b1ec469c442c818104121211510&q=Basel&aqi=no

import requests
from pprint import pprint
import json


# Contains all important weather and location data from rest call
class FilteredItems:
    country: str
    place: str
    date: str
    time: str

    condition_text: str
    condition_code: str
    condition_windy: str
    condition_humidity: str
    temp_c: str


class WeatherStatus:
    moon_stars_image: bool = False
    moon_image: bool = False
    sunny_image: bool = False
    partly_cloudy_image: bool = False
    cloudy_image: bool = False
    drizzle_image: bool = False
    rainy_image: bool = False
    storm_image: bool = False
    snowy_image: bool = False


class ClothesStatus:
    # Either "cap", "beanie" or "empty"
    hat: str = "empty"

    scarf: bool = False

    # Either "heavy", "medium", "light" or "empty"
    jacket: str = "empty"

    # If jacket is set, hoodie = False
    hoodie: bool = False

    # If hoodie is True, tshirt = False
    tshirt: bool = False

    # Either "jeans", "shorts" - default is "jeans"
    pants: str = "jeans"

    # Either "boots", "sneakers" or "sandals" - default is "sneakers"
    shoes: str = "sneakers"

    show_outfit: bool = True


def return_needed_info():
    response = requests.get(
        "http://api.weatherapi.com/v1/current.json?key=c809b1ec469c442c818104121211510&q=Basel&aqi=no").json()

    local_time = response["location"]["localtime"]
    local_time = local_time.split()

    filtered_obj: FilteredItems = FilteredItems()

    filtered_obj.country = response["location"]["country"]
    filtered_obj.place = response["location"]["name"]
    filtered_obj.date = local_time[0]
    filtered_obj.time = local_time[1]

    filtered_obj.condition_text = response["current"]["condition"]["text"]
    filtered_obj.condition_code = response["current"]["condition"]["code"]
    filtered_obj.condition_windy = response["current"]["wind_kph"]
    filtered_obj.temp_c = response["current"]["temp_c"]
    filtered_obj.condition_humidity = response["location"]["name"]

    print(response)
    print(filtered_obj)

    return filtered_obj


def return_clothes_image_logic():
    filtered_obj: FilteredItems = return_needed_info()
    clothes_status: ClothesStatus = ClothesStatus()

    # Snowy
    if int(filtered_obj.temp_c) <= 0:
        clothes_status.shoes = "boots"
        clothes_status.pants = "jeans"
        clothes_status.tshirt = False
        clothes_status.hoodie = False
        clothes_status.jacket = "heavy"
        clothes_status.scarf = True
        clothes_status.hat = "beanie"

    # Cold
    elif int(filtered_obj.temp_c) <= 10:
        clothes_status.shoes = "sneakers"
        clothes_status.pants = "jeans"
        clothes_status.tshirt = False
        clothes_status.hoodie = False
        clothes_status.jacket = "heavy"
        clothes_status.scarf = False
        clothes_status.hat = "empty"

    # Not too cold, not warm either
    elif int(filtered_obj.temp_c) <= 14:
        clothes_status.shoes = "sneakers"
        clothes_status.pants = "jeans"
        clothes_status.tshirt = False
        clothes_status.hoodie = False
        clothes_status.jacket = "medium"
        clothes_status.scarf = False
        clothes_status.hat = "empty"

    # Fall weather
    elif int(filtered_obj.temp_c) <= 19:
        clothes_status.shoes = "sneakers"
        clothes_status.pants = "jeans"
        clothes_status.tshirt = False
        clothes_status.hoodie = False
        clothes_status.jacket = "light"
        clothes_status.scarf = False
        clothes_status.hat = "empty"

    # Spring Weather
    elif int(filtered_obj.temp_c) <= 23:
        clothes_status.shoes = "sneakers"
        clothes_status.pants = "jeans"
        clothes_status.tshirt = False
        clothes_status.hoodie = True
        clothes_status.jacket = "empty"
        clothes_status.scarf = False
        clothes_status.hat = "empty"

    # Warm Weather
    elif int(filtered_obj.temp_c) <= 30:
        clothes_status.shoes = "sneakers"
        clothes_status.pants = "shorts"
        clothes_status.tshirt = True
        clothes_status.hoodie = False
        clothes_status.jacket = "empty"
        clothes_status.scarf = False
        clothes_status.hat = "empty"

    # Summer Weather
    elif int(filtered_obj.temp_c) > 31:
        clothes_status.shoes = "sandals"
        clothes_status.pants = "shorts"
        clothes_status.tshirt = True
        clothes_status.hoodie = False
        clothes_status.jacket = "empty"
        clothes_status.scarf = False
        clothes_status.hat = "cap"

    clothes_status.show_outfit = True

    print("CLOTHES STATUS")
    pprint(vars(clothes_status))

    return clothes_status


def return_weather_image_logic():
    filtered_obj: FilteredItems = return_needed_info()
    weather_status: WeatherStatus = WeatherStatus()

    weather_status.moon_stars_image = False
    weather_status.moon_image = False
    weather_status.sunny_image = False
    weather_status.partly_cloudy_image = False
    weather_status.cloudy_image = False
    weather_status.drizzle_image = False
    weather_status.rainy_image = False
    weather_status.storm_image = False
    weather_status.snowy_image = False

    # Night - Clear skies - Code 1000
    if filtered_obj.condition_text == "Clear":
        weather_status.moon_image = True

    # Sunny - Code 1000
    if filtered_obj.condition_text == "Sunny":
        weather_status.sunny_image = True

    # Partly Cloudy
    if int(filtered_obj.condition_code) == 1003:
        weather_status.partly_cloudy_image = True

    # Cloudy
    if int(filtered_obj.condition_code) == 1006:
        weather_status.cloudy_image = True

    # Drizzle
    if int(filtered_obj.condition_code) == 1153 \
            or int(filtered_obj.condition_code) == 1063 \
            or int(filtered_obj.condition_code) == 1180 \
            or int(filtered_obj.condition_code) == 1183 \
            or int(filtered_obj.condition_code) == 1186:
        weather_status.drizzle_image = True

    # Rainy
    if int(filtered_obj.condition_code) == 1189 \
            or int(filtered_obj.condition_code) == 1192 \
            or int(filtered_obj.condition_code) == 1195 \
            or int(filtered_obj.condition_code) == 1240 \
            or int(filtered_obj.condition_code) == 1243 \
            or int(filtered_obj.condition_code) == 1246:
        weather_status.rainy_image = True

    # Storms
    if int(filtered_obj.condition_code) == str(1276) \
            or int(filtered_obj.condition_code) == 1087 \
            or int(filtered_obj.condition_code) == 1273 \
            or int(filtered_obj.condition_code) == 1276 \
            or int(filtered_obj.condition_code) == 1279 \
            or int(filtered_obj.condition_code) == 1282:
        weather_status.storm_image = True

    # Snowy
    if int(filtered_obj.condition_code) == 1066 \
            or int(filtered_obj.condition_code) == 1114 \
            or int(filtered_obj.condition_code) == 1210 \
            or int(filtered_obj.condition_code) == 1213 \
            or int(filtered_obj.condition_code) == 1216 \
            or int(filtered_obj.condition_code) == 1219 \
            or int(filtered_obj.condition_code) == 1222 \
            or int(filtered_obj.condition_code) == 1225 \
            or int(filtered_obj.condition_code) == 1255 \
            or int(filtered_obj.condition_code) == 1258 \
            or int(filtered_obj.condition_code) == 1279 \
            or int(filtered_obj.condition_code) == 1282:
        weather_status.snowy_image = True

    print("WEATHER STATUS")
    pprint(vars(weather_status))

    return weather_status


# return_needed_info()

return_clothes_image_logic()
return_weather_image_logic()
