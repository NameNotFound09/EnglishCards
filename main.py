from flask import Flask, render_template, request
from data import db_session
from data.db_session import global_init, create_session
from data.Banks import Bank
import random

app = Flask(__name__)
user_id = 1
word = ''
word_translation = ''


@app.route('/main', methods=['GET', 'POST'])
def main():
    global word, word_translation
    db_session.global_init("db/banks.sqlite")
    db_sess = create_session()
    user_bank = db_sess.query(Bank).filter(Bank.id == user_id).first().bank
    if request.method == 'GET':
        word = random.choice(list(user_bank.keys()))
        word_translation = user_bank[word]
    elif request.method == 'POST':
        action = request.form.get('action')
        user_translation = request.form.get('translation', '').strip().lower()
        if action == 'button_input_word':
            if user_translation.strip().lower() == word_translation.lower():
                f = random.choice(list(user_bank.keys()))
                while f == word:
                    f = random.choice(list(user_bank.keys()))
                word = f
                word_translation = user_bank[word]

    return render_template('main.html', word=word)


if __name__ == '__main__':
    app.run()
