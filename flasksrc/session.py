from marshmallow import Schema, fields, ValidationError
from flask_restful import abort
from flask_apispec import marshal_with, MethodResource, use_kwargs
from flasksrc.db import get_db

from xml.etree import ElementTree as ET
from flasksrc.emulator.commandParser import parseModificationCommand
from toynet_mininet.toynet_manager import ToynetManager
import requests
import time
import os
import sys

MINI_FLASK_PORT=os.environ['MINI_FLASK_PORT']

# Schema definitions
class ToyNetSessionPostReq(Schema):
    toynet_topo_id = fields.Int()
    toynet_user_id = fields.Str()


class ToyNetSessionPostResp(Schema):
    toynet_session_id = fields.Int()
    running = fields.Bool()


class ToyNetSessionByIdGetResp(Schema):
    topo_id = fields.Int()
    user_id = fields.Str()
    topology = fields.Str()
    running = fields.Bool()


class ToyNetSessionByIdPutReq(Schema):
    command = fields.Str(required=True)


class ToyNetSessionByIdPostReq(Schema):
    toynet_command = fields.Str()


class ToyNetSessionByIdPostResp(Schema):
    output = fields.Str()


# Hack to maintain docker container tracking state across requests, should not
# be an issue at this scale, contains a ToynetManager instance
# This class contains:
#   manager: ToynetManager object
#   containers: dict[session_id - int]: name of Docker Container object - str
class State():
    manager = ToynetManager()
    dev_status = os.environ['FLASK_ENV'] == 'development'
    if not manager.import_image(dev_status, os.environ['TOYNET_IMAGE_TAG']):
        print('Failed to import image: {}'.format(os.environ['TOYNET_IMAGE_TAG']), file=sys.stderr)
        sys.exit(1)
    containers = dict()
            
    @staticmethod
    def getDevStatus():
        return State.dev_status

    @staticmethod
    def getManager():
        return State.manager

    @staticmethod
    def getContainer(session):
        if session in State.containers:
            return State.manager.running_containers[State.containers[session]]
        else:
            return None

    @staticmethod
    def setContainer(session, container):
        State.containers[session] = container

    @staticmethod
    def delContainer(session):
        if session in State.containers:
            State.manager.kill_container(State.containers[session])
            del State.containers[session]


class ToyNetSession(MethodResource):
    @use_kwargs(ToyNetSessionPostReq)
    @marshal_with(ToyNetSessionPostResp)
    def post(self, **kwargs):
        try:
            req = ToyNetSessionPostReq().load(kwargs)
        except ValidationError as e:
            abort(400, message=f'malformed request: {e.messages}')

        toynet_topo_id = req['toynet_topo_id']
        toynet_user_id = req['toynet_user_id']

        db = get_db()

        try:
            topo_rows = db.execute(
                'SELECT topology'
                ' FROM toynet_topos'
                ' WHERE topo_id = (?)',
                (str(toynet_topo_id),)
            ).fetchall()
        except Exception as e:
            print(e.args[0])
            abort(500, message='topo_id query failed: {}'.format(toynet_topo_id))

        if not len(topo_rows):
            abort(400, message='topo_id is invalid: {}'.format(toynet_topo_id))

        try:
            user_rows = db.execute(
                'SELECT username'
                ' FROM users'
                ' WHERE username = (?)',
                (str(toynet_user_id),)
            ).fetchall()
        except Exception as e:
            print(e.args[0])
            abort(500, message='user_id query failed: {}'.format(toynet_user_id))

        if not len(user_rows):
            abort(400, message='user_id is invalid: {}'.format(toynet_user_id))

        try:
            cur = db.cursor()
            cur.execute(
                'INSERT INTO toynet_sessions(topo_id, topology, user_id)'
                ' VALUES(?,?,?)',
                (str(toynet_topo_id), topo_rows[0]['topology'], toynet_user_id,)
            )
            db.commit()
            session_id = cur.lastrowid
        except Exception as e:
            abort(500, message='Failed to create new session')
        
        manager = State.getManager()
        running = True

        if manager.check_cpu_availability and manager.check_memory_availability:
            name = manager.run_mininet_container(dev=State.getDevStatus())
            State.setContainer(session_id, name)
            container = State.getContainer(session_id)
            counter = 500
            #wait for container to 'come up' so that we can post the topology to it
            container.reload()
            while not container.attrs['State']['Running'] and counter > 0:
                time.sleep(10)
                counter-=1 #counter intuitive?
                container.reload()
            if counter == 0:
                State.delContainer(toynet_session_id)
                running = False
            else:
                ip = container.attrs['NetworkSettings']['IPAddress']
                args = {'topology': topo_rows[0]['topology']}
                res_code = 404
                while res_code != 200:
                    try:
                        res_code = requests.get('http://'+ip+':'+MINI_FLASK_PORT+'/').status_code 
                    except:
                        time.sleep(10)
                res = requests.post('http://' + ip + ':' + MINI_FLASK_PORT + '/api/topo', json = args)
                if res.status_code != 200:
                    running=False
                    print(res.status_code)
                    for item in res.__dict__.keys():
                        print(item, res.__dict__[item])
                    
        else:
            running = False

        return {
            'toynet_session_id': session_id,
            'running': running,
            }, 201


