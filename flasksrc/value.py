from flask_restful import Resource, abort

from flasksrc.db import get_db


class ToyNetValueById(Resource):
    def get(self, value_id):
        db = get_db()

        try:
            rows = db.execute(
                'SELECT v.name, vi.organization, vi.quote' +
                ' FROM toynet_values AS v' +
                ' LEFT JOIN toynet_value_inspirations as vi' +
                ' ON v.id = vi.value_id WHERE v.id = (?)',
                (str(value_id),)
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
