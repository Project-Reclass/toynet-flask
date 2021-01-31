from flask import Flask, request
from flask_restful import Resource, Api, abort

from flasksrc.db import get_db

class ToyNetQuiz(Resource):
    def get(self, quiz_id):
        db = get_db()
        error = None

        rows_question = db.execute(
            'SELECT qq.question_id, qq.question, qq.answer'
            ' FROM toynet_quiz_questions AS qq'
            ' WHERE qq.quiz_id = (?) ',
            (str(quiz_id),)
        ).fetchall()

        rows_option = db.execute(
            'SELECT qo.question_id, qo.option'
            ' FROM toynet_quiz_options AS qo'
            ' WHERE qo.quiz_id = (?)'
            ' ORDER BY qo.question_id, qo.option_id',
            (str(quiz_id),)
        ).fetchall()

        if not len(rows_question):
            abort(404, message=f"quiz {quiz_id} doesn't exist")

        question_id_options = {}
        for row in rows_option:
            if row['question_id'] not in question_id_options:
                question_id_options[row['question_id']] = [row['option']]
            else:
                question_id_options[row['question_id']].append(row['option'])

        return [
            {
                'question': row['question'],
                'options': question_id_options[row['question_id']],
                'answer': row['answer']
            }
            for row in rows_question
        ], 200
