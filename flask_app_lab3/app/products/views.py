from flask import Blueprint, render_template

products_bp = Blueprint('products', __name__, template_folder='templates', url_prefix='/products')

@products_bp.route('/')
def products_list():
    products = [
        {'title': 'Product 1', 'desc': 'Опис 1'},
        {'title': 'Product 2', 'desc': 'Опис 2'},
    ]
    return render_template('products/list.html', products=products)
