from flask_restful import Resource, abort, reqparse
from flask import request

from flasksrc.db import get_db


class ToyNetSession(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('toynet_topo_id', type=int)
        parser.add_argument('toynet_user_id', type=str)
        request.get_json(force=True)

        args = parser.parse_args()
        toynet_topo_id = int(args['toynet_topo_id'])
        toynet_user_id = str(args['toynet_user_id'])

        db = get_db()

        try:
            topo_rows = db.execute(
                'SELECT topology' +
                ' FROM toynet_topos' +
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
                'SELECT id' +
                ' FROM users' +
                ' WHERE id = (?)',
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
                    'INSERT INTO toynet_sessions(topo_id, topology, user_id)' +
                    ' VALUES(?,?,?)',
                    (str(toynet_topo_id), topo_rows[0]['topology'], toynet_user_id,)
                    )
            db.commit()
        except Exception as e:
            print(e.args[0])
            abort(500, message='Failed to create new session')

        return {
            'status': True,
            'toynet_session_id': cur.lastrowid
            }, 201


class ToyNetSessionById(Resource):
    def get(self, toynet_session_id):
        db = get_db()

        try:
            rows = db.execute(
                'SELECT topo_id, topology, user_id, create_time, update_time' +
                ' FROM toynet_sessions' +
                ' WHERE session_id = (?)',
                (str(toynet_session_id),)
            ).fetchall()
        except Exception as e:
            print(e.args[0])
            abort(500, message='Query for session_id failed: {}'.format(toynet_session_id))

        if not len(rows):
            abort(400, message='session_id {} does not exist'.format(toynet_session_id))

        return {
            'topo_id': rows[0]['topo_id'],
            'topology': rows[0]['topology'],
            'user_id': rows[0]['user_id'],
        }, 200

    def put(self, toynet_session_id):
        db = get_db()

        parser = reqparse.RequestParser()
        parser.add_argument('new_topology', type=str)
        request.get_json(force=True)

        args = parser.parse_args()
        new_topo = str(args['new_topology'])

        try:
            db.execute(
                    'UPDATE toynet_sessions' +
                    ' SET topology = (?)' +
                    ' WHERE session_id = (?)',
                    (new_topo, str(toynet_session_id),)
                    )
            db.commit()
        except Exception as e:
            print(e.args[0])
            abort(500, message='Query for toynet_session_id failed: {}'.format(toynet_session_id))

        return {
        }, 200
