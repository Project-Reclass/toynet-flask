from marshmallow import Schema, fields
from flask_restful import abort
from flasksrc.db import get_db
from flask_apispec import marshal_with, MethodResource


# Schema definitions
class ToyNetQuizItem(Schema):
    question = fields.Str()
    options = fields.List(fields.Str())
    answer = fields.Int()


class ToyNetQuizGetResp(Schema):
    items = fields.List(fields.Nested(ToyNetQuizItem))


class ToyNetQuizById(MethodResource):
    def get(self, quiz_id):
        db = get_db()

        try:
            rows = db.execute(
                'SELECT q.question_id, q.question, q.answer, qo.option'
                ' FROM toynet_quizzes AS q'
                ' LEFT JOIN toynet_quiz_options as qo'
                ' on q.quiz_id = qo.quiz_id AND q.question_id = qo.question_id'
                ' WHERE q.quiz_id = (?) '
                ' ORDER BY q.question_id, qo.option_id',
                (str(quiz_id),)
            ).fetchall()
        except Exception as e:
            print(e.args[0])
            abort(500, message=f"query for quiz failed: {quiz_id}")

        if not len(rows):
            abort(404, message=f"quiz ID {quiz_id} doesn't exist")

        result = list()
        current_question_id = None
        for row in rows:
            if current_question_id != row['question_id']:
                current_question_id = row['question_id']
                result.append({
                    'question': row['question'],
                    'options': [row['option']],
                    'answer': row['answer']})
            else:
                result[-1]['options'].append(row['option'])

        for question in result:
            if len(question['options']) <= question['answer']:
                abort(
                    500,
                    message=f"The answer for question '{question['question']}' is greater than the"
                    " length of its options."
                )

        return {'items': result}, 200
