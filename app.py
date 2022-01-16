import logging

from flask import Flask, render_template, request, redirect, session

from flask_wtf.csrf import CSRFProtect

from REST.register_service import save_data_to_database, check_if_user_exists_in_db
from REST.weather_service import *
from db.register_db_controller import check_password, getAllUsers, getAllRoles
from flask_session import Session

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
csrf = CSRFProtect(app)
csrf.init_app(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def index():
    try:
        return render_template('index.html', data=return_needed_info(), weather_data=return_weather_image_logic())
    except Exception:
        logging.exception("Die Seite konnte nicht geladen werden. Please check the logs!")


@app.route('/settings')
def settings():
    try:
        print(session.get("username"))
        if not session.get("username"):
            # if not there in the session then redirect to the login page
            return redirect("/log-in")
        return render_template("settings.html", allUsers=getAllUsers(), allRoles=getAllRoles())
    except Exception:
        logging.exception(
            "Die Rollen konnten nicht angezeigt werden. Dies liegt vermutlich daran, dass der Benutzer nicht eingeloggt ist oder die Session nicht gültig ist!")


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    try:
        if request.method == "POST":
            req = request.form

            username = req.get("username")
            email = req.get("email")
            password = req.get("password")

            session["username"] = request.form.get("username")

            # check if username exists in db before doing the next step
            check_if_user_exists_in_db(username, email)

            save_data_to_database(username, email, password)

            return redirect(request.url)

        return render_template("signup.html")

    except Exception:
        logging.exception("Der Benutzer konnte nicht eingeloggt werden")


@app.route("/log-in", methods=["GET", "POST"])
def log_in():
    try:
        if request.method == "POST":
            req = request.form

            username = req.get("username")
            password = req.get("password")

            check_password(username, password)

            session["username"] = request.form.get("username")

            return redirect("index.html")

        return render_template("login.html")

    except Exception:
        logging.exception("Der Benutzer konnte nicht eingeloggt werden")


@app.route('/logout')
def logout():
    try:
        session["username"] = None
        return redirect("/")
    except Exception:
        logging.exception("Der Benutzer konnte nicht ausgeloggt werden")


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
