import functools


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

from bcrypt import gensalt

bp = Blueprint('auth', __name__)

@bp.route('/apl/auth/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] # Password confimation to be done client side

        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.getUserAccount(username) is not None:
            error = 'Username {} is already taken.'.format(username)
        
        if error is None:
            salt = gensalt(12)
            passHash = generate_password_hash(password + salt)
            db.insertApplicantUser(username, passHash, salt)
            return redirect(url_for('auth.applicantLogin'))
        
        flash(error)
    
    return render_template('auth/apl/register.html')

@bp.route('/login')
def login():
    return render_template('login.html')

@bp.route('/apl/auth/login', methods=('GET', 'POST'))
def applicantLogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.getApplicantAccount(username)

        if user is None:
            error = 'Incorrect username or password.'
        elif not check_password_hash(user.password, password + user.salt):
            error = 'Incorrect username or password.'

        if error is None:
            session.clear()
            session['user_id'] = "A" + str(user.id)
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/apl/login.html')

@bp.route('/cli/auth/login', methods=('GET', 'POST'))
def clientLogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.getClientAccount(username)

        if user is None:
            error = 'Incorrect username or password.'
        elif not check_password_hash(user.password, password + user.salt):
            error = 'Incorrect username or password.'

        if error is None:
            session.clear()
            session['user_id'] = "C" + str(user.id)
            return redirect(url_for('index'))

        flash(error)

        return render_template('auth/cli/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    elif user_id[0] == "A":
        g.user = get_db().getApplicantUserID(user_id)
    elif user_id[0] == "C":
        g.user = get_db().getClientUserID(user_id)
    else:
        g.user = None
        session['user_id'] = None

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required_A(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or session.get('user_id')[0] != "A":
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def login_required_C(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or session.get('user_id')[0] != "C":
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view