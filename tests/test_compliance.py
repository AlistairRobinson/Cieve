import pytest
import json
from flask import g, session, jsonify
from flaskr.db import get_db
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bson.objectid import ObjectId

# Checks that the privacy policy is accessible (R21)

def test_privacy_policy(client):
    assert client.get('/privacy').status_code == 200

# Checks that the database is GDPR compliant (R21)

def test_compliance(client):
    db = get_db()
    assert db.gdprCompliance()

# Checks that the database is no longer GDPR compliant if we insert old data and that old data is deleted (R21)

def test_malcompliance_insertion(client):
    db = get_db()
    db.db.application.insert_one({
        "date inputted": datetime.today() - relativedelta(months=7), 
        "applicant id":ObjectId("000000000000000000000000"), 
        "vacancy id":ObjectId("000000000000000000000000"),
        "preferred": 1,
        "specialized score": 1,
        "completed": True})
    assert not db.gdprCompliance()

# Checks that we are not able to access malcompliant data (R21)

def test_malcompliance_access(client):
    db = get_db()
    query = db.db.application.find({"date inputted": {"$lt": datetime.today() - relativedelta(months=6)}})
    assert list(query) == []