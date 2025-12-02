from flask import Blueprint, request, redirect, url_for, render_template, flash, session, make_response
from app.users.forms import LoginForm

users_bp = Blueprint('users', __name__, template_folder='templates', static_folder='static', url_prefix='/users')

USER_DATA = {
    "username": "user1",
    "password": "1234"
}


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('users.profile'))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        if username == USER_DATA['username'] and password == USER_DATA['password']:
            session['username'] = username

            msg = "Успішний вхід!"
            if remember:
                msg += " (Функцію 'Запам'ятати мене' активовано)"

            flash(msg, "success")
            return redirect(url_for('users.profile'))
        else:
            flash("Невірні дані! Спробуйте ще раз.", "danger")
            return redirect(url_for('users.login'))

    return render_template('users/login.html', title='Вхід', form=form)


@users_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash("Ви вийшли з системи.", "info")
    return redirect(url_for('users.login'))


@users_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for('users.login'))

    if request.method == 'POST':
        action = request.form.get('action')
        resp = make_response(redirect(url_for('users.profile')))

        if action == 'add':
            key = request.form.get('key')
            value = request.form.get('value')
            expiry = request.form.get('expiry')
            if expiry and expiry.isdigit():
                max_age = int(expiry)
            else:
                max_age = 60 * 60 * 24

            resp.set_cookie(key, value, max_age=max_age)
            flash(f"Кукі '{key}' успішно додано.", "success")
            return resp

        elif action == 'delete':
            key = request.form.get('key')
            resp.set_cookie(key, '', expires=0)
            flash(f"Кукі '{key}' видалено.", "warning")
            return resp

        elif action == 'delete_all':
            cookies = request.cookies
            for key in cookies:
                if key != 'session':
                    resp.set_cookie(key, '', expires=0)
            flash("Всі кукі видалено.", "danger")
            return resp

    return render_template('users/profile.html',
                           username=session.get('username'),
                           cookies=request.cookies,
                           title='Профіль')


@users_bp.route('/change-theme/<theme>')
def change_theme(theme):
    if theme not in ['light', 'dark']:
        theme = 'light'
    resp = make_response(redirect(url_for('users.profile')))
    resp.set_cookie('theme', theme, max_age=60 * 60 * 24 * 30)
    return resp


@users_bp.route('/hi/<string:name>')
def greetings(name):
    name = name.upper()
    age = request.args.get('age', None, int)
    return render_template('users/hi.html', name=name, age=age, title='Привітання')


@users_bp.route('/admin')
def admin():
    return redirect(url_for('users.greetings', name='Administrator', age=45))
