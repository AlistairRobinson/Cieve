from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, session
)
from werkzeug.exceptions import abort
from werkzeug.datastructures import ImmutableMultiDict
from bson.objectid import ObjectId

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
        division = request.form['divisions']
        role = request.form['roles']
        country = request.form['country']
        jobDescription = request.form['job_desc']
        noVacancies = request.form['numVacancies']



        data = request.form.to_dict(flat=False)
        try:
            stage_list = data['Stage_Description']
        except:
            stage_list = []
        skills = data['skill']
        skillVal = data['skillVal']

        stage_list.insert(0,'000000000000000000000000') #Onboarding Stage

        error = None
        
        if jobTitle == "":
            error = "Empty Job Title"

        if division not in db.getDivisions():
            db.newDivision(division)

        if role not in db.getRoles():
            db.newRole(role)

        if country not in db.getLocations():
            db.newLocation(country)

        if jobDescription == "":
            error = "No Job description"

        if str.isdigit(str(noVacancies)):
            if int(noVacancies) <= 0:
                error = "Number of vacancies must be positive"
        else:
            error = "Non-integer value for number of vacancies"

        if len(skills) != len(skillVal):
            error = "Skills and scores don't match"

        for val in skillVal:
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
                    'stages':stage_list,
                    'skills':skills,
                    'skillVal':skillVal}

            skillDic = {}
            skillVal = json.pop('skillVal', None)
            skills = json.pop('skills', None)
            for i in range(len(skills)):
                skillDic[skills[i]] = skillVal[i]
            json['skills'] = skillDic
            json['stagesDetail'] = []
            interviews = {}
            for stage in json['stages']:
                i = 1
                if stage != '000000000000000000000000':
                    title = db.getStageTitle(stage)
                    json['stagesDetail'].append(title)
                    if stage in db.getInterviewStages():
                        interviews[i] = [title, str(stage)]
                i += 1


            return render_template('/cli/review.html', json = json, interviews = interviews)
    # Generate post data and pass to front end
    return render_template('/cli/createJob.html', stages=stages,divisons = db.getDivisions(), roles = db.getRoles(), locations = db.getLocations())

@bp.route('/newJobSummary' , methods=('GET', 'POST'))
@login_required_C
def newJobSummary():
    if request.method == "POST":
            data = request.form.to_dict(flat=False)

            json = data['json']
            del data[json]

            db = get_db()
            for stage in data:
                db.insertStageAvailability(stage) #Stage = {of ["dd/mm/yy", start time, end time, number of slots]}

            db.addNewJob(json, session.get('user_id')[1:])
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
    db = get_db()
    jobData = db.getClientJobs(session.get('user_id')[1:])
    applicants = {}
    if request.method == "POST":
        jobID = request.form["jobID"]
        stageNumber = request.form["stageID"]
        error = None

        if error is not None:
            applicants = db.getApplicantsJob(jobID, stageNumber)

    return render_template('/cli/jobBreakdown.html', jobData = jobData, applicants = {})
