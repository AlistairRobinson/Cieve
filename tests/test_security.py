import pytest
from flask import g, session, flash

# Client login tests (R1)

def test_cli_login(client, auth):
    assert client.get('/cli/auth/login').status_code == 200

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', 'Incorrect username or password'),
    ('test', 'a', 'Incorrect username or password'),
))
def test_cli_login_validate_input(auth, username, password, message):
    response = auth.login_cli(username, password)
    with auth._client.session_transaction() as session:
        try:
            error = session['_flashes'][0]
        except KeyError:
            raise AssertionError('nothing flashed')
        assert message in error[1]

# Applicant login tests (R1)

def test_apl_login(client, auth):
    assert client.get('/apl/auth/login').status_code == 200

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', 'Incorrect username or password'),
    ('test', 'a', 'Incorrect username or password'),
))
def test_apl_login_validate_input(auth, username, password, message):
    response = auth.login_apl(username, password)
    with auth._client.session_transaction() as session:
        try:
            error = session['_flashes'][0]
        except KeyError:
            raise AssertionError('nothing flashed')
        assert message in error[1]

# Applicant registration tests (R1)

def test_register(client, app):
    assert client.get('/apl/auth/register').status_code == 200
    response = client.post('/apl/auth/register', data={'username': 'test', 'password': 'test'})

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', 'Username is required'),
    ('a', '', 'Password is required'),
    ('test', 'test', 'Username test is already taken'),
))
def test_register_validate_input(client, auth, username, password, message):
    response = auth._client.post(
        '/apl/auth/register',
        data={'username': username, 'password': password}
    )
    with auth._client.session_transaction() as session:
        try:
            error = session['_flashes'][0]
        except KeyError:
            raise AssertionError('nothing flashed')
        assert message in error[1]
