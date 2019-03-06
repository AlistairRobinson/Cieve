from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from datetime import datetime
from random import shuffle

from flaskr.Evaluator import Evaluator
from flaskr.auth import login_required_A
from flaskr.db import get_db
bp = Blueprint('applicant', __name__, url_prefix='/apl')

#Definition for the applicant dashboard
@bp.route('/dashboard')
@bp.route('/')
@login_required_A
def dashboard():
    # Generate post data and pass to front end

    userData = get_db().getApplicantUserID(g.user)

    return render_template('/apl/Dashboard.html', userData=userData)

#Definition for the applicant job search page`
@bp.route('/jobsearch', methods=('GET', 'POST'))
@login_required_A
def jobSearch():
    db = get_db()
    return render_template('/apl/jobSearch.html', divisions = db.getDivisions(), roles = db.getRoles(), locations = db.getLocations())
            # Return first 20 (use a page count, get[1,2,...])

#Definition for the application
@bp.route('/newapplication', methods=('GET', 'POST'))
@login_required_A
def newApplication():
    # Generate post data and pass to front end
    skills = {}
    jobs = {}
    others = ""
    db = get_db()
    if request.method == 'POST':
        error = None
        phoneNumber = request.form['Phone_Number']
        address = request.form["Address"]

        degreeQualification = request.form["Degree_Qualification"]
        degreeLevel = request.form["Degree_Level"]
        universityAttended = request.form['University_Attended']

        gradutationDate = ""
        try:
            gradutationDate = request.form['yearGraduation']
        except:
            pass

        alevels = []
        try:
            i = 0
            while 1==1:
                alevels.append(request.form.to_dict(flat=False)["a_levels["+str(i)+"][]"])
                i += 1
        except:
            pass


        employmentHistory = []
        try:
            i = 0
            while 1==1:
                employmentHistory.append(request.form.to_dict(flat=False)["Employment_History["+str(i)+"][]"])
                i += 1
        except:
            pass


        languages = []
        try:
            i = 0
            while 1==1:
                languages.append(request.form.to_dict(flat=False)["Languages["+str(i)+"][]"])
                i += 1
        except:
            pass


        skills = []
        try:
            i = 0
            while 1==1:
                skills.append(request.form.to_dict(flat=False)["Skills["+str(i)+"][]"])
                i += 1
        except:
            pass


        selectedJobs = []
        try:
            selectedJobs = request.form.to_dict(flat=False)["Selected_Jobs[]"]
        except:
            pass

        unselectedJobs = []
        if request.form['Consider_for_other_roles'] == "1":
            try:
                unselectedJobs = request.form.to_dict(flat=False)["Unselected_Jobs[]"]
            except:
                pass

        if request.form['Consider_for_other_roles'] == "0" and selectedJobs == []:
            flash("An unexpected error occurred")

        coverLetter = request.form['Cover_Letter']
        interestingFacts = request.form['Interesting_Facts']

        userID = session.get('user_id')[1:]

        appData = {}
        appData["Degree Qualification"] = degreeQualification
        appData["Degree Level"] = degreeLevel
        appData["University Attended"] = universityAttended
        appData["Graduation Date"] = gradutationDate
        appData["A-Level Qualifications"] = []
        for alevel in alevels:
            appData["A-Level Qualifications"].append({"Subject" : alevel[0], "Grade" : alevel[1]})
        appData["Languages Known"] = []
        for language in languages:
            appData["Languages Known"].append({"Language" : language[0], "Expertise" : language[1]})
        appData["Previous Employment"] = []
        for employ in employmentHistory:
            try:
                x = datetime.strptime(employ[3],"%Y-%m-%d")
            except:
                x = datetime.today()

            try:
                y = datetime.strptime(employ[2],"%Y-%m-%d")
            except:
                y = datetime.today()
            appData["Previous Employment"].append({"Company" : employ[0], "Position" : employ[1], "Length of Employment" : (x-y).days})
        appData["Skills"] = []
        for skill in skills:
            appData["Skills"].append({"Skill" : skill[0], "Expertise" : skill[1]})




        db.addUserScore(userID, Evaluator().basicEvaluate(appData))  # USER GENERAL SCORE





        for job in selectedJobs:
            data = db.getJob(job)
            jobData = {}
            jobData["Degree Qualification"] = [] #CHANGE
            jobData["Minimum Degree Level"] = data["min degree level"]
            jobData["Type"] = data["role type"]
            try:
                jobData["Start Date"] = datetime.strptime(data["start date"], "%d/%m/%Y").year
            except:
                jobData["Start Date"] = datetime.today().year
            jobData["Languages Known"] = []
            for language, expertise in data["languages"].items():
                jobData["Languages Known"].append({"Language" : language, "Expertise" : expertise})
            jobData["Skills"] = []
            for skill, expertise in data["skills"].items():
                jobData["Skills"].append({"Skill" : skill, "Expertise" : expertise})


            jobScore = Evaluator().jobEvaluate(jobData, appData)

            db.applyJob(userID, job, 1, jobScore)

        for job in unselectedJobs:
            data = db.getJob(job)
            jobData = {}
            jobData["Degree Qualification"] = [] #CHANGE
            jobData["Minimum Degree Level"] = data["min degree level"]
            jobData["Type"] = data["role type"]
            try:
                jobData["Start Date"] = datetime.strptime(data["start date"], "%d/%m/%Y").year
            except:
                jobData["Start Date"] = datetime.today().year
            jobData["Languages Known"] = []
            for language, expertise in data["languages"].items():
                jobData["Languages Known"].append({"Language" : language, "Expertise" : expertise})
            jobData["Skills"] = []
            for skill, expertise in data["skills"].items():
                jobData["Skills"].append({"Skill" : skill, "Expertise" : expertise})

            jobScore = Evaluator().jobEvaluate(jobData, appData)

            db.applyJob(userID, job, 0, jobScore)

        db.addUserEducation(userID, alevels, degreeQualification, degreeLevel, universityAttended)

        db.addUserSkills(userID, skills)

        db.addUserLanguages(userID, languages)

        db.addUserEmployment(userID, employmentHistory)

        db.addUserContacts(userID, phoneNumber, address)

        db.addUserMetaData(userID, coverLetter, interestingFacts)


        flash("Application successful")
    return render_template('/apl/applicationCreation.html', divisions = db.getDivisions(), roles = db.getRoles(), locations = db.getLocations())

