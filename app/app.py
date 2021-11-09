from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///question.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Question(db.Model):

    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Integer, nullable=False)


db.create_all()


@app.route('/')
def home():
    questions = Question.query.all()
    return render_template('home.html', questions=questions)


@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        new_question = Question()
        new_question.question = request.form['new_question']
        new_question.answer = request.form['answer']
        if new_question.question == '':
            return render_template('page_not_found.html')
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add_question.html')


@app.route('/delete', methods=['POST'])
def delete():
    i = request.form['btn-delete']
    question = Question.query.filter_by(id=i).first()
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/judge', methods=['POST'])
def judge():
    correct_count = int()
    wrong_count = int()
    answers = Question.query.all()
    for answer in answers:
        user_answer = int(request.form[str(answer.id)])
        if user_answer == answer.answer:
            correct_count += 1
        else:
            wrong_count += 1

    return render_template('answer.html', correct_count=correct_count, wrong_count=wrong_count, q_num=len(answers))


if __name__ == '__main__':
    app.run()

