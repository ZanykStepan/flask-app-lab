import os
from flask import Blueprint

current_path = os.path.dirname(os.path.abspath(__file__))

posts_bp = Blueprint(
    'posts',
    __name__,
    template_folder='templates/posts',
    static_folder=os.path.join(current_path, 'static'),
    static_url_path='/posts_content/static'
)

from . import views