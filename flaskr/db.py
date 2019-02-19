from pymongo import MongoClient

def get_db():
    uri = "mongodb+srv://cieve:N3gNW20iJNqwL0fC@cievedatabase-gzmjp.mongodb.net/test?retryWrites=true"
    client = MongoClient(uri)
    return Mongo(client.cieve_database)

class Mongo:
    def __init__(self, db):
        self.db = db
    
    # Return an account class
    def getClientAccount(self, username):
        query = get_db().applicantInfo.find_one({"username": username})
        if query == None:
            return query
        else:
            print("This username does not exist")
    
    # Return JSON of the account data for the client with username=username
    def getClientAccount(self, username):
        query = get_db().client.find_one({"username": username})
        if query == None:
            return query
        else:
            print("This username does not exist")

    # Insert to user account, return userID if completed (None if not)
    def insertApplicantUser(self, username, passHash, salt):
        applicantData = {"setup": True}
        get_db().applicant.insert_one(applicantData)
        applicantID = get_db().applicant.insert_one(applicantData).inserted_id
        
        applicantInfoData = {"applicant_id": applicantID,
                             "username": username,
                             "password_hash": passHash,
                             "salt": salt}
        get_db().applicantInfo.insert_one(applicantInfoData)
        return applicantID
    
    # Insert to client account, return userID if completed (None if not)
    def insertClientUser(self, username, passHash, salt):
        clientData = {"username": username,
                      "password_hash": passHash,
                      "salt": salt}
        get_db().client.insert_one(clientInfoData)
        return get_db().client.insert_one(clientInfoData).inserted_id
    
    # Return JSON of applicant info populated based on id
    def getApplicantUserID(self, id):
        return

    # Return JSON of client info populated based on id
    def getClientUserID(self, id):
        return
    
    # Returns all the jobs currently available to applications
    def getJobs(self, number, division, role, location):
        return

    # Adds a new job to the database
    def addJob(self, jsonData):
        return

    # Assign Applicant to Job
    def applyJob(self, userID, jobID):
        return