import cgi

import bcrypt

from db.register_db_controller import insert_into_database


def save_data_to_database(username, email, password):
    hash_and_salt = hash_password_save_salt(password)
    insert_into_database(username, email, hash_and_salt.get("hashed_password").decode('utf-8'),
                         hash_and_salt.get("salt").decode('utf-8'))


def hash_password_save_salt(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    return {"hashed_password": hashed, "salt": salt}
