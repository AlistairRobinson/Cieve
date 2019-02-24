from pymongo import MongoClient
from bson.objectid import ObjectId 

def get_db():
    uri = "mongodb+srv://cieve:N3gNW20iJNqwL0fC@cievedatabase-gzmjp.mongodb.net/test?retryWrites=true"
    client = MongoClient(uri)
    return Mongo(client.cieve_database)
    

class Mongo:
    def __init__(self, db):
        self.db = db.db
    
    
    # Return an account class
    def getApplicantAccount(self, username):
        query = self.db.applicantInfo.find_one({"username": username})
        if query != None:
            return query
        else:
            return None
    
    
    # Return JSON of the account data for the client with username=username
    def getClientAccount(self, username):
        query = self.db.client.find_one({"username": username})
        if query != None:
            return query
        else:
            return None


    # Insert to user account, return userID if completed (None if not)
    def insertApplicantUser(self, name, username, passHash, salt):
        applicantData = {"setup": True}
        applicantID = self.db.applicant.insert_one(applicantData).inserted_id
        
        applicantInfoData = {"applicant_id": applicantID,
                             "name": name,
                             "username": username,
                             "password_hash": passHash,
                             "salt": salt}
        self.db.applicantInfo.insert_one(applicantInfoData)
        return applicantID
    
    
    # Insert to client account, return userID if completed (None if not)
    def insertClientUser(self, username, passHash, salt):
        clientData = {"username": username,
                      "password_hash": passHash,
                      "salt": salt}
        clientID = self.db.client.insert_one(clientData).inserted_id
        return clientID
    
    
    # Create an application, return the applicationID if completed (None if not)
    def createApplication(self, applicantID, jobID, stage, score):
        query = self.db.applicant.find_one({"preferred vacancies": jobID})
        if query != None:
            preferred = True
        else:
            preferred = False

        applicationData = {"applicant id": applicantID,
                           "vacancy id": jobID,
                           "current stage": stage,
                           "specialized score": score,
                           "preferred": preferred,
                           "completed": False}
        applicationID = self.db.application.insert_one(applicationData).inserted_id
        return applicationID
    
    
    
    def updateApplication(self, applicantID, stage, completed):
        self.db.application.update_one({"applicant id": applicantID}, {"$set": {"stage": stage, "completed": completed}})
    
    
    # Return JSON of applicant info populated based on id
    def getApplicantUserID(self, id):
        query = self.db.applicantInfo.find_one({"applicant_id": ObjectId(id)})
        if query != None:
            return query
        else:
            return None


    # Return JSON of client info populated based on id
    def getClientUserID(self, id):
        query = self.db.client.find_one({"_id": ObjectId(id)})
        if query != None:
            return query
        else:
            return None


    # Returns all the jobs currently available to applications
    def getJobs(self, number, division, role, location):
        Jobs = []
        queryMaker = {"positions available": {"$gt": 0}}
        if division != "":
            queryMaker['division'] = division
        
        if role != "":
            queryMaker['role type'] = role
        
        if location != "":
            queryMaker['location'] = location
        
        query = self.db.vacancy.find(queryMaker, {"_id": 0, "positions available": 0, "applicants recieved": 0})
        for doc in query:
            Jobs.append(doc)
        
        if number == 0:
            return Jobs
        else:
            return Jobs[(number-1)*20:((number-1)*20)+20]


    # Wiil accept a json parameter which will be defined by the input, adds the new job to the DB
    def addNewJob(self, json, clientID):
        self.db.vacancy.insert_one(json)


    # Given an ID return all vacancies an applicant has applied too (including non-preferenced ones)
    def getApplications(self, applicantID):
        applications = []
        idQuery = self.db.application.find({"applicant id": ObjectId(applicantID)}, {"vacancy id": 1, "_id": 0})
        for id in idQuery:
            titleQuery = self.db.vacancy.find({"_id": id}, {"vacancy title": 1, "_id": 0})
            for title in titleQuery:
                applications.append(title)
        return applications

    def applyJob(self, userID, jobID, preferred, score):
        self.db.application.insert_one({"applicant id": userID,
                                        "vacancy id": jobID,
                                        "preferred": preferred,
                                        "specialized score": score,
                                        "completed": False})

    # Return all stages, dictionary of stage id and title
    def getStages(self):
        return ""

    # Return the details for all jobs the client is linked too
    def getClientJobs(self, clientID):
        return ""

    # Return a list of all applicants applying to a role for a specific step (1 = First stages, etc)
    # In order of job related score
    def getApplicantsJob(self, jobID, stepOrder):
        return ""
    
    #Move applicants to the next stage in the steps for the jobs and update complted flag
    def moveToNextStage(self, applicantID, JobID):
        return ""
        
get_db().insertApplicantUser("name", "user", "123", "abc")
print(get_db().getApplicantAccount("user"))
