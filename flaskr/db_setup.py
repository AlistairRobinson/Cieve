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
db.db.client.insert_one({"_id":ObjectId("5c7d77bb9a22a60680b9037c"),"username":"recruitment@db.com","vacancies":[ObjectId("5c7d793d9a22a60680b903a7"), ObjectId("5c7d7a709a22a60680b903c4")],"salt":"$2b$12$uCxKfl9I4eT5CTjazl2oxu", "phish":["Durban"],"password_hash":"pbkdf2:sha256:50000$ALoKpG6R$885b74f15cbdd145d48354dd12867ee7bfe70ac73015800eacfb7fc764e6e042","message": ""})
db.db.vacancy.insert_one({"_id":ObjectId("5c7d793d9a22a60680b903a7"),"vacancy title":"Software Engineer Intern","division":"Technology","prefered degrees":"University of Warwick","role type":"Internship","skills":{"Git":"8","Team Work":"7"},"vacancy description":"We are looking for bright, new interns to join us in our London office this summer as interns.","languages":{"Python":"9","Java":"7"},"location":"London, United Kingdom","positions available":"10","stages":["000000000000000000000000","5c7438ecad9bb61ff6d81d38","5c74389bad9bb61fbcc01a3a","111111111111111111111111"],"start date":"2019-07-01","min degree level":"1:1"})
db.db.vacancy.insert_one({"_id":ObjectId("5c7d7a709a22a60680b903c4"),"vacancy title":"Business Analyst","division":"Finance","prefered degrees":"University of Leicester","role type":"Graduate","skills":{"Team Work":"9","Presentation":"7","Powerpoint":"6","Project Management":"7"},"vacancy description":"We are looking for business-minded graduates to join our Business Analyst team in New York","languages":{"Python":"2"},"location":"New York, United States","positions available":"5","stages":["000000000000000000000000","5c7438edad9bb61ff6d81d39","5c7438ecad9bb61ff6d81d38","5c74389bad9bb61fbcc01a3a","111111111111111111111111"],"start date":"ASAP","min degree level":"2:1"})
db.db.interviewStage.insert_one({"_id":ObjectId("5c7d793d9a22a60680b903a8"),"slots":["2019-04-08","09:00","17:00","20"],"job id":ObjectId("5c7d793d9a22a60680b903a7"),"stage id":"5c74389bad9bb61fbcc01a3a"})
db.db.interviewStage.insert_one({"_id":ObjectId("5c7d793d9a22a60680b903a9"),"slots":["2019-04-01","09:00","17:00","40"],"job id":ObjectId("5c7d793d9a22a60680b903a7"),"stage id":"5c7438ecad9bb61ff6d81d38"})
db.db.interviewStage.insert_one({"_id":ObjectId("5c7d7a719a22a60680b903c5"),"slots":["2019-03-19","09:00","17:00","20"],"job id":ObjectId("5c7d7a709a22a60680b903c4"),"stage id":"5c7438ecad9bb61ff6d81d38"})
db.db.interviewStage.insert_one({"_id":ObjectId("5c7d7a719a22a60680b903c6"),"slots":["2019-03-20","09:00","17:00","10"],"job id":ObjectId("5c7d7a709a22a60680b903c4"),"stage id":"5c74389bad9bb61fbcc01a3a"})
# Password: M@ttC0rp
db.db.accountInfo.insert_one({"_id":ObjectId("5c7d7c3c9a22a60680b903d1"),"username":"matt@mattcorp.com","name":"Matthew Pull","applicant id":ObjectId("5c7d7c3c9a22a60680b903cf"),"salt":"$2b$12$5vOoeY8Db0SbLObodDoC7O","phish":["Saint Petersburg"],"password_hash":"pbkdf2:sha256:50000$XYog8dp5$37a0b8ac9923b714cd4e8c20bdd1ea08503030801af8ed4add8bcd17ba81dacf","message": ""})
# Password: INGAr0ck$
db.db.accountInfo.insert_one({"_id":ObjectId("5c7d7fde9a22a60680b903f7"),"username":"s.akiyama@warwick.ac.uk","name":"Shinemon Akiyama","applicant id":ObjectId("5c7d7fde9a22a60680b903f5"),"salt":"$2b$12$Ke6BIY42XPfXcKj7DL9iVO","phish":["Xiamen"],"password_hash":"pbkdf2:sha256:50000$cocIcy5M$6d70810a994c44f1442ef9967759296a01ddf2b2d5f4e5658900b09fe066a4c1","message": ""})
db.db.application.insert_one({"_id":ObjectId("5c7d7cf49a22a60680b903ef"),"completed":True,"preferred":1,"specialized score":0.014889223377397731,"current step":0,"applicant id":ObjectId("5c7d7c3c9a22a60680b903cf"),"vacancy id":ObjectId("5c7d793d9a22a60680b903a7")})
db.db.applicantInfo.insert_one({"_id":ObjectId("5c7d7c3c9a22a60680b903d0"),"applicant id":ObjectId("5c7d7c3c9a22a60680b903cf"),"basic score":{"education_score":0.5926125102493686,"score":0.554175719415677,"experience_score":0.633613433299023},"skills_score":0.9460405477974173,"a-level qualifications":[["Computer Science","A"],["Mathematics","B"],["Further Maths","C"]],"attended university":"Imperial College London","degree level":"2:1","degree qualification":"Computer Science","skills":[["Word","3"]],"languages":[["Python","7"],["C","3"]],"previous employment":[["Self Employed","Self Employed","2019-01-01","2019-03-03"]],"address":"MattCorp headquarters","phone number":"0201142975","cover letter":"I believe I am the perfect candidate for the job","interesting facts":"I am the perfect candidate for the job"})
db.db.application.insert_one({"_id":ObjectId("5c7d80ec9a22a60680b9040f"),"completed":True,"preferred":1,"specialized score":0.6372246969273931,"current step":0,"applicant id":ObjectId("5c7d7fde9a22a60680b903f5"),"vacancy id":ObjectId("5c7d7a709a22a60680b903c4")})
db.db.applicantInfo.insert_one({"_id":ObjectId("5c7d7fde9a22a60680b903f6"),"applicant id":ObjectId("5c7d7fde9a22a60680b903f5"),"basic score":{"education_score":0.7435868720423295,"score":0.4447773941347738,"experience_score":0.740390707464065},"skills_score":0.7563615388341594,"a-level qualifications":[["Business Management","B"],["General Studies","A"]],"attended university":"Warwick University","degree level":"2:1","degree qualification":"Business Management","skills":[["Public Speaking","3"]],"languages":[["Python","3"],["HTML","6"]],"previous employment":[["INGA","CEO","2018-08-01","2019-03-01"]],"address":"INGA Headquarters","phone number":"02875463528","cover letter":"Not required","interesting facts":"I own INGA"})
db.db.questionStage.insert_one({"_id":ObjectId("5c7ae3f88c5b5b2198252f2c"),"stage id":ObjectId("5c74389bad9bb61fbcc01a3b"),"questions":[{"What is my favorite colour":["Blue","Red"]},{"2+2":[4,3]}]})
db.db.metaData.insert_one({"divisions" : ["Technology", "HR", "Finance"],"roles" : ["Internship", "Graduate", "Full-Time", "Part-Time"],"locations" : ["London, United Kingdom", "New York, United States", "Paris, France"]})
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