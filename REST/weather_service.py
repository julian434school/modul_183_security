# http://api.weatherapi.com/v1/current.json?key=c809b1ec469c442c818104121211510&q=Basel&aqi=no

import os
from pprint import pprint

import requests
from PIL import Image


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


def generate_combined_image(images_list: list):
    # Before anything, delete the outfit.png so a fresh outfit can be generated
    if os.path.exists("static/clothes/outfit.png"):
        os.remove("static/clothes/outfit.png")

    if os.path.exists("static/clothes/outfit.jpg"):
        os.remove("static/clothes/outfit.jpg")

    if os.path.exists("static/clothes/outfit_small.png"):
        os.remove("static/clothes/outfit_small.png")

    if os.path.exists("static/clothes/outfit_small.jpg"):
        os.remove("static/clothes/outfit_small.jpg")

    images = [Image.open(x) for x in images_list]
    widths, heights = zip(*(i.size for i in images))

    total_width = max(widths)
    max_height = sum(heights)

    img_png_normal = Image.new('RGBA', (total_width, max_height))
    img_jpg_normal = Image.new('RGB', (total_width, max_height))
    img_png_small = Image.new('RGBA', (int(total_width / 2), int(max_height / 2)))
    img_jpg_small = Image.new('RGB', (int(total_width / 2), int(max_height / 2)))

    y_offset_regular = 0
    y_offset_small = 0
    for im in images:

        # Regular 512 x 512 format, resize to 256 x 256 because otherwise it'd be too big
        # im = im.resize((256, 256))
        img_png_normal.paste(im, (0, y_offset_regular))
        img_jpg_normal.paste(im, (0, y_offset_regular))
        y_offset_regular += im.size[0]

        # Smaller scaled 256 x 256 format for tablet & phone
        im = im.resize((256, 256))
        img_png_small.paste(im, (0, y_offset_small))
        img_jpg_small.paste(im, (0, y_offset_small))
        y_offset_small += im.size[0]

    img_png_normal.save('static/clothes/outfit.png')
    img_jpg_normal.save('static/clothes/outfit.jpg')

    img_png_small.save('static/clothes/outfit_small.png')
    img_jpg_small.save('static/clothes/outfit_small.jpg')


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

    return filtered_obj


def return_clothes_image_logic():
    filtered_obj: FilteredItems = return_needed_info()

    # Snowy
    if int(filtered_obj.temp_c) <= 0:
        generate_combined_image(
            ['static/clothes/beanie.png', 'static/clothes/scarf.png', 'static/clothes/heavy_jacket.png',
             'static/clothes/jeans.png', 'static/clothes/boots.png'])

    # Cold
    elif int(filtered_obj.temp_c) <= 10:
        generate_combined_image(
            ['static/clothes/heavy_jacket.png', 'static/clothes/jeans.png', 'static/clothes/sneakers.png'])

    # Not too cold, not warm either
    elif int(filtered_obj.temp_c) <= 14:
        generate_combined_image(
            ['static/clothes/medium_jacket.png', 'static/clothes/jeans.png', 'static/clothes/sneakers.png'])

    # Fall weather
    elif int(filtered_obj.temp_c) <= 19:
        generate_combined_image(
            ['static/clothes/light_jacket.png', 'static/clothes/jeans.png', 'static/clothes/sneakers.png'])


    # Spring Weather
    elif int(filtered_obj.temp_c) <= 23:
        generate_combined_image(
            ['static/clothes/hoodie.png', 'static/clothes/jeans.png', 'static/clothes/sneakers.png'])

    # Warm Weather
    elif int(filtered_obj.temp_c) <= 30:
        generate_combined_image(
            ['static/clothes/tshirt.png', 'static/clothes/shorts.png', 'static/clothes/sneakers.png'])

    # Summer Weather
    elif int(filtered_obj.temp_c) > 31:
        generate_combined_image(
            ['static/clothes/cap.png', 'static/clothes/tshirt.png', 'static/clothes/shorts.png',
             'static/clothes/sandals.png'])


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

    return weather_status


return_clothes_image_logic()
return_weather_image_logic()
