from pymongo import MongoClient

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
    
    
    # Return JSON of applicant info populated based on id
    def getApplicantUserID(self, id):
        query = self.db.applicantInfo.find_one({"applicant_id": id})
        if query != None:
            return query
        else:
            return None


    # Return JSON of client info populated based on id
    def getClientUserID(self, id):
        query = self.db.client.find_one({"_id": id})
        if query != None:
            return query
        else:
            return None


    # Returns all the jobs currently available to applications
    def getJobs(self, number, division, role, location):
        Jobs = []
        queryMaker = {"positions_available": {"$gt": 0}}
        if division != "":
            queryMaker['division'] = division
        
        if role != "":
            queryMaker['role type'] = role
        
        if location != "":
            queryMaker['location'] = location
        
        query = self.db.vacancy.find(queryMaker, {"_id": 0, "positions_available": 0, "applicants_recieved": 0})
        for doc in query:
            Jobs.append(doc)
        return Jobs[(number-1)*20:((number-1)*20)+20]

        # Wiil accept a json parameter which will be defined by the input, adds the new job to the DB
        def addJob(self, json):
            return
    
    
test = Mongo(get_db())
applicantID = test.insertApplicantUser("Applicant1", "nathan", "password123", "123")
print(applicantID)
clientID = test.insertClientUser("Client1", "password321", "321")
print(clientID)
print(test.getApplicantAccount("Applicant1"))
print(test.getClientAccount("Client1"))
print(test.getClientUserID(clientID))
print(test.getApplicantUserID(applicantID))
print(test.getJobs(1, "Manager", None, "London"))
