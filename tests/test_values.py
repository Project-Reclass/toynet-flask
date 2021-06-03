import os
import tempfile
import pytest
import json
import time
from flasksrc import create_app, db
from flask_jwt_extended import create_access_token


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

def test_valueById_get(client):
    """Check that values can be retrieved by ID"""

    rv = client.get('/api/value/5004/inspirations')
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['value'] == 'Loyalty'
    print(rv_json)
    assert len(rv_json['inspiration']) == 1

    inspiration = rv_json['inspiration'][0]
    assert inspiration['organization'] == 'U.S. Army'
    assert inspiration['definition'][:21] == 'Bear true faith and a'
    assert inspiration['definition'][-21:] == 'loyalty to your unit.'

    rv = client.get('/api/value/1/inspirations')

def test_valueEntryById_put(client):
    """Check that values can be retrieved by ID"""

    # create user
    rv = client.post(
        '/api/user',
        data={
            'username': 'veteran@projectreclass.org',
            'password': 'bossvet123',
            'first_name': 'Boss',
        },
    )
    assert rv.status_code == 200

    # login as user
    rv = client.post(
        '/api/login',
        data={
            'username': 'veteran@projectreclass.org',
            'password': 'bossvet123',
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['verified'] == True
    access_token = rv_json['token']

    # check that value_entries table is empty for user
    rv = client.get(
        '/api/value/5004/entry',
        headers = {'Authorization': 'Bearer {}'.format(access_token)},
    )
    assert rv.status_code == 404
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['message'][:30] == 'no entries for value 5004 for '

    # insert personal entry
    rv = client.put(
        '/api/value/5004/entry',
        data={'quote': "Integrity is honesty."},
        headers = {'Authorization': 'Bearer {}'.format(access_token)},
    )
    assert rv.status_code == 200

    # retrieve personal entry and verify text
    rv = client.get(
        '/api/value/5004/entry',
        headers = {'Authorization': 'Bearer {}'.format(access_token)},
    )
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['entry'] == "Integrity is honesty."

def test_valueEntryById_putTwice(client):
    """Check that a new entry for the same user updates the database."""

    # create user
    rv = client.post(
        '/api/user',
        data={
            'username': 'veteran@projectreclass.org',
            'password': 'bossvet123',
            'first_name': 'Boss',
        },
    )
    assert rv.status_code == 200

    # login as user
    rv = client.post(
        '/api/login',
        data={
            'username': 'veteran@projectreclass.org',
            'password': 'bossvet123',
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['verified'] == True
    access_token = rv_json['token']

    # insert personal entry
    rv = client.put(
        '/api/value/5004/entry',
        data={'quote': "Integrity is honesty."},
        headers = {'Authorization': 'Bearer {}'.format(access_token)},
    )
    assert rv.status_code == 200

    # insert new personal entry
    rv = client.put(
        '/api/value/5004/entry',
        data={'quote': "Integrity is MORE THAN honesty."},
        headers = {'Authorization': 'Bearer {}'.format(access_token)},
    )
    assert rv.status_code == 200

    # retrieve personal entry and verify change
    rv = client.get(
        '/api/value/5004/entry',
        headers = {'Authorization': 'Bearer {}'.format(access_token)},
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['entry'] == "Integrity is MORE THAN honesty."
