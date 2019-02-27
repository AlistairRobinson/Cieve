import pytest
import json
from flask import g, session, jsonify
from flaskr import db, csrf

# Client login tests (to ensure security)

def test_cli_login(client, jobs):
    token = csrf.generate_csrf_token_with_session(jobs._client)
    response = jobs._client.post('/cli/auth/login', data={'username': '1@1', 'password': '1', '_csrf_token': token})
    with jobs._client:
        client.get('/')
        assert 'C' in session['user_id']

# Vacany posting tests (R8, R14)

@pytest.mark.parametrize(('data', 'message'), (
    ({
        'job_title': 'test',
        'division': 'HR',
        'roles': 'Graduate',
        'country': 'Germany',
        'job_desc': 'test',
        'numVacancies': 1,
        'Stage_Description': [1, 2, 3],
        'skill': ['Python', 'C'],
        'skillVal': [7, 6]
    }, 'Vacancy post successful'),
))
def test_post_vacancy(client, jobs, data, message):
    token = csrf.generate_csrf_token_with_session(jobs._client)
    jobs._client.post('/cli/auth/login', data={'username': '1@1', 'password': '1', '_csrf_token': token})
    response = jobs.post_vacancy(data)
    with jobs._client.session_transaction() as session:
        try:
            error = session['_flashes'][0]
        except KeyError:
            raise AssertionError('nothing flashed')
        assert message in error[1]
    
# Vacancy retrieval tests (R15)

def test_get_vacancies(client, jobs):
    json = {}
    json['page'] = 0
    json['division'] = 'HR'
    json['role'] = 'Graduate'
    json['location'] = 'Germany'
    response = jobs.get_vacancies(json)
    assert b'test' in response.data

# Application posting tests (R15)

json = {} # TODO
json['skills'] = None
json['jobs'] = None
json['other'] = None

@pytest.mark.parametrize(('data', 'message'), (
    (json, 'Application post successful'),
))
def test_post_application(client, jobs, data, message):
    token = csrf.generate_csrf_token_with_session(jobs._client)
    jobs._client.post('/apl/auth/login', data={'username': '1@1', 'password': '1', '_csrf_token': token})
    response = jobs.apply_to_vacancy(data)
    with jobs._client.session_transaction() as session:
        try:
            error = session['_flashes'][0]
        except KeyError:
            raise AssertionError('nothing flashed')
        assert message in error[1]
