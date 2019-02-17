import os

from flask import Flask
from flask import render_template

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import applicant
    app.register_blueprint(applicant.bp)

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
    

    return app
