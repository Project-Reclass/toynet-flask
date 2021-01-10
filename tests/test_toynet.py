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

def test_hello_reclass(client):
    """Check the app is running"""

    rv = client.get('/')
    assert b'Hello, Reclass!' in rv.data

def test_value_get(client):
    """Check the app is running"""

    rv = client.get('/values/5004')
    rv_json = json.loads(rv.data.decode('utf-8'))

    assert rv_json['value'] == 'Loyalty'
    assert len(rv_json['inspiration']) == 1

    inspiration = rv_json['inspiration'][0]
    assert inspiration['organization'] == 'U.S. Army'
    assert inspiration['definition'][:21] == 'Bear true faith and a'
    assert inspiration['definition'][-21:] == 'loyalty to your unit.'