#Code for intialisation of DB
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb+srv://cieve:N3gNW20iJNqwL0fC@cievedatabase-gzmjp.mongodb.net/test?retryWrites=true")
db = client.cieve_database

db.db.stage.insert_one({"_id":ObjectId("5c74389bad9bb61fbcc01a3a"),"type":"Interview","description":"Face to face meeting with applicant","title":"Interview"})
db.db.stage.insert_one({"_id":ObjectId("5c74389bad9bb61fbcc01a3b"),"type":"Test","description":"Reasoning and logic test","title":"Logic Test"})
db.db.stage.insert_one({"_id":ObjectId("5c7438ecad9bb61ff6d81d38"),"type":"Interview","description":"Phone meeting with applicant","title":"Mobile Interview"})
db.db.stage.insert_one({"_id":ObjectId("5c7438edad9bb61ff6d81d39"),"type":"Test","description":"Tests the verbal resonaling of an applicant","title":"Verbal Test"})
db.db.stage.insert_one({"_id":ObjectId("000000000000000000000000"),"type":"Onboarding","description":"Initial onboarding stage","title":"Onboarding"})
db.db.stage.insert_one({"_id":ObjectId("111111111111111111111111"),"type":"Accepted","description":"Final Applicants that have been offered the role","title":"Accepted"})
db.db.metaData.insert_one({"_id":ObjectId("5c7a8740229dfb0e0963c34d"),"divisions":["Technology","HR","Finance"],"locations":["London, United Kingdom","New York, United States","Paris, France"],"roles":["Internship","Graduate","Full-Time","Part-Time"]})
# Password: D3utsche$Bank
db.db.vacancy.insert_one({"_id":{"oid":"5c7d793d9a22a60680b903a7"},"vacancy title":"Software Engineer Intern","division":"Technology","prefered degrees":"University of Warwick","role type":"Internship","skills":{"Git":"8","Team Work":"7"},"vacancy description":"We are looking for bright, new interns to join us in our London office this summer as interns.","languages":{"Python":"9","Java":"7"},"location":"London, United Kingdom","positions available":10,"stages":["000000000000000000000000","5c7438ecad9bb61ff6d81d38","5c74389bad9bb61fbcc01a3a","111111111111111111111111"],"start date":"2019-07-01","min degree level":"1:1"})
db.db.vacancy.insert_one({"_id":{"oid":"5c7d7a709a22a60680b903c4"},"vacancy title":"Business Analyst","division":"Finance","prefered degrees":"University of Leicester","role type":"Graduate","skills":{"Team Work":"9","Presentation":"7","Powerpoint":"6","Project Management":"7"},"vacancy description":"We are looking for business-minded graduates to join our Business Analyst team in New York","languages":{"Python":"2"},"location":"New York, United States","positions available":5,"stages":["000000000000000000000000","5c7438edad9bb61ff6d81d39","5c7438ecad9bb61ff6d81d38","5c74389bad9bb61fbcc01a3a","111111111111111111111111"],"start date":"ASAP","min degree level":"2:1"})
db.db.interviewStage.insert_one({"_id":{"oid":"5c7d793d9a22a60680b903a8"},"slots":["2019-04-08","09:00","17:00","20"],"job id":{"oid":"5c7d793d9a22a60680b903a7"},"stage id":"5c74389bad9bb61fbcc01a3a"})
db.db.interviewStage.insert_one({"_id":{"oid":"5c7d793d9a22a60680b903a9"},"slots":["2019-04-01","09:00","17:00","40"],"job id":{"oid":"5c7d793d9a22a60680b903a7"},"stage id":"5c7438ecad9bb61ff6d81d38"})
db.db.interviewStage.insert_one({"_id":{"oid":"5c7d7a719a22a60680b903c5"},"slots":["2019-03-19","09:00","17:00","20"],"job id":{"oid":"5c7d7a709a22a60680b903c4"},"stage id":"5c7438ecad9bb61ff6d81d38"})
db.db.interviewStage.insert_one({"_id":{"oid":"5c7d7a719a22a60680b903c6"},"slots":["2019-03-20","09:00","17:00","10"],"job id":{"oid":"5c7d7a709a22a60680b903c4"},"stage id":"5c74389bad9bb61fbcc01a3a"})
# Password: M@ttC0rp
db.db.assessment.insert_one({})
db.db.feedbackWeights.insert_one({
  "Universities weight": {    },
  "Skillset weight": 0.3,
  "Experience Weight": 0.3,
  "Previous Employment Company": {  },
  "Employment length weight": 1,
  "Languages weight": 0.3,
  "Education Weight": 0.3,
  "University experience Weight": 0.3,
  "Subjects Weight": 0.3,
  "Degree Level Weight": 0.3,
  "Skills Weight":0.3,
  "Previous Employment position": {  },
  "Skills": {  },
  "Degree Qualifications": {  },
  "A-Level Qualifications": {  },
  "Languages Known": {  }
})
"""
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
"""