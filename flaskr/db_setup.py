#Code for intialisation of DB
from pymongo import MongoClient

client = MongoClient("mongodb+srv://cieve:N3gNW20iJNqwL0fC@cievedatabase-gzmjp.mongodb.net/test?retryWrites=true")
db = client.cieve_database

db.applicant.insert_one({"preferred vacancies": 0,
                         "considered vacancies": 0,
                         "basic score": 0,
                         "main skills": 0})

db.clients.insert_one({"username": 0,
                       "passHash": 0,
                       "salt": 0,
                       "email": 0,
                       "vacancies": 0})

db.applicantInfo.insert_one({"username": 0,
                             "passHash": 0,
                             "salt": 0,
                             "email": 0,
                             "name": 0,
                             "phone number": 0,
                             "degree qualification": 0,
                             "degree level": 0,
                             "attended university": 0,
                             "a-level qualifications": 0,
                             "known programming languages": 0,
                             "previous employment": 0,
                             "skills": 0})

db.application.insert_one({"applicant id": 0,
                           "vacancy id": 0,
                           "current stage": 0,
                           "specialized score": 0,
                           "preferred": 0,
                           "completed": 0})

db.vacancy.insert_one({"vacancy title": 0,
                       "vacancy description": 0,
                       "positions available": 0,
                       "division": 0,
                       "location": 0,
                       "role type": 0,
                       "applications receieved": 0})

db.stage.insert_one({"vacancy id": 0,
                     "type": 0,
                     "questions": 0,
                     "description": 0})

db.assessment.insert_one({"stage id": 0,
                          "correct answers": 0,
                          "incorrect answers": 0,
                          "score": 0})
