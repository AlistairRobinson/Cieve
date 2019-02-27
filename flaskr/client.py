from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, session
)
from werkzeug.exceptions import abort
from werkzeug.datastructures import ImmutableMultiDict

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
        
        stage_list.insert(0,"0") #Onboarding Stage
        
        error = None
        
        if jobTitle == "":
            error = "Empty Job Title"
        
        if division not in ["HR", "Technology", "Finance"]:
            error = "Incorrect Division"

        if role not in ["Full-Time", "Part-Time", "Internship", "Graduate", "Insight Program"]:
            error = "Incorrect Role"

        if country not in ["United Kingdom", "United States", "Germany"]:
            error = "Incorrect Country"

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
            db = get_db()
            json = {'jobTitle':jobTitle,
                    'division':division,
                    'role':role,
                    'country':country,
                    'jobDescription':jobDescription,
                    'noVacancies':noVacancies,
                    'stages':stage_list,
                    'skills':skills,
                    'skillVal':skillVal}
                    
            # Populate json with job data
            db.addNewJob(json, session.get('user_id')[1:])
            flash("Vacancy post successful")
            return redirect(url_for('client.jobs'))
    # Generate post data and pass to front end
    return render_template('/cli/createJob.html', stages=stages)

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