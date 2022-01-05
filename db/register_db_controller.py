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

users_collection.delete_many({})


def insert_into_database(username: str, email: str, hashed_password: str, salt: str):
    users_collection.insert_one({"username": username, "email": email, "password": hashed_password, "salt": salt})
    for x in users_collection.find():
        print("DB Result: ")
        print(x)


def check_password(email: str, password: str):
    salt = None
    hashed_password_from_db = None
    results = users_collection.find({"email": email}, {"_id": 0, "salt": 1, "password": 1})

    for x in results:
        print(x)
        salt = x.get("salt")
        hashed_password_from_db = x.get("password")
    print(salt)

    if salt is None:
        # return exception or something else
        pass

    # TODO
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password_from_db.encode('utf-8')):
        print("match")
    else:
        print("does not match")


