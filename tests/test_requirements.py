import pytest
import json
from flask import g, session, jsonify
from flaskr import csrf
from flaskr.db import get_db

# Client login tests (to ensure security)

def test_setup_cli(client, jobs):
    token = csrf.generate_csrf_token_with_session(client)
    jobs._client.post(
        '/cli/auth/register',
        data={'username': 'test', 'password': 'test', 'name': 'test', '_csrf_token': token}
    )
    with client.session_transaction() as session:
        try:
            error = session['_flashes'][0]
        except KeyError:
            raise AssertionError('nothing flashed')
        assert 'Registration successful' in error[1]

# Vacany posting tests (R8, R14)

@pytest.mark.parametrize(('data', 'message'), (
    ({
        'job_title': '',
        'division': 'HR',
        'roles': 'Graduate',
        'country': 'Germany',
        'job_desc': 'test',
        'numVacancies': 1,
        'Stage_Description': ["000000000000000000000000"],
        'skill': ['Python', 'C'],
        'skillVal': [7, 6]
    }, 'Empty job title'),
    ({
        'job_title': 'test',
        'division': 'HR',
        'roles': 'Graduate',
        'country': 'Germany',
        'job_desc': '',
        'numVacancies': 1,
        'Stage_Description': ["000000000000000000000000"],
        'skill': ['Python', 'C'],
        'skillVal': [7, 6]
    }, 'No job description'),
    ({
        'job_title': 'test',
        'division': 'HR',
        'roles': 'Graduate',
        'country': 'Germany',
        'job_desc': 'test',
        'numVacancies': -1,
        'Stage_Description': ["000000000000000000000000"],
        'skill': ['Python', 'C'],
        'skillVal': [7, 6]
    }, 'Non-integer value for number of vacancies'),
    ({
        'job_title': 'test',
        'division': 'HR',
        'roles': 'Graduate',
        'country': 'Germany',
        'job_desc': 'test',
        'numVacancies': 1,
        'Stage_Description': ["000000000000000000000000"],
        'skill': ['Python', 'C'],
        'skillVal': [1]
    }, "Skills and scores don't match"),
    ({
        'job_title': 'test',
        'division': 'HR',
        'roles': 'Graduate',
        'country': 'Germany',
        'job_desc': 'test',
        'numVacancies': 1,
        'Stage_Description': ["000000000000000000000000"],
        'skill': ['Python'],
        'skillVal': [7, 6]
    }, "Skills and scores don't match"),
    ({
        'job_title': 'test',
        'division': 'HR',
        'roles': 'Graduate',
        'country': 'Germany',
        'job_desc': 'test',
        'numVacancies': 1,
        'Stage_Description': ["000000000000000000000000"],
        'skill': ['Python', 'C'],
        'skillVal': [77, 6]
    }, 'Score out of range'),
    ({
        'job_title': 'test',
        'division': 'HR',
        'roles': 'Graduate',
        'country': 'Germany',
        'job_desc': 'test',
        'numVacancies': 1,
        'Stage_Description': ["000000000000000000000000"],
        'skill': ['Python', 'C'],
        'skillVal': ['77', '6']
    }, 'Score out of range'),
    ({
        'job_title': 'test',
        'division': 'HR',
        'roles': 'Graduate',
        'country': 'Germany',
        'job_desc': 'test',
        'numVacancies': 1,
        'Stage_Description': ["987654321987654321987654"],
        'skill': ['Python', 'C'],
        'skillVal': [7, 6]
    }, 'Wrong stage'),
    ({
        'job_title': 'test',
        'division': 'HR',
        'roles': 'Graduate',
        'country': 'Germany',
        'job_desc': 'test',
        'numVacancies': 1,
        'Stage_Description': ["000000000000000000000000"],
        'skill': ['Python', 'C'],
        'skillVal': [7, 6]
    }, 'Vacancy data accepted'),
))
def test_post_vacancy(client, jobs, data, message):
    token = csrf.generate_csrf_token_with_session(jobs._client)
    jobs._client.post('/cli/auth/login', data={'username': 'test', 'password': 'test', '_csrf_token': token})
    response = jobs.post_vacancy(data)
    with jobs._client.session_transaction() as session:
        try:
            error = session['_flashes'][1]
        except KeyError:
            raise AssertionError('nothing flashed')
        assert message in error[1]

# Vacancy retrieval tests (R15)

def test_get_vacancies(client, jobs):
    json = {}
    json['page'] = 0
    json['division'] = ''
    json['role'] = ''
    json['location'] = ''
    response = jobs.get_vacancies(json)
    print(response.data)
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
    jobs._client.post('/apl/auth/login', data={'username': 'test', 'password': 'test', '_csrf_token': token})
    response = jobs.apply_to_vacancy(data)
    with jobs._client.session_transaction() as session:
        try:
            error = session['_flashes'][0]
        except KeyError:
            raise AssertionError('nothing flashed')
        assert message in error[1]

def test_cleanup_job():
    db = get_db()
    assert db.deleteJob("test") 
    
def test_cleanup_appl():
    db = get_db()
    assert db.deleteApplication("test") 
    
def test_cleanup_cli():
    db = get_db()
    assert db.deleteClientAccount("test")
