from flask import Flask, render_template, request, redirect, url_for, flash
from data import db_session
from data.db_session import global_init, create_session
from data.words import Word

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Нужно для работы flash-сообщений
user_id = '123'


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Простая проверка данных
        if username in USERS and USERS[username] == password:
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')

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
