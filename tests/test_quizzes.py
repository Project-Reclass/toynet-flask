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

def test_quizById_get(client):
    """Check that quizzes can be retrieved by ID"""

    rv = client.get('/api/quiz/4002')
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))

    assert rv_json['items'][0]['question'] == 'Which Protocol do Internet Browsers (Chrome, Firefox, Internet Explorer) use?'
    assert len(rv_json['items']) == 10
    assert len(rv_json['items'][0]['options']) == 4

    assert rv_json['items'][1]['options'][0] == 'Physical'
    assert rv_json['items'][1]['answer'] == 1
    assert rv_json['items'][2]['options'][3] == 'IPP'
    assert rv_json['items'][2]['answer'] == 2

    rv = client.get('/api/quiz/2')
    assert rv.status_code == 404
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['message'] == 'quiz ID 2 doesn\'t exist'
