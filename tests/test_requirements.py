import pytest
import json
from flask import g, session, jsonify
from flaskr import db

# Client login tests (to ensure security)

def test_cli_login(client, jobs):
    jobs._client.post('/cli/auth/login', data={'username': 'test@test.tet', 'password': '123'})
    with jobs._client:
        client.get('/')
        assert 'C' in session['user_id']

# Vacany posting tests (R8, R14)

json = {}                       # TODO
json['user_id'] = 1
json['name'] = 'test'
json['skills'] = 'something'

@pytest.mark.parametrize(('data', 'message'), (
    (json, 'Vacany post successful'),
    ({}, 'Vacancy post unsuccessful'),
))
def test_post_vacancy(client, jobs, data, message):
    response = jobs.post_vacancy(data)
    with jobs._client.session_transaction() as session:
        try:
            error = session['_flashes'][0]
        except KeyError:
            raise AssertionError('nothing flashed')
        assert message in error[1]
    
# Vacancy retrieval tests (R15)

json = {}           # TODO
json['user_id'] = 1

def test_get_vacancies(client, jobs):
    response = jobs.get_vacancies(json)
    assert b'test' in response.data

# Application posting tests (R15)

json = {}                       # TODO
json['user_id'] = 1
json['name'] = 'applicant'
json['skills'] = 'something'

@pytest.mark.parametrize(('data', 'message'), (
    (json, 'Application post successful'),
    ({}, 'Application post unsuccessful'),
))
def test_post_application(client, jobs, data, message):
    response = jobs.apply_to_vacancy(data)
    with jobs._client.session_transaction() as session:
        try:
            error = session['_flashes'][0]
        except KeyError:
            raise AssertionError('nothing flashed')
        assert message in error[1]

# Application retrival tests (R5)

json = {}               # TODO
json['user_id'] = 1

def test_get_applications(client, jobs):
    response = jobs.retrieve_application(json)
    assert b'applicant' in response.data
