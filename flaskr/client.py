from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required_C
from flaskr.db import get_db

bp = Blueprint('client', __name__, url_prefix='/cli')

#Definition for the client dashboard
@bp.route('/dashboard')
@bp.route('/')
#@login_required_C
def dashboard():
    # Generate post data and pass to front end
    return render_template('/cli/Dashboard.html')

#Definition for the client job creation
@bp.route('/newjob', methods=('GET', 'POST'))
@login_required_C
def newJob():
    if request.method == 'POST':
        # Get job post data
        error = None

        # Error checks
        if error is not None:
            flash(error)
        else:
            db = get_db()
            json = {}
            # Populate json with job data
            db.addJob(json)
            return redirect(url_for('cli.jobs'))
    # Generate post data and pass to front end
    return render_template('/cli/jobCreation.html')

#Definition for the application
@bp.route('/jobs')
@login_required_C
def jobs():
    # Generate post data and pass to front end
    return render_template('/cli/jobs.html')