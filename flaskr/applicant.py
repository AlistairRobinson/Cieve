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
    return render_template('/apl/Dashboard.html')

#Definition for the applicant job search page
@bp.route('/jobsearch', methods=('GET', 'POST'))
@login_required_A
def jobSearch():
    no = 1
    division = ""
    role = ""
    location = ""
    if request.method == 'POST':
        no = request.form['page']
        division = request.form['division']
        role = request.form['role']
        location = request.form['location']

        error = None

        #ERROR CHECK

        if error is not None:
            flash(error)

    db = get_db()
    postData = db.getJobs(no, division, role, location)
    
    return render_template('/apl/jobSearch.html', post = postData)
            # Return first 20 (use a page count, get[1,2,...])

#Definition for the application
@bp.route('/newapplication', methods=('GET', 'POST'))
@login_required_A
def newApplication():
    # Generate post data and pass to front end
    skills = {}
    jobs = {}
    others = False
    if request.method == 'POST':
        skills = request.form['skills']
        jobs = request.form['jobs']
        other = request.form['other']
        error = None

        # Error check
            # other != T or F
        if error is not None:
            flash(error)
        else:
            if other == "T":
                #otherJobs Suitable function
                otherJobs = {}

                jobs.extend(otherJobs)
            
            for job in jobs:
                db = get_db()
                userID = session.get('user_id')[1:]
                db.applyJob(userID, job)
            
            # APPLY SKILS SCORE ....

            # APPLICANT SCORING FUNCTION HERE
            return render_template(url_for('apl.applications'))

    return render_template('/apl/applicationCreation.html')

#Definition for the application
@bp.route('/applications')
@login_required_A
def applications():
    # Generate post data and pass to front end
    return render_template('/apl/applications.html')