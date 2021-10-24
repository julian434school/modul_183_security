from flask import Flask, render_template, request, redirect, url_for

from REST.weather_service import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', data=return_needed_info(), weather_data=return_weather_image_logic())


if __name__ == '__main__':
    app.run()
