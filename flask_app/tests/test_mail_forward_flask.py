#import os
#import tempfile

import pytest
import json

import mail_forward_flask

@pytest.fixture
def client():
    #    db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    #    flaskr.app.config['TESTING'] = Truedd
    client = mail_forward_flask.app.test_client()

    #with flaskr.app.app_context():
    #    flaskr.init_db()

    yield client

    #os.close(db_fd)
    #os.unlink(flaskr.app.config['DATABASE'])

def test_home_page(client):
    """
        Test that we're getting the index.html template
    """
    rv = client.get('/')
    assert b'ola' in rv.data

def test_email_post_json(client):
    """
        Test happy path /email
    """
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'to': "bob@example.com",
        'to_name': "bob",
        'from': "fancy@example.com",
        'from_name': "fancy",
        'subject': "A Subject.",
        'body': "A message.",
    }

    response = client.post("/email" , json=json.dumps(data), headers=headers)

    assert response.json["status"] == "ok"
    assert response.json["provider"] == "noop"

def test_email_post_text(client):
    """
        Test happy path /email
    """
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'to': "bob@example.com",
        'to_name': "bob",
        'from': "fancy@example.com",
        'from_name': "fancy",
        'subject': "A Subject.",
        'body': "A message.",
    }

    response = client.post("/email" , data=json.dumps(data), headers=headers)

    assert response.json["status"] == "ok"
    assert response.json["provider"] == "noop"

def test_email_post_bad_json(client):
    """
        Test happy missing fields
    """
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'to': "bob@example.com",
        'from_name': "fancy",
        'subject': "A Subject.",
        'body': "A message.",
    }

    response = client.post("/email" , json=json.dumps(data), headers=headers)

    assert response.json["status"] == "error"
