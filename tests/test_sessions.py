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
    client.post(
          '/api/user',
          data={
              'username': 'Arthur@projectreclass.org',
              'password': 'BaLtH@$0R',
              'first_name': 'Arthur',
          },
    )
    url = "/api/toynet/session"

    pv = ({'toynet_topo_id': 1, 'toynet_user_id': 'Arthur@projectreclass.org',})
    rv = client.post(url, data = pv,) 

    rv_json = json.loads(rv.data.decode('utf-8'))
    #print(rv_json['message'])
    assert rv.status_code == 201
    assert rv_json['status'] == True
    # check that a session id was returned
    assert type(rv_json['toynet_session_id']) == int

    #Invalid toynet_topo_id number
    pv = ({'toynet_topo_id': -5, 'toynet_user_id': 'Arthur@projectreclass.org',})
    rv = client.post(url, data = pv,)
    rv_json = json.loads(rv.data.decode('utf-8'))
    print(rv_json['message'])
    assert rv.status_code == 400
    assert rv_json['message'] == 'topo_id is invalid: -5'

    #invalid user id
    pv = ({'toynet_topo_id': 1, 'toynet_user_id': "Loser@projectreclass.org",}) #this should produce an error because we have no losers. #facts
    rv = client.post(url, data = pv,)
    rv_json = json.loads(rv.data.decode('utf-8'))
    print(rv_json['message'])
    assert rv.status_code == 400
    assert rv_json['message'] == 'user_id is invalid: Loser@projectreclass.org'

def test_session_by_id_get(client):
    url = "/api/toynet/session/"#session_id
    #200 on success
    session_id = "1"
    rv = client.get(url+session_id)
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    '''expected rv_json output
    {
        'topo_id': <int>,
        'topology': <XML?>,
        'user_id': <str>,
    }
    '''
    print(rv_json)
    assert rv_json['topo_id'] == 1
    assert rv_json['topology'][:67] == r'<?xml version=\"1.0\" encoding=\"UTF-8\"?><topology><root>r0</root>'
    assert rv_json['user_id'] == '0'
