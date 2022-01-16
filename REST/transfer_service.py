import re

import bcrypt

from db.db_controller import check_if_user_exists, update_role, insert_user_data, update_valid_user_data, \
    insert_issue_data, \
    is_admin


def check_if_user_exists_in_db(username: str, email: str) -> bool:
    if check_if_user_exists(username, email):
        return True
    return False


def hash_password_save_salt(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    return {"hashed_password": hashed, "salt": salt}


def save_user_data(username, email, password) -> str:
    if is_valid_user_data(username.strip(), email.strip(), password.strip()):
        hash_and_salt = hash_password_save_salt(password)
        insert_user_data(username, email, hash_and_salt.get("hashed_password").decode('utf-8'),
                         hash_and_salt.get("salt").decode('utf-8'))
        return "success"
    else:
        return None


def update_user_data(old_username: str, username: str, email: str, password: str, user: str, role: str) -> str:
    isValidUserData = False
    if username and email and password:
        isValidUserData = is_valid_user_data(username.strip(), email.strip(), password.strip())
    if not role and not isValidUserData:
        return None
    if role:
        update_role(user, int(role))
    if isValidUserData:
        hash_and_salt = hash_password_save_salt(password)
        update_valid_user_data(old_username, username, email, hash_and_salt.get("hashed_password").decode('utf-8'),
                               hash_and_salt.get("salt").decode('utf-8'))
    return "success"


def save_issue_data(name: str, email: str, check_email: bool, phone: str, check_phone: bool, issue: str, comments: str) \
        -> str:
    if is_valid_issue_data(name.strip(), email.strip(), phone.strip(), comments.strip()):
        insert_issue_data(name, email, check_email, phone, check_phone, issue, comments)
        return "success"
    return None


def get_current_role(username: str) -> int:
    if is_admin(username):
        return 1
    return 0


def is_valid_user_data(username: str, email: str, password: str) -> bool:
    isValidUsername = re.search("^[a-zA-Z][a-zA-Z0-9-_.]{4,20}$", username)
    isValidEmail = re.search("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$", email)
    isValidPassword = re.search("^(?=.*[a-z])(?=.*[A-Z]).{8,40}$", password)
    return isValidUsername and isValidEmail and isValidPassword


def is_valid_issue_data(name: str, email: str, phone: str, comments: str) -> bool:
    isValidName = re.search("^[a-zA-Z0-9]{2,40}$", name)
    isValidEmail = re.search("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$", email)
    isValidPhone = True
    areValidComments = True
    if phone:
        isValidPhone = re.search("^(\+41|0041|0){1}(\(0\))?[0-9]{9}$", phone)
    if comments:
        areValidComments = re.search("^[A-Za-z0-9_@.#&+-=?!* ]{1,200}$", comments)
    return isValidName and isValidEmail and isValidPhone and areValidComments
