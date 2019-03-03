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
def test_post_vacancy_validation(client, jobs, data, message):
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

# Vacancy post tests (R8, R14)

@pytest.mark.parametrize(('data_input', 'message'), (
({
        'json': "{'vacancy title': 'test'," + 
            "'division': 'HR'," +
            "'role type': 'Graduate'," +
            "'country': 'Germany'," +
            "'job_desc': 'test'," +
            "'positions available': '1'," +
            "'skills': {'Git': 7, 'Presentation': 6}," +
            "'languages': {'Python': 6, 'C':7}," +
            "'start date': '03/03/2019'," +
            "'asap': 'off'," + 
            "'min degree level': '1:1'," + 
            "'preferred degrees': 'University of Warwick'" + 
        "}",
        'interviews': "{'3': ['Interview', '5c74389bad9bb61fbcc01a3a'],'2': ['Mobile Interview', '5c7438ecad9bb61ff6d81d38']}",
        "vacancies[]2": ["2", "3"],
        "Date[]2": ["03/03/2019", "04/03/2019"],
        "startTime[]2": ["12:00", "13:00"],
        "endTime[]2": ["15:00", "17:00"],
        "vacancies[]3": ["2", "3"],
        "Date[]3": ["05/03/2019"],
        "startTime[]3": ["11:00"],
        "endTime[]3": ["17:00"]
    }, 'Vacancy post successful'),
))

# {'job_title': 'test','division': 'HR','roles': 'Graduate','country': 'Germany','job_desc': 'test','numVacancies': 1,'Stage_Description': ['000000000000000000000000', '5c74389bad9bb61fbcc01a3b'],'skill': ['Git', 'Presentation'],'skillVal': [7, 6],'lang': ['Python', 'C'],'langVal': [7, 6],'start_date': '03/03/2019','asap': 'off','min_degree_level': '1:1','preferred_degrees': 'University of Warwick'}

def test_post_vacancy(client, jobs, data_input, message):
    token = csrf.generate_csrf_token_with_session(jobs._client)
    jobs._client.post('/cli/auth/login', data={'username': 'test', 'password': 'test', '_csrf_token': token})
    token = csrf.generate_csrf_token_with_session(jobs._client)
    print(data_input['json'])
    response = jobs._client.post('/cli/newJobSummary', data={
        'json': data_input['json'],
        'interviews': data_input['interviews'],
        'vacancies[]2': data_input['vacancies[]2'],
        "Date[]2": data_input['Date[]2'],
        "startTime[]2": data_input['startTime[]2'],
        "endTime[]2": data_input['endTime[]2'],
        "vacancies[]3": data_input['vacancies[]3'],
        "Date[]3": data_input['Date[]3'],
        "startTime[]3": data_input['startTime[]3'],
        "endTime[]3": data_input['endTime[]3'],
        '_csrf_token': token
    })
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
