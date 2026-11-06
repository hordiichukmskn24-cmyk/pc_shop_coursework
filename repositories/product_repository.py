from database import db
from models.product import Product, Category

class ProductRepository:
    @staticmethod
    def get_all():
        return Product.query.all()

    @staticmethod
    def get_by_id(product_id: int):
        return Product.query.get(product_id)

    @staticmethod
    def get_by_category(category_id: int):
        return Product.query.filter_by(category_id=category_id).all()

    @staticmethod
    def search(query: str):
        return Product.query.filter(Product.name.ilike(f"%{query}%")).all()

    @staticmethod
    def add(product: Product):
        db.session.add(product)
        db.session.commit()

    @staticmethod
    def delete(product_id: int):
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()

class CategoryRepository:
    @staticmethod
    def get_all():
        return Category.query.all()

    @staticmethod
    def get_by_slug(slug: str):
        return Category.query.filter_by(slug=slug).first()

    @staticmethod
    def add(category: Category):
        db.session.add(category)
        db.session.commit()