import os

from flask import Flask
from flask import render_template

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
    
    @app.route('/LandingPage')
    @app.route('/index')
    @app.route('/')
    def index():
        return render_template("LandingPage.html")

    @app.route('/about')
    def about():
        return render_template("about.html")

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
            return jsonify(db.getJobs(no, division, role, location))
        return None

    return app
