# This file is part of Toynet-Flask.
#
# Toynet-Flask is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Toynet-Flask is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Toynet-Flask.  If not, see <https://www.gnu.org/licenses/>.

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
    
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
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

    # Confirm host adds with CIDR default gateway
    rv = client.put(
        f'/api/toynet/session/{session_id}/create/host',
        json={
            'name': 'h20',
            'ip': '172.16.1.10/24',
            'def_gateway': '172.16.1.1/24',
            },
    )
    
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    rv = client.get(f'/api/toynet/session/{session_id}')
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['topology'][451:555] == '<host name="h20" ip="172.16.1.10/24"><defaultRouter><name>r1</name><intf>2</intf></defaultRouter></host>'

    # Confirm host with CIDR default gateway deletes
    rv = client.put(
        f'/api/toynet/session/{session_id}/delete/host',
        json={
            'name': 'h20',
            },
    )
    
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    rv = client.get(f'/api/toynet/session/{session_id}')
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['topology'][237:462] == '<hostList><host name="h1" ip="172.16.0.2/24"><defaultRouter><name>r1</name><intf>1</intf></defaultRouter></host><host name="h2" ip="172.16.1.2/24"><defaultRouter><name>r1</name><intf>2</intf></defaultRouter></host></hostList>'

    # Confirm switch adds
    rv = client.put(
        f'/api/toynet/session/{session_id}/create/switch',
        json={
            'name': 's20',
            },
    )
    
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    rv = client.get(f'/api/toynet/session/{session_id}')
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['topology'][224:245] == '<switch name="s20" />'

    # Confirm switch deletes
    rv = client.put(
        f'/api/toynet/session/{session_id}/delete/switch',
        json={
            'name': 's20',
            },
    )
    
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    rv = client.get(f'/api/toynet/session/{session_id}')
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['topology'][224:237] == '</switchList>'

    # Confirm router adds
    rv = client.put(
        f'/api/toynet/session/{session_id}/create/router',
        json={
            'name': 'r20',
            'ip': '172.16.1.10/24',
            'intfs': ['172.16.1.1/24', '192.168.2.2/24']
            },
    )
    
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 200
    rv = client.get(f'/api/toynet/session/{session_id}')
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['topology'][159:260] == '<router name="r20" ip="172.16.1.10/24"><intf>172.16.1.1/24</intf><intf>192.168.2.2/24</intf></router>'

    # Confirm router deletes
    rv = client.put(
        f'/api/toynet/session/{session_id}/delete/router',
        json={
            'name': 'r20',
            },
    )
    
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 200
    rv = client.get(f'/api/toynet/session/{session_id}')
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['topology'][159:172] == '</routerList>'

    # Confirm host does not delete if still connected
    rv = client.put(
        f'/api/toynet/session/{session_id}/delete/host',
        json={
            'name': 'h1',
            },
    )

    assert rv.status_code == 400
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['message'] == 'Device h1 is connected to another device'

    # Validate host name
    rv = client.put(
        f'/api/toynet/session/{session_id}/create/host',
        json={
            'name': 'h20 ',
            'ip': '172.16.1.10/24',
            'def_gateway': '172.16.1.1',
            },
    )
    
    assert rv.status_code == 400
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['message'] == 'Invalid hostname'

    # Teardown
    rv = client.post(
        f'/api/toynet/session/{session_id}/terminate',
    )
    assert rv.status_code == 200

