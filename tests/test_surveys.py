import os
import tempfile
import pytest
import json
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

def test_surveyById_get(client):
    """Check that surveys can be retrieved by ID"""

    rv = client.get('/api/survey/6001')
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))

    assert rv_json['items'][0]['question'] == 'What is your first name?'
    assert len(rv_json['items']) == 7
    assert len(rv_json['items'][1]['options']) == 4

    assert rv_json['items'][1]['options'][0] == 'As of now, I don\'t plan on it.'
    assert rv_json['items'][3]['options'][4] == 'Professional Experience'
    assert rv_json['items'][6]['unit'] == 'months'

    rv = client.get('/api/survey/4')
    assert rv.status_code == 404
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['message'] == 'survey ID 4 doesn\'t exist'
