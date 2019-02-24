from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

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
    return render_template('/apl/jobSearch.html')
            # Return first 20 (use a page count, get[1,2,...])

#Definition for the application
@bp.route('/newapplication', methods=('GET', 'POST'))
@login_required_A
def newApplication():
    # Generate post data and pass to front end
    skills = {}
    jobs = {}
    others = ""
    if request.method == 'POST':
        skills = request.form['skills']
        jobs = request.form['jobs'] # Dictionary of jobID to prefered or not (1 or 0)
        other = request.form['other']
        error = None

        if other not in ["T", "F"]:
            error = 'Error! Other is not T or F'
        
        if skills == None:
            error = "No skills"

        if jobs == None:
            error = "No jobs selected"
        
        # STANDARD SCORE + DB UPDATE

        if error is not None:
            flash(error)
        else:
            if other == "F":

                for job, prefered in jobs.items():
                    if prefered == 0:
                        del jobs[job]
            
            for jobID, prefered in jobs.items():
                db = get_db()
                userID = session.get('user_id')[1:]
                score = 0 #CALCLUATE JOB SPECIFIC SCORE

                db.applyJob(userID, jobID, score, prefered)
            
            # APPLY SKILS SCORE ....

            # APPLICANT SCORING FUNCTION HERE
            return render_template(url_for('apl.applications'))

    return render_template('/apl/applicationCreation.html')

#Definition for the application
@bp.route('/applications')
@login_required_A
def applications():
    db = get_db()
    applicationsData = db.getApplications(session.get('user_id')[1:])
    filteredData = {}
    for applicationData in applicationsData:
        if (applicationData["current stage"] != 0) or (applicationData["preferred"] == 1):
            filteredData.append(applicationData)
    return render_template('/apl/applications.html', applications = filteredData)

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