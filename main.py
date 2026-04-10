from flask import Flask, render_template, request
from data import db_session
from data.db_session import global_init, create_session
from data.words import Word

app = Flask(__name__)
user_id = '123'


@app.route('/main', methods=['GET', 'POST'])
def main():
    # db_session.global_init("db/banks.sqlite")
    # db_sess = create_session()
    # words = db_sess.query(eval(f"WordBank{user_id}")).all()
    # print(words)
    word = 'Привет'
    word_translation = 'hello' # рандомный выбор слова
    if request.method == 'POST':
        action = request.form.get('action')
        user_translation = request.form.get('translation', '').strip().lower()
        if action == 'button_input_word':
            if user_translation == word_translation.lower():
                word = 'hello' # здесь должна быть замена слова
    return render_template('main.html', word=word)


if __name__ == '__main__':
    app.run()
