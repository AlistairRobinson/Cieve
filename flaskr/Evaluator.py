import json
import random

# Skeleto for evaluation class

class Evaluator:
    def __init__(self):
        self.weights = self.getWeights()
        self.rankings = self.getRankings()

    def getWeights(self):
        # Connect to database to get rankings
        return list()

    def getRankings(self):
        # Connect to database to get rankings
        with open('rankings.txt') as f:
            ranks = json.load(f)
        return ranks

    def evaluate(self, applicant):
        score = random.randint(1,101)
        education_score = random.randint(1,101)
        skills_score = random.randint(1,101)
        experience_score = random.randint(1,101)

        uni = applicant["University Attended"].upper()
        if uni in self.rankings:
            uniScore = self.rankings[uni]

        applicant['score'] = score
        applicant['education_score'] = score
        applicant['experience_score'] = score
        applicant['skills_score'] = score

        return applicant
