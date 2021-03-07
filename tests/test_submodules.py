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

def test_valueById_get(client):
    """Check that values can be retrieved by ID"""

    rv = client.get('/api/value/5004')
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))

    assert rv_json['value'] == 'Loyalty'
    assert len(rv_json['inspiration']) == 1

    inspiration = rv_json['inspiration'][0]
    assert inspiration['organization'] == 'U.S. Army'
    assert inspiration['definition'][:21] == 'Bear true faith and a'
    assert inspiration['definition'][-21:] == 'loyalty to your unit.'

    rv = client.get('/api/value/1')
    assert rv.status_code == 404
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['message'] == 'value ID 1 does not exist'

def test_quizById_get(client):
    """Check that quizzes can be retrieved by ID"""

    rv = client.get('/api/quiz/4002')
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))

    assert rv_json[0]["question"] == 'Which Protocol do Internet Browsers (Chrome, Firefox, Internet Explorer) use?'
    assert len(rv_json) == 10
    assert len(rv_json[0]['options']) == 4

    assert rv_json[1]["options"][0] == "Physical"
    assert rv_json[1]["answer"] == 1
    assert rv_json[2]["options"][3] == "IPP"
    assert rv_json[2]["answer"] == 2

    rv = client.get('/api/quiz/2')
    assert rv.status_code == 404
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['message'] == 'quiz ID 2 doesn\'t exist'

def test_surveyById_get(client):
    """Check that surveys can be retrieved by ID"""

    rv = client.get('/api/survey/6001')
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))

    assert rv_json[0]["question"] == 'What is your first name?'
    assert len(rv_json) == 7
    assert len(rv_json[1]['options']) == 4

    assert rv_json[1]["options"][0] == "As of now, I don't plan on it."
    assert rv_json[3]["options"][4] == "Professional Experience"
    assert rv_json[6]["unit"] == "months"

    rv = client.get('/api/survey/4')
    assert rv.status_code == 404
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['message'] == 'survey ID 4 doesn\'t exist'
