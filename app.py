from flask import Flask, render_template, request, redirect

from REST.register_service import save_data_to_database
from REST.weather_service import *
from db.register_db_controller import check_password

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', data=return_needed_info(), weather_data=return_weather_image_logic())


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        req = request.form

        username = req.get("username")
        email = req.get("email")
        password = req.get("password")

        save_data_to_database(username, email, password)

        check_password(email, password)

        return redirect(request.url)

    return render_template("signup.html")


@app.route('/logout')
def logout():
    return 'Logout'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