# Confirms that user created links take effect in mininet, must test each
# combination of devices
def test_session_by_id_links(client):
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

    # Add two routers
    rv = client.put(
        f'/api/toynet/session/{session_id}/create/router',
        json={
            'name': 'r20',
            'ip': '172.16.1.10/24',
            'intfs': ['172.16.2.1/24', '192.168.2.1/24']
            },
    )
    assert rv.status_code == 200

    rv = client.put(
        f'/api/toynet/session/{session_id}/create/router',
        json={
            'name': 'r21',
            'ip': '172.16.1.11/24',
            'intfs': ['172.16.2.2/24', '10.10.10.10/24']
            },
    )
    assert rv.status_code == 200

    # Add a link between them
    rv = client.put(
            f'/api/toynet/session/{session_id}/create/link',
            json={
                'dev_1': 'r20',
                'dev_2': 'r21',
                },
    )
    assert rv.status_code == 200

    # Confirm link is created
    rv = client.get(f'/api/toynet/session/{session_id}')
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['topology'][664:1066] == '<linkList><link><dvc name="r1"><intf>1</intf></dvc><dvc name="s1"><intf>0</intf></dvc></link><link><dvc name="r1"><intf>2</intf></dvc><dvc name="s2"><intf>0</intf></dvc></link><link><dvc name="s1"><intf>1</intf></dvc><dvc name="h1" /></link><link><dvc name="s2"><intf>1</intf></dvc><dvc name="h2" /></link><link><dvc name="r20"><intf>0</intf></dvc><dvc name="r21"><intf>0</intf></dvc></link></linkList>'

    # Confirm they can ping now
    rv = client.post(
        f'/api/toynet/session/{session_id}',
        json={
            'toynet_command': 'r20 ping r21',
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    # Note that the hostname resolution forces the ping between the IP
    # attributes of each router rather than the connected interfaces' IPs.
    # However, the fact that they can communicate does in fact indicate that
    # the link creation succeeded
    assert rv_json['output'][:91] == 'PING 172.16.1.11 (172.16.1.11) 56(84) bytes of data.\r\n64 bytes from 172.16.1.11: icmp_seq=1'

    # Add two switches
    rv = client.put(
        f'/api/toynet/session/{session_id}/create/switch',
        json={
            'name': 's20',
            },
    )
    assert rv.status_code == 200

    rv = client.put(
        f'/api/toynet/session/{session_id}/create/switch',
        json={
            'name': 's21',
            },
    )
    assert rv.status_code == 200

    # Add a link between them
    rv = client.put(
            f'/api/toynet/session/{session_id}/create/link',
            json={
                'dev_1': 's20',
                'dev_2': 's21',
                },
    )
    assert rv.status_code == 200

    # Add two hosts
    rv = client.put(
        f'/api/toynet/session/{session_id}/create/host',
        json={
            'name': 'h20',
            'ip': '192.168.2.10/24',
            'def_gateway': '192.168.2.1',
            },
    )
    assert rv.status_code == 200

    rv = client.put(
        f'/api/toynet/session/{session_id}/create/host',
        json={
            'name': 'h21',
            'ip': '192.168.2.11/24',
            'def_gateway': '192.168.2.1',
            },
    )
    assert rv.status_code == 200

    # Link each host to a switch
    rv = client.put(
            f'/api/toynet/session/{session_id}/create/link',
            json={
                'dev_1': 'h20',
                'dev_2': 's20',
                },
    )
    assert rv.status_code == 200

    rv = client.put(
            f'/api/toynet/session/{session_id}/create/link',
            json={
                'dev_1': 'h21',
                'dev_2': 's21',
                },
    )
    assert rv.status_code == 200

    # Confirm they can ping through the switches
    rv = client.post(
        f'/api/toynet/session/{session_id}',
        json={
            'toynet_command': 'h20 ping h21',
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['output'][:94] == 'PING 192.168.2.11 (192.168.2.11) 56(84) bytes of data.\r\n64 bytes from 192.168.2.11: icmp_seq=1'

    # Connect a router and a switch
    rv = client.put(
            f'/api/toynet/session/{session_id}/create/link',
            json={
                'dev_1': 'r20',
                'dev_2': 's20',
                },
    )
    assert rv.status_code == 200

    # Confirm router and host can ping across switch
    rv = client.post(
        f'/api/toynet/session/{session_id}',
        json={
            'toynet_command': 'r20 ping h21',
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['output'][:94] == 'PING 192.168.2.11 (192.168.2.11) 56(84) bytes of data.\r\n64 bytes from 192.168.2.11: icmp_seq=1'

    # Confirm link deletes
    rv = client.put(
            f'/api/toynet/session/{session_id}/delete/link',
            json={
                'dev_1': 'r20',
                'dev_2': 'r21',
                },
    )
    assert rv.status_code == 200

    rv = client.get(f'/api/toynet/session/{session_id}')
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['topology'][918:1539] == '<linkList><link><dvc name="r1"><intf>1</intf></dvc><dvc name="s1"><intf>0</intf></dvc></link><link><dvc name="r1"><intf>2</intf></dvc><dvc name="s2"><intf>0</intf></dvc></link><link><dvc name="s1"><intf>1</intf></dvc><dvc name="h1" /></link><link><dvc name="s2"><intf>1</intf></dvc><dvc name="h2" /></link><link><dvc name="s20"><intf>0</intf></dvc><dvc name="s21"><intf>0</intf></dvc></link><link><dvc name="h20" /><dvc name="s20"><intf>1</intf></dvc></link><link><dvc name="h21" /><dvc name="s21"><intf>1</intf></dvc></link><link><dvc name="r20"><intf>1</intf></dvc><dvc name="s20"><intf>2</intf></dvc></link></linkList>'

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
