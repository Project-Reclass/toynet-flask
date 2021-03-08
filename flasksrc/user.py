import uuid
import argon2
from marshmallow import Schema, fields, ValidationError

from flask import request
from flask_restful import Resource, abort
from flasksrc.db import get_db

hasher = argon2.PasswordHasher()


class ToyNetUserCreateReq(Schema):
    """ /api/user - POST

    Parameters:
     - password (str)
     - username (str)
     - first_name (str, optional)
    """
    password = fields.Str(required=True)
    username = fields.Str(required=True)
    first_name = fields.Str(required=False)


class ToyNetUser(Resource):
    def post(self):
        try:
            req = ToyNetUserCreateReq().load(request.form)
        except ValidationError as e:
            abort(400, message=f'malformed create user request: {e.messages}')

        user_id = str(uuid.uuid1())
        pw_hash = hasher.hash(req['password'])
        first_name = 'first_name' in req and req['first_name'] or 'NULL'
        username = req['username']

        db = get_db()
        try:
            script = 'BEGIN;' + \
                'INSERT INTO users(id, password_hash, first_name)' + \
                ' VALUES(\'' + user_id + '\', \'' + pw_hash + '\', \'' + first_name + '\');' + \
                'INSERT INTO usernames(username, toynet_userid)' + \
                ' VALUES(\'' + username + '\', \'' + user_id + '\');' + \
                'END TRANSACTION;'
            db.executescript(script)
        except Exception as e:
            print(e.args[0])
            abort(500, message=f"Insert operation failed for user: {username}")

        return dict(user_id=user_id), 200


class ToyNetUserGetByUsernameReq(Schema):
    """ /api/username/<string:username> - GET

    Parameters:
     - username (str)
    """
    username = fields.Str(required=True)


class ToyNetUserByUsername(Resource):
    def get(self):
        try:
            req = ToyNetUserGetByUsernameReq().load(request.form)
        except ValidationError as e:
            abort(400, message=f"cannot parse username {request.form['username']} ({e.messages})")

        db = get_db()
        try:
            rows = db.execute(
                'SELECT usernames.username, usernames.toynet_userid, users.id, users.first_name'
                ' FROM usernames LEFT JOIN users'
                ' ON usernames.toynet_userid = users.id'
                ' WHERE usernames.username=(?)',
                (req['username'],)
            ).fetchall()
        except Exception as e:
            print(e.args[0])
            abort(500, message=f"query for username failed: {req['username']}")

        if not len(rows):
            abort(404, message=f"no user exists with username: {req['username']}")

        return {
            'username': rows[0]['username'],
            'id': rows[0]['id'],
            'first_name': rows[0]['first_name'],
        }, 200


class ToyNetUserLoginReq(Schema):
    """ /api/user - POST

    Parameters:
     - username (str)
     - password (str)
    """
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class ToyNetUserLogin(Resource):
    def post(self):
        try:
            req = ToyNetUserLoginReq().load(request.form)
        except ValidationError:
            # TODO: log details

            # avoid including username/password in abort message
            abort(400, message='malformed login request')

        db = get_db()
        try:
            rows = db.execute(
                'SELECT users.password_hash'
                ' FROM usernames LEFT JOIN users'
                ' ON usernames.toynet_userid = users.id'
                ' WHERE usernames.username=(?)',
                (req['username'],)
            ).fetchall()
        except Exception as e:
            print(e.args[0])
            abort(500, message=f"Retrieve operation failed for user: {req['username']}")

        if not len(rows):
            abort(404, message=f"no user exists with username: {req['username']}")

        try:
            hasher.verify(rows[0]['password_hash'], req['password'])
        except argon2.exceptions.VerifyMismatchError as e:
            print(e.args[0])
            return {'verified': False}, 401

        return {'verified': True}, 200
