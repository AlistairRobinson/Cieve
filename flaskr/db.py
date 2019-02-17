from pymongo import MongoClient

def get_db():
    uri = "mongodb+srv://cieve:N3gNW20iJNqwL0fC@cievedatabase-gzmjp.mongodb.net/test?retryWrites=true"
    client = MongoClient(uri)
    return Mongo(client.cieve_database)

class Mongo:
    def __init__(self, db):
        self.db = db
    
    # Return JSON of the account data for the applicant with username=username
    def getApplicantAccount(self, username):
        return
    
    # Return JSON of the account data for the client with username=username
    def getClientAccount(self, username):
        return

    # Insert to user account, return userID if completed (None if not)
    def insertApplicantUser(self, username, passHash, salt):
        return
    
    # Insert to client account, return userID if completed (None if not)
    def insertClientUser(self, username, passHash, salt):
        return
    
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