#Definition for the application
@bp.route('/applications')
@login_required_A
def applications():
    db = get_db()
    applicationsData = db.getApplications(session.get('user_id')[1:])
    filteredData = []
    for applicationData in applicationsData:
        if (applicationData["current step"] != 0) or (applicationData["preferred"] == 1):
            applicationData["stagesDetail"] = []
            applicationData["stagesType"] = []
            for stage in applicationData["stages"]:
                title = db.getStageTitle(stage)
                applicationData['stagesDetail'].append(title)
                type = db.getStageType(stage)
                applicationData['stagesType'].append(type)

            filteredData.append(applicationData)
    return render_template('/apl/applications.html', applications = filteredData)

@bp.route('/testing', methods=('GET', 'POST'))
@login_required_A
def testing():
    if request.method == "POST":
        jobID = request.form["vacancyId"]
        applicantID = request.form["applicantId"]
        stepNo = request.form["currentStep"]
        stageID = request.form["stageId"]

        db = get_db()
        questions = db.getQuestions(stageID)

        for q in questions:
            q[0] = shuffle(q.values()[0])


        return render_template('/apl/compquestions.html', questions=questions, jobID=jobID, applicantID=applicantID, stepNo=stepNo, stageId=stageID)
    return redirect(url_for('applicant.applications'))

@bp.route('/testingCheck', methods=('GET', 'POST'))
@login_required_A
def testingCheck():
    if request.method == "POST":
        jobID = request.form["vacancyId"]
        applicantID = request.form["applicantId"]
        stepNo = request.form["stepNo"]
        stepStageID = request.form["stageId"]


        answers = []
        try:
            i = 1
            while 1==1:
                answers.append(request.form["answer[]"+str(i)])
                i += 1
        except:
            pass
        db = get_db()
        db.assessQuestions(answers, stepNo, applicantID, jobID, stepStageID)

        db.setCompletedTrue(applicantID, jobID)

        redirect(url_for('applicant.applications'))
    return redirect(url_for('applicant.applications'))

@bp.route('/booking', methods=('GET', 'POST'))
@login_required_A
def booking():
    if request.method == "POST":
        jobID = request.form["vacancyId"]
        applicantID = request.form["applicantId"]
        stepNo = request.form["currentStep"]

        slots = get_db().getInterviewSlots(jobID, stepNo)

        return render_template('/apl/interview.html', slots=slots, jobID=jobID, applicantID=applicantID, stepNo=stepNo)
    return redirect(url_for('applicant.applications'))

@bp.route('/bookingSet', methods=('GET', 'POST'))
@login_required_A
def bookingSet():
    if request.method == "POST":
        jobID = request.form["vacancyId"]
        applicantID = request.form["applicantId"]
        stepNo = request.form["currentStep"]

        bookingRequest = request.form["booking[]"]

        #db call

        return redirect(url_for('applicant.applications'))
    return redirect(url_for('applicant.applications'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    elif user_id[0] == "A":
        g.user = user_id[1:]
    elif user_id[0] == "C":
        g.user = user_id[1:]
    else:
        g.user = None
        session['user_id'] = None
