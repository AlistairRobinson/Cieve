import pytest
from flask import g, session

def test_post_vacancy(client, jobs):
    assert client.get('path/to/post/vacancy').status_code == 200