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

import pytest
import json
from flasksrc import create_app

@pytest.fixture
def client():
    app = create_app()
    yield app.test_client()

def test_terminate_post(client):
    '''test terminate POST functionality'''
    #clear system state
    rv = client.post(
        '/api/terminate',
        json = {
            'terminate': True,
        },
    )
    assert rv.status_code in [200, 500]

    #empty, i.e. terminate not specified
    rv = client.post(
        '/api/terminate',
        json = {
        },
    )
    assert rv.status_code == 400
    
    #validate the post terminate:True does not terminate if state is None
    rv = client.post(
        '/api/terminate',
        json = {
            'terminate': True,
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['terminated'] == False

    #validate the post terminate:False succeeds if state is None
    rv = client.post(
        '/api/terminate',
        json = {
            'terminate': False,
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['terminated'] == False

    #create state
    with open('sample.xml','r') as sample_topo:
        rv = client.post(
            '/api/topo',
            json = { 
                'topology': sample_topo.read(),
            },
        )
    assert rv.status_code == 200

    #validate the post terminate:False succeeds if state is not None
    rv = client.post(
        '/api/terminate',
        json = {
            'terminate': False,
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['terminated'] == False

    #validate the post terminate:True succeeds if state is not None (should still be set after previous test)
    rv = client.post(
        '/api/terminate',
        json = {
            'terminate': True,
        },
    )
    assert rv.status_code == 200
    rv_json = json.loads(rv.data.decode('utf-8'))
    assert rv_json['terminated'] == True
