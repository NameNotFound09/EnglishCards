from flask import Flask, render_template, request, redirect
from data import db_session
from data.db_session import global_init, create_session
from data.Banks import Bank
from sqlalchemy import orm
import random

app = Flask(__name__)
db_session.global_init("db/banks.sqlite")
user_id = 1
word = ''
word_translation = ''


@app.route('/main', methods=['GET', 'POST'])
def main():
    global word, word_translation
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
        elif action == 'word_bank':
            return redirect('/words')
    return render_template('main.html', word=word)


@app.route('/words', methods=['GET', 'POST'])
def words():
    global word, word_translation
    db_sess = create_session()
    user = db_sess.query(Bank).filter(Bank.id == user_id).first()
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
