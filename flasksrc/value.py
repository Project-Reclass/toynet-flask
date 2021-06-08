from marshmallow import Schema, fields, ValidationError
from flask import request, current_app
from flask_restful import abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasksrc.db import get_db
from flask_apispec import marshal_with, MethodResource


# Schema definitions
class ToyNetValueInspiration(Schema):
    organization = fields.Str()
    definition = fields.Str()


class ToyNetValueByIdPostResp(Schema):
    value = fields.Str()
    inspiration = fields.List(fields.Nested(ToyNetValueInspiration))


class ToyNetEntryByIdGetResp(Schema):
    entry = fields.Str()


class ToyNetValueEntryPutReq(Schema):
    quote = fields.Str(required=True)


class ToyNetValueById(MethodResource):
    @marshal_with(ToyNetValueByIdPostResp)
    def get(self, value_id):
        db = get_db()

        try:
            rows = db.execute(
                'SELECT v.name, vi.organization, vi.quote'
                ' FROM toynet_values AS v'
                ' LEFT JOIN toynet_value_inspirations as vi'
                ' ON v.id = vi.value_id WHERE v.id = (?)',
                (value_id,)
            ).fetchall()
        except Exception as e:
            print(e.args[0])
            abort(500, message="query for value failed: {}".format(value_id))

        if not len(rows):
            abort(404, message="value ID {} does not exist".format(value_id))

        inspirations = [{'organization': r['organization'], 'definition': r['quote']} for r in rows]

        return {
            'value': rows[0]['name'],
            'inspiration': inspirations
        }, 200


class ToyNetValueEntryById(MethodResource):
    @marshal_with(ToyNetEntryByIdGetResp)
    @jwt_required()
    def get(self, value_id):
        username = get_jwt_identity()
        group_id = current_app.config['USER_GROUP']

        db = get_db()
        try:
            rows = db.execute(
                'SELECT ve.quote'
                ' FROM toynet_values AS v LEFT JOIN toynet_value_entries as ve'
                ' ON v.id = ve.value_id'
                ' WHERE v.id = (?) AND ve.username = (?) AND ve.user_group_id = (?)'
                ' ORDER BY ve.created DESC',
                (value_id, username, group_id,)
            ).fetchall()
        except Exception as e:
            print(e.args[0])
            abort(500, message="query for value failed: {}".format(value_id))

        if not len(rows):
            msg = "no entries for value {} for {}, group {}".format(value_id, username, group_id)
            abort(404, message=msg)

        return {'entry': rows[0]['quote']}, 200

    @jwt_required()
    def put(self, value_id):
        try:
            req = ToyNetValueEntryPutReq().load(request.form)
        except ValidationError as e:
            abort(400, message=f'malformed create user request: {e.messages}')

        username = get_jwt_identity()
        user_group_id = current_app.config['USER_GROUP']

        db = get_db()
        try:
            db.execute(
                'INSERT or REPLACE INTO'
                ' toynet_value_entries(value_id, username, user_group_id, quote, created)'
                ' VALUES((?), (?), (?), (?), datetime(\'now\'))',
                (value_id, username, user_group_id, req['quote'],)
            )
            db.commit()
        except Exception as e:
            print(e.args[0])
            abort(
                500,
                message=f"Insert operation failed for value_id: {value_id} & user: {username}"
            )

        return {}, 200
