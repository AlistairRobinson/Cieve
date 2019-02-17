import pytest
import json
from flask import g, session, jsonify

# Client login tests (to ensure security)

def test_cli_login(client, auth):
    assert client.get('/auth/cli/login').status_code == 200
    response = auth.login_cli()

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

# Vacany posting tests (R8, R14)

json = {}
json['id'] = 1
json['name'] = 'test'
json['skills'] = 'something'

@pytest.mark.parametrize(('data', 'message'), (
    (json, b'Vacany post successful'),
    ({}, b'Vacancy post unsuccessful'),
))
def test_post_vacancy(client, jobs, data, message):
    response = jobs.post_vacancy(data)
    assert message in response.
    
# Vacancy retrieval tests (R15)

json = {}
json['id'] = 1

def test_get_vacancies(client, jobs):
    response = jobs.get_vacancies(json)
    assert 'test' in response

# Application posting tests (R15)

json = {}
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

json = {}
json['id'] = 1

def test_get_applications(client, jobs):
    response = jobs.retrieve_application(json)
    assert 'applicant' in response
