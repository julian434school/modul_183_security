import re

import bcrypt

from db.register_db_controller import insert_into_database, check_if_user_exists


def check_if_user_exists_in_db(username: str, email: str) -> bool:
    if check_if_user_exists(username, email):
        return True
    return False


def hash_password_save_salt(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    return {"hashed_password": hashed, "salt": salt}


def save_data_to_database(username, email, password):
    if isValid(username.strip(), email.strip(), password.strip()):
        hash_and_salt = hash_password_save_salt(password)
        insert_into_database(username, email, hash_and_salt.get("hashed_password").decode('utf-8'),
                             hash_and_salt.get("salt").decode('utf-8'))

    # TODO: else: error message to user


def isValid(username: str, email: str, password: str):
    isValidUsername = re.search("^[a-zA-Z][a-zA-Z0-9-_.]{4,20}$", username)
    isValidEmail = re.search("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)
    isValidPassword = re.search("^(?=.*[a-z])(?=.*[A-Z]).{8,40}$", password)
    return isValidUsername and isValidEmail and isValidPassword
