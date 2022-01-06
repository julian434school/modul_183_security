import cgi

from flask import Flask, render_template, request, redirect, session
from flask_session import Session

from REST.register_service import save_data_to_database
from REST.weather_service import *
from db.register_db_controller import check_password
import cgitb
# from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# csrf = CSRFProtect(app)
Session(app)


@app.route('/')
def index():
    return render_template('index.html', data=return_needed_info(), weather_data=return_weather_image_logic())


@app.route('/roles')
def roles():
    print(session.get("username"))
    if not session.get("username"):
        # if not there in the session then redirect to the login page
        return redirect("/log-in")
    return render_template("roles.html")


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        req = request.form

        username = req.get("username").encode()
        email = req.get("email")
        password = req.get("password")

        session["username"] = request.form.get("username")

        save_data_to_database(username, email, password)

        return redirect(request.url)

    return render_template("signup.html")


@app.route("/log-in", methods=["GET", "POST"])
def log_in():
    if request.method == "POST":
        req = request.form

        username = req.get("username")
        password = req.get("password")

        check_password(username, password)

        session["username"] = request.form.get("username")

        return redirect("/")

    return render_template("login.html")


@app.route('/logout')
def logout():
    session["username"] = None
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
