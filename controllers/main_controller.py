from flask import Blueprint, render_template, request
from repositories.product_repository import ProductRepository, CategoryRepository

main_bp = Blueprint('main', __name__)
product_repo = ProductRepository()
category_repo = CategoryRepository()

@main_bp.route('/')
def index():
    categories = category_repo.get_all()
    featured_products = product_repo.get_all()[:6]
    return render_template('index.html', categories=categories, products=featured_products)

@main_bp.route('/catalog')
def catalog():
    category_slug = request.args.get('category')
    categories = category_repo.get_all()
    
    if category_slug:
        category = category_repo.get_by_slug(category_slug)
        products = product_repo.get_by_category(category.id) if category else []
    else:
        products = product_repo.get_all()
        
    return render_template('catalog.html', categories=categories, products=products, selected_category=category_slug)

@main_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = product_repo.get_by_id(product_id)
    if not product:
        return "Товар не найден", 404
    return render_template('product_detail.html', product=product)