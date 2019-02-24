from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
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
        stages = data['Stage_Description']
        skills = data['skill']
        skillVal = data['skillVal']

       
        error = None

        # Error checks!!


        if error is not None:
            flash(error)
        else:
            db = get_db()
            json = {jobTitle,
                    division,
                    role,
                    country,
                    jobDescription,
                    noVacancies,
                    stages,
                    skills,
                    skillVal}
            # Populate json with job data
            db.addNewJob(json)
            #return redirect(url_for('client.jobs'))
    # Generate post data and pass to front end
    return render_template('/cli/createJob.html', stages=stages)

#Definition for the application
@bp.route('/jobs')
@login_required_C
def jobs():
    # Generate post data and pass to front end
    return render_template('/cli/jobs.html')