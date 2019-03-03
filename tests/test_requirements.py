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
        'skill': ['Git', 'Presentation'],
        'skillVal': [7, 6],
        'lang': ['Python', 'C'],
        'langVal': [7, 6],
        'start_date': '03/03/2019',
        'asap': 'off',
        'min_degree_level': '1:1',
        'preferred_degrees': 'University of Warwick'
    }, 'Empty job title'),
    ({
        'job_title': 'test',
        'division': 'HR',
        'roles': 'Graduate',
        'country': 'Germany',
        'job_desc': '',
        'numVacancies': 1,
        'Stage_Description': ["000000000000000000000000"],
        'skill': ['Git', 'Presentation'],
        'skillVal': [7, 6],
        'lang': ['Python', 'C'],
        'langVal': [7, 6],
        'start_date': '03/03/2019',
        'asap': 'off',
        'min_degree_level': '1:1',
        'preferred_degrees': 'University of Warwick'
    }, 'No job description'),
    ({
        'job_title': 'test',
        'division': 'HR',
        'roles': 'Graduate',
        'country': 'Germany',
        'job_desc': 'test',
        'numVacancies': 'abc',
        'Stage_Description': ["000000000000000000000000"],
        'skill': ['Git', 'Presentation'],
        'skillVal': [7, 6],
        'lang': ['Python', 'C'],
        'langVal': [7, 6],
        'start_date': '03/03/2019',
        'asap': 'off',
        'min_degree_level': '1:1',
        'preferred_degrees': 'University of Warwick'
    }, 'Non-integer value for number of vacancies'),
    ({
        'job_title': 'test',
        'division': 'HR',
        'roles': 'Graduate',
        'country': 'Germany',
        'job_desc': 'test',
        'numVacancies': 1,
        'Stage_Description': ["000000000000000000000000"],
        'skill': ['Presentation'],
        'skillVal': [7, 6],
        'lang': ['Python', 'C'],
        'langVal': [7, 6],
        'start_date': '03/03/2019',
        'asap': 'off',
        'min_degree_level': '1:1',
        'preferred_degrees': 'University of Warwick'
    }, "Skills and scores don't match"),
    ({
        'job_title': 'test',
        'division': 'HR',
        'roles': 'Graduate',
        'country': 'Germany',
        'job_desc': 'test',
        'numVacancies': 1,
        'Stage_Description': ["000000000000000000000000"],
        'skill': ['Git', 'Presentation'],
        'skillVal': [7, 6],
        'lang': ['Python', 'C'],
        'langVal': [7, 6, 8],
        'start_date': '03/03/2019',
        'asap': 'off',
        'min_degree_level': '1:1',
        'preferred_degrees': 'University of Warwick'
    }, "Languages and scores don't match"),
    ({
        'job_title': 'test',
        'division': 'HR',
        'roles': 'Graduate',
        'country': 'Germany',
        'job_desc': 'test',
        'numVacancies': 1,
        'Stage_Description': ["000000000000000000000000"],
        'skill': ['Git', 'Presentation'],
        'skillVal': [17, 6],
        'lang': ['Python', 'C'],
        'langVal': [7, 6],
        'start_date': '03/03/2019',
        'asap': 'off',
        'min_degree_level': '1:1',
        'preferred_degrees': 'University of Warwick'
    }, 'Score out of range'),
    ({
        'job_title': 'test',
        'division': 'HR',
        'roles': 'Graduate',
        'country': 'Germany',
        'job_desc': 'test',
        'numVacancies': 1,
        'Stage_Description': ["000000000000000000000000"],
        'skill': ['Git', 'Presentation'],
        'skillVal': [7, 6],
        'lang': ['Python', 'C'],
        'langVal': [17, 6],
        'start_date': '03/03/2019',
        'asap': 'off',
        'min_degree_level': '1:1',
        'preferred_degrees': 'University of Warwick'
    }, 'Score out of range'),
    ({
        'job_title': 'test',
        'division': 'HR',
        'roles': 'Graduate',
        'country': 'Germany',
        'job_desc': 'test',
        'numVacancies': 1,
        'Stage_Description': ["000000000000000000000000"],
        'skill': ['Git', 'Presentation'],
        'skillVal': [7, 6],
        'lang': ['Python', 'C'],
        'langVal': [7, 6],
        'start_date': '03/03/2019',
        'asap': 'off',
        'min_degree_level': '1:1',
        'preferred_degrees': 'University of Warwick'
    }, 'Vacancy data accepted'),
))
def test_post_vacancy(client, jobs, data, message):
    token = csrf.generate_csrf_token_with_session(jobs._client)
    jobs._client.post('/cli/auth/login', data={'username': 'test', 'password': 'test', '_csrf_token': token})
    response = jobs.post_vacancy(data)
    print(response)
    with jobs._client.session_transaction() as session:
        try:
            print(session['_flashes'])
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
