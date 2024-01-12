from db import DB
from flask import Flask, redirect, render_template, session
from loginform import LoginForm
from regform import RegForm
from models import Models
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'jOaqY9515WL6IxQB'
db = DB('db.db')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        models = Models(db.get_connection())
        exists = models.exists(user_name, password)
        if (exists[0]):
            session['username'] = user_name
            session['role'] = exists[1][2]
            session['content'] = exists[1][-1]
            return redirect("/")
        else:
            error = 'Логин или пароль неверны'
    return render_template('login.html', title='Авторизация', form=form, error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        repassword = form.repassword.data
        fio = form.fio.data
        content = form.content.data
        models = Models(db.get_connection())
        exists = models.login_used(user_name)
        if exists:
            return render_template('register.html', title='Регистрация', form=form)
        else:
            if password == repassword:
                if content:
                    filename = secure_filename(content.filename)
                    if os.path.isfile(os.path.join('static', 'img', filename)):
                        while os.path.isfile(os.path.join('static', 'img', filename)):
                            filename = filename.split('.')
                            filename = '.'.join(
                                [filename[0] + 'A', filename[-1]])
                    content.save(os.path.join('static', 'img', filename))
                    models.insert(user_name, password, "Заказчик", fio, filename)
                else:
                    models.insert(user_name, password, "Заказчик", fio)
                exists = models.exists(user_name, password)
                session['username'] = user_name
                session['role'] = exists[1][2]
                session['content'] = exists[1][-1]
            else:
                return render_template('register.html', title='Регистрация', form=form)
        return redirect("/")
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('role', 0)
    session.pop('content', 0)
    return redirect('/login')


@app.route('/')
def main():
    if 'role' in session:
        if session['role'] == 'Заказчик':
            return redirect('/customer')
        if session['role'] == 'Менеджер по продажам':
            return redirect('/csmanager')
        if session['role'] == 'Менеджер по закупкам':
            return redirect('/manager')
        if session['role'] == 'Мастер':
            return redirect('/master')
        if session['role'] == 'Директор':
            return redirect('/director')
    return render_template('main.html')


@app.route('/main')
def redirect_to_main():
    return redirect('/')


@app.route('/customer')
def customer():
    if 'role' not in session:
        return redirect('/login')
    if session['role'] != 'Заказчик':
        return redirect('/')
    return render_template('customer.html')


@app.route('/csmanager')
def csmanager():
    if 'role' not in session:
        return redirect('/login')
    if session['role'] != 'Менеджер по продажам':
        return redirect('/')
    return render_template('csmanager.html')


@app.route('/manager')
def manager():
    if 'role' not in session:
        return redirect('/login')
    if session['role'] != 'Менеджер по закупкам':
        return redirect('/')
    return render_template('manager.html')


@app.route('/master')
def master():
    if 'role' not in session:
        return redirect('/login')
    if session['role'] != 'Мастер':
        return redirect('/')
    return render_template('master.html')


@app.route('/director')
def director():
    if 'role' not in session:
        return redirect('/login')
    if session['role'] != 'Директор':
        return redirect('/')
    return render_template('director.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
