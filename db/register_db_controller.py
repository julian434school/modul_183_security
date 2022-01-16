import bcrypt
from pymongo import *

mongodb_client = MongoClient('localhost', 27017)

database = mongodb_client["weatherapp"]

users_collection = database["users"]

dblist = mongodb_client.list_database_names()
if "weatherapp" in dblist:
    print("The database exists.")
else:
    print("The database does not exist, yet")


def check_if_user_exists(email: str):
    results = users_collection.find({"email": email}, {"_id": 0, "username": 1, "email": 1})

    for x in results:
        print(x)
        # salt = x.get("salt")
        # hashed_password_from_db = x.get("password")

    if results is not None:
        return True

    return False


print(check_if_user_exists("julian.mathis04@gmail.com"))


def insert_into_database(username: str, email: str, hashed_password: str, salt: str):
    users_collection.insert_one({"username": username, "email": email, "password": hashed_password, "salt": salt, "role": 0})
    for x in users_collection.find():
        print("DB Result: ")
        print(x)


def check_password(username: str, password: str):
    salt = None
    hashed_password_from_db = None
    results = users_collection.find({"username": username}, {"_id": 0, "salt": 1, "password": 1})

    for x in results:
        print(x)
        salt = x.get("salt")
        hashed_password_from_db = x.get("password")
    print(salt)

    if salt is None:
        # return exception or something else
        pass

    if hashed_password_from_db is None:
        print("PASSWORD NOT FOUND")
    else:
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password_from_db.encode('utf-8')):
            print("match")
        else:
            print("does not match")


def getAllUsers():
    return users_collection.find({}, {"username": 1})


def getAllRoles():
    return users_collection.find({}, {"role": 1})
