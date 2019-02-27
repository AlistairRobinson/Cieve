import os
import json

from flask import Flask
from flask import render_template
from flask import request, session, abort
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
        csp = "default-src 'self' 'unsafe-inline' https://*.googleapis.com https://*.gstatic.com https://maxcdn.bootstrapcdn.com https://cdnjs.cloudflare.com https://use.fontawesome.com"
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'  # Enforce HTTPS in browser
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'                                     # Only allow HTML frames from this origin
        response.headers['X-Content-Type-Options'] = 'nosniff'                                 # Prevent browsers from autodetecting content
        response.headers['Content-Security-Policy'] = csp                                      # Prevent content loading from outside origin
        return response                                                                        # ^ This is very strict and may cause issues, edit if necessary

    # Allows templates to set unique CSRF tokens on load
                
    app.jinja_env.globals['csrf_token'] = csrf.generate_csrf_token 
    
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
            return jsonify(db.getJobs(no, division, role, location)).append({"pageTotal" : db.getPageTotal()})
        return None

    return app
