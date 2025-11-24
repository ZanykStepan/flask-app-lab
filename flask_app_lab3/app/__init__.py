from flask import Flask

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config.from_pyfile("../config.py", silent=True)

# register blueprints
from .users.views import users_bp
from .products.views import products_bp
from . import views as main_views  # import main routes

app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
