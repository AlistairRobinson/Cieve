
from flask import session
from bcrypt import gensalt

# This module allos for protection from CSRF attacks. In order for it to work, all post requests directed
# to the application must contain the following input:
# (in HTML) <input name=_csrf_token type=hidden value="{{ csrf_token() }}">
# (in Pytest) token = csrf.generate_csrf_token_with_session(<obj>._client)
#             response = auth._client.post(<url>, data={<data>, '_csrf_token': token}

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = str(gensalt(20))
    return session['_csrf_token']

def generate_csrf_token_with_session(s):
    with s.session_transaction() as session:
        if '_csrf_token' not in session:
            session['_csrf_token'] = str(gensalt(20))
        return session['_csrf_token']