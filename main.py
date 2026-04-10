from flask import Flask, render_template, request

# from data import db_session

app = Flask(__name__)


# app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


# def main():
#     # db_session.global_init("db/blogs.db")
#     app.run()


@app.route('/main')
def main():
    return render_template('pages/main.html')


@app.route('/buttons_clicks', methods=['GET', 'POST'])
def buttons_clicks():
    pressed = request.form.get('action')
    if pressed == 'button_input_word':
        pass
    elif pressed == 'word_bank':
        pass


if __name__ == '__main__':
    app.run()
