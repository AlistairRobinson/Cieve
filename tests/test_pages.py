import pytest
from flaskr import csrf
from flaskr.db import get_db

def test_setup_cli(client, page):
    token = csrf.generate_csrf_token_with_session(client)
    page._client.post(
        '/cli/auth/register',
        data={'username': 'test', 'password': 'test', 'name': 'test', '_csrf_token': token}
    )
    with client.session_transaction() as session:
        try:
            error = session['_flashes'][0]
        except KeyError:
            raise AssertionError('nothing flashed')
        assert 'Registration successful' in error[1]

def test_setup_apl(client, page):
    token = csrf.generate_csrf_token_with_session(client)
    page._client.post(
        '/apl/auth/register',
        data={'username': 'test', 'password': 'test', 'name': 'test', '_csrf_token': token}
    )
    with client.session_transaction() as session:
        try:
            error = session['_flashes'][0]
        except KeyError:
            raise AssertionError('nothing flashed')
        assert 'Registration successful' in error[1]

def test_page_home(client, page):
    assert page._client.get('/').status_code == 200

def test_page_cli_login(client, page):
    assert page._client.get('/cli/auth/login').status_code == 200

def test_page_apl_login(client, page):
    assert page._client.get('/apl/auth/login').status_code == 200

def test_page_cli_registration(client, page):
    assert page._client.get('/cli/auth/register').status_code == 200

def test_page_apl_registration(client, page):
    assert page._client.get('/apl/auth/register').status_code == 200

def test_page_privacy(client, page):
    assert page._client.get('/privacy').status_code == 200

def test_page_apl_dashboard(client, page):
    token = csrf.generate_csrf_token_with_session(client)
    page._client.post('/apl/auth/login', data={'username':'test', 'password':'test', '_csrf_token':token})
    assert page._client.get('/apl/').status_code == 200

def test_page_apl_apply(client, page):
    token = csrf.generate_csrf_token_with_session(client)
    page._client.post('/apl/auth/login', data={'username':'test', 'password':'test', '_csrf_token':token})
    assert page._client.get('/apl/newapplication').status_code == 200

def test_page_apl_search(client, page):
    token = csrf.generate_csrf_token_with_session(client)
    page._client.post('/apl/auth/login', data={'username':'test', 'password':'test', '_csrf_token':token})
    assert page._client.get('/apl/jobsearch').status_code == 200

def test_page_apl_search(client, page):
    token = csrf.generate_csrf_token_with_session(client)
    page._client.post('/apl/auth/login', data={'username':'test', 'password':'test', '_csrf_token':token})
    assert page._client.get('/apl/applications').status_code == 200

def test_page_cli_dashboard(client, page):
    token = csrf.generate_csrf_token_with_session(client)
    page._client.post('/cli/auth/login', data={'username':'test', 'password':'test', '_csrf_token':token})
    assert page._client.get('/cli/').status_code == 200

def test_page_cli_jobs(client, page):
    token = csrf.generate_csrf_token_with_session(client)
    page._client.post('/cli/auth/login', data={'username':'test', 'password':'test', '_csrf_token':token})
    assert page._client.get('/cli/jobs').status_code == 200

def test_page_cli_newjob(client, page):
    token = csrf.generate_csrf_token_with_session(client)
    page._client.post('/cli/auth/login', data={'username':'test', 'password':'test', '_csrf_token':token})
    assert page._client.get('/cli/newjob').status_code == 200

def test_cli_cleanup(client, auth):
    db = get_db()
    assert db.deleteClientAccount("test")

def test_apl_cleanup(client, auth):
    db = get_db()
    assert db.deleteApplicantAccount("test")