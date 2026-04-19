from data import db_session
from data.db_session import global_init, create_session
from data.Banks import Bank
from sqlalchemy import orm
import os
import random
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_required, current_user, LoginManager, UserMixin, login_user, logout_user

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_session'
db_session.global_init("data/banks.sqlite")
user_id = 1
word = ''
word_translation = ''
login_manager = LoginManager(app)
login_manager.login_view = 'login'
basedir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(basedir, 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(data_dir, 'banks.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


@app.route('/')
def index():
    return redirect(url_for('register'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    db_sess = db_session.create_session()
    user_data = db_sess.query(Bank).filter(Bank.id == current_user.id).first()
    if user_data is None:
        user_data = Bank(id=current_user.id, bank=[])
        db_sess.add(user_data)
        db_sess.commit()

    user_bank = user_data.bank

    if request.method == 'GET':
        if user_bank:
            word = random.choice(list(user_bank.keys()))
            session['current_word'] = word
            session['current_translation'] = user_bank[word]
        else:
            return redirect(url_for('words'))

    elif request.method == 'POST':
        action = request.form.get('action')

        if action == 'button_input_word':
            user_translation = request.form.get('translation', '').strip().lower()
            correct_translation = session.get('current_translation', '').lower()

            if user_translation == correct_translation:
                new_word = random.choice(list(user_bank.keys()))
                if len(user_bank) > 1:
                    while new_word == session.get('current_word'):
                        new_word = random.choice(list(user_bank.keys()))

                session['current_word'] = new_word
                session['current_translation'] = user_bank[new_word]

        elif action == 'word_bank':
            return redirect(url_for('words'))
    return render_template('main.html', bank=user_bank, word=session.get('current_word'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Пользователь уже существует\n',
                  'Используйте другое имя')
            return redirect(url_for('register'))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.flush()
        # if form.validate_on_submit():
        #     db_sess = db_session.create_session()
        #     user = User(
        #         name=form.name.data,
        #         email=form.email.data
        #     )
        #     user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        new_bank = Bank(id=new_user.id, bank={})
        db.session.add(new_bank)
        db.session.commit()

        # new_bank = User(user_id=new_user.id, bank=0)
        # db.session.add(new_bank)
        # db.session.commit()
        flash("Регистрация прошла успешно! Теперь вы можете войти.")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('main'))
        else:
            flash("Неверные данные для входа")
        return redirect(url_for('main'))

    return render_template('login.html')


@app.route('/words', methods=['GET', 'POST'])
@login_required
def words():
    db_sess = db_session.create_session()
    user_data = db_sess.query(Bank).filter(Bank.id == current_user.id).first()
    user_bank = user_data.bank

    if not user_data or not isinstance(user_data.bank, dict):
        user_bank = {}
    else:
        user_bank = user_data.bank

    if request.method == 'POST':
        if 'add_word' in request.form:
            new_w = request.form.get('new_word')
            new_t = request.form.get('new_translation')
            if new_w and new_t:
                user_bank[new_w] = new_t

        elif 'delete_action' in request.form:
            word_to_del = request.form.get('delete_action')
            if word_to_del in user_bank:
                del user_bank[word_to_del]

        user_data.bank = user_bank
        sqlalchemy.orm.attributes.flag_modified(user_data, "bank")
        db_sess.commit()
        return redirect(url_for('main'))

    return render_template('words.html', words=user_bank)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            test_user = User(username='admin', password='123')
            db.session.add(test_user)
            db.session.commit()
            print("Тестовый пользователь создан: admin / 123")
    app.run(debug=True)
