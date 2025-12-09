from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
from app.forms import ContactForm

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='default'):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from .users.views import users_bp
    app.register_blueprint(users_bp)

    from .products.views import products_bp
    app.register_blueprint(products_bp)

    from .posts.views import posts_bp
    app.register_blueprint(posts_bp, url_prefix='/post')
    @app.route('/')
    def resume():
        return render_template('resume.html', title='Резюме')

    @app.route('/contacts', methods=['GET', 'POST'])
    def contacts():
        form = ContactForm()
        if form.validate_on_submit():
            flash(f"Повідомлення від {form.name.data} надіслано!", "success")
            return redirect(url_for('contacts'))
        return render_template('contacts.html', title='Контакти', form=form)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app