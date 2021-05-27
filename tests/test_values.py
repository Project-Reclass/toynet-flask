import os
import tempfile

import pytest
import json

from flasksrc import create_app, db
from flask_jwt_extended import create_access_token

import time

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
    assert len(rv_json['inspiration']) == 1

    inspiration = rv_json['inspiration'][0]
    assert inspiration['organization'] == 'U.S. Army'
    assert inspiration['definition'][:21] == 'Bear true faith and a'
    assert inspiration['definition'][-21:] == 'loyalty to your unit.'

    rv = client.get('/api/value/1/inspirations')
    assert rv.status_code == 404
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['message'] == 'value ID 1 does not exist'

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

    # login using user
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

    # get all entries regarding value 5004, Integrity
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

def test_valueEntryById_putTwice(client):
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

    # login using user
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
