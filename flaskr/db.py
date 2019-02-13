from pymongo import MongoClient

def get_db():
    uri = ""
    client = MongoClient(uri)
    return Mongo(client.my_database)

class Mongo:
    def __init__(self, db):
        self.db = db
    
    # Return an account class
    def getUserAccount(self, username):
        return
    
    # Return an account class
    def getClientAccount(self, username):
        return

    # Insert to user account, return userID if completed (None if not)
    def insertApplicantUser(self, username, passHash, salt):
        return
    
    # Insert to client account, return userID if completed (None if not)
    def insertClientUser(self, username, passHash, salt):
        return
    
    # Return applicant class populated based on id
    def getApplicantUserID(self, id):
        return

    # Return client class populated based on id
    def getClientUserID(self, id):
        return

#Stores details from user and client account details
class Account:
    def __init__(self, id, username, password, salt):
        self.id = id
        self.username = username
        self.password = password
        self.salt = salt

class Applicant:
    def __init__():
        return

class Client:
    def __init__():
        return