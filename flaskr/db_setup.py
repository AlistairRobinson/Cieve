#Code for intialisation of DB
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb+srv://cieve:N3gNW20iJNqwL0fC@cievedatabase-gzmjp.mongodb.net/test?retryWrites=true")
db = client.cieve_database
        
db.db.applicant.insert_one({"preferred vacancies": 0,
                            "considered vacancies": 0,
                            "basic score": 0,
                            "main skills": 0})

db.db.clients.insert_one({"username": 0,
                          "passHash": 0,
                          "salt": 0,
                          "email": 0,
                          "vacancies": 0})

db.db.applicantInfo.insert_one({"email": 0,
                                "name": 0,
                                "phone number": 0,
                                "degree qualification": 0,
                                "degree level": 0,
                                "attended university": 0,
                                "a-level qualifications": 0,
                                "known programming languages": 0,
                                "previous employment": 0,
                                "skills": 0})

db.db.accountInfo.insert_one({"username": 0,
                              "passHash": 0,
                              "salt": 0})

db.db.application.insert_one({"applicant id": 0,
                              "vacancy id": 0,
                              "current step": 0,
                              "specialized score": 0,
                              "preferred": 0,
                              "completed": 0})

db.db.vacancy.insert_one({"vacancy title": 0,
                          "vacancy description": 0,
                          "positions available": 0,
                          "division": 0,
                          "location": 0,
                          "role type": 0,
                          "stages" : 0,
                          "skills": 0})

db.db.stage.insert_one({"_id": ObjectId('000000000000000000000000'),
                        "type": "Onboarding",
                        "title": "Onboarding",
                        "description": "Initial onboarding stage"})

db.db.questionStage.insert_one({"stage id": 0,
                                "questions": 0})

#[QUESTIONS [ answer,  (WRONG ANSWERS)]]]

db.db.interviewStage.insert_one({"stage id": 0,
                                 "job id": 0, 
                                 "slots": ["dd/mm/yy", "hh:mm", "hh:mm", 0]})

db.db.metaData.insert_one(  { "divisions" : ["Technology", "HR", "Finance"],
                              "roles" : ["Internship", "Graduate", "Full-Time", "Part-Time"],
                              "locations" : ["London, United Kingdom", "New York, United States", "Paris, France"]})

#SLOT
#{
#    "DD/MM/YYYY : HH:MM" : APPLICATIONID
#    "21/10/20 12:00" : ""
#}

db.db.stage.insert_one({"vacancy id": 0,
                        "type": 0,
                        "questions": 0,
                        "description": 0})

db.db.assessment.insert_one({"stage id": 0,
                             "application id": 0,
                             "correct answers": 0,
                             "incorrect answers": 0,
                             "score": 0})

db.db.feedbackWeights.insert_one({
   "Education Weight": 0.3,
   "Experience Weight": 0.3,
   "Skills Weight": 0.3,
   "University experience Weight": 0.3,
   "Subjects Weight" : 0.7,
   "Degree Qualification": [
     {
       "Qualification": "Physics, MPhys",
       "Weight": 1
     },
     {
       "Qualification": "Mathematics and Statistics, MMathStat",
       "Weight": 0.7
     }
   ],
   "Degree Level Weight": 0.3,
   "University Attended Weight": 0.7,
   "A-Level Qualifications": [
     {
       "Subject": "Mathematics",
       "Weight": 0.3
     },
     {
       "Subject": "Japanese",
       "Weight": 0.1
     }
   ],

   "Languages weight": 0.6,
   "Skillset weight": 0.3,
   "Languages Known": [
     {
       "Language": "Visual Basic .NET",
       "Weight": 1.1
     },
     {
       "Language": "Ruby",
       "Weight": 0.7
     }
   ],
   "Skills": [
     {
       "Skill": "Data Entry",
       "Weight": 0.3
     },
     {
       "Skill": "Maya",
       "Weight": 0.2
     }
   ],

   "Previous Employment": [
     {
       "Position": "Senior Architect",
       "Weight": 0.3
     }
   ]
 })
