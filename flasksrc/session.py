from marshmallow import Schema, fields, ValidationError
from flask_restful import abort
from flask_apispec import marshal_with, MethodResource
from flask import request
from flasksrc.db import get_db

from xml.etree import ElementTree as ET
from flasksrc.emulator.commandParser import parseModificationCommand

# Schema definitions
class ToyNetSessionPostReq(Schema):
    toynet_topo_id = fields.Int(required=True)
    toynet_user_id = fields.Str(required=True)


class ToyNetSessionPostResp(Schema):
    toynet_session_id = fields.Int()


class ToyNetSessionByIdGetResp(Schema):
    topo_id = fields.Int()
    user_id = fields.Str()
    topology = fields.Str()


class ToyNetSessionByIdPutReq(Schema):
    command = fields.Str(required=True)


class ToyNetSession(MethodResource):    
    @marshal_with(ToyNetSessionPostResp)
    def post(self):
        try:
            req = ToyNetSessionPostReq().load(request.form)
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
        except Exception as e:
            print(e.args[0])
            abort(500, message='Failehttps://input.djr.com/d to create new session')

        return {
            'toynet_session_id': cur.lastrowid
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

        return {
            'topo_id': sessionInfo['topo_id'],
            'topology': sessionInfo['topology'],
            'user_id': sessionInfo['user_id'],
        }, 200

    @marshal_with(ToyNetSessionByIdPutReq)
    def put(self, toynet_session_id):
        try:
            req = ToyNetSessionByIdPutReq().load(request.form)
        except ValidationError as e:
            abort(400, message=f'malformed request: {e.messages}')

        db = get_db()

        sessionInfo = self.getTopologyFromDb(db, toynet_session_id)
        xmlTopology:ET = ET.fromstring(sessionInfo['topology'])
    
        newXmlTopology = parseModificationCommand(req['command'], xmlTopology)
        new_topo = topology=ET.tostring(xmlTopology, encoding='utf-8').decode('utf-8')

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

        return {
        }, 200
