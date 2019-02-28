import json
import random
import math
# Skeleto for evaluation class

class Evaluator:
    def __init__(self):
        self.weights = self.getWeights()
        self.rankings = self.getRankings()
        self.degreeLevelConversion = {"1":1,"2:1":0.7,"2:2":0.3}
        self.ALevelConversion = {"A":1,"B":0.7,"C":0.3}
        self.BaseDegreeQualificationWeight = 1
        self.BaseAlevelWeight = 1
        self.BaseLanguageWeight = 1
        self.baseSkillWeight = 1
    def getWeights(self):
        with open('weights.json') as w:
            weights = json.load(w)
        return weights

    def getRankings(self):
        # Connect to database to get rankings
        with open('rankings2.txt') as f:
            ranks = json.load(f)
        return ranks

    def activation(self, x):
        return self.sigmoid(x)

    def sigmoid(self, x):
        return 2 / (1 + math.exp(-x*2)) - 1
      # return 1 / (1 + math.exp(-x))
      # 2/(1 + exp(-x))-1

      #  Use 2/(1 + exp(-x))-1 with x > 0, x = 0 if x < 0 ??????????? Done
      # Change gPrime to be function above derivative   ///////////// Done

    def gprime(x):
        return sigmoid(x) * (1 - sigmoid(x))
        # 2*exp(x)/(exp(x)+1)^2

    def basicEvaluate(self, applicant):

        # Calculate education, skills and experience scores

        # ////////////////////// education

        partialES1 = 0

        if "Degree Qualification" in applicant:
            degreeQualification = applicant["Degree Qualification"]

            if degreeQualification in self.weights["Degree Qualifications"]:
                degreeQualificationWeight = self.weights["Degree Qualifications"].get(degreeQualification)
            else:
                degreeQualificationWeight = self.BaseDegreeQualificationWeight
                self.addNewWeight("Degree Qualifications", degreeQualification, degreeQualificationWeight)

            degreeLevel = applicant["Degree Level"]
            degreeLevelScore = 0
            if degreeLevel in self.degreeLevelConversion:
                degreeLevelScore = self.degreeLevelConversion.get(degreeLevel)

            uni = applicant["University Attended"].upper()
            uniScore = 0
            if uni in self.rankings:
                uniScore = float(self.rankings[uni]) / 100

            partialES1 = self.activation(1 * degreeQualificationWeight
            + degreeLevelScore * self.weights["Degree Level Weight"]
            + uniScore * self.weights["University Attended Weight"])

        partialES2 = 0
        if "A-Level Qualifications" in applicant:
            for q in applicant["A-Level Qualifications"]:
                subject = q["Subject"]
                subjectWeight = 0
                grade = q["Grade"]
                gradeScore = 0
                if grade in self.ALevelConversion:
                    gradeScore = self.ALevelConversion.get(grade)

                if subject in self.weights["A-Level Qualifications"]:
                    subjectWeight = self.weights["A-Level Qualifications"].get(subject)
                else:
                    subjectWeight = self.BaseAlevelWeight
                    self.addNewWeight("A-Level Qualifications", subject, subjectWeight)
                partialES2 += gradeScore * subjectWeight
            partialES2 = self.activation(partialES2)

        ES = self.activation(partialES1 * self.weights["University experience Weight"]
        + partialES2 * self.weights["Subjects Weight"])
        #
        # print("Education =   " + str(partialES1) + "   " + str(partialES2) + "    " + str(ES))



        # ////////////////////// skills

        partialS1 = 0
        if "Languages Known" in applicant:
            for q in applicant["Languages Known"]:
                language = q["Language"]
                languageWeight = 0
                expertiseScore = float(q["Expertise"]) / 10

                if language in self.weights["Languages Known"]:
                    languageWeight = self.weights["Languages Known"].get(language)
                else:
                    languageWeight = self.BaseLanguageWeight
                    self.addNewWeight("Languages Known", language, languageWeight)
                partialS1 += languageWeight * expertiseScore
            partialS1 = self.activation(partialS1)

        partialS2 = 0
        if "Skills" in applicant:
            for q in applicant["Skills"]:
                skill = q["Skill"]
                skillWeight = 0
                expertiseScore = float(q["Expertise"]) / 10

                if skill in self.weights["Skills"]:
                    skillWeight = self.weights["Skills"].get(skill)
                else:
                    skillWeight = self.baseSkillWeight
                    self.addNewWeight("Skills", skill, skillWeight)
                partialS2 += skillWeight * expertiseScore
            partialS2 = self.activation(partialS1)

        SS = self.activation(partialS1 * self.weights["Languages weight"]
        + partialS2 * self.weights["Subjects Weight"])

        #
        # print("Skills =  " + str(partialS1) + "   " + str(partialS2) + "    " + str(SS))

        # ////////////////////// Experience


        ExS = 0
        if "Previous Employment" in applicant:
            for q in applicant["Previous Employment"]:
                position = q["Position"]
                positionWeight = 0
                lengthScore = self.getLengthScore(q["Length of Employment"])
                if position in self.weights["Previous Employment"]:
                    positionWeight = self.weights["Previous Employment"].get(position)
                else:
                    positionWeight = self.baseSkillWeight
                    self.addNewWeight("Previous Employment", position, positionWeight)
                ExS += positionWeight * lengthScore
            ExS = self.activation(ExS)
        #
        # print("Experience =  " + str(ExS))

        # Combine scores to overall basic score

        score = self.activation(ES * self.weights["Education Weight"]
        + SS * self.weights["Skills Weight"]
        + ExS * self.weights["Experience Weight"])

        # print("Overall score : " + str(score) )
        # print()
        # print()

        applicant['score'] = score
        applicant['education_score'] = ES
        applicant['experience_score'] = ExS
        applicant['skills_score'] = SS
        return applicant
        # return score

        # Match job and applicant data
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
                count += 1
                degreeLevel = applicant["Degree Level"]
                minDegreeLevel = job["Minimum Degree Level"]
                if degreeLevel in self.degreeLevelConversion and minDegreeLevel in self.degreeLevelConversion:
                    if self.degreeLevelConversion.get(degreeLevel) >= self.degreeLevelConversion(minDegreeLevel):
                        sum += 1

        langSum = 0
        langCount = 0
        if "Languages Known" in job:
            for l in job["Languages Known"]:
                langCount += 1
                language = l["Language"]
                expertise = l["Expertise"]
                lSum = 0
                if "Languages Known" in applicant:
                    for appLang in applicant["Languages Known"]:
                        if appLang["Language"] == language:
                            appExpertise = appLang["Expertise"]
                            if appExpertise >= expertise:
                                lSum = 1
                            else:
                                lSum = appExpertise / expertise
                langSum += lSum

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

        if "Minimum Work Experience" in job:
            minExp = job["Minimum Work Experience"]
            count += 1
            expSum = 0
            if "Previous Employment" in applicant:
                for q in applicant["Previous Employment"]:
                    expSum += self.getLength(q["Length of Employment"])
            if minExp < expSum:
                sum += 1

        if count != 0:
            score = sum / count
        else:
            score = 0

        return score


    def addNewWeight(self, dictionaryName, weightName, weight):
        return 0

    def getLengthScore(self, s):
        p = s.find('year')
        if p == -1:
            return 0
        else:
            l = float(s[0:(p-1)])
            if l > 5:
                return 1
            else:
                 return l/5

    def getLength(self, s):
        p = s.find('year')
        if p == -1:
            return 0
        else:
            l = float(s[0:(p-1)])
            return l
