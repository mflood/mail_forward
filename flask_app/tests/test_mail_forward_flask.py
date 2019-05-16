#import os
#import tempfile

import pytest

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

def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'ola' in rv.data
