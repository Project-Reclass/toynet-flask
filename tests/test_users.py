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
        json={
            'username': 'bob@projectreclass.org',
            'password': 'bobisdabomb',
            'first_name': 'Bob',
        },
    )
    assert rv.status_code == 200

    # without first_name
    rv = client.post(
        '/api/user',
        json={
            'username': 'alice@projectreclass.org',
            'password': 'aliceisdabomb',
        },
    )
    assert rv.status_code == 200

    # missing password
    rv = client.post(
        '/api/user',
        json={'username': 'alice@projectreclass.org'},
    )
    assert rv.status_code == 422
    assert rv.data.decode('utf-8')[:30] == r'<!DOCTYPE HTML PUBLIC "-//W3C/'

def test_userLogin_post(client):
    """Check that only users with good username/password can login """

    # insert
    rv = client.post(
        '/api/user',
        json={
            'username': 'bob@projectreclass.org',
            'password': 'bobisdabomb',
            'first_name': 'Bob',
        },
    )

    assert rv.status_code == 200

    # good login attempt
    rv = client.post(
        '/api/login',
        json={
            'username': 'bob@projectreclass.org',
            'password': 'bobisdabomb',
        },
    )

    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert 'token' in rv_json and len(rv_json['token']) > 100
    assert rv_json['verified'] == True

    # bad login attempt
    rv = client.post(
        '/api/login',
        json={
            'username': 'bob@projectreclass.org',
            'password': 'bobisdabroom',
        },
    )

    assert rv.status_code == 401
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['verified'] == False

def test_jwtRequired_wrongUser(client):
    """Check that users cannot see other user data"""

    # create veteran user
    rv = client.post(
        '/api/user',
        json={
            'username': 'veteran@projectreclass.org',
            'password': 'bossvet123',
            'first_name': 'Boss',
        },
    )
    assert rv.status_code == 200

    # login as veteran user
    rv = client.post(
        '/api/login',
        json={
            'username': 'veteran@projectreclass.org',
            'password': 'bossvet123',
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    vet_access_token = rv_json['token']

    # insert personal entry as veteran user
    rv = client.put(
        '/api/value/5004/entry',
        json={'quote': "Integrity is honesty."},
        headers = {'Authorization': 'Bearer {}'.format(vet_access_token)},
    )
    assert rv.status_code == 200

    # create civilian user
    rv = client.post(
        '/api/user',
        json={
            'username': 'civilian@projectreclass.org',
            'password': 'civilboss123',
            'first_name': 'Boss',
        },
    )
    assert rv.status_code == 200

    # login as civilian user
    rv = client.post(
        '/api/login',
        json={
            'username': 'civilian@projectreclass.org',
            'password': 'civilboss123',
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    civ_access_token = rv_json['token']

    # get entry regarding value 5004 as civilian
    rv = client.get(
        '/api/value/5004/entry',
        headers = {'Authorization': 'Bearer {}'.format(civ_access_token)},
    )
    assert rv.status_code == 404
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['message'][:30] == 'no entries for value 5004 for '

def test_jwtRequired_twoActiveUsers(client):
    """Check that two different users can interact with their data in parallel"""

    # create veteran user
    rv = client.post(
        '/api/user',
        json={
            'username': 'veteran@projectreclass.org',
            'password': 'bossvet123',
            'first_name': 'Boss',
        },
    )
    assert rv.status_code == 200

    # login as veteran user
    rv = client.post(
        '/api/login',
        json={
            'username': 'veteran@projectreclass.org',
            'password': 'bossvet123',
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    vet_access_token = rv_json['token']

    # insert personal entry as veteran user
    rv = client.put(
        '/api/value/5004/entry',
        json={'quote': "I am a veteran. I have integrity."},
        headers = {'Authorization': 'Bearer {}'.format(vet_access_token)},
    )
    assert rv.status_code == 200

    # create civilian user
    rv = client.post(
        '/api/user',
        json={
            'username': 'civilian@projectreclass.org',
            'password': 'civilboss123',
            'first_name': 'Boss',
        },
    )
    assert rv.status_code == 200

    # login as civilian user
    rv = client.post(
        '/api/login',
        json={
            'username': 'civilian@projectreclass.org',
            'password': 'civilboss123',
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    civ_access_token = rv_json['token']

    # insert personal entry as civilian user
    rv = client.put(
        '/api/value/5004/entry',
        json={'quote': "I am a civilian. I have integrity."},
        headers = {'Authorization': 'Bearer {}'.format(civ_access_token)},
    )
    assert rv.status_code == 200

    # get entry regarding value 5004 as vet
    rv = client.get(
        '/api/value/5004/entry',
        headers = {'Authorization': 'Bearer {}'.format(vet_access_token)},
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['entry'] == "I am a veteran. I have integrity."

    # get entry regarding value 5004 as civilian
    rv = client.get(
        '/api/value/5004/entry',
        headers = {'Authorization': 'Bearer {}'.format(civ_access_token)},
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['entry'] == "I am a civilian. I have integrity."
