import os
import pytest
from flaskr import create_app, csrf

# This is the test config. It contains the application definition as well as class definitions for each individual test.

# Defines the testing application
@pytest.fixture 
def app():

    app = create_app({
        'TESTING': True
    })

    yield app

# Allows the creation of a test client
@pytest.fixture
def client(app):
    return app.test_client()

# Allows the creation of a test client runner
@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# Encapsulates functions used to test authentication
class AuthActions(object):

    # Set up a virtual client to store session variables
    def __init__(self, client):
        self._client = client

    # Log into a client account
    def login_cli(self, username='test', password='test'):
        token = csrf.generate_csrf_token_with_session(self._client)
        return self._client.post(
            '/cli/auth/login',
            data={'username': username, 'password': password, '_csrf_token': token}
        )

    # Log into an applicant account
    def login_apl(self, username='test', password='test'):
        token = csrf.generate_csrf_token_with_session(self._client)
        return self._client.post(
            '/apl/auth/login',
            data={'username': username, 'password': password, '_csrf_token': token}
        )

    # Register an applicant account
    def register(self, username='test', password='test'):
        token = csrf.generate_csrf_token_with_session(self._client)
        return self._client.post(
            'apl/auth/register',
            data={'username': username, 'password': password, '_csrf_token': token}
        ) 

    # Log out a user by clearing session
    def logout(self):
        return self._client.get('/auth/logout')

# Returns an authentication test object
@pytest.fixture
def auth(client):
    return AuthActions(client)

# Encapsulates functions used to test jobs and applications
class JobActions(object):

    # Set up a virtual client to store session variables
    def __init__(self, client):
        self._client = client

    # Post a vacancy to the database
    def post_vacancy(self, vacancy):
        token = csrf.generate_csrf_token_with_session(self._client)
        return self._client.post(
            '/cli/newjob', # TODO
            data={
                # TODO
                '_csrf_token': token
            }
        )
    
    # Post an application to a vacancy
    def apply_to_vacancy(self, application):
        token = csrf.generate_csrf_token_with_session(self._client)
        return self._client.post(
            '/apl/apply', # TODO
            data={
                # TODO
                '_csrf_token': token
            }
        )

    # Retrieve an application from the database
    def retrieve_application(self, info):
        token = csrf.generate_csrf_token_with_session(self._client)
        return self._client.post(
            '/cli/applications', # TODO
            data={
                # TODO
                '_csrf_token': token
            }
        )

    # Retrieve a vacancy from the database
    def get_vacancies(self, info):
        token = csrf.generate_csrf_token_with_session(self._client)
        return self._client.post(
            '/apl/vacancies', # TODO
            data={
                # TODO
                '_csrf_token': token
            }
        )

# Returns a job test object
@pytest.fixture
def jobs(client):
    return JobActions(client)