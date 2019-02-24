
from flask import session
from bcrypt import gensalt

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = str(gensalt(12))
    return session['_csrf_token']

def generate_csrf_token_with_session(s):
    with s.session_transaction() as session:
        if '_csrf_token' not in session:
            session['_csrf_token'] = str(gensalt(12))
        return session['_csrf_token']