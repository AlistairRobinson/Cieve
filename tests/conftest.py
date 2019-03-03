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
                'job_title': vacancy['job_title'],
                'division': vacancy['division'],
                'roles': vacancy['roles'],
                'country': vacancy['country'],
                'job_desc': vacancy['job_desc'],
                'numVacancies': vacancy['numVacancies'],
                'Stage_Description': vacancy['Stage_Description'],
                'skill': vacancy['skill'],
                'skillVal': vacancy['skillVal'],
                'lang': vacancy['lang'],
                'langVal': vacancy['langVal'],
                'start_date': vacancy['start_date'],
                'min_degree_level': vacancy['min_degree_level'],
                'preferred_degrees': vacancy['preferred_degrees'],
                'asap': vacancy['asap'],
                '_csrf_token': token
            }
        )
    
    # Post an application to a vacancy
    def apply_to_vacancy(self, application):
        token = csrf.generate_csrf_token_with_session(self._client)
        return self._client.post(
            '/apl/newapplication',
            data={
                'Phone_Number': application['Phone_Number'],
                'Address': application['Address'],
                'Degree_Qualification': application['Degree_Qualification'],
                'Degree_Level': application['Degree_Level'],
                'University_Attended': application['University_Attended'],
                'a_levels[0][]': application['a_levels[0][]'],
                'Employment_History[0][]': application['Employment_History[0][]'],
                'Languages[0][]': application['Languages[0][]'],
                'Skills[0][]': application['Skills[0][]'],
                'Selected_Jobs[]': application['Selected_Jobs[]'],
                'Consider_for_other_roles': application['Consider_for_other_roles'],
                'Cover_Letter': application['Cover_Letter'],
                'Interesting_Facts': application['Interesting_Facts'],
                '_csrf_token': token
            }
        )

    # Retrieve a vacancy from the database
    def get_vacancies(self, info):
        token = csrf.generate_csrf_token_with_session(self._client)
        return self._client.post(
            '/getJobs',
            data={
                'page': info['page'],
                'division': info['division'],
                'role': info['role'],
                'location': info['location'],
                '_csrf_token': token
            }
        )

# Returns a job test object
@pytest.fixture
def jobs(client):
    return JobActions(client)

class PageActions:

     # Set up a virtual client to store session variables
    def __init__(self, client):
        self._client = client

# Returns a page test object
@pytest.fixture
def page(client):
    return AuthActions(client)
