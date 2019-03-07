from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, session
)
from werkzeug.exceptions import abort
from werkzeug.datastructures import ImmutableMultiDict
from bson.objectid import ObjectId
import operator
import json
from flaskr.auth import login_required_C
from flaskr.db import get_db
from flaskr.Evaluator import Evaluator
import collections

bp = Blueprint('client', __name__, url_prefix='/cli')

#Definition for the client dashboard
@bp.route('/dashboard')
@bp.route('/')
@login_required_C
def dashboard():
    db = get_db()
    data = db.getWeights()[0]
    del data["Universities weight"]
    del data["Previous Employment position"]
    del data["Previous Employment Company"]
    del data["Skills"]
    del data["Degree Qualifications"]
    del data["A-Level Qualifications"]
    del data["Languages Known"]
    print(data)
    info = []
    info.append(data["Education Weight"])
    info.append(data["Skills Weight"])
    info.append(data["Experience Weight"])
    info.append(data["Subjects Weight"])
    info.append(data["University experience Weight"])
    info.append(data["Languages weight"])
    info.append(data["Skillset weight"])
    print(info)
    # Generate post data and pass to front end
    return render_template('/cli/Dashboard.html', weights=info)

#Definition for the client job creation
@bp.route('/newjob', methods=('GET', 'POST'))
@login_required_C
def newJob():
    db = get_db()
    stages = db.getStages()

    if request.method == 'POST':
        jobTitle = request.form['job_title']
        division = request.form['division']
        role = request.form['roles']
        country = request.form['country']
        jobDescription = request.form['job_desc']
        noVacancies = request.form['numVacancies']
        startDate = request.form['start_date']

        try:
            request.form['asap']
            startDate = "ASAP"
        except:
            pass

        minDegreeLevel = request.form['min_degree_level']
        preferedDegrees = request.form.get('preferred_degrees',[])

        data = request.form.to_dict(flat=False)
        try:
            stage_list = data['Stage_Description']
        except:
            stage_list = []
        skills = data['skill']
        skillVal = data['skillVal']
        langVal = data['langVal']
        languages = data['lang']

        stage_list.insert(0,'000000000000000000000000') #Onboarding Stage
        stage_list.append('111111111111111111111111') #Accepted Stage
        error = None

        if jobTitle == "":
            error = "Empty job title"

        if division not in db.getDivisions():
            db.newDivision(division)

        if role not in db.getRoles():
            db.newRole(role)

        if country not in db.getLocations():
            db.newLocation(country)

        if jobDescription == "":
            error = "No job description"

        if str.isdigit(str(noVacancies)):
            if int(noVacancies) <= 0:
                error = "Number of vacancies must be positive"
        else:
            error = "Non-integer value for number of vacancies"

        if len(skills) != len(skillVal):
            error = "Skills and scores don't match"

        if len(languages) != len(langVal):
            error = "Languages and scores don't match"

        for val in skillVal:
            if str.isdigit(str(val)):
                if int(val) <= 0 or int(val) > 10:
                    error = "Score out of range"
            else:
                error = "Score is not a number"

        for val in langVal:
            if str.isdigit(str(val)):
                if int(val) <= 0 or int(val) > 10:
                    error = "Score out of range"
            else:
                error = "Score is not a number"

        for stage in stages:
            if stage not in get_db().getStages():
                error = "Wrong stage"

        if error is not None:
            flash(error)
        else:
            flash("Vacancy data accepted")
            db = get_db()
            json = {'vacancy title':jobTitle,
                    'division':division,
                    'role type':role,
                    'location':country,
                    'vacancy description':jobDescription,
                    'positions available': int(noVacancies),
                    'start date':startDate,
                    'min degree level':minDegreeLevel,
                    'prefered degrees':preferedDegrees,
                    'stages':stage_list,
                    'skills':skills,
                    'skillVal':skillVal,
                    'languages':languages,
                    'langVal': langVal}

            skillDic = {}
            skillVal = json.pop('skillVal', None)
            skills = json.pop('skills', None)
            for i in range(len(skills)):
                skillDic[skills[i]] = skillVal[i]
            json['skills'] = skillDic

            langDic = {}
            langVal = json.pop('langVal', None)
            langs = json.pop('languages', None)
            for i in range(len(langs)):
                langDic[langs[i]] = langVal[i]
            json['languages'] = langDic

            json['stagesDetail'] = []

            interviews = {}
            i = 1
            for stage in json['stages']:

                title = db.getStageTitle(stage)
                json['stagesDetail'].append(title)
                if stage != '000000000000000000000000':
                    if stage != '111111111111111111111111':
                        if stage in db.getInterviewStages():
                            interviews[str(i)] = [title, str(stage)]
                i += 1
            return render_template('cli/review.html', json = json, interviews = interviews)
    # Generate post data and pass to front end
    return render_template('cli/createjob.html', stages=stages, divisions = db.getDivisions(), roles = db.getRoles(), locations = db.getLocations())

@bp.route('/newJobSummary' , methods=('GET', 'POST'))
@login_required_C
def newJobSummary():
    if request.method == "POST":
        db = get_db()

        data = request.form.to_dict(flat=False)

        jsonData = data["json"][0].replace("'",'"')
        jsonData = jsonData.replace('u"','"')
        jsonData = json.loads(jsonData)
        if 'stagesDetail' in jsonData:
            del jsonData['stagesDetail']
        jsonData['positions available'] = int(jsonData['positions available'])
        userID = session.get('user_id')[1:]
        jobID =  db.addNewJob(jsonData, userID)
        interviewsData = json.loads(data["interviews"][0].replace("'",'"').replace('u"','"'))
        for stepID, interviews in interviewsData.items():
            stageID = interviews[1]
            dates = data.get("Date[]" + stepID, [])
            startTimes = data.get("startTime[]" + stepID, [])
            endTimes = data.get("endTime[]" + stepID, [])

            if len(startTimes) != len(endTimes) or len(dates) != len(startTimes):
                flash("An unexpected error occured")
                continue

            stagesData = []
            for i in range(len(dates)):
                stagesData.append([dates[i], startTimes[i], endTimes[i]])

            for stageData in stagesData:
                db.insertStageAvailability(stageID, jobID, stageData)

        flash("Vacancy post successful")
        return redirect(url_for('client.jobs'))

    render_template(url_for('client.dashboard'))

#Definition for the application
@bp.route('/jobs')
@login_required_C
def jobs():
    db = get_db()
    jobData = db.getClientJobs(session.get('user_id')[1:])
    return render_template('/cli/jobs.html', jobData = jobData)

@bp.route('/jobBreakdown', methods=('GET', 'POST'))
@login_required_C
def jobBreakdown():
    if request.method == "POST":
        db = get_db()
        jobID = request.form['jobID']
        jobData = db.getJob(jobID)
        jobData["stagesDetail"] = []
        jobData['stagesType'] = []
        for stage in jobData["stages"]:
            title = db.getStageTitle(stage)
            jobData['stagesDetail'].append(title)
            type = db.getStageType(stage)
            jobData['stagesType'].append(str(type))

        stepNumber = 0

        applicants = db.getApplicantsJob(jobID, stepNumber)
        applicantsData = {}
        for applicant in applicants:
            applicant["stage score"] = db.getStageResults(stepNumber, applicant["applicant id"], jobID)
            applicant["name"] = db.getApplicantNameID(applicant["applicant id"])
            applicant["basic scores"] = db.getApplicantUserID(applicant["applicant id"])["basic score"]
            applicantsData[str((applicant["specialized score"] + applicant["basic scores"]["score"])/2)] = applicant

        appData = []
        for key, val in sorted(applicantsData.items(), reverse=True):
            appData.append(val)

        return render_template('/cli/jobBreakdown.html', jobData = jobData, applicants = appData)
    return redirect(url_for('client.jobs'))


@bp.route('/stageDetail', methods=('GET', 'POST'))
@login_required_C
def stageDetail():
    if request.method == "POST":
        db = get_db()
        jobID = request.form['jobID']
        stepNumber = int(request.form["stageID"])
        applicants = db.getApplicantsJob(jobID, stepNumber)
        applicantsData = {}
        for applicant in applicants:
            applicant["name"] = db.getApplicantNameID(applicant["applicant id"])
            applicant["basic scores"] = db.getApplicantUserID(applicant["applicant id"])["basic score"]
            applicant["stage score"] = db.getStageResults(stepNumber, applicant["applicant id"], jobID)
            applicantsData[str((applicant["specialized score"] + applicant["basic scores"]["score"])/2)] = applicant

        appDataComp = []
        appDataNon = []
        for key, val in sorted(applicantsData.items(), reverse=True):
            val["_id"] = str(val["_id"])
            val["vacancy id"] = str(val["vacancy id"])
            val["applicant id"] = str(val["applicant id"])
            if val["completed"]:
                appDataComp.append(val)
            else:
                appDataNon.append(val)

        return jsonify([appDataComp, appDataNon])

    return None

@bp.route('/moveApplicant', methods=('GET', 'POST'))
@login_required_C
def moveApplicant():
    if request.method == "POST":
        appID = request.form["applicant id"]
        jobID = request.form["job id"]
        db = get_db()
        db.moveToNextStage(appID, jobID)
        return "Success"
    return "Fail"

@bp.route('/rejectApplicant', methods=('GET', 'POST'))
@login_required_C
def rejectApplicant():
    if request.method == "POST":
        appID = request.form["_id"]
        db = get_db()
        db.rejectApplication(appID)
        return "Success"
    return "Fail"

@bp.route('/delete', methods=('GET', 'POST'))
@login_required_C
def delete():
    if request.method == "POST":
        jobID = request.form["jobID"]
        Evaluator().deleteJob(jobID)
        get_db().deleteJobByID(jobID)
    return "Fail"

@bp.route('/weightUpdate', methods=('GET', 'POST'))
@login_required_C
def weightUpdate():
    if request.method == "POST":
        weight = request.form.to_dict(flat=False)["weight"]

        
        Evaluator().dashboardWeights(weight)
        return "Success"
    return "Fail"

@bp.route('/applicantReview', methods=('GET', 'POST'))
@login_required_C
def applicantReview():
    if request.method == "POST":
        appID = request.form["applicant id"]

        name = request.form["name"]

        data = get_db().getApplicantUserID(appID)
        data["name"] = name
        return render_template('/cli/appreview.html', name = name, application = data)
    return redirect(url_for('client.dashboard'))
