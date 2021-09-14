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


def test_quizScore_post(client):
    # create user
    rv = client.post(
        '/api/user',
        json={
            'username': 'vet@projectreclass.org',
            'password': 'yayvets123$',
            'first_name': 'Jeff'
        })
    
    assert rv.status_code == 200

    # login as user
    rv = client.post(
        '/api/login',
        json={
            'username': 'vet@projectreclass.org',
            'password': 'yayvets123$'
        }
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['verified'] == True
    access_token = rv_json['token']

    # insert new submission
    rv = client.post(
        '/api/quizscore',
        json={
            'quiz_id': 4001,
            'count_correct': 5,
            'count_wrong': 3
        },
        headers={'Authorization': 'Bearer {}'.format(access_token)}
    )
    assert rv.status_code == 201
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['submission_id'] == 1

    # insert new submission to verify that submission_id is incrementing
    rv = client.post(
        '/api/quizscore',
        json={
            'quiz_id': 4001,
            'count_correct': 1,
            'count_wrong': 7
        },
        headers={'Authorization': 'Bearer {}'.format(access_token)}
    )
    assert rv.status_code == 201
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['submission_id'] == 2

    # create new user 
    rv = client.post(
        '/api/user',
        json={
            'username': 'tay@projectreclass.org',
            'password': 'rootbeer123$',
            'first_name': 'Tay'
        })
    
    assert rv.status_code == 200

    # login as user
    rv = client.post(
        '/api/login',
        json={
            'username': 'tay@projectreclass.org',
            'password': 'rootbeer123$'
        }
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['verified'] == True
    access_token = rv_json['token']

    # insert new submission
    rv = client.post(
        '/api/quizscore',
        json={
            'quiz_id': 4001,
            'count_correct': 1,
            'count_wrong': 7
        },
        headers={'Authorization': 'Bearer {}'.format(access_token)}
    )
    assert rv.status_code == 201
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['submission_id'] == 3

    rv = client.post(
        '/api/quizscore',
        json={
            'quiz_id': 4001,
            'count_correct': 8,
            'count_wrong': 0
        },
        headers={'Authorization': 'Bearer {}'.format(access_token)}
    )
    assert rv.status_code == 201
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['submission_id'] == 4

def test_quizScoreByUser_get(client):
    # create user
    rv = client.post(
        '/api/user',
        json={
            'username': 'vet@projectreclass.org',
            'password': 'yayvets123$',
            'first_name': 'Jeff'
        })
    
    assert rv.status_code == 200

    # login as user
    rv = client.post(
        '/api/login',
        json={
            'username': 'vet@projectreclass.org',
            'password': 'yayvets123$'
        }
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['verified'] == True
    access_token = rv_json['token']

    # insert new submission
    rv = client.post(
        '/api/quizscore',
        json={
            'quiz_id': 4001,
            'count_correct': 5,
            'count_wrong': 3
        },
        headers={'Authorization': 'Bearer {}'.format(access_token)}
    )
    assert rv.status_code == 201
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['submission_id'] == 1

    # insert new submission to verify that submission_id is incrementing
    rv = client.post(
        '/api/quizscore',
        json={
            'quiz_id': 4001,
            'count_correct': 1,
            'count_wrong': 7
        },
        headers={'Authorization': 'Bearer {}'.format(access_token)}
    )
    assert rv.status_code == 201
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['submission_id'] == 2

    # create new user 
    rv = client.post(
        '/api/user',
        json={
            'username': 'tay@projectreclass.org',
            'password': 'rootbeer123$',
            'first_name': 'Tay'
        })
    
    assert rv.status_code == 200

    # login as user
    rv = client.post(
        '/api/login',
        json={
            'username': 'tay@projectreclass.org',
            'password': 'rootbeer123$'
        }
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['verified'] == True
    access_token = rv_json['token']

    # insert new submission
    rv = client.post(
        '/api/quizscore',
        json={
            'quiz_id': 4001,
            'count_correct': 1,
            'count_wrong': 7
        },
        headers={'Authorization': 'Bearer {}'.format(access_token)}
    )
    assert rv.status_code == 201
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['submission_id'] == 3

    rv = client.post(
        '/api/quizscore',
        json={
            'quiz_id': 4001,
            'count_correct': 8,
            'count_wrong': 0
        },
        headers={'Authorization': 'Bearer {}'.format(access_token)}
    )
    assert rv.status_code == 201
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['submission_id'] == 4

    # login as user
    rv = client.post(
        '/api/login',
        json={
            'username': 'vet@projectreclass.org',
            'password': 'yayvets123$'
        }
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['verified'] == True
    access_token = rv_json['token']

    # insert new submission
    rv = client.post(
        '/api/quizscore',
        json={
            'quiz_id': 4002,
            'count_correct': 2,
            'count_wrong': 8
        },
        headers={'Authorization': 'Bearer {}'.format(access_token)}
    )
    assert rv.status_code == 201
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['submission_id'] == 5

    # insert new submission
    rv = client.post(
        '/api/quizscore',
        json={
            'quiz_id': 4002,
            'count_correct': 4,
            'count_wrong': 6
        },
        headers={'Authorization': 'Bearer {}'.format(access_token)}
    )
    assert rv.status_code == 201
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['submission_id'] == 6

    # insert new submission
    rv = client.post(
        '/api/quizscore',
        json={
            'quiz_id': 4003,
            'count_correct': 3,
            'count_wrong': 4
        },
        headers={'Authorization': 'Bearer {}'.format(access_token)}
    )
    assert rv.status_code == 201
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['submission_id'] == 7

    # login as user
    rv = client.post(
        '/api/login',
        json={
            'username': 'tay@projectreclass.org',
            'password': 'rootbeer123$'
        }
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['verified'] == True
    access_token = rv_json['token']

    # insert new submission
    rv = client.post(
        '/api/quizscore',
        json={
            'quiz_id': 4002,
            'count_correct': 1,
            'count_wrong': 9
        },
        headers={'Authorization': 'Bearer {}'.format(access_token)}
    )
    assert rv.status_code == 201
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['submission_id'] == 8

    rv = client.post(
        '/api/quizscore',
        json={
            'quiz_id': 4002,
            'count_correct': 7,
            'count_wrong': 3
        },
        headers={'Authorization': 'Bearer {}'.format(access_token)}
    )
    assert rv.status_code == 201
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['submission_id'] == 9

    rv = client.post(
        '/api/quizscore',
        json={
            'quiz_id': 4003,
            'count_correct': 5,
            'count_wrong': 2
        },
        headers={'Authorization': 'Bearer {}'.format(access_token)}
    )
    assert rv.status_code == 201
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['submission_id'] == 10

    # get tay@projectreclass quizscores
    rv = client.get(
        '/api/quizscores',
        headers={'Authorization': 'Bearer {}'.format(access_token)}
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    print(rv_json)
    assert len(rv_json['scores'][0]['scores']) == 2
    assert len(rv_json['scores'][1]['scores']) == 2
    assert len(rv_json['scores'][2]['scores']) == 1

    # login as user
    rv = client.post(
        '/api/login',
        json={
            'username': 'vet@projectreclass.org',
            'password': 'yayvets123$'
        }
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['verified'] == True
    access_token = rv_json['token']

    # get vet@projectreclass quizscores
    rv = client.get(
        '/api/quizscores',
        headers={'Authorization': 'Bearer {}'.format(access_token)}
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    print(rv_json)
    assert len(rv_json['scores'][0]['scores']) == 2
    assert len(rv_json['scores'][1]['scores']) == 2
    assert len(rv_json['scores'][2]['scores']) == 1
    