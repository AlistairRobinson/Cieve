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
    db = get_db()
    return render_template('/apl/jobSearch.html', divisons = db.getDivisions(), roles = db.getRoles(), locations = db.getLocations())
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
        universtiyAttended = request.form['University_Attended']

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
                unselected_Jobs = request.form.to_dict(flat=False)["Unselected_Jobs[]"]
            except:
                pass

        coverLetter = request.form['Cover_Letter']
        interestingFacts = request.form['Interesting_Facts']

        userID = session.get('user_id')[1:]

        db = get_db()
        for job in selectedJobs:
            jobScore = 0 #INSERT APPLICANT PROCESSING HERE
            db.applyJob(userID, job, 1, jobScore)

        for job in unselectedJobs:
            jobScore = 0 #INSERT APPLICANT PROCESSING HERE
            db.applyJob(userID, job, 0, jobScore)
        
        db.addUserEducation(userID, alevels, degreeQualification, degreeLevel, universtiyAttended)

        db.addUserSkills(userID, skills)

        db.addUserLanguages(userID, languages)

        db.addUserEmployment(userID, employmentHistory)

        db.addUserContacts(userID, phoneNumber, address)

        db.addUserMetaData(userID, coverLetter, interestingFacts)

        db.addUserScore(userID, 0)  # USER GENERAL SCORE
        """
        skills = request.form['skills']
        jobs = request.form['jobs']
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
                userID = session.get('user_id')[1:]
                score = 0 #CALCLUATE JOB SPECIFIC SCORE

                db.applyJob(userID, jobID, score, prefered)

            # APPLY SKILS SCORE ....

            # APPLICANT SCORING FUNCTION HERE
            return render_template(url_for('apl.applications'))
        """

    return render_template('/apl/applicationCreation.html', divisons = db.getDivisions(), roles = db.getRoles(), locations = db.getLocations())

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
