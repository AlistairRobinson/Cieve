import pytest
import json
from flask import g, session, jsonify

# Checks that the privacy policy is accessible (R21)

def test_register(client, app):
    assert client.get('/privacy').status_code == 200