from flask_restful import Resource, abort

from flasksrc.db import get_db


class ToyNetSurvey(Resource):
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
                    result.append({
                        'type': row['type'],
                        'question': row['question'],
                        'options': [row['option']]
                    })
                elif row['unit']:
                    result.append({
                        'type': row['type'],
                        'question': row['question'],
                        'unit': row['unit']
                    })
                else:
                    result.append({
                        'type': row['type'],
                        'question': row['question'],
                    })
            else:
                result[-1]['options'].append(row['option'])

        return result, 200
