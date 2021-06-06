import datetime
import argon2
from marshmallow import Schema, fields, ValidationError
from flask import request, current_app
from flask_restful import Resource, abort
from flasksrc.db import get_db
from flask_jwt_extended import create_access_token
from flask_apispec import marshal_with, MethodResource



hasher = argon2.PasswordHasher()


# Schema definitions
class ToyNetUserPostReq(Schema):
    password = fields.Str(required=True)
    username = fields.Str(required=True)
    first_name = fields.Str(required=False)


class ToyNetUserPostResp(Schema):
    username = fields.Str(required=True)


class ToyNetUserLoginPostReq(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class ToyNetUserLoginPostResp(Schema):
    verified = fields.Bool(required=True)
    token = fields.Str(required=True)


class ToyNetUser(MethodResource):
    @marshal_with(ToyNetUserPostResp)
    def post(self):
        try:
            req = ToyNetUserPostReq().load(request.form)
        except ValidationError as e:
            abort(400, message=f'malformed create user request: {e.messages}')

        username = req['username']
        user_group_id = current_app.config['USER_GROUP']
        pw_hash = hasher.hash(req['password'])
        first_name = 'first_name' in req and req['first_name'] or 'NULL'

        db = get_db()
        try:
            db.execute(
                'INSERT INTO users(username, user_group_id, password_hash, first_name)'
                ' VALUES((?), (?), (?), (?))',
                (username, user_group_id, pw_hash, first_name,)
            )
            db.commit()
        except Exception as e:
            print(e.args[0])
            abort(500, message=f"Insert operation failed for user: {username}")

        return {'username': req['username']}, 200


class ToyNetUserLogin(MethodResource):
    @marshal_with(ToyNetUserLoginPostResp)
    def post(self):
        try:
            req = ToyNetUserLoginPostReq().load(request.form)
        except ValidationError:
            # avoid including username/password in abort message
            abort(
                400,
                message='malformed login request'
            )

        db = get_db()
        try:
            rows = db.execute(
                'SELECT users.password_hash'
                ' FROM users'
                ' WHERE username=(?) AND user_group_id=(?)',
                (req['username'], current_app.config['USER_GROUP'],)
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
            return {'verified': False}, 401, {'WWW-Authenticate': 'Basic realm="ToyNet"'}

        # generate JWT token

        expires = datetime.timedelta(hours=9)  # a "workday"
        access_token = create_access_token(identity=req['username'], expires_delta=expires)

        return {
            'verified': True,
            'token': access_token
        }, 200
