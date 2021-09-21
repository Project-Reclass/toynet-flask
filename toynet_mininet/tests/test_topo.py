import pytest
import json
from flasksrc import create_app

@pytest.fixture
def client():
    app = create_app()
    yield app.test_client()

def test_topo_post(client):
    '''Checks the post topology functionality'''
    #clear system state
    rv = client.post(
        '/api/terminate',
        json = {
            'terminate': True,
        },
    )
    assert rv.status_code in [200, 500]

    #checks when no 'topology' is posted
    rv = client.post(
        '/api/topo',
        json = {
        },
    )
    assert rv.status_code == 400
    
    #checks when the topology provided is invalid and there is no current state
    rv = client.post(
        '/api/topo',
        json = {
            'topology': 'bad topo is bad',
        },
    )
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['message'][:28] == 'failed to parse XML topology'

    #checks when the topology provided is valid and there is no current state
    with open('sample.xml','r') as sample_topo:
        rv = client.post(
            '/api/topo',
            json = { 
                'topology': sample_topo.read(),
            },
        )
    assert rv.status_code == 200
   
    #checks when the topology provided is valid and there is a current state
    with open('sample.xml','r') as sample_topo:
        rv = client.post(
            '/api/topo',
            json = { 'topology': sample_topo.read(),},
        )
    assert rv.status_code == 200
   
    #checks when the topology provided is invalid and there is a current state
    rv = client.post(
        '/api/topo',
        json = {
            'topology': 'bad topo is bad',
        },
    )
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['message'][:28] == 'failed to parse XML topology'
