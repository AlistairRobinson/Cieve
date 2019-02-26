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
        number = int(number)
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
        skillDic = {}
        skillVal = json.pop('skillVal', None)
        skills = json.pop('skills', None)
        for i in range(len(skills)):
            skillDic[skills[i]] = skillVal[i]
        json['skills'] = skillDic
        jobID = self.db.vacancy.insert_one(json).inserted_id
        self.db.client.update_one({"_id": clientID}, {"$push": {"vacancies": jobID}})

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
                                        "completed": True})


    def addNewStage(self, stageType, title, description):
        self.db.stage.insert_one({"type": stageType,
                                  "title": title,
                                  "description": description})


    # Return all stages, dictionary of stage id and title
    def getStages(self):
        stageDic = {}
        query = self.db.stage.find({}, {"title": 1})
        for doc in query:
            stageDic[doc['_id']] = doc['title']
        return stageDic


    # Return the details for all jobs the client is linked too
    def getClientJobs(self, clientID):
        jobDetails = []
        clientQuery = self.db.client.find({"_id": clientID}, {"vacancies": 1, "_id": 0})
        for doc in clientQuery:
            for id in doc['vacancies']:
                jobQuery = self.db.vacancy.find({"_id": id})
                for job in jobQuery:
                    jobDetails.append(job)
        return jobDetails


    # Return a list of all applicants applying to a role for a specific step (1 = First stages, etc)
    # In order of job related score
    def getApplicantsJob(self, jobID, stepOrder):
        applicantList = []
        applicationQuery = self.db.application.find({"vacancy id": jobID, "current step": stepOrder}).sort({"specialized score": -1})
        for doc in applicationQuery:
            applicantList.append(doc)
        return applicantList
    
    
    #Move applicants to the next stage in the steps for the jobs and update completed flag
    def moveToNextStage(self, applicationID, jobID):
        self.db.application.update_one({"_id": applicationID}, {"$inc": {"current step": 1}}, {"$set": {"completed": False}})
        
    # Return the total number of pages for a specific job sort
    def getPageTotal(self, division, role, location):
        return ""
#delete all applications older than 6 months along with all application info

#cascade with deleting vacancies and also applications

#retreive all applications older than 6 months

get_db().insertApplicantUser("name", "user", "123", "abc")
print(get_db().getApplicantAccount("user"))
