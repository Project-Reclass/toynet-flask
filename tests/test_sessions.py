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
    '''Check the POST topo_id returns a session id if valid or error if not'''
    client.post(
          '/api/user',
          json={
              'username': 'arthur@projectreclass.org',
              'password': 'BaLtH@$0R',
              'first_name': 'Arthur',
          },
    )

    rv = client.post(
        '/api/toynet/session',
        json={
            'toynet_topo_id': 1,
            'toynet_user_id': 'arthur@projectreclass.org',
        },
    ) 

    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 201
    # check that a session id was returned
    assert type(rv_json['toynet_session_id']) == int
    terminate_session_id=rv_json['toynet_session_id']

    #Invalid toynet_topo_id number
    rv = client.post(
        '/api/toynet/session',
        json={
            'toynet_topo_id': -5,
            'toynet_user_id': 'arthur@projectreclass.org',
        },
    )
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 400
    assert rv_json['message'] == 'topo_id is invalid: -5'

    #invalid user id
    rv = client.post(
        '/api/toynet/session',
        json={
            'toynet_topo_id': 1,
            'toynet_user_id': 'loser@projectreclass.org', #this should produce an error because we have no losers. #facts
        },
    )
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 400
    assert rv_json['message'] == 'user_id is invalid: loser@projectreclass.org'

    
    rv = client.post(
        '/api/toynet/session/'+str(terminate_session_id)+'/terminate',
    )
    assert rv.status_code == 200
    

def test_session_by_id_get(client):
    session_id = '1'
    url = '/api/toynet/session/' + session_id 

    rv = client.get(url)
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    '''expected rv_json output
    {
        'topo_id': <int>,
        'topology': <XML?>,
        'user_id': <str>,
    }
    '''
    assert rv_json['topo_id'] == 1
    assert rv_json['topology'][:63] == r'<?xml version="1.0" encoding="UTF-8"?><topology><root>r1</root>'
    assert rv_json['user_id'] == '0'

    rv = client.post(
        f'/api/toynet/session/{session_id}/terminate',
    )
    assert rv.status_code == 200

def test_session_by_id_put(client):
    # Establish session
    client.post(
          '/api/user',
          json={
              'username': 'arthur@projectreclass.org',
              'password': 'BaLtH@$0R',
              'first_name': 'Arthur',
          },
    )

    rv = client.post(
        '/api/toynet/session',
        json={
            'toynet_topo_id': 1,
            'toynet_user_id': 'arthur@projectreclass.org',
        },
    ) 
    assert rv.status_code == 201
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['running'] == True
    # Save session id
    session_id = rv_json['toynet_session_id']

    # Confirm host adds
    rv = client.put(
        f'/api/toynet/session/{session_id}/create/host',
        json={
            'name': 'h20',
            'ip': '172.16.1.10/24',
            'def_gateway': '172.16.1.1',
            },
    )
    
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 200
    rv = client.get(f'/api/toynet/session/{session_id}')
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['topology'][451:555] == '<host name="h20" ip="172.16.1.10/24"><defaultRouter><name>r1</name><intf>2</intf></defaultRouter></host>'

    # Confirm host deletes
    rv = client.put(
        f'/api/toynet/session/{session_id}/delete/host',
        json={
            'name': 'h20',
            },
    )
    
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 200
    rv = client.get(f'/api/toynet/session/{session_id}')
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['topology'][237:462] == '<hostList><host name="h1" ip="172.16.0.2/24"><defaultRouter><name>r1</name><intf>1</intf></defaultRouter></host><host name="h2" ip="172.16.1.2/24"><defaultRouter><name>r1</name><intf>2</intf></defaultRouter></host></hostList>'

    # Teardown
    rv = client.post(
        f'/api/toynet/session/{session_id}/terminate',
    )
    assert rv.status_code == 200

#the /api/toynet/session/<id>:POST endpoint sends a toynet_command to the
#corresponding session's MiniFlask /api/toynet/command:POST endpoint
def test_session_by_id_post(client):
    #establish session
    url = '/api/toynet/session' 
    client.post(
          '/api/user',
          json={
              'username': 'arthur@projectreclass.org',
              'password': 'BaLtH@$0R',
              'first_name': 'Arthur',
          },
    )

    rv = client.post(
        url,
        json={
            'toynet_topo_id': 1,
            'toynet_user_id': 'arthur@projectreclass.org',
        },
    ) 
    assert rv.status_code == 201
    rv_json = json.loads(rv.data.decode('utf-8'))
    session_id = rv_json['toynet_session_id']
    assert rv_json['running'] == True

    #valid request
    rv = client.post(
        '/api/toynet/session/'+str(session_id),
        json={'toynet_command': 'h1 arp',},
    )
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 200

    #invalid request
    rv = client.post(
        url+'/'+str(session_id),
    )
    assert rv.status_code == 400

    rv = client.post(
        url+'/10',
        json={'toynet_command': 'h1 ping h2',},
    )
    assert rv.status_code == 500

    #terminate session
    rv = client.post(
        url+'/'+str(session_id)+'/terminate',
    )
    assert rv.status_code == 200
