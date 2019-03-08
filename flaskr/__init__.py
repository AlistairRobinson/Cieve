import os
import json

from flask import Flask
from flask import render_template
from flask import request, session, abort
from flask import jsonify
from flaskr import csrf
from flaskr.db import get_db

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import applicant
    app.register_blueprint(applicant.bp)

    from . import client
    app.register_blueprint(client.bp)

    app.config.from_mapping(SECRET_KEY='disgrace abstain umbilical freehand isotope staleness swerve matrimony babbling clock')
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Enforces the inclusion of CSRF protection tokens in all POST requests

    @app.before_request
    def csrf_protect():
        if request.method == "POST":
            token = session['_csrf_token']
            session['_csrf_token'] = csrf.generate_csrf_token()
            if not token or token != request.form.get('_csrf_token'):
                abort(403)

    # Enforce security standards in all HTTP responses

    @app.after_request
    def enforce_security(response):
        csp = "default-src 'self' 'unsafe-inline' https://*.googleapis.com https://*.gstatic.com https://maxcdn.bootstrapcdn.com https://cdnjs.cloudflare.com https://use.fontawesome.com https://cdn.jsdelivr.net"
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'  # Enforce HTTPS in browser
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'                                     # Only allow HTML frames from this origin
        response.headers['Content-Security-Policy'] = csp                                      # Prevent content loading from outside origin
        return response                                                                        # ^ This is very strict and may cause issues, edit if necessary

    # Returns a user's phish code, if they are logged in

    def get_phish():
        if 'user_id' in session:
            if get_db().getApplicantPhish(session['user_id']) != "":
                return get_db().getApplicantPhish(session['user_id'])
            if get_db().getClientPhish(session['user_id']) != "":
                return get_db().getClientPhish(session['user_id'])
        return ""

    # Returns a user's name as entered during registration, if they are logged in

    def get_name():
        if 'user_id' in session:
            if get_db().getApplicantNameID(session['user_id'][1:]) != "":
                return get_db().getApplicantNameID(session['user_id'][1:])
            if get_db().getClientNameID(session['user_id'][1:]) != "":
                return get_db().getClientNameID(session['user_id'][1:])
        return ""

    # Returns a user's message which updates as they interact with the system (e.g. apply to a job)

    def get_message():
        if 'user_id' in session:
            if get_db().applicantExists(session['user_id'][1:]):
                return get_db().getApplicantMessage(session['user_id'][1:])
            if get_db().clientExists(session['user_id'][1:]):
                return get_db().getClientMessage(session['user_id'][1:])

    # Allows templates to set unique CSRF tokens, phish codes, names and messages on load
                
    app.jinja_env.globals['csrf_token'] = csrf.generate_csrf_token
    app.jinja_env.globals['phish'] = get_phish
    app.jinja_env.globals['name'] = get_name
    app.jinja_env.globals['message'] = get_message
    
    @app.route('/LandingPage')
    @app.route('/index')
    @app.route('/')
    def index():
        return render_template("LandingPage.html")

    @app.route('/about')
    def about():
        return render_template("about.html")

    @app.route('/privacy')
    def privacy():
        return render_template("privacy.html")

    # Can be called by a AJAX request to return the job data
    # For applications pass 0 to return all jobs
    @app.route('/getJobs', methods=('GET', 'POST'))
    def getJobs():
        if request.method == "POST":
            no = request.form['page']
            division = request.form['division']
            role = request.form['role']
            location = request.form['location']
            error = None

            # ERROR checks

            if error is not None:
                return None

            db = get_db()
            x = db.getJobs(no, division, role, location)
            for o in x:
                o['_id'] = str(o['_id'])
            x.append({"pageTotal" : db.getPageTotal(division, role, location)})
            return jsonify(x)
        return None

    return app