class ToyNetSessionById(MethodResource):
    def getTopologyFromDb(self, db, toynet_session_id):
        try:
            rows = db.execute(
                'SELECT topo_id, topology, user_id'
                ' FROM toynet_sessions'
                ' WHERE session_id = (?)',
                (str(toynet_session_id),)
            ).fetchall()
        except Exception as e:
            print(e.args[0])
            abort(500, message='Query for session_id failed: {}'.format(toynet_session_id))

        if not len(rows):
            abort(400, message='session_id {} does not exist'.format(toynet_session_id))

        return rows[0]

    @marshal_with(ToyNetSessionByIdGetResp)
    def get(self, toynet_session_id):
        db = get_db()

        sessionInfo = self.getTopologyFromDb(db, toynet_session_id)
        container = State.getContainer(toynet_session_id)
        manager = State.getManager()
        running = True
        if container is None:
            if manager.check_cpu_availability and manager.check_memory_availability:
                name = manager.run_mininet_container(dev=State.getDevStatus())
                State.setContainer(toynet_session_id, name)
                container = State.getContainer(toynet_session_id)
                counter = 500
                #wait for container to 'come up' so that we can post the topology to it
                container.reload()
                while not container.attrs['State']['Running'] and counter > 0:
                    time.sleep(10)
                    counter-=1 #counter intuitive?
                    container.reload()
                if counter == 0:
                    State.delContainer(toynet_session_id)
                    running = False
                else:
                    ip = container.attrs['NetworkSettings']['IPAddress']
                    args = {'topology': sessionInfo['topology']}
                    res_code = 404
                    while res_code != 200:
                        try:
                            res_code = requests.get('http://'+ip+':'+MINI_FLASK_PORT+'/').status_code 
                        except:
                            time.sleep(10)
                    res = requests.post('http://' + ip + ':' + MINI_FLASK_PORT + '/api/topo', json = args)
                    #assuming that the topology posted is valid (because it's pulled from the DB, which should only store valid topos)
            else:
                running = False

        return {
            'topo_id': sessionInfo['topo_id'],
            'topology': sessionInfo['topology'],
            'user_id': sessionInfo['user_id'],
            'running': running,
        }, 200

    @use_kwargs(ToyNetSessionByIdPutReq)
    def put(self, toynet_session_id, **kwargs):
        try:
            req = ToyNetSessionByIdPutReq().load(kwargs)
        except ValidationError as e:
            abort(400, message=f'malformed request: {e.messages}')

        db = get_db()

        sessionInfo = self.getTopologyFromDb(db, toynet_session_id)
        xmlTopology = ET.fromstring(sessionInfo['topology'])
        parseModificationCommand(req['command'], xmlTopology)

        new_topo = ET.tostring(xmlTopology, encoding='utf-8').decode('utf-8')
        
        try:
            db.execute(
                'UPDATE toynet_sessions'
                ' SET topology = (?)'
                ' WHERE session_id = (?)',
                (new_topo, str(toynet_session_id),)
            )
            db.commit()
        except Exception as e:
            print(e.args[0])
            abort(500, message='Query for toynet_session_id failed: {}'.format(toynet_session_id))

        container = State.getContainer(toynet_session_id)
        if container is not None:
            ip = container.attrs['NetworkSettings']['IPAddress']
            args = {'topology': sessionInfo['topology']}
            res_code = 404
            while res_code != 200:
                try:
                    res_code = requests.get('http://'+ip+':'+MINI_FLASK_PORT+'/').status_code 
                except:
                    time.sleep(10)
            res = requests.post('http://' + ip + ':' + MINI_FLASK_PORT + '/api/topo', json = args)
        else:
            abort(500, message='Container for session does not exist, cannot update topology')

        return {
        }, 200

    @use_kwargs(ToyNetSessionByIdPostReq)
    @marshal_with(ToyNetSessionByIdPostResp)
    def post(self, toynet_session_id, **kwargs):
        try:
            req = ToyNetSessionByIdPostReq().load(kwargs)
        except ValidationError as e:
            abort(400, message='Invalid request: {}'.format(e))
        container = State.getContainer(toynet_session_id)
        if container is None:
            abort(500, message='Invalid Session ID. No corresponding toynet container.')
        if 'toynet_command' not in req:
            abort(400, message='toynet_command not specified')
        ip = container.attrs['NetworkSettings']['IPAddress']
        args = {'command': req['toynet_command']}
        res = requests.post('http://' + ip + ':' + MINI_FLASK_PORT + '/api/command', json = args)
        if res.status_code != 200:
            print(res.status_code)
            print(res)
            abort(res.status_code, message=res.json()['message'])
        return {
            'output': res.json()['output']
        }, 200


class ToyNetSessionByIdTerminate(MethodResource):
    def post(self, toynet_session_id):
        container = State.getContainer(toynet_session_id) #get container by session
        if container is None:
            abort(500, message='Failed to terminate')
        
        ip = container.attrs['NetworkSettings']['IPAddress']
        args = {'terminate': True}
        res = requests.post('http://' + ip + ':' + MINI_FLASK_PORT + '/api/terminate', json = args)
        
        #In the future we may want to handle failed MiniFlask terminate requests differently.
        #For now we are not preserving state, so we terminate the container within State's ToynetManager
        #if res.status_code != 200 or not res.json()['terminated']:
            #abort(500, message='Failed to terminate')

        State.delContainer(container)

        return {
        }, 200
