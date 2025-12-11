from flask import Blueprint, request, redirect, url_for, render_template, flash, session, make_response
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app import db
from .forms import LoginForm, RegistrationForm

users_bp = Blueprint('users', __name__, template_folder='templates', static_folder='static', url_prefix='/users')


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            flash('Ви успішно увійшли!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.profile'))
        else:
            flash('Невірний логін або пароль.', 'danger')

    return render_template('users/login.html', form=form, title='Вхід')


@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('users.login'))


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('resume.list_resumes'))

    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Такий користувач вже існує!', 'danger')
            return redirect(url_for('users.register'))

        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Акаунт створено! Увійдіть у систему.', 'success')
        return redirect(url_for('users.login'))

    return render_template('users/register.html', form=form, title='Реєстрація')


@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        action = request.form.get('action')
        resp = make_response(redirect(url_for('users.profile')))

        if action == 'add':
            key = request.form.get('key')
            value = request.form.get('value')
            expiry = request.form.get('expiry')
            max_age = int(expiry) if expiry and expiry.isdigit() else 60 * 60 * 24

            resp.set_cookie(key, value, max_age=max_age)
            flash(f"Кукі '{key}' додано.", "success")
            return resp

        elif action == 'delete':
            key = request.form.get('key')
            resp.set_cookie(key, '', expires=0)
            flash(f"Кукі '{key}' видалено.", "warning")
            return resp

        elif action == 'delete_all':
            cookies = request.cookies
            for key in cookies:
                if key not in ['session', 'remember_token']:
                    resp.set_cookie(key, '', expires=0)
            flash("Всі кукі (крім сесійних) видалено.", "danger")
            return resp

    return render_template('users/profile.html',
                           user=current_user,
                           cookies=request.cookies)


@users_bp.route('/change-theme/<theme>')
@login_required
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
