#Code for intialisation of DB
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb+srv://cieve:N3gNW20iJNqwL0fC@cievedatabase-gzmjp.mongodb.net/test?retryWrites=true")
db = client.cieve_database

db.db.stage.insert_one({"_id":ObjectId("5c74389bad9bb61fbcc01a3a"),"type":"Interview","description":"Face to face meeting with applicant","title":"Interview"})
db.db.stage.insert_one({"_id":ObjectId("5c74389bad9bb61fbcc01a3b"),"type":"Test","description":"Reasoning and logic test","title":"Logic Test"})
db.db.stage.insert_one({"_id":ObjectId("5c7438ecad9bb61ff6d81d38"),"type":"Interview","description":"Phone meeting with applicant","title":"Mobile Interview"})
db.db.stage.insert_one({"_id":ObjectId("5c7438edad9bb61ff6d81d39"),"type":"Test","description":"Tests the mathematical ability of an applicant","title":"Math Test"})
db.db.stage.insert_one({"_id":ObjectId("000000000000000000000000"),"type":"Onboarding","description":"Initial onboarding stage","title":"Onboarding"})
db.db.stage.insert_one({"_id":ObjectId("111111111111111111111111"),"type":"Accepted","description":"Final Applicants that have been offered the role","title":"Accepted"})
# Password: D3utsche$Bank
db.db.client.insert_one({"_id":ObjectId("5c7d77bb9a22a60680b9037c"),"username":"recruitment@db.com","vacancies":[ObjectId("5c7d793d9a22a60680b903a7"), ObjectId("5c7d7a709a22a60680b903c4")],"salt":"$2b$12$uCxKfl9I4eT5CTjazl2oxu", "phish":["Durban"],"password_hash":"pbkdf2:sha256:50000$ALoKpG6R$885b74f15cbdd145d48354dd12867ee7bfe70ac73015800eacfb7fc764e6e042","message": "Welcome to Cieve. You can create a job posting by clicking New Job. You can view your vacancies and applications by clicking Your Jobs"})
db.db.vacancy.insert_one({"_id":ObjectId("5c7d793d9a22a60680b903a7"),"vacancy title":"Software Engineer Intern","division":"Technology","preferred degrees":["University of Warwick"],"role type":"Internship","skills":{"Git":"8","Team Work":"7"},"vacancy description":"We are looking for bright, new interns to join us in our London office this summer as interns.","languages":{"Python":"9","Java":"7"},"location":"London, United Kingdom","positions available":10,"stages":["000000000000000000000000","5c7438ecad9bb61ff6d81d38","5c74389bad9bb61fbcc01a3a","111111111111111111111111"],"start date":"2019-07-01","min degree level":"1:1"})
db.db.vacancy.insert_one({"_id":ObjectId("5c7d7a709a22a60680b903c4"),"vacancy title":"Business Analyst","division":"Finance","preferred degrees":["University of Leicester"],"role type":"Graduate","skills":{"Team Work":"9","Presentation":"7","Powerpoint":"6","Project Management":"7"},"vacancy description":"We are looking for business-minded graduates to join our Business Analyst team in New York","languages":{"Python":"2"},"location":"New York, United States","positions available":5,"stages":["000000000000000000000000","5c7438edad9bb61ff6d81d39","5c7438ecad9bb61ff6d81d38","5c74389bad9bb61fbcc01a3a","111111111111111111111111"],"start date":"ASAP","min degree level":"2:1"})
db.db.vacancy.insert_one({"_id":ObjectId("5c8051911c9d4400004a696c"), "vacancy title": "Managing Director", "division": "Corporate & Investment Bank", "preferred degrees": ["University of Durham", "University of Southampton"], "role type": "Full-Time", "skills": {"Excel": "6", "Database Management": "5"}, "vacancy description": "We are looking for dedicated individuals with excellent analysis skills to join us full time as a Managing Director in Paris, France", "location": "Paris, France", "languages":{"Python":"9","Java":"7"}, "positions available": 15, "stages":["000000000000000000000000", "5c7438ecad9bb61ff6d81d38","5c74389bad9bb61fbcc01a3a","111111111111111111111111"], "start date": "ASAP", "min degree level":"2:1"})
db.db.vacancy.insert_one({"_id":ObjectId("5c80fef41c9d44000044f8a3"), "vacancy title": "Associate", "division": "Asset Managing", "preferred degrees": ["University of Nottingham"], "role type": "Internship", "skills": {"Report Writing": "9"}, "vacancy description": "We are looking for dedicated individuals with excellent and independant working methods to work with us in Berlin", "location": "Berlin, Germany", "languages":{"C": 3}, "positions available": 2, "stages":["000000000000000000000000","5c74389bad9bb61fbcc01a3b","5c74389bad9bb61fbcc01a3a","111111111111111111111111"], "start date": "2019-05-01", "min degree level": "1:1"})
db.db.interviewStage.insert_one({"_id":ObjectId("5c7d793d9a22a60680b903a8"),"slots":["2019-04-08","09:00","10:00"],"job id":ObjectId("5c7d793d9a22a60680b903a7"),"stage id":"5c74389bad9bb61fbcc01a3a"})
db.db.interviewStage.insert_one({"_id":ObjectId("5c7d793d9a22a60680b903a9"),"slots":["2019-04-01","11:00","12:00"],"job id":ObjectId("5c7d793d9a22a60680b903a7"),"stage id":"5c7438ecad9bb61ff6d81d38"})
db.db.interviewStage.insert_one({"_id":ObjectId("5c7d7a719a22a60680b903c5"),"slots":["2019-03-19","13:00","14:00"],"job id":ObjectId("5c7d7a709a22a60680b903c4"),"stage id":"5c7438ecad9bb61ff6d81d38"})
db.db.interviewStage.insert_one({"_id":ObjectId("5c7d7a719a22a60680b903c6"),"slots":["2019-03-20","15:00","16:00"],"job id":ObjectId("5c7d7a709a22a60680b903c4"),"stage id":"5c74389bad9bb61fbcc01a3a"})
# Password: M@ttC0rp
db.db.accountInfo.insert_one({"_id":ObjectId("5c7d7c3c9a22a60680b903d1"),"username":"matt@mattcorp.com","name":"Matthew Pull","applicant id":ObjectId("5c7d7c3c9a22a60680b903cf"),"salt":"$2b$12$5vOoeY8Db0SbLObodDoC7O","phish":["Saint Petersburg"],"password_hash":"pbkdf2:sha256:50000$XYog8dp5$37a0b8ac9923b714cd4e8c20bdd1ea08503030801af8ed4add8bcd17ba81dacf","message": "Welcome to Cieve. You can search for available jobs by clicking Job Search. You can make an application by clicking Applications"})
# Password: INGAr0ck$
db.db.accountInfo.insert_one({"_id":ObjectId("5c7d7fde9a22a60680b903f7"),"username":"s.akiyama@warwick.ac.uk","name":"Shinemon Akiyama","applicant id":ObjectId("5c7d7fde9a22a60680b903f5"),"salt":"$2b$12$Ke6BIY42XPfXcKj7DL9iVO","phish":["Xiamen"],"password_hash":"pbkdf2:sha256:50000$cocIcy5M$6d70810a994c44f1442ef9967759296a01ddf2b2d5f4e5658900b09fe066a4c1","message": "Welcome to Cieve. You can search for available jobs by clicking Job Search. You can make an application by clicking Applications"})
db.db.accountInfo.insert_one({"_id":ObjectId("5c805fca8c5b5b0e84252168"),"applicant id":ObjectId("5c805fca8c5b5b0e84252166"),"name":"John Smith","username":"John@Smith","password_hash":"pbkdf2:sha256:50000$SJ4WRFUA$b472e439a7bcdcfce2a8e4843878213817de5bc84b0e27c0e3cac7b3fe400c07","salt":"b'$2b$12$zHHzIBYUGIBUziT.2w5dHe'","phish":["Cape Town"],"message":"Welcome to Cieve. You can search for available jobs by clicking Job Search. You can make an application by clicking Applications"})
db.db.accountInfo.insert_one({"_id":ObjectId("5c8062368c5b5b087483b14b"),"applicant id":ObjectId("5c8062358c5b5b087483b149"),"name":"Emerson Trujillo","username":"emerson.trujillo@gmail.com","password_hash":"pbkdf2:sha256:50000$dil8reua$5225b496a87a6f972a116135ea188dd0e74262f806f12b64f7b8f936f22c2a63","salt":"b'$2b$12$u2RZ7Hjgi4n11HDgTdSKme'","phish":["Osaka"],"message":"Welcome to Cieve. You can search for available jobs by clicking Job Search. You can make an application by clicking Applications"})
db.db.application.insert_one({"_id":ObjectId("5c7d7cf49a22a60680b903ef"),"completed":True,"preferred":1,"specialized score":0.014889223377397731,"current step":0,"applicant id":ObjectId("5c7d7c3c9a22a60680b903cf"),"vacancy id":ObjectId("5c7d793d9a22a60680b903a7")})
db.db.applicantInfo.insert_one({"_id":ObjectId("5c7d7c3c9a22a60680b903d0"),"applicant id":ObjectId("5c7d7c3c9a22a60680b903cf"),"basic score":{"education_score":0.5926125102493686,"score":0.554175719415677,"experience_score":0.633613433299023,"skills_score":0.9460405477974173},"a-level qualifications":[["Computer Science","A"],["Mathematics","B"],["Further Maths","C"]],"attended university":"Imperial College London","degree level":"2:1","degree qualification":"Computer Science","skills":[["Word","3"]],"languages":[["Python","7"],["C","3"]],"previous employment":[["Self Employed","Self Employed","2019-01-01","2019-03-03"]],"address":"MattCorp headquarters","phone number":"0201142975","cover letter":"I believe I am the perfect candidate for the job","interesting facts":"I am the perfect candidate for the job"})
db.db.application.insert_one({"_id":ObjectId("5c7d80ec9a22a60680b9040f"),"completed":True,"preferred":1,"specialized score":0.6372246969273931,"current step":0,"applicant id":ObjectId("5c7d7fde9a22a60680b903f5"),"vacancy id":ObjectId("5c7d7a709a22a60680b903c4")})
db.db.applicantInfo.insert_one({"_id":ObjectId("5c7d7fde9a22a60680b903f6"),"applicant id":ObjectId("5c7d7fde9a22a60680b903f5"),"basic score":{"education_score":0.7435868720423295,"score":0.4447773941347738,"experience_score":0.740390707464065,"skills_score":0.7563615388341594},"a-level qualifications":[["Business Management","B"],["General Studies","A"]],"attended university":"Warwick University","degree level":"2:1","degree qualification":"Business Management","skills":[["Public Speaking","3"]],"languages":[["Python","3"],["HTML","6"]],"previous employment":[["INGA","CEO","2018-08-01","2019-03-01"]],"address":"INGA Headquarters","phone number":"02875463528","cover letter":"Not required","interesting facts":"I own INGA"})
db.db.metaData.insert_one({"divisions" : ["Technology", "Corporate & Investment Bank", "HR", "Finance", "Asset Managing"],"roles" : ["Internship", "Graduate", "Full-Time", "Part-Time"],"locations" : ["London, United Kingdom", "Berlin, Germany" "New York, United States", "Paris, France"]})
db.db.assessment.insert_one({})
db.db.questionStage.insert_one({"_id":ObjectId("5c7ae3f88c5b5b2198252f2c"),"stage id":ObjectId("5c74389bad9bb61fbcc01a3b"),"questions":[{"The Large Silver Watch states the time as 15:50  The Small Silver Watch displays the same time as the Gold Watch  The Bronze Watch is small in size  The Gold Watch is ten minutes slower than the Large Silver Watch  The Bronze Watch is five minutes faster than the Small Silver Watch  The Small Silver Watch displays the time as 16:00":["False","True", "Insufficient Information"]}, {"The Large Silver Watch states the time as 15:50  The Small Silver Watch displays the same time as the Gold Watch  The Bronze Watch is small in size  The Gold Watch is ten minutes slower than the Large Silver Watch  The Bronze Watch is five minutes faster than the Small Silver Watch  The Bronze Watch displays the time as 15:45":["True","False", "Insufficient Information"]}, {"The Large Silver Watch states the time as 15:50  The Small Silver Watch displays the same time as the Gold Watch  The Bronze Watch is small in size  The Gold Watch is ten minutes slower than the Large Silver Watch  The Bronze Watch is five minutes faster than the Small Silver Watch  The Bronze Watch is the same size as the Gold Watch":["Insufficient Information","True", "False"]}, {"Most TV shows are not boring  Most TV shows are violent  There is at least one boring TV show that is not violent":["Conclusion does not follow", "Conclusion follows"]}, {"All Germans speak Italian  All Italian speakers ride bicycles  Which of the following statements must be true?": ["All Germans ride bicycles", "All bicycle riders are German", "All Italians speak German", "Some of the Italians riding bicycles are Germans"]}]})
db.db.questionStage.insert_one({"_id":ObjectId("5c80947a1c9d440000a2f64d"),"stage id":ObjectId("5c7438edad9bb61ff6d81d39"), "questions":[{"4 + 8 = ?": [12, 10, 14]}, {"1 + 8 = ?": [9, 10, 7]}, {"5 + 5 = ?": [10, 15, 20]}, {"20 - 7 = ?": [13, 10, 15]}, {"9 - 3 = ?": [6, 5, 3]}, {"18 - 6 = ?": [12, 10, 14]}]})
db.db.feedbackWeights.insert_one({
    "University experience Weight": 0.3686119654015682,
    "Universities weight": {
        "UNIVERSITY OF LIVERPOOL": 0.09763682220101103,
        "NORTHWESTERN UNIVERSITY": 0.10687610890896868,
        "SEOUL NATIONAL UNIVERSITY": 0.09522218087684255,
        "UNIVERSITY OF SHEFFIELD": 0.10207867689952736,
        "CARNEGIE MELLON UNIVERSITY": 0.11596863565281344,
        "UNIVERSITY OF TORONTO": 0.09191675380584866,
        "UNIVERSITY OF CALIFORNIA": 0.10778322305176832,
        "UNIVERSITY OF WARWICK": 0.39662481783589176,
        "UNIVERSITY OF ILLINOIS AT URBANA-CHAMPAIGN": 0.11395450882151346,
        "PRINCETON UNIVERSITY": 0.09892866545881653
    },
    "Skillset weight": 0.47885566722572287,
    "Subjects Weight": 0.3640605197654619,
    "Degree Qualifications": {
        "Civil Engineering, MEng": 0.09191675380584866,
        "Physics, MPhys": 0.09214785684543206,
        "Mathematics and Physics, MMathPhys": 0.10207867689952736,
        "Mathematics and Statistics, MMathStat": 0.11395450882151346,
        "Economic Studies and Global Sustainable Development, BA": 0.09763682220101103,
        "Law with Humanities, BA": 0.09522218087684255,
        "Mathematics and Philosophy, BA": 0.10778322305176832,
        "Law and Sociology, BA": 0.10678080861338447,
        "Mathematics and Statistics, BSc": 0.11596863565281344,
        "Discrete Mathematics, MEng": 0.10687610890896868
    },
    "Experience Weight": 0.6292322512874572,
    "Degree Level Weight": 0.31035102049901986,
    "Previous Employment position": {
        "Senior Software Developer": 0.15556087085225206,
        "Senior Architect": 0.07208907070135202,
        "Systems Analyst": 0.14906295512735912,
        "Senior Web Developer": 0.12391069212917742,
        "Project Lead": 0.07176828123339908,
        "Consultant": 0.07154751826341679,
        "Senior Systems Analyst": 0.17421521812554083,
        "Technology Architect": 0.12391069212917742,
        "Module Lead": 0.018163536498634218,
        "Software Tester": 0.12515226299818166,
        "Technology Specialist": 0.12391069212917742,
        "Project Manager": 0.061139925443454174,
        "Associate Manager": 0.07154751826341679
    },
    "Previous Employment Company": {
        "Consumer Recreation Services": 0.07154751826341679,
        "Vault-Tec": 0.12515226299818166,
        "Scolex Industries": 0.12391069212917742,
        "Shoreline": 0.08547609279176324,
        "The New Firm": 0.07154751826341679,
        "Buy N Large": 0.07154751826341679,
        "Dunder Mifflin": 0.07208907070135202,
        "Peptic Thunder": 0.12515226299818166,
        "The Hellsing Organisation": 0.061139925443454174,
        "Heartland Play Systems": 0.12391069212917742,
        "Quark Industries": 0.061139925443454174,
        "Olivia Pope and Associates": 0.12391069212917742,
        "Gekko and Co": 0.08547609279176324,
        "The Straw Hat Grand Fleet": 0.12391069212917742,
        "T'orrud Cabal": 0.12391069212917742,
        "Xanatos Industries": 0.12515226299818166,
        "Hooli": 0.15556087085225206,
        "Spectre": 0.061139925443454174,
        "Monsters Inc": 0.12515226299818166,
        "Barrytron Limited": 0.12515226299818166
    },
    "Employment length weight": 0.34411145805092946,
    "Skills": {
        "Evernote": 0.08915905223774627,
        "Team work": 0.10469389120856244,
        "Time management": 0.10083571467567061,
        "Access": 0.10432496103079533,
        "Negotiating": 0.1192381542205939,
        "Networking": 0.11620235534931507,
        "Piano": 0.08915905223774627,
        "Keynote": 0.09445348659572915,
        "Motivated": 0.11776401857730151,
        "Content Creation": 0.08858128849313777,
        "Flute": 0.11203129540967624,
        "French": 0.10144165367693178,
        "Guitar": 0.10168484093990758,
        "Mentoring": 0.11810214944946777,
        "Quality Assurance": 0.09854976097475643,
        "Search engine optimization": 0.10672446638236874,
        "Video Editing": 0.10537598546293896,
        "Publisher": 0.10403768056088804,
        "Word": 0.08892803164958159,
        "Slack": 0.09156815174046934,
        "Public Speaking": 0.11537481254236982,
        "Google Drive": 0.11829203708578594,
        "Google analytics": 0.10475850739935395,
        "Maya": 0.09609207526858049,
        "Powerpoint": 0.08922503507959448,
        "Fundraising": 0.13870760313435992,
        "Chinese": 0.12744396416743808,
        "German": 0.1199411988185898,
        "Text Editing": 0.12309289750526334,
        "Japanese": 0.10258602134992396,
        "Skype": 0.09828017508282556,
        "Accounting": 0.11293010674961983,
        "Data Entry": 0.15987781612409466
    },
    "Languages weight": 0.604522755004162,
    "Skills Weight": 0.9386414586703947,
    "A-Level Qualifications": {
        "Engineering ": 0.09842289929943498,
        "General Studies ": 0.09489471353833734,
        "Physical Education ": 0.10022088661587149,
        "Hindi ": 0.10941808630763676,
        "Mathematics": 0.12453330210105822,
        "Critical Thinking ": 0.1072204062047279,
        "Psychology ": 0.10224561571083293,
        "Food Technology ": 0.09842289929943498,
        "Portuguese ": 0.09842289929943498,
        "Archaeology ": 0.10646512187757205,
        "Technology and Design ": 0.11558982160603276,
        "Panjabi ": 0.10646512187757205,
        "English Language and Literature ": 0.0923049879826608,
        "Bengali ": 0.1,
        "Thinking Skills ": 0.09931600911895974,
        "Creative Writing ": 0.09270673362619615,
        "Japanese ": 0.09072788728209578,
        "Media Studies ": 0.09270673362619615,
        "Product Design ": 0.10216612186141837,
        "Irish ": 0.0923049879826608,
        "Politics ": 0.10659266041534571,
        "Professional Business Services ": 0.10659266041534571,
        "Economics and Business ": 0.09489471353833734,
        "Film Studies ": 0.10764881842044341,
        "Further Mathematics": 0.12281022781076063,
        "Digital Media and Design ": 0.10646512187757205,
        "Classical Greek ": 0.10251553214200453,
        "Applied Business ": 0.11091287512422293
    },
    "Education Weight": 0.6195060549288977,
    "Languages Known": {
        "LaTeX": 0.08922012088538732,
        "Unix Shell": 0.1298778128950027,
        "Java": 0.13113906046239257,
        "Ruby-on-rails": 0.12536154112406808,
        "Mathematica": 0.10010424492831921,
        "Perl": 0.09281341392359155,
        "Fortran": 0.12891313619094463,
        "Visual J++": 0.11194466538744666,
        "BASIC": 0.09281341392359155,
        "Assembly": 0.08562682784718308,
        "Python": 0.137643037649752,
        "Scala": 0.13252727821481272,
        "Executable UML": 0.11453996403812772,
        "JSON": 0.13252727821481272,
        "HTML": 0.14534045929626857,
        "MATLAB": 0.15044704183351393,
        "Ruby": 0.13943607790827148,
        "Bash": 0.12153390564256934,
        "CUDA": 0.11343774856087749,
        "C": 0.12090524542458685,
        "Lisp": 0.12929374965126397,
        "C++": 0.15902841126642814,
        "TeX": 0.08922012088538732,
        "High Level Assembly": 0.1053640869706503,
        "UNITY": 0.09281341392359155,
        "R": 0.09062315786004158,
        "Prolog": 0.11807071011934037,
        "PostScript": 0.09101676740448945,
        "Visual Basic NET": 0.16000048230508032,
        "C#": 0.1336482265538109,
        "Haskell": 0.11707303594000157,
        "SQL": 0.1738390275476383,
        "Visual Basic": 0.09101676740448945
    }
})