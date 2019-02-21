import pytest
from flask import g, session, flash

# Client login tests (R1)

def test_cli_login(client, auth):
    assert client.get('/cli/auth/login').status_code == 200
    response = auth.login_cli()

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username or password'),
    ('test', 'a', b'Incorrect username or password'),
))
def test_cli_login_validate_input(auth, username, password, message):
    response = auth.login_cli(username, password)
    assert message in response.data

# Applicant login tests (R1)

def test_apl_login(client, auth):
    assert client.get('/apl/auth/login').status_code == 200
    response = auth.login_apl()

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username or password'),
    ('test', 'a', b'Incorrect username or password'),
))
def test_apl_login_validate_input(auth, username, password, message):
    response = auth.login_apl(username, password)
    assert message in response.data

# Applicant registration tests (R1)

def test_register(client, app):
    assert client.get('/apl/auth/register').status_code == 200
    response = client.post('/apl/auth/register', data={'username': 'a', 'password': 'a'})

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', 'Username is required'),
    ('a', '', 'Password is required'),
    ('test', 'test', 'Username test is already taken'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/apl/auth/register',
        data={'username': username, 'password': password}
    )
    with client.session_transaction() as session:
            try:
                error = session['_flashes'][0]
            except KeyError:
                raise AssertionError('nothing flashed')
            assert message in error[1]
    print(str(response))
    assert message in response.data
