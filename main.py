from flask import Flask, render_template, request, redirect, flash, url_for
from data.db_session import global_init, create_session
from data.Banks import Bank
from data.Users import User
from sqlalchemy import orm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegisterForm
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567890'
global_init("db/banks.sqlite")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id_):
    db_sess = create_session()
    return db_sess.get(User, user_id_)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/main')
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.login == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/main")
        else:
            flash('Неверный логин или пароль', 'danger')
    return render_template('login.html', title='Вход', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/main')
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = create_session()
        if db_sess.query(User).filter(User.login == form.username.data).first():
            flash("Этот логин уже занят", "danger")
            return render_template('register.html', form=form)
        user = User()
        user.login = form.username.data
        user.password = form.password.data
        db_sess.add(user)
        db_sess.flush()
        new_bank = Bank(id=user.id, bank={})
        db_sess.add(new_bank)
        db_sess.commit()
        flash("Регистрация успешна!", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    db_sess = create_session()
    bank_entry = db_sess.query(Bank).filter(Bank.id == current_user.id).first()

    # Получаем словарь или пустой словарь, если записи нет
    user_bank = bank_entry.bank if bank_entry and bank_entry.bank else {}
    words_list = list(user_bank.keys())

    word = None
    if words_list:
        word = random.choice(words_list)

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'word_bank':
            return redirect('/words')

        if action == 'button_input_word':
            if len(words_list) < 2:
                flash('Добавьте минимум 2 слова в банк, чтобы начать тренировку!', 'warning')
                return redirect(url_for('main'))

            current_word = request.form.get('current_word')
            user_translation = request.form.get('translation', '').strip().lower()
            correct_translation = user_bank.get(current_word, "").lower()
            if user_translation == correct_translation:
                flash('Правильно!', 'success')
                new_word = random.choice([w for w in words_list if w != current_word])
                return render_template('main.html', word=new_word)
            else:
                flash('Неверно, попробуйте еще раз', 'danger')
                return render_template('main.html', word=current_word)

    return render_template('main.html', word=word)


@app.route('/words', methods=['GET', 'POST'])
@login_required
def words():
    global word, word_translation
    db_sess = create_session()
    user = db_sess.query(Bank).filter(Bank.id == current_user.id).first()
    user_bank = user.bank
    if request.method == 'POST':
        action = request.form.get('action')
        add_word = request.form.get('add_word')
        home = request.form.get('home')
        if add_word:
            new_word = request.form.get('new_word')
            new_translation = request.form.get('new_translation')
            user_bank[new_word] = new_translation
            user.bank = user_bank
            orm.attributes.flag_modified(user, "bank")
            db_sess.commit()
        elif action:
            del user_bank[action]
            user.bank = user_bank
            orm.attributes.flag_modified(user, "bank")
            db_sess.commit()
        elif home:
            return redirect('/main')
    return render_template('words.html', words=user_bank)


if __name__ == '__main__':
    app.run()
