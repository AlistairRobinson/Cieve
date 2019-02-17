#Code for intialisation of DB
from pymongo import MongoClient

client = MongoClient("mongodb+srv://cieve:N3gNW20iJNqwL0fC@cievedatabase-gzmjp.mongodb.net/test?retryWrites=true")
db = client.cieve_database

applicant = db.applicants
client = db.clients
applicantInfo = db.applicantInfo
application = db.application
vacancy = db.vacancy
stage = db.stage
assessment = db.assessment
