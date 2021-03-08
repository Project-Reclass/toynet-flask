import os
import tempfile

import pytest
import json

from flasksrc import create_app, db

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

    rv = client.post('/api/user', data={
        'username': 'bob@projectreclass.org',
        'password': 'bobisdabomb',
        'first_name': 'Bob',
    })

    assert rv.status_code == 200

    rv_json = json.loads(rv.data.decode('utf-8'))

    # without first_name

    rv = client.post('/api/user', data={
        'username': 'alice@projectreclass.org',
        'password': 'aliceisdabomb',
    })

    assert rv.status_code == 200

    rv_json_2 = json.loads(rv.data.decode('utf-8'))
    assert rv_json['user_id'] != rv_json_2['user_id']

    # missing password

    rv = client.post('/api/user', data={
        'username': 'alice@projectreclass.org',
    })

    assert rv.status_code == 400
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['message'][:30] == "malformed create user request:"

def test_userByUsername_get(client):
    """Check users can be retrieved by username"""

    # insert

    rv = client.post('/api/user', data={
        'password': 'bobisdabomb',
        'username': 'bob@projectreclass.org',
        'first_name': 'Bob',
    })

    assert rv.status_code == 200

    rv_json = json.loads(rv.data.decode('utf-8'))
    unique_id = rv_json['user_id']

    # retrieve

    rv = client.get('/api/username', data= {'username': 'bob@projectreclass.org'})

    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))

    assert rv_json['username'] == 'bob@projectreclass.org'
    assert rv_json['id'] == unique_id
    assert rv_json['first_name'] == 'Bob'

    # bad data

    bad_get_data = {
        'username': 'tay@projectreclass.org',
    }

    rv = client.get('/api/username', data=bad_get_data)
    assert rv.status_code == 404
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['message'] == "no user exists with username: tay@projectreclass.org"

def test_userLogin_post(client):
    """Check users login vets password correctly"""

    # insert

    rv = client.post('/api/user', data={
        'username': 'bob@projectreclass.org',
        'password': 'bobisdabomb',
        'first_name': 'Bob',
    })

    assert rv.status_code == 200

    # good login attempt

    rv = client.post('/api/login', data={
        'username': 'bob@projectreclass.org',
        'password': 'bobisdabomb',
    })

    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))

    assert rv_json['verified'] == True

    # bad login attempt

    rv = client.post('/api/login', data={
        'username': 'bob@projectreclass.org',
        'password': 'bobisdabroom',
    })

    assert rv.status_code == 401
    rv_json = json.loads(rv.data.decode('utf-8'))

    assert rv_json['verified'] == False
