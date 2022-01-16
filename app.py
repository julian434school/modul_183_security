import logging

from flask import Flask, render_template, request, redirect, session
from flask_mail import Mail
from flask_mail import Message
from flask_wtf.csrf import CSRFProtect

from REST.transfer_service import check_if_user_exists_in_db, save_issue_data, save_user_data, update_user_data, \
    get_current_role
from REST.weather_service import *
from db.db_controller import check_password, getAllUsers
from flask_session import Session

app = Flask(__name__)
mail = Mail(app)
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'a2674fac17b183'
app.config['MAIL_PASSWORD'] = 'b771f4451ce7d4'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
csrf = CSRFProtect(app)
csrf.init_app(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


logging.basicConfig(filename='error.log', level=logging.ERROR, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.route('/')
def index():
    try:
        session["role"] = None
        return render_template('index.html', data=return_needed_info(), weather_data=return_weather_image_logic())
    except Exception as e:
        app.logger.error(e)
        return redirect("/error")


@app.route('/settings', methods=["GET", "POST"])
def settings():
    try:
        if not session.get("username"):
            # if not there in the session then redirect to the login page
            return redirect("/log-in")

        session["role"] = get_current_role(session["username"])
        if request.method == "POST":
            req = request.form

            old_username = session["username"]
            username = req.get("username")
            email = req.get("email")
            password = req.get("password")

            user = req.get("user")
            role = req.get("role")

            # update
            if update_user_data(old_username, username, email, password, user, role) is None:
                app.logger.error("Could not update user data - invalid input")
                return redirect("/error")
            if req.get("username"):
                session["username"] = req.get("username")

        return render_template("settings.html", allUsers=getAllUsers())
    except Exception as e:
        app.logger.error(e)
        return redirect("/error")


@app.route('/contact', methods=["GET", "POST"])
def contact():
    try:
        if not session.get("username"):
            # if not there in the session then redirect to the login page
            return redirect("/log-in")

        session["role"] = None
        if request.method == "POST":
            req = request.form

            name = req.get("name")
            email = req.get("email")
            check_email = req.get("checkEmail")
            phone = req.get("tel")
            check_phone = req.get("checkPhone")
            issue = req.get("issue")
            comments = req.get("comments")

            if save_issue_data(name, email, check_email, phone, check_phone, issue, comments) is None:
                app.logger.error("Could not save issue data - invalid input")
                return redirect("/error")

            msg = Message("Hello", sender="julian.mathis@bbzbl-it.ch", recipients=["julian.mathis04@gmail.com"])
            msg.body = "Python Flask Test"

            # mail.send(msg)

        return render_template('contact.html')

    except Exception as e:
        app.logger.error(e)
        return redirect("/error")


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
                if save_user_data(username, email, password) is None:
                    app.logger.error("Could not save user data - invalid input")
                    return redirect("/error")
                session["username"] = request.form.get("username")
                return redirect(request.url)

        return render_template("signup.html")

    except Exception as e:
        app.logger.error(e)
        return redirect("/error")


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

    except Exception as e:
        app.logger.error(e)
        return redirect("/error")


@app.route("/logout")
def logout():
    try:
        session["username"] = None
        return redirect("/")
    except Exception as e:
        app.logger.error(e)
        return redirect("/error")


@app.route("/error")
def error():
    return render_template("error.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
