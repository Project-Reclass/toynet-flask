from flask import Flask, request
from flask_restful import Resource, Api, abort

from flasksrc.db import get_db

class ToyNetQuiz(Resource):
    def get(self, quiz_id):
        db = get_db()

        try:
            rows_question = db.execute(
                'SELECT q.question_id, q.question, q.answer'
                ' FROM toynet_quizzes AS q'
                ' WHERE q.quiz_id = (?) ',
                (str(quiz_id),)
            ).fetchall()
        except Exception as e:
            print(e.args[0])
            abort(500, message=f"query for quiz failed: {quiz_id}")

        if not len(rows_question):
            abort(404, message=f"quiz {quiz_id} doesn't exist")

        try:
            rows_option = db.execute(
                'SELECT qo.question_id, qo.option'
                ' FROM toynet_quiz_options AS qo'
                ' WHERE qo.quiz_id = (?)'
                ' ORDER BY qo.question_id, qo.option_id',
                (str(quiz_id),)
            ).fetchall()
        except Exception as e:
            print(e.args[0])
            abort(500, message=f"query for options failed for quiz_id {quiz_id}")

        question_id_options = {}
        for row in rows_option:
            if row['question_id'] not in question_id_options:
                question_id_options[row['question_id']] = [row['option']]
            else:
                question_id_options[row['question_id']].append(row['option'])

        for row in rows_question:
            if len(question_id_options[row['question_id']]) <= row['answer']:
                abort(500, message=f"The answer for question {row['question_id']} is greater than the length of its options.")

        return [
            {
                'question': row['question'],
                'options': question_id_options[row['question_id']],
                'answer': row['answer']
            }
            for row in rows_question
        ], 200
