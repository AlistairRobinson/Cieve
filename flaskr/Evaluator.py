import json
import random
import math
import pprint
from db import get_db



class Evaluator:
    def __init__(self):

        self.alpha = 0.2
        self.db = get_db()
        self.weights = self.getWeights()

        self.degreeLevelConversion = {"1":1,"2:1":0.7,"2:2":0.3}
        self.ALevelConversion = {"A":1,"B":0.7,"C":0.3}

        self.baseWeights = {"Degree Qualifications":0.1, "Universities weight":0.1,
         "A-Level Qualifications":0.1, "Languages Known":0.1,
         "Skills":0.1, "Previous Employment position":0.1, "Previous Employment Company":0.1}


    # functions to retrieve and send weights to the database

    def getWeights(self):
        return self.db.getWeights()[0]

    def writeWeights(self):
        self.db.updateWeights(self.weights)

    # Wrapper for activation function
    def activation(self, x):
        return self.sigmoid(x)

    # Modified sigmoid function
    def sigmoid(self, x):
        return 2 / (1 + math.exp(-x*2)) - 1

    # Sigmoid function derivative
    def gprime(self, x):
        return (4*math.exp(2*x))/((math.exp(2*x)+1)*(math.exp(2*x)+1))

    # Function to retrieve weight with specific name,
    # if it is not present, get an base weight and store it
    # with given string, therefore creating new weight in NN

    def getWeight(self, attribute, value):
        if value in self.weights[attribute]:
            weight = self.weights[attribute].get(value)
        else:
            weight = self.baseWeights.get(attribute)
            self.addNewWeight(attribute, value, weight)
        return weight

    # Conversion function to get a score from 0 to 1
    # from applicant A levels, skills or language know scores.

    def levelConversion(self, group, level):
        score = 0
        if group == "A-Level Qualifications":
            if level in self.ALevelConversion:
                score = self.ALevelConversion.get(level)
        elif group == "Languages Known" or group == "Skills":
            score = float(float(level) / 10)
        return score

    # Helper function to perform forward propogation

    def attributeGroup(self, applicant, group, weightAttribute, levelAttribute, outputs):
        sum = 0
        if group in applicant:
            outputs[group] = list()
            for apl in applicant[group]:
                attributeValue = apl[weightAttribute]
                weight = self.getWeight(group, attributeValue)
                level = apl[levelAttribute]
                score = self.levelConversion(group, level)
                sum += score * weight
                outputs[group].append({"weight Attribute":str(attributeValue), "score": score})
        return sum

    # Function to retrieve applicant score.

    def basicEvaluate(self, applicant):
        return self.basicEvaluateFeedback(applicant, {})


    # Function that performs forward propogation to Calculate
    # Baisc, experience, education, skills scores.

    def basicEvaluateFeedback(self, applicant, outputs):

        # Calculate Education Score

        partialES1 = 0
        if "Degree Qualification" in applicant:

            degreeQualification = applicant["Degree Qualification"]
            degreeQualificationWeight = self.getWeight("Degree Qualifications", degreeQualification)
            UniversityWeight = 0
            uni = ""
            if "University Attended" in applicant:
                uni = applicant["University Attended"].upper()
                UniversityWeight = self.getWeight("Universities weight", uni)
            elif "attended university" in applicant:
                uni = applicant["attended university"].upper()
                UniversityWeight = self.getWeight("Universities weight", uni)

            degreeLevel = ""
            if "Degree Level" in applicant:
                degreeLevel = applicant["Degree Level"]
            elif "degree level" in applicant:
                degreeLevel = applicant["degree level"]

            degreeLevelScore = 0
            if degreeLevel in self.degreeLevelConversion:
                degreeLevelScore = self.degreeLevelConversion.get(degreeLevel)

            partialES1 = self.activation(1 * degreeQualificationWeight
            + degreeLevelScore * self.weights["Degree Level Weight"]
            + 1 * UniversityWeight)

            outputs["Degree Qualification"] = degreeQualification
            outputs["University Attended"] = uni
            outputs["Degree Level Score"] = degreeLevelScore
            outputs["University Score"] = partialES1

        partialES2 = self.attributeGroup(applicant,"A-Level Qualifications","Subject","Grade",outputs)
        partialES2 = self.activation(partialES2)

        outputs["A-levels Score"] = partialES2

        ES = self.activation(partialES1 * self.weights["University experience Weight"]
        + partialES2 * self.weights["Subjects Weight"])

        outputs["Education Score"] = ES

        # Calculate Skill Score

        partialS1 = self.attributeGroup(applicant, "Languages Known", "Language", "Expertise",outputs)
        partialS1 = self.activation(partialS1)

        outputs["Languages Score"] = partialS1

        partialS2 = self.attributeGroup(applicant, "Skills", "Skill", "Expertise",outputs)
        partialS2 = self.activation(partialS2)

        outputs["Skillset Score"] = partialS2

        SS = self.activation(partialS1 * self.weights["Languages weight"]
        + partialS2 * self.weights["Subjects Weight"])

        outputs["Skill Score"] = SS

        # Calculate Experience Score

        ExS = 0
        if "Previous Employment" in applicant:
            outputs["Previous Employment"] = []
            for q in applicant["Previous Employment"]:
                position = q["Position"]
                positionWeight = self.getWeight("Previous Employment position", position)

                company = q["Company"]
                companyWeight = self.getWeight("Previous Employment Company", company)

                lengthScore = self.getLengthScore(q["Length of Employment"])

                EmploymentScore = self.activation(self.weights["Employment length weight"] * lengthScore +
                positionWeight * 1 + companyWeight *1)

                outputs["Previous Employment"].append({"Position":position, "Company":company,"Length of Employment Score":lengthScore,"Employment Score":EmploymentScore})

                ExS += EmploymentScore

        ExS = self.activation(ExS)
        outputs["Experience Score"] = ExS

        # Calculate Main Score

        score = self.activation(ES * self.weights["Education Weight"]
        + SS * self.weights["Skills Weight"]
        + ExS * self.weights["Experience Weight"])

        scores = {}
        if score < 0:
            score = 0
        if ES < 0:
            ES = 0
        if ExS < 0:
            ExS = 0
        if SS < 0:
            SS = 0
        scores['score'] = score
        scores['education_score'] = ES
        scores['experience_score'] = ExS
        scores['skills_score'] = SS
        self.writeWeights()

        return scores

    # Function to match applicant entry to job specificic requirements

    def jobEvaluate(self, job, applicant):

        sum = 0
        count = 0
        if "Degree Qualification" in job:
            count += 1
            if "Degree Qualification" in applicant:
                degreeQualification = applicant["Degree Qualification"]
                if degreeQualification in job["Degree Qualification"]:
                    sum += 1
                    if "Minimum Degree Level" in job:
                        degreeLevel = applicant["Degree Level"]
                        minDegreeLevel = job["Minimum Degree Level"]
                        if degreeLevel in self.degreeLevelConversion and minDegreeLevel in self.degreeLevelConversion:
                            if self.degreeLevelConversion.get(degreeLevel) >= self.degreeLevelConversion.get(minDegreeLevel):
                                sum += 1
        if "Minimum Degree Level" in job:
            count += 1

        langSum = 0.0
        langCount = 0
        if "Languages Known" in job:
            for l in job["Languages Known"]:
                langCount += 1
                language = l["Language"]
                expertise = l["Expertise"]
                lSum = 0.0
                if "Languages Known" in applicant:
                    for appLang in applicant["Languages Known"]:
                        if appLang["Language"] == language:
                            appExpertise = appLang["Expertise"]
                            if appExpertise >= expertise:
                                lSum = 1
                            else:
                                lSum = float( int(appExpertise) / int(expertise))
                langSum += lSum

        print(str(langCount) + "   " + str(langSum))
        if langCount > 0:
            count += 1
            sum += langSum / langCount

        langSum = 0
        langCount = 0
        if "Skills" in job:
            for l in job["Skills"]:
                langCount += 1
                language = l["Skill"]
                expertise = l["Expertise"]
                lSum = 0
                if "Skills" in applicant:
                    for appLang in applicant["Skills"]:
                        if appLang["Skill"] == language:
                            appExpertise = appLang["Expertise"]
                            if appExpertise >= expertise:
                                lSum = 1
                            else:
                                lSum = appExpertise / expertise
                langSum += lSum
        if langCount > 0:
            count += 1
            sum += langSum / langCount


        if count != 0:
            score = sum / count
        else:
            score = 0

        if "Type" in job:
            if job["Type"] != "Intern":
                if "Start Date" in job:
                    if "Graduation Date" in applicant:
                        if len(applicant["Graduation Date"]) > 0:
                            if job["Start Date"] < applicant["Graduation Date"]:
                                score = score #* 0.3


        return score


    # Function to locally add new weight which was not seen before

    def addNewWeight(self, dictionaryName, weightName, weight):
        if not (dictionaryName in self.weights):
            self.weights[dictionaryName] = {}
        self.weights[dictionaryName][weightName] = weight

    # Get a score of a length of previous employment of an applicant

    def getLengthScore(self, s):
        p = str(s).find('year')
        b = str(s).find('months')
        if p == -1 or b== -1:
            return 0
            l = float(s) / 365
            if l > 5:
                return 1
            else:
                 return l/5
        else:
            l = float(s[0:(p-1)])
            if l > 5:
                return 1
            else:
                 return l/5

    # helper function to help backpropogation

    def getError(self, weight, prevError, score):
        return weight * prevError * self.gprime(score)

    # Function to be ca;;ed for weights update,
    # It takes array of applicants, which contains
    # applicant info next to score indicating
    # wether they've been accepted or rejected and
    # their specialized score.

    def updateWeights(self, applicants, accessMode):
        newWeights = dict(self.weights)
        batch_size = len(applicants)
        for apl in applicants:
            normalApl = apl[0]
            if accessMode == 1:
                normalApl = self.changeApplicationBindings(apl[0])
            self.getWeightsUpdate(normalApl, apl[1], newWeights, batch_size)

        self.weights = newWeights
        self.writeWeights()

    # Function calculate change of temporary
    # weights within one given applicant.

    def getWeightsUpdate(self, applicant, wantedScore, newWeights, batch_size):

        outputs = {}
        self.basicEvaluateFeedback(applicant, outputs)

        # Calculate the errors (gradients) of an neural netowrk given wanted score

        baseError =  wantedScore - outputs["Base Score"]
        errors = {"Base Error": baseError}

        errors["Education Error"] = self.getError(self.weights["Education Weight"], baseError, outputs["Education Score"])
        errors["Experience Error"] = self.getError(self.weights["Experience Weight"], baseError, outputs["Experience Score"])
        errors["Skills Error"] = self.getError(self.weights["Skills Weight"], baseError, outputs["Skill Score"])


        errors["Skillset Error"] = self.getError(self.weights["Subjects Weight"], errors["Skills Error"], outputs["Skillset Score"])
        errors["Languages Error"] = self.getError(self.weights["Languages weight"], errors["Skills Error"], outputs["Languages Score"])

        errors["University Error"] = self.getError(self.weights["University experience Weight"], errors["Education Error"], outputs["University Score"])
        errors["A-levels Error"] = self.getError(self.weights["Subjects Weight"], errors["Education Error"], outputs["A-levels Score"])

        if "Previous Employment" in outputs:
            errors["Previous Employment Errors"] = []
            for q in outputs["Previous Employment"]:
                company = q["Company"]
                position = q["Position"]
                lengthScore = q["Length of Employment Score"]
                EmploymentError = self.getError(1, errors["Experience Error"], outputs["Experience Score"])
                errors["Previous Employment Errors"].append({"Company":company,"Position":position,"Employment Error":EmploymentError,"Length of Employment Score":lengthScore})


        # Functions to update the temporary score.

        self.updateSkillsWeight(outputs["Skill Score"], baseError, newWeights, batch_size)
        self.updateExperienceWeight(outputs["Experience Score"], baseError, newWeights, batch_size)
        self.updateEducationWeight(outputs["Education Score"], baseError, newWeights, batch_size)

        self.updateSkillSetWeight(outputs["Skillset Score"], errors["Skills Error"], newWeights, batch_size)
        self.updateLanguagesWeight(outputs["Languages Score"], errors["Skills Error"], newWeights, batch_size)

        self.updateALevelsWeight(outputs["A-levels Score"], errors["Education Error"], newWeights, batch_size)
        self.updateUniversityExperienceWeight(outputs["University Score"], errors["Education Error"], newWeights, batch_size)

        self.updateDegreeLevelWeight(outputs["Degree Level Score"], errors["University Error"], newWeights, batch_size)

        self.updateUniversityWeight(outputs["University Attended"], errors["University Error"], newWeights, batch_size)
        self.updateDegreeWeight(outputs["Degree Qualification"], errors["University Error"], newWeights, batch_size)

        self.updateGroup("Languages Known", errors["Languages Error"], outputs, newWeights, batch_size)
        self.updateGroup("A-Level Qualifications", errors["A-levels Error"], outputs, newWeights, batch_size)
        self.updateGroup("Skills", errors["Skillset Error"], outputs, newWeights, batch_size)

        if "Previous Employment Errors" in errors:
            for q in errors["Previous Employment Errors"]:
                company = q["Company"]
                lengthScore = q["Length of Employment Score"]
                position = q["Position"]
                EmploymentError = q["Employment Error"]
                self.updateCompanyWeight(company, EmploymentError, newWeights, batch_size)
                self.updatePrevPositionWeight(position, EmploymentError, newWeights, batch_size)
                self.updateEmploymentLengthWeight(lengthScore, EmploymentError, newWeights, batch_size)

        return 0

    # Functions to update different weights

    def updateSkillsWeight(self, output, error, weights, batch_size):
        weights["Skills Weight"] += self.multiplyToWeight(output, error, batch_size)

    def updateExperienceWeight(self, output, error, weights, batch_size):
        weights["Experience Weight"] += self.multiplyToWeight(output, error, batch_size)

    def updateEducationWeight(self, output, error, weights, batch_size):
        weights["Education Weight"] += self.multiplyToWeight(output, error, batch_size)

    def updateSkillSetWeight(self, output, error, weights, batch_size):
        weights["Skillset weight"] += self.multiplyToWeight(output, error, batch_size)

    def updateLanguagesWeight(self, output, error, weights, batch_size):
        weights["Languages weight"] += self.multiplyToWeight(output, error, batch_size)

    def updateALevelsWeight(self, output, error, weights, batch_size):
        weights["Subjects Weight"] += self.multiplyToWeight(output, error, batch_size)

    def updateUniversityExperienceWeight(self, output, error, weights, batch_size):
        weights["University experience Weight"] += self.multiplyToWeight(output, error, batch_size)

    def updateEmploymentLengthWeight(self, output, error, weights, batch_size):
        weights["Employment length weight"] += self.multiplyToWeight(output, error, batch_size)

    def updateDegreeLevelWeight(self, output, error, weights, batch_size):
        weights["Degree Level Weight"] += self.multiplyToWeight(output, error, batch_size)

    def updateUniversityWeight(self, university, error, weights, batch_size):
        weights["Universities weight"][university] += self.multiplyToWeight(1, error, batch_size)

    def updateDegreeWeight(self, degree, error, weights, batch_size):
        weights["Degree Qualifications"][degree] += self.multiplyToWeight(1, error, batch_size)

    def updateCompanyWeight(self, company, error, weights, batch_size):
        weights["Previous Employment Company"][company] += self.multiplyToWeight(1, error, batch_size)

    def updatePrevPositionWeight(self, position, error, weights, batch_size):
        weights["Previous Employment position"][position] += self.multiplyToWeight(1, error, batch_size)

    def updateGroup(self, group, error, outputs, weights, batch_size):

        if group in outputs:
            for attribute in outputs[group]:
                name = attribute["weight Attribute"]
                score = attribute["score"]
                weights[group][name] += self.multiplyToWeight(score, error, batch_size)

    def multiplyToWeight(self, score, error, batch_size):
        return score * error * self.alpha / batch_size

    # Function to change weights by reqruiter
    # dashboard weight input.

    def dashboardWeights(self, newWeights):

        if newWeights:
            self.weights["Education Weight"] = float(newWeights[0])
            self.weights["Skills Weight"] = float(newWeights[1])
            self.weights["Experience Weight"] = float(newWeights[2])
            self.weights["Subjects Weight"] = float(newWeights[3])
            self.weights["University experience Weight"] = float(newWeights[4])
            self.weights["Skillset weight"] = float(newWeights[5])
            self.weights["Languages weight"] = float(newWeights[6])
            print(newWeights)
            self.updateAllApplicantScores()
            self.writeWeights()

    # Function to delete job by its ID,
    # it invokes weight adjusting and
    # all applicant base score recalculation

    def deleteJob(self, jobID):
        applicants = self.db.deleteJobByID(jobID)
        self.updateWeights(applicants, 1)
        self.updateAllApplicantScores()

    # Function to update all applicant scores

    def updateAllApplicantScores(self):
        applicantIDS = self.db.getAllApplicants()
        for id in applicantIDS:
            apl = self.db.getApplicantUserID(id)
            if apl != None:
                normalApl = self.changeApplicationBindings(apl)
                scores = self.basicEvaluate(normalApl)
                self.db.addUserScore(id, scores)

    # Helper function to normalize some strings

    def changeApplicationBindings(self, apl):
        normalApl = {}
        if "a-level qualifications" in apl:
            normalApl["A-Level Qualifications"] = []
            for entry in apl["a-level qualifications"]:
                normalApl["A-Level Qualifications"].append({"Subject": entry[0], "Grade":entry[1]})
        if "attended university" in apl:
            normalApl["University Attended"] = apl["attended university"]
        if "degree level" in apl:
            normalApl["Degree Level"] = apl["degree level"]
        if "degree qualification" in apl:
             normalApl["Degree Qualification"] = apl["degree qualification"]
        if "languages" in apl:
            normalApl["Languages Known"] = []
            for entry in apl["languages"]:
                normalApl["Languages Known"].append({"Language": entry[0], "Expertise":entry[1]})
        if "previous employment" in apl:
            normalApl["Previous Employment"] = []
            for entry in apl["previous employment"]:
                normalApl["Previous Employment"].append({"Company": entry[0], "Position":entry[1], "Length of Employment" : 300})
        if "skills" in apl:
            normalApl["Skills"] = []
            for entry in apl["skills"]:
                normalApl["Skills"].append({"Skill": entry[0], "Expertise":entry[1]})
        return normalApl
