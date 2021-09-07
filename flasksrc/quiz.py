from marshmallow import Schema, fields, ValidationError
from flask_restful import abort
from flasksrc.db import get_db
from flask_apispec import marshal_with, MethodResource, use_kwargs
from flask_jwt_extended import jwt_required

# Schema definitions
class ToyNetQuizItem(Schema):
    question = fields.Str()
    options = fields.List(fields.Str())
    answer = fields.Int()


class ToyNetQuizGetResp(Schema):
    items = fields.List(fields.Nested(ToyNetQuizItem))


class ToyNetQuizScorePostReq(Schema):
    quiz_id = fields.Int(required=True)
    user_id = fields.String(required=True)
    count_correct = fields.Int(required=True)
    count_wrong = fields.Int(required=True)


class ToyNetQuizScorePostResp(Schema):
    submission_id = fields.Int()


class ToyNetQuizScore(Schema):
    count_correct = fields.Int()
    datetime = fields.DateTime()


class ToyNetQuizScoreHistory(Schema):
    quiz_id = fields.Int()
    count_total = fields.Int()
    scores = fields.List(fields.Nested(ToyNetQuizScore))


class ToyNetQuizScoresGetResp(Schema):
    scores = fields.List(fields.Nested(ToyNetQuizScoreHistory))


class ToyNetQuizById(MethodResource):
    @marshal_with(ToyNetQuizGetResp)
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


class ToyNetQuizScore(MethodResource):
    @jwt_required()
    @use_kwargs(ToyNetQuizScorePostReq)
    @marshal_with(ToyNetQuizScorePostResp)
    def post(self, **kwargs):
        try:
            req = ToyNetQuizScorePostReq().load(kwargs)
        except ValidationError as e:
            abort(400, message=f'malformed create submission request: {e.messages}')

        quiz_id = req['quiz_id']
        user_id = req['user_id']
        count_correct = req['count_correct']
        count_wrong = req['count_wrong']

        db = get_db()
        try:
            db.execute(
                'INSERT INTO toynet_quiz_scores(quiz_id,user_id,count_correct,count_wrong)'
                ' VALUES((?), (?), (?), (?))',
                (quiz_id, user_id, count_correct, count_wrong)
            )
            db.commit()
            rows = db.execute(
                'SELECT scores.submission_id, scores.submitted'
                ' FROM toynet_quiz_scores AS scores'
                ' WHERE scores.quiz_id = (?) AND scores.user_id = (?)'
                ' ORDER BY scores.submitted DESC',
                (quiz_id, user_id)
            ).fetchall()
        except Exception as e:
            print(e.args[0])
            abort(400, message="Insertion failed")

        return {'submission_id': rows[0]['submission_id']}, 201


class ToyNetQuizScoresByUser(MethodResource):
    @jwt_required()
    @marshal_with(ToyNetQuizScoresGetResp)
    def get(self, user_id):
        db = get_db()
        try:
            rows = db.execute(
                'SELECT * FROM toynet_quiz_scores as scores'
                ' WHERE scores.user_id = (?)'
                ' GROUP BY scores.quiz_id'
                ' ORDER BY scores.submitted',
                user_id
            ).fetchall()
        except Exception as e:
            print(e.args[0])
            abort(500, message="query for quiz scores failed: {}".format(user_id))

        if not len(rows):
            abort(404, "no quiz scores for user {}".format(user_id))

        scores = list()
        count = 0
        current_quiz_id = rows[0]['quiz_id']
        for row in rows:
            if current_quiz_id == row['quiz_id']:
                scores[count]['scores'].append({'count_correct': row['count_correct'], 'datetime': row['submitted']})
            else:
                current_quiz_id = row['quiz_id'] 
                count += 1
                scores[count]['quiz_id'] = current_quiz_id
                scores[count]['count_total'] = row['count_correct'] + row['count_wrong']
                scores[count]['scores'] = {'count_correct': row['count_correct'], 'datetime': row['submitted']}

        return {'scores': scores}, 200