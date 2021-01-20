from flask import Flask, request
from flask_restful import Resource, Api, abort

from flasksrc.db import get_db

class ToyNetValue(Resource):
    def get(self, value_id):
        db = get_db()
        error = None

        rows = db.execute(
            'SELECT v.name, vi.organization, vi.quote ' + \
            'FROM toynet_values AS v LEFT JOIN toynet_value_inspirations as vi ' + \
            'ON v.id = vi.value_id WHERE v.id = (?) ',
            (str(value_id),)
        ).fetchall()

        if not len(rows):
            abort(404, message="value {} doesn't exist".format(value_id))

        return {
            'value': rows[0]['name'],
            'inspiration': [{'organization': r['organization'], 'definition': r['quote']} for r in rows]
        }, 200
