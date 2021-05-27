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
def test_topo_id_post(client):
    """Check the POST topo_id returns a session id if valid or error if not"""
    url = "/api/toynet/session"
    accept_json=[('Content-Type', 'application/json;')]

    pv = json.dumps({'toynet_topo_id': 1, 'toynet_user_id': 'abc',})
    rv = client.post(url, data = pv, headers = accept_json,) 

    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 201
    assert rv_json['status'] == True
    # check that a session id was returned

    #Invalid toynet_topo_id number
    pv = json.dumps({'toynet_topo_id': -5, 'toynet_user_id': 'abc',})
    rv = client.post(url, data = pv, headers = accept_json)
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 400
    assert rv_json['message'] == 'topo_id is invalid: -5'


    pv = json.dumps({'toynet_topo_id': 1, 'toynet_user_id': "1",})
    rv = client.post(url, data = pv, headers = accept_json)
    rv_json = json.loads(rv.data.decode('utf-8'))i
    assert rv.status_code == 400
    assert rv_json['message'] == 'user_id is invalid: 1'

def test_topo_id_by_session_id_get(client):
    url = "/api/toynet/session/"#session_id
    #200 on success
    session_id = "1"
    rv = client.get(url+session_id)
    assert rv.status_code == 500
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['message'] == "Query for session_id failed: {}".format(session_id)
