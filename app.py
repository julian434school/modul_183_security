import logging

from flask import Flask, render_template, request, redirect, session

from flask_wtf.csrf import CSRFProtect

from REST.transfer_service import check_if_user_exists_in_db, save_issue_data, save_user_data
from REST.weather_service import *
from db.db_controller import check_password, getAllUsers, update_user_data
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


@app.route('/settings', methods=["GET", "POST"])
def settings():
    try:
        print(session.get("username"))
        if not session.get("username"):
            # if not there in the session then redirect to the login page
            return redirect("/log-in")

        if request.method == "POST":
            req = request.form

            old_username = session["username"]
            username = req.get("username")
            email = req.get("email")
            password = req.get("password")

            user = req.get("user")
            role = req.get("role")

            # update
            update_user_data(old_username, username, email, password, user, role)  # TODO: CSRF Token missing

            session["username"] = request.form.get("username")

        return render_template("settings.html", allUsers=getAllUsers())
    except Exception:
        logging.exception(
            "Die Rollen konnten nicht angezeigt werden. Dies liegt vermutlich daran, dass der Benutzer nicht eingeloggt ist oder die Session nicht gültig ist!")


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        req = request.form

        name = req.get("name")
        email = req.get("email")
        check_email = req.get("checkEmail")
        phone = req.get("tel")
        check_phone = req.get("checkPhone")
        issue = req.get("issue")
        comments = req.get("comments")

        save_issue_data(name, email, check_email, phone, check_phone, issue, comments)

    return render_template('contact.html')


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    try:
        if request.method == "POST":
            req = request.form

            username = req.get("username")
            email = req.get("email")
            password = req.get("password")

            # check if username exists in db before doing the next step
            if not check_if_user_exists_in_db(username, email):
                save_user_data(username, email, password)
                session["username"] = request.form.get("username")
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

            return redirect("/")

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
