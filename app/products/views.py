from flask import Blueprint, render_template

products_bp = Blueprint('products', __name__, template_folder='templates', url_prefix='/products')

@products_bp.route('/')
def products_list():
    products = [
        {'title': 'Apples', 'desc': 'Red'},
        {'title': 'Oranges', 'desc': 'Orange'},
        {'title': 'Bananas', 'desc': 'Yellow'},
    ]
    return render_template('products/list.html', products=products, title='Продукти')
