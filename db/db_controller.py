import bcrypt
from pymongo import *

mongodb_client = MongoClient('localhost', 27017)

database = mongodb_client["weatherapp"]

users_collection = database["users"]
issues_collection = database["issues"]

dblist = mongodb_client.list_database_names()

# on initialisation
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw("Password1".encode('utf-8'), salt)

if users_collection.count_documents(({"username": "admin", "email": "natascha.wernli@bbzbl-it.ch"})) == 0:
    users_collection.insert_one({"username": "admin", "email": "natascha.wernli@bbzbl-it.ch",
                                 "password": hashed.decode('utf-8'),
                                 "salt": salt.decode('utf-8'), "role": 1})


def check_if_user_exists(username: str, email: str):
    if users_collection.count_documents({"username": username, "email": email}) == 1:
        return True
    return False


def insert_user_data(username: str, email: str, hashed_password: str, salt: str):
    users_collection.insert_one(
        {"username": username, "email": email, "password": hashed_password, "salt": salt, "role": 0})


def insert_issue_data(name: str, email: str, check_email: bool, phone: str, check_phone: bool, issue: str,
                     comments: str):
    issues_collection.insert_one(
        {"name": name, "email": email, "check_email": check_email, "phone": phone, "check_phone": check_phone,
         "issue": issue, "comments": comments}
    )


def update_valid_user_data(old_username: str, username: str, email: str, hashed_password: str, salt: str):
    update_filter = {"username": old_username}
    values = {"$set": {"username": username, "email": email, "password": hashed_password, "salt": salt}}
    users_collection.update_one(update_filter, values)


def update_role(user: str, role: int):
    update_filter = {"username": user}
    values = {"$set": {"role": role}}
    users_collection.update_one(update_filter, values)


def check_password(username: str, password: str) -> str:
    salt = None
    hashed_password_from_db = None
    results = users_collection.find({"username": username}, {"_id": 0, "salt": 1, "password": 1})

    for x in results:
        salt = x.get("salt")
        hashed_password_from_db = x.get("password")

    if hashed_password_from_db is None or salt is None:
        return None
    else:
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password_from_db.encode('utf-8')):
            return "success"
        else:
            return None


def getAllUsers():
    return users_collection.find({}, {"username": 1})


def is_admin(username: str) -> bool:
    result = users_collection.find_one({"username": username})
    if result["role"] == 1:
        return True
    return False
