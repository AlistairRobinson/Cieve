import pytest
import json
from flask import g, session, jsonify
from flaskr import db

# Client login tests (to ensure security)

def test_cli_login(client, auth):
<<<<<<< HEAD
    assert client.get('cli/auth/login').status_code == 200
=======
    assert client.get('/cli/auth/login').status_code == 200
>>>>>>> fbf477d422de66fc368eaa13acbe3ddce5141c3c
    response = auth.login_cli()

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

# Vacany posting tests (R8, R14)

json = {}                       # TODO
json['id'] = 1
json['name'] = 'test'
json['skills'] = 'something'

@pytest.mark.parametrize(('data', 'message'), (
    (json, b'Vacany post successful'),
    ({}, b'Vacancy post unsuccessful'),
))
def test_post_vacancy(client, jobs, data, message):
    response = jobs.post_vacancy(data)
    assert message in response.data
    
# Vacancy retrieval tests (R15)

json = {}           # TODO
json['id'] = 1

def test_get_vacancies(client, jobs):
    response = jobs.get_vacancies(json)
    assert 'test' in response.data

# Application posting tests (R15)

json = {}                       # TODO
json['id'] = 1
json['name'] = 'applicant'
json['skills'] = 'something'

@pytest.mark.parametrize(('data', 'message'), (
    (json, b'Application post successful'),
    ({}, b'Application post unsuccessful'),
))
def test_post_application(client, jobs, data, message):
    response = jobs.apply_to_vacancy(data)
    assert message in response.data

# Application retrival tests (R5)

json = {}               # TODO
json['id'] = 1

def test_get_applications(client, jobs):
    response = jobs.retrieve_application(json)
    assert 'applicant' in response.data
