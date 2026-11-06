from database import db

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)

    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg')
    manufacturer = db.Column(db.String(100), nullable=True)
    specs = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    def in_stock(self) -> bool:
        return self.stock > 0

    def reduce_stock(self, quantity: int):
        if quantity <= self.stock:
            self.stock -= quantity
        else:
            raise ValueError("Недостатньо товару на складі!")

    def __repr__(self):
        return f"<Product {self.name} - {self.price} UAH>"