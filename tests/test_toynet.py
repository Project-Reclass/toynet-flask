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

def test_user_post(client):
    """Check users can be added"""

    assert True

def test_userByUsername_get(client):
    """Check users can be retrieved by username"""

    assert True

