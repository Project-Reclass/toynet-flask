import os
import tempfile

import pytest
import json

from flasksrc import create_app, db
from base64 import b64encode

@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()

    with app.test_client() as client:
        with app.app_context():
            db.init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_user_post(client):
    """Check users can be added"""

    # with first_name

    rv = client.post(
        '/api/user',
        data={
            'username': 'bob@projectreclass.org',
            'password': 'bobisdabomb',
            'first_name': 'Bob',
        },
    )

    assert rv.status_code == 200

    rv_json = json.loads(rv.data.decode('utf-8'))

    # without first_name

    rv = client.post(
        '/api/user',
        data={
            'username': 'alice@projectreclass.org',
            'password': 'aliceisdabomb',
        },
    )

    assert rv.status_code == 200

    # missing password

    rv = client.post(
        '/api/user',
        data={'username': 'alice@projectreclass.org'},
    )

    assert rv.status_code == 400
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['message'][:30] == 'malformed create user request:'

def test_userLogin_post(client):
    """Check users login vets password correctly"""

    # insert

    rv = client.post(
        '/api/user',
        data={
            'username': 'bob@projectreclass.org',
            'password': 'bobisdabomb',
            'first_name': 'Bob',
        },
    )

    assert rv.status_code == 200

    # good login attempt
  
    rv = client.post(
        '/api/login',
        data={
            'username': 'bob@projectreclass.org',
            'password': 'bobisdabomb',
        },
    )

    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))

    assert rv_json['verified'] == True

    # bad login attempt

    rv = client.post(
        '/api/login',
        data={
            'username': 'bob@projectreclass.org',
            'password': 'bobisdabroom',
        },
    )

    assert rv.status_code == 401
    rv_json = json.loads(rv.data.decode('utf-8'))

    assert rv_json['verified'] == False
