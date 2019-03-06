from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import jsonify
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math


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

    def getApplicantPhish(self, id):
        query = self.db.accountInfo.find_one({"applicant id": ObjectId(id[1:])}, {'phish': 1})
        if query is not None:
            return query.get('phish', [""])[0]
        return ""

    def getClientPhish(self, id):
        query = self.db.client.find_one({"_id": ObjectId(id[1:])}, {'phish': 1})
        if query is not None:
            return query.get('phish', [""])[0]
        return ""

    def getInterviewStages(self):
        interviewStages = []
        query = self.db.stage.find({"type": "Interview"}, {"_id": 1})
        for doc in query:
            interviewStages.append(str(doc["_id"]))
        return interviewStages

    # Insert to user account, return userID if completed (None if not)
    def insertApplicantUser(self, name, username, passHash, salt, phish):
        applicantData = {"setup": True}
        applicantID = self.db.applicant.insert_one(applicantData).inserted_id

        applicantInfoData = {"applicant id": applicantID}

        accountInfoData = {"applicant id": applicantID,
                           "name": name,
                           "username": username,
                           "password_hash": passHash,
                           "salt": salt,
                           "phish": phish,
                           "message": "Welcome to Cieve. You can search for available jobs by clicking Job Search. You can make an application by clicking Applications"}

        self.db.applicantInfo.insert_one(applicantInfoData)
        self.db.accountInfo.insert_one(accountInfoData)
        return applicantID


    # Insert to client account, return userID if completed (None if not)
    def insertClientUser(self, username, passHash, salt, phish):
        clientData = {"username": username,
                      "password_hash": passHash,
                      "salt": salt,
                      "phish": phish,
                      "vacancies": [],
                      "message": "Welcome to Cieve. You can create a job posting by clicking New Job. You can view your vacancies and applications by clicking Your Jobs"}
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
        query = self.db.applicantInfo.find_one({"applicant id": ObjectId(id)})
        if query != None:
            return query
        else:
            return None
    
    def getApplicantNameID(self, id):
        query = self.db.accountInfo.find_one({"applicant id": ObjectId(id)})
        if query is not None:
            return query.get("name", "")
        return None

    def getClientNameID(self, id):
        query = self.db.client.find_one({"_id": ObjectId(id)})
        if query is not None:
            return query.get("name", "")
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

        query = self.db.vacancy.find(queryMaker, {"positions available": 0, "skills": 0})
        for doc in query:
            Jobs.append(doc)

        if number == 0:
            return Jobs
        else:
            return Jobs

    #Return the data of a job given the jobID
    def getJob(self, jobID):
        return list(self.db.vacancy.find({"_id": ObjectId(jobID)}))[0]

    # Wiil accept a json parameter which will be defined by the input, adds the new job to the DB
    def addNewJob(self, json, clientID):
        jobID = self.db.vacancy.insert_one(json).inserted_id
        self.db.client.update_one({"_id": ObjectId(clientID)}, {"$push": {"vacancies": jobID}})
        return jobID

    # Given an ID return all vacancies an applicant has applied too (including non-preferenced ones)
    def getApplications(self, applicantID):
        applicationQuery = list(self.db.application.find({"applicant id": ObjectId(applicantID)}, {"date inputted": 0, "specialized score": 0}))
        for application in applicationQuery:
            vacancyID = application['vacancy id']
            vacancy = list(self.db.vacancy.find({"_id": ObjectId(vacancyID)}, {"positions available": 0, "skills": 0, "_id": 0}))[0]
            for key, item in vacancy.items():
                application[key] = item
        return applicationQuery


    def applyJob(self, userID, jobID, preferred, score):
        self.db.application.insert_one({"applicant id": ObjectId(userID),
                                        "vacancy id": ObjectId(jobID),
                                        "current step": 0,
                                        "preferred": preferred,
                                        "specialized score": score,
                                        "completed": True})

    def getJobID(self, title):
        return self.db.vacancy.find_one({"vacancy title": title})['_id']

    def addNewStage(self, stageType, title, description):
        self.db.stage.insert_one({"type": stageType,
                                  "title": title,
                                  "description": description})


    # Return all stages, dictionary of stage id and title
    def getStages(self):
        stageDic = {}
        query = self.db.stage.find({}, {"title": 1})
        for doc in query:
            if str(doc['_id']) != '000000000000000000000000':
                if str(doc['_id']) != '111111111111111111111111':
                    stageDic[str(doc['_id'])] = doc['title']
        return stageDic


    # Return the details for all jobs the client is linked too
    def getClientJobs(self, clientID):
        jobDetails = []
        clientQuery = self.db.client.find({"_id": ObjectId(clientID)}, {"vacancies": 1, "_id": 0})
        for doc in clientQuery:
            for id in doc['vacancies']:
                jobQuery = self.db.vacancy.find({"_id": ObjectId(id)})
                for job in jobQuery:
                    job["_id"] = str(job["_id"])
                    jobDetails.append(job)
        return jobDetails


    # Return a list of all applicants applying to a role for a specific step (1 = First stages, etc)
    # In order of job related score
    def getApplicantsJob(self, jobID, stepOrder):
        applicantList = []
        applicationQuery = self.db.application.find({"vacancy id": ObjectId(jobID), "current step" : stepOrder})#.sort({"specialized score": -1})
        for doc in applicationQuery:
            applicantList.append(doc)
        return applicantList


    #Move applicants to the next stage in the steps for the jobs and update completed flag
    def moveToNextStage(self, applicantID, jobID):
        stageQuery = self.db.vacancy.find_one({"_id": ObjectId(jobID)}, {"stages": 1, "_id": 0})
        noOfStages = len(stageQuery['stages'])
        self.db.application.update_one({"applicant id": ObjectId(applicantID), "vacancy id": ObjectId(jobID)}, {"$inc": {"current step": 1}, "$set": {"completed": False}})
        stepQuery = self.db.application.find_one({"applicant id": ObjectId(applicantID), "vacancy id": ObjectId(jobID), "current step": noOfStages-1})
        jobTitle = self.db.vacancy.find_one({"_id": ObjectId(jobID)})
        if stepQuery != None:
            self.db.vacancy.update_one({"_id": ObjectId(jobID)}, {"$inc": {"positions available": -1}})
            message = "You have been accepted for " + jobTitle + "!"
        else:
            message = "You have been moved onto the next stage for your application for " + jobTitle + ""
        self.db.accountInfo.update_one({"applicant id": applicantID}, {"$set": {"message": message}})
        return True


    # Return the total number of pages for a specific job sort
    def getPageTotal(self, division, role, location):
        queryMaker = {"positions available": {"$gt": 0}}
        if division != "":
            queryMaker['division'] = division

        if role != "":
            queryMaker['role type'] = role

        if location != "":
            queryMaker['location'] = location

        availableJobs = list(self.db.vacancy.find(queryMaker))
        return math.ceil(len(availableJobs)/20)


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
        self.db.vacancies.delete_one({"_id": ObjectId(jobID)})
        return True


    #Returns the weights stored
    def getWeights(self):
        weights = []
        query = self.db.feedbackWeights.find({}, {"_id": 0})
        for doc in query:
            weights.append(doc)
        return weights


    def updateWeights(self, json):
        self.db.feedbackWeights.update_one({}, {"$set": json})
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
        if self.db.applicant.find({"_id": ObjectId(user_id)}) != None:
            return True
        else:
            if self.db.client.find({"_id": ObjectId(user_id)}) != None:
                return True
        return False

    def clientExists(self, user_id):
        if self.db.client.find({"_id": ObjectId(user_id)}) != None:
            return True
        return False

    def applicantExists(self, user_id):
        if self.db.applicant.find({"_id": ObjectId(user_id)}) != None:
            return True
        return False

    # Return a list of all divisions
    def getDivisions(self):
        divisions = []
        query = self.db.metaData.find({},{"divisions": 1, "_id": 0})
        for x in query[0]["divisions"]:
            divisions.append(x)
        return divisions

    def getRoles(self):
        roles = []
        query = self.db.metaData.find({},{"roles": 1, "_id": 0})
        for x in query[0]["roles"]:
            roles.append(x)
        return roles

    def getLocations(self):
        locations = []
        query = self.db.metaData.find({},{"locations": 1, "_id": 0})
        for x in query[0]["locations"]:
            locations.append(x)
        return locations

    def newDivision(self, division):
        self.db.metaData.update_one({}, {"$addToSet": {"divisions": division}})
        return True

    def newRole(self, role):
        self.db.metaData.update_one({}, {"$addToSet": {"roles": role}})
        return True

    def newLocation(self, location):
        self.db.metaData.update_one({}, {"$addToSet": {"locations": location}})
        return True

    def getQuestions(self, stageID):
        query = self.db.questionStage.find_one({"stage id": ObjectId(stageID)})
        return query['questions']

    def insertQuestions(self, stageID, questions):
        self.db.questionStage.insert_one({"stage id": stageID, "questions": questions})
        return True


    def getInterviewSlots(self, stageID, jobID):
        timeSlots = self.db.interviewStage.find_one({"stage id": stageID, "vacancy id": jobID})
        return timeSlots['slots']


    def bookInterviewSlots(self, applicantID, jobID, stageID, slot):
        self.db.application.update_one({"applicant id": applicantID, "vacancy id": jobID}, {"$push": {"interviews": slot}})
        self.db.interviewStage.update_one({"job id": jobID, "stage id": stageID}, {"$pull": {"slots": slot}})
        jobTitle = self.db.vacancy.find_one({"_id": ObjectId(jobID)})['vacancy title']
        message = "An interview has been booked for your application to " + jobTitle + " at the time " + slot[1] + ", " + slot[0] + ""
        self.db.accountInfo.update_one({"applicant id": applicantID}, {"$set": {"message": message}})
        return True

    def getBookedInterviews(self, applicantID):
        return list(self.db.application.find({"applicant id": applicantID}, {"interviews": 1, "_id": 0}))        

    def insertStageAvailability(self, stageID, jobID, stageData):
        self.db.interviewStage.insert_one({"stage id": stageID,
                                            "job id": jobID,
                                            "slots": stageData})
        return True


    #Generate the assessment details for the stage
    def assessQuestions(self, answers, currentStep, applicantID, jobID, stepStageID):
        self.db.assessement.insert_one({"applicant id": ObjectId(applicantID),
                                        "job id": ObjectId(jobID),
                                        "current step": currentStep,
                                        "score": 0})
        print answers
        print currentStep
        print applicantID
        print jobID
        print stepStageID
        stepQuestions = self.db.questionStage.find_one({"stage id": ObjectId(stepStageID)}, {"questions": 1, "_id": 0})
        for i in range(len(answers)):
            if answers[i] == stepQuestions['questions'][i].values()[0][0]:
                self.db.assessement.update_one({"applicant id": ObjectId(applicantID), "job id": ObjectId(jobID), "current step": currentStep}, {"$inc": {"score"}})

    def getStageResults(self, currentStep, applicantID, jobID):
        return self.db.assessment.find_one({"applicant id": ObjectId(applicantID), "job id": ObjectId(jobID), "current step": currentStep})['score']


    #If applicant is rejected on step 0, set step to -1. Otherwise if rejected the set is set to -2
    def rejectApplication(self, applicationID):
        stepQuery = self.db.application.find_one({"_id": ObjectId(applicationID)}, {"current step": 1, "applicant id": 1, "vacancy id": 1, "_id": 0})
        if stepQuery['current step'] == 0:
            self.db.application.update_one({"_id": ObjectId(applicationID)}, {"$set": {"current step": -1}})
        else:
            self.db.application.update_one({"_id": ObjectId(applicationID)}, {"$set": {"current step": -2}})
        jobTitle = self.db.vacancy.find_one({"_id": ObjectId(stepQuery['vacancy id'])})['vacancy title']
        message = "Your application for " + jobTitle + " has been rejected"
        self.db.accountInfo.update_one({"applicant id": stepQuery['applicant id']}, {"$set": {"message": message}})

    def getAccepted(self, jobID):
        return list(self.db.application.find({"vacancy id": jobID, "current step": {"$gt": 0}}))

    def getRejected(self, jobID):
        rejectedQuery = self.db.application.find({"vacancy id": jobID, "current step": {"$lt": 0}})
        rejected = list(rejectedQuery)

        for doc in rejectedQuery:
            self.db.application.delete_one({"applicant id": doc['applicant id'], "vacancy id": jobID})
            if len(self.db.applicantInfo.find_one({"applicant id": ObjectId(doc['applicant id'])}, {"vacancy ids": 1, "_id": 0})['vacancy ids']) == 0:        
                self.db.applicantInfo.delete_one({"applicant id": doc['applicant id']})
            else:
                self.db.applicantInfo.update_one({"applicant id": ObjectId(doc['applicant id'])}, {"$pull": {"vacancy ids": jobID}})

        return rejected


    def getApplicantMessage(self, applicantID):
        if self.db.accountInfo.find_one({"applicant id": ObjectId(applicantID)}) is not None:
            return self.db.accountInfo.find_one({"applicant id": ObjectId(applicantID)}).get('message', "")
        return ""

    def getClientMessage(self, id):
        if self.db.client.find_one({"_id": ObjectId(id)}) is not None:
            return self.db.client.find_one({"_id": ObjectId(id)}).get('message', "")
        return ""

    #Given an id will return the title of the stage
    def getStageTitle(self, id):
        query = self.db.stage.find_one({"_id": ObjectId(id)}, {"title": 1, "_id": 0})
        if query is not None:
            return query['title']
        return ""

    def getStageType(self, id):
        query = self.db.stage.find_one({"_id": ObjectId(id)}, {"type": 1, "_id": 0})
        if query is not None:
            return query['type']
        return ""

    def deleteApplicantAccount(self, username):
        self.db.accountInfo.delete_many({"username": username})
        return True

    def deleteClientAccount(self, username):
        self.db.client.delete_many({"username": username})
        return True

    def deleteApplication(self, username):
        self.db.application.delete_many({"applicant id": self.getApplicantAccount(username)['applicant id']})
        self.db.applicantInfo.delete_many({"applicant id": self.getApplicantAccount(username)['applicant id']})
        return True

    def deleteJob(self, title):
        self.db.vacancy.delete_many({"vacancy title": title})
        clientQuery = self.db.client.find({"vacancies": title})
        message = "Vacancy " + title + "has been deleted"
        for doc in clientQuery:
            self.db.client.update_one({"_id": ObjectId(doc['_id'])}, {"$set": {message}})
        return True

    def addUserEducation(self, userID, alevels, degreeQualification, degreeLevel, universityAttended):
        self.db.applicantInfo.update_one({"applicant id": ObjectId(userID)},
                                         {"$set": {"a-level qualifications": alevels, "degree qualification": degreeQualification, "degree level": degreeLevel, "attended university": universityAttended}})
        return True

    def addUserSkills(self, userID, skills):
        self.db.applicantInfo.update_one({"applicant id": ObjectId(userID)},
                                         {"$set": {"skills": skills}})
        return True

    def addUserLanguages(self, userID, languages):
        self.db.applicantInfo.update_one({"applicant id": ObjectId(userID)},
                                         {"$set": {"languages": languages}})
        return True

    def addUserEmployment(self, userID, employmentHistory):
        self.db.applicantInfo.update_one({"applicant id": ObjectId(userID)},
                                         {"$set": {"previous employment": employmentHistory}})
        return True

    def addUserContacts(self, userID, phoneNumber, address):
        self.db.applicantInfo.update_one({"applicant id": ObjectId(userID)},
                                         {"$set": {"phone number": phoneNumber, "address": address}})
        return True

    def addUserMetaData(self, userID, coverLetter, interestingFacts):
        self.db.applicantInfo.update_one({"applicant id": ObjectId(userID)},
                                         {"$set": {"cover letter": coverLetter, "interesting facts": interestingFacts}})
        return True

    def addUserScore(self, userID, userScore):
        self.db.applicantInfo.update_one({"applicant id": ObjectId(userID)},
                                         {"$set": {"basic score": userScore}})
        return True

    def addUserJobs(self, userID, jobIDs):
        self.db.applicantInfo.update_one({"applicant id": ObjectId(userID)},
                                         {"$set": {"vacancy ids": jobIDs}})
        return True