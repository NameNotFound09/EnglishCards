from flask import Flask, render_template, request, redirect, url_for, flash
from data import db_session
from data.db_session import global_init, create_session
from data.words import Word
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Нужно для работы flash-сообщений
user_id = '123'

# Настройка пути к базе данных SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'user.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


# Создание базы данных и тестового пользователя (выполнить один раз)
with app.app_context():
    db.create_all()
    # Добавим админа, если его еще нет
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password='password123')
        db.session.add(admin)
        db.session.commit()


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Поиск пользователя в БД
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            flash('Успешный вход через БД!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Пользователь не найден или пароль неверен', 'danger')

    return render_template('login.html')


@app.route('/main', methods=['GET', 'POST'])
def main():
    # db_session.global_init("db/banks.sqlite")
    # db_sess = create_session()
    # words = db_sess.query(eval(f"WordBank{user_id}")).all()
    # print(words)
    word = 'Привет'
    word_translation = 'hello'  # рандомный выбор слова
    if request.method == 'POST':
        action = request.form.get('action')
        user_translation = request.form.get('translation', '').strip().lower()
        if action == 'button_input_word':
            if user_translation == word_translation.lower():
                word = 'hello'  # здесь должна быть замена слова
    return render_template('main.html', word=word)


if __name__ == '__main__':
    app.run(debug=True)
