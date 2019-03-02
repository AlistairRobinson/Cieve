from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import jsonify
from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_db():
    uri = "mongodb+srv://cieve:N3gNW20iJNqwL0fC@cievedatabase-gzmjp.mongodb.net/test?retryWrites=true"
    client = MongoClient(uri)
    return Mongo(client.cieve_database)


class Mongo:
    def __init__(self, db):
        self.db = db.db


    # Return an account class
    def getApplicantAccount(self, username):
        query = self.db.accountInfo.find_one({"username": username})
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

        applicantInfoData = {"applicant_id": applicantID}

        accountInfoData = {"name": name,
                           "username": username,
                           "password_hash": passHash,
                           "salt": salt}

        self.db.applicantInfo.insert_one(applicantInfoData)
        self.db.accountInfo.insert_one(accountInfoData)
        return applicantID


    # Insert to client account, return userID if completed (None if not)
    def insertClientUser(self, username, passHash, salt):
        clientData = {"username": username,
                      "password_hash": passHash,
                      "salt": salt}
        clientID = self.db.client.insert_one(clientData).inserted_id
        return clientID


    # Create an application, return the applicationID if completed (None if not)
    '''
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
                           "completed": False,
                           "date inputted": datetime.today()}
        print(datetime.today())
        applicationID = self.db.application.insert_one(applicationData).inserted_id
        return applicationID
    '''



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
        queryMaker = {"positions available": {"$gt": "0"}}
        if division != "":
            queryMaker['division'] = division

        if role != "":
            queryMaker['role type'] = role

        if location != "":
            queryMaker['location'] = location
        query = self.db.vacancy.find(queryMaker, {"positions available": 0, "skills": 0})
        for doc in query:
            Jobs.append(doc)

        if number == 0:
            return Jobs
        else:
            return Jobs[(number-1)*20:((number-1)*20)+20]


    # Wiil accept a json parameter which will be defined by the input, adds the new job to the DB
    def addNewJob(self, json, clientID):
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
                                        "current step": 0,
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
            stageDic[str(doc['_id'])] = doc['title']
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
        return 0


    #Return list of applications older than 6 months, delete the applications and relevent info
    def gdprCompliance(self):
        compliant = True
        query = self.db.application.find({"date inputted": {"$lt": datetime.today() - relativedelta(months=6)}}, {"applicant id": 1, "vacancy id": 1})
        for doc in query:
            compliant = False
            self.db.applicantInfo.delete_one({"applicant id": doc['applicant id']})
        self.db.application.delete_many({"date inputted": {"$lt": datetime.today() - relativedelta(months=6)}})
        return compliant


    def deleteJobByID(self, jobID):
        query = self.db.application.find_one({"vacancy id": jobID}, {"applicant id": 1, "_id": 0})
        for doc in query:
            self.db.applicantInfo.delete_one({"applicant id": doc['applicant id']})
        self.db.application.delete_many({"vacancy id": jobID})
        self.db.vacancies.delete_one({"_id": jobID})
        return True
    
    
    #Returns the weights stored
    def getWeights(self):
        weights = []
        query = self.db.feedbackWeights.find({}, {"_id": 0})
        for doc in query:
            weights.append(doc)
        return weights
    
    
    def updateWeights(self, json):
        self.db.feedbackWeights.update_one({"$set": json})
        return True
    
    #Retuns the applicants who have been accepted for the first stage or had a specialized score higher than 0.8
    def getFeedbackApplicants(self):
        feedbackApplicants = []
        query = self.db.application.find({"current step": {"$gt": 0}, "$or": [{"current step": 0, "completed": True, "specialized score": {"$gt": 0.8}}]}, {"applicant id": 1, "_id": 0})
        for doc in query:
            feedbackApplicants.append(doc)
        return feedbackApplicants
    
    #Returns the percentage of applicants that were accepted for the first stage
    def getAcceptedRate(self):
        return float(self.db.application.find({"current step": {"$gt": 1}}).size())/float(self.db.application.find({}).size())
    
    # Return true if a userID exists for either client or applicants
    def userExists(self, user_id):
        if self.db.applicant.find({"_id": user_id}) != None:
            return True
        else:
            if self.db.client.find({"_id": user_id}) != None:
                return True
        return False

    # Return a list of all divisions
    def getDivisions(self):
        divisions = []
        query = self.db.metaData.find({"divisions": 1, "_id": 0})
        for doc in query:
            divisions.append(doc)
        return divisions

    def getRoles(self):
        roles = []
        query = self.db.metaData.find({"roles": 1, "_id": 0})
        for doc in query:
            roles.append(doc)
        return roles

    def getLocations(self):
        locations = []
        query = self.db.metaData.find({"locations": 1, "_id": 0})
        for doc in query:
            locations.append(doc)
        return locations

    def newDivision(self, division):
        self.db.metaData.update_one({"$addToSet": {"divisions": division}})
        return True

    def newRole(self, role):
        self.db.metaData.update_one({"$addToSet": {"roles": role}})
        return True
    
    def newLocation(self, location):
        self.db.metaData.update_one({"$addToSet": {"locations": location}})
        return True

    # Return the id's of the stages of type "Interview"
    def getInterviewStages(self):
        interviewStages = []
        query = self.db.stage.find({"type": "Interview"}, {"_id": 1})
        for doc in query:
            interviewStages.append(doc)
        return interviewStages

    def insertStageAvailability(self):
        return

    #Given an id will return the title of the stage
    def getStageTitle(self, id):
        return self.db.stage.find_one({"_id": id}, {"title": 1, "_id": 0})['title']

    def deleteApplicantAccount(self, username):
        self.db.applicantInfo.delete_one({"username": username})
        self.db.application.delete_one({"username": username})
        return True

    def deleteClientAccount(self, username):
        self.db.client.delete_one({"username": username})
        return True

    def deleteApplication(self, username):
        self.db.application.delete_one({"username": username})
        return True

    def deleteJob(self, title):
        self.db.vacancy.delete_one({"vacancy title": title})
        return True
