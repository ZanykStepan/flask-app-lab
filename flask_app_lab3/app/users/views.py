from flask import Blueprint, request, redirect, url_for, render_template

users_bp = Blueprint('users', __name__, template_folder='templates', static_folder='static', url_prefix='/users')

@users_bp.route('/hi/<string:name>')
def greetings(name):
    name = name.upper()
    age = request.args.get('age', None, int)
    return render_template('users/hi.html', name=name, age=age)

@users_bp.route('/admin')
def admin():
    return redirect(url_for('users.greetings', name='Administrator', age=45))
