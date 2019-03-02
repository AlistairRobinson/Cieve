import pytest
from flask import g, session, flash
from flaskr import csrf
from flaskr.db import get_db

# Applicant registration tests (R1)

def test_apl_registration_get(client, app):
    assert client.get('/apl/auth/register').status_code == 200

@pytest.mark.parametrize(('username', 'password', 'name', 'message'), (
    ('test', 'test', 'test', 'Registration successful'),
    ('', '', '', 'Username is required'),
    ('test', '', '', 'Password is required'),
    ('test', 'test', 'test', 'Username test is already taken'),
))
def test_apl_registration(client, auth, username, password, name, message):
    token = csrf.generate_csrf_token_with_session(auth._client)
    response = auth._client.post(
        '/apl/auth/register',
        data={'username': username, 'password': password, 'name': name, '_csrf_token': token}
    )
    with auth._client.session_transaction() as session:
        try:
            error = session['_flashes'][0]
        except KeyError:
            raise AssertionError('nothing flashed')
        assert message in error[1]

# Client registration tests (R1)

def test_cli_registration_get(client, app):
    assert client.get('/cli/auth/register').status_code == 200

@pytest.mark.parametrize(('username', 'password', 'name', 'message'), (
    ('test', 'test', 'test', 'Registration successful'),
    ('', '', '', 'Username is required'),
    ('test', '', '', 'Password is required'),
    ('test', 'test', 'test', 'Username test is already taken'),
))
def test_cli_registration(client, auth, username, password, name, message):
    token = csrf.generate_csrf_token_with_session(auth._client)
    response = auth._client.post(
        '/cli/auth/register',
        data={'username': username, 'password': password, 'name': name, '_csrf_token': token}
    )
    with auth._client.session_transaction() as session:
        try:
            error = session['_flashes'][0]
        except KeyError:
            raise AssertionError('nothing flashed')
        assert message in error[1]

# Client login tests (R1)

def test_cli_login_get(client, auth):
    assert client.get('/cli/auth/login').status_code == 200

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', 'Incorrect username or password'),
    ('', '', 'Incorrect username or password'),
    ('a', 'test', 'Incorrect username or password'),
    ('test', 'a', 'Incorrect username or password'),
    ('test', 'test', 'Login successful'),
))
def test_cli_login(auth, username, password, message):
    response = auth.login_cli(username, password)
    with auth._client.session_transaction() as session:
        try:
            error = session['_flashes'][0]
        except KeyError:
            raise AssertionError('nothing flashed')
        assert message in error[1]

# Applicant login tests (R1)

def test_apl_login_get(client, auth):
    assert client.get('/apl/auth/login').status_code == 200

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', 'Incorrect username or password'),
    ('', '', 'Incorrect username or password'),
    ('a', 'test', 'Incorrect username or password'),
    ('test', 'a', 'Incorrect username or password'),
    ('test', 'test', 'Login successful'),
))
def test_apl_login(auth, username, password, message):
    response = auth.login_apl(username, password)
    with auth._client.session_transaction() as session:
        try:
            error = session['_flashes'][0]
        except KeyError:
            raise AssertionError('nothing flashed')
        assert message in error[1]

# NoSQL injection tests (R16)

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('abc', '[%24ne]=', 'Incorrect username or password'),
    ('abc', '{"&gt": ""}', 'Incorrect username or password'),
))
def test_cli_nosql_injection(client, auth, username, password, message):
    token = csrf.generate_csrf_token_with_session(auth._client)
    auth._client.post('/cli/auth/login', data={'username': username, 'password': password, '_csrf_token': token})
    with auth._client.session_transaction() as session:
        try:
            error = session['_flashes'][0]
        except KeyError:
            raise AssertionError('nothing flashed')
        assert message in error[1]

def test_cleanup(client, auth):
    db = get_db()
    assert db.deleteApplicantAccount("test")
    assert db.deleteClientAccount("test")