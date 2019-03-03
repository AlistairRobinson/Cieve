from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, session
)
from werkzeug.exceptions import abort
from werkzeug.datastructures import ImmutableMultiDict
from bson.objectid import ObjectId
import json

from flaskr.auth import login_required_C
from flaskr.db import get_db

bp = Blueprint('client', __name__, url_prefix='/cli')

#Definition for the client dashboard
@bp.route('/dashboard')
@bp.route('/')
@login_required_C
def dashboard():
    # Generate post data and pass to front end
    return render_template('/cli/Dashboard.html')

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
        preferedDegrees = request.form['preferred_degrees']


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
                    'positions available':noVacancies,
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
                    if stage in db.getInterviewStages():
                        interviews[str(i)] = [title, str(stage)]
                i += 1
            return render_template('cli/review.html', json = json, interviews = interviews)
    # Generate post data and pass to front end
    return render_template('cli/createjob.html', stages=stages,divisons = db.getDivisions(), roles = db.getRoles(), locations = db.getLocations())

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

        userID = session.get('user_id')[1:]
        jobID =  db.addNewJob(jsonData, userID)
        interviewsData = json.loads(data["interviews"][0].replace("'",'"').replace('u"','"'))
        for stepID, interviews in interviewsData.items():
            stageID = interviews[1]
            dates = data.get("Date[]" + stepID, [])
            startTimes = data.get("startTime[]" + stepID, [])
            endTimes = data.get("endTime[]" + stepID, [])
            vacancies = data.get("vacancies[]" + stepID, [])

            if len(startTimes) != len(endTimes) or len(dates) != len(startTimes):
                flash("An unexpected error occured")
                continue
            
            if len(vacancies) == 0:
                flash("An unexpected error occured")
                continue
            
            if any(int(v) <= 0 for v in vacancies):
                flash("An unexpected error occured")
                continue

            stagesData = []
            for i in range(len(dates)):
                stagesData.append([dates[i], startTimes[i], endTimes[i], vacancies[i]])
            
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
        #jobData = db.getJob(jobID)
        print jobID
        jobData = ""
        applicants = {}

        stepNumber = 0
        try:
            stepNumber = request.form["stageID"]
        except:
            pass
        
        error = None
        
        if error is None:
            applicants = db.getApplicantsJob(jobID, stepNumber)
        
        return render_template('/cli/jobBreakdown.html', jobData = jobData, applicants = applicants)

    return redirect(url_for('client.jobs'))
