import pytest
import json
from flasksrc import create_app

@pytest.fixture
def client():
    app = create_app()
    yield app.test_client()

def test_command_post(client):
    '''test command POST functionality'''
    #clear system state
    rv = client.post(
        '/api/terminate',
        json = {
            'terminate': True,
        },
    )
    assert rv.status_code in [200, 500]

    #Post command without a defined topology
    rv = client.post(
        '/api/command',
        json = {
            'command': 'h1 ping h2',
        },
    )
    assert rv.status_code == 500
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['message'] == 'No topology defined'

    #post a topology to generate a valid state
    with open('sample.xml','r') as sample_topo:
        rv = client.post(
            '/api/topo',
            json = {
                'topology': sample_topo.read(),
            },
        )
    assert rv.status_code == 200

    #Arp without a loaded entry
    rv = client.post(
        '/api/command',
        json = {
            'command': 'h1 arp',
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['output'] == ''

    #ping between two connected hosts
    rv = client.post(
        '/api/command',
        json = {
            'command': 'h1 ping h2',
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['output'][:100] == 'PING 172.16.176.101 (172.16.176.101) 56(84) bytes of data.\r\n64 bytes from 172.16.176.101: icmp_seq=1'

    #Arp with a loaded entry
    rv = client.post(
        '/api/command',
        json = {
            'command': 'h1 arp',
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['output'][:94] == 'Address                  HWtype  HWaddress           Flags Mask            Iface\r\n172.16.160.1'
    
    #validate interface properly setup for specified host
    rv = client.post(
        '/api/command',
        json = {
            'command': 'h1 ifconfig',
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['output'].split('\r\n')[1] == '        inet 172.16.160.101  netmask 255.255.240.0  broadcast 172.16.175.255' 

    #valid host provided, command not provided
    rv = client.post(
        '/api/command',
        json = {
            'command': 'h1',
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['output'] == 'Invalid command: h1'

    #valid host, invalid command
    rv = client.post(
        '/api/command',
        json = {
            'command': 'h1 AtEase!',
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['output'] == 'bash: AtEase!: command not found\r\n'

    #some invalid command with an invalid host
    rv = client.post(
        '/api/command',
        json = {
            'command': 'h9001 AtEase!',
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['output'] == 'Invalid host: h9001'

    #ping between two non-connected hosts
    rv = client.post(
        '/api/command',
        json = {
            'command': 'h1 ping h8',
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['output'][:116] == 'PING 172.16.240.104 (172.16.240.104) 56(84) bytes of data.\r\nFrom 172.16.160.1 icmp_seq=1 Destination Net Unreachable'

    #ping between two hosts- second host invalid
    rv = client.post(
        '/api/command',
        json = {
            'command': 'h1 ping h9001',
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['output'] == 'Invalid host: h9001'
