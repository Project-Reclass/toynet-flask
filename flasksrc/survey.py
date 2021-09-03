from marshmallow import Schema, fields
from flask_restful import abort
from flasksrc.db import get_db
from flask_apispec import marshal_with, MethodResource
from enum import Enum


class ItemType(Enum):
    TEXT = "TEXT"
    CHOICE = "CHOICE"
    LONGTEXT = "LONGTEXT"
    SCALE = "SCALE"


# Schema definitions
class ToyNetSurveyItem(Schema):
    item_type = fields.Str()
    question = fields.Str()
    options = fields.List(fields.Str())
    unit = fields.Str()


class ToyNetSurveyGetResp(Schema):
    items = fields.List(fields.Nested(ToyNetSurveyItem))


class ToyNetSurveyById(MethodResource):
    @marshal_with(ToyNetSurveyGetResp)
    def get(self, survey_id):
        db = get_db()

        try:
            rows = db.execute(
                'SELECT sq.question_id, sq.question, sq.unit, so.option, st.type'
                ' FROM (toynet_surveys AS s'
                '     LEFT JOIN toynet_survey_questions as sq'
                '     on s.survey_id = sq.survey_id)'
                '           LEFT JOIN toynet_survey_options as so'
                '           on s.survey_id = so.survey_id AND sq.question_id = so.question_id'
                '                   LEFT JOIN toynet_survey_types as st'
                '                   on sq.type_id = st.type_id'
                ' WHERE s.survey_id = (?) '
                ' ORDER BY sq.question_id, so.option_id',
                (str(survey_id),)
            ).fetchall()
        except Exception as e:
            print(e.args[0])
            abort(500, message=f"query for survey failed: {survey_id}")

        if not len(rows):
            abort(404, message=f"survey ID {survey_id} doesn't exist")

        result = list()
        current_question_id = None
        for row in rows:
            if current_question_id != row['question_id']:
                current_question_id = row['question_id']
                if row['option']:
                    entry = {
                        'item_type': row['type'],
                        'question': row['question'],
                        'options': [row['option']]
                    }
                elif row['unit']:
                    entry = {
                        'item_type': row['type'],
                        'question': row['question'],
                        'unit': row['unit']
                    }
                else:
                    entry = {
                        'item_type': row['type'],
                        'question': row['question'],
                    }
                result.append(entry)
            else:
                # append to the options list of the last result
                result[-1]['options'].append(row['option'])

        return {
            'items': result,
        }, 200
