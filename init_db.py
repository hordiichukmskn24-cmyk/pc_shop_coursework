import models
from app import create_app
from database import db
from models.product import Category
from models.user import User, Admin
from services.factories import ProductFactory

app = create_app()

def seed_database():
    with app.app_context():
        # Створення всіх таблиць у MySQL
        db.create_all()

        # Перевірка, чи БД вже наповнена
        if Category.query.first():
            print("База даних вже містить дані!")
            return

        print("Створення таблиць та наповнення бази даних тестовими даними...")

        # 1. Створення категорій
        categories_data = [
            ("Процесори", "cpu"),
            ("Відеокарти", "gpu"),
            ("Материнські плати", "motherboards"),
            ("Оперативна пам'ять", "ram"),
            ("SSD та HDD накопичувачі", "storage"),
            ("Блоки живлення", "power-supplies"),
            ("Корпуси", "cases"),
            ("Системи охолодження", "cooling"),
            ("Монітори", "monitors"),
            ("Периферія", "peripherals")
        ]

        categories = {}
        for name, slug in categories_data:
            cat = Category(name=name, slug=slug)
            db.session.add(cat)
            categories[name] = cat
        
        db.session.commit()

        # 2. Створення адміна та тестового користувача
        admin = Admin(username="admin", email="admin@pcstore.com")
        admin.set_password("admin123")
        
        user = User(username="user", email="user@gmail.com")
        user.set_password("user123")

        db.session.add(admin)
        db.session.add(user)
        db.session.commit()

        # 3. Створення товарів за допомогою Factory Method (GoF Pattern)
        products = [
            ProductFactory.create_product(
                category_name="Процесори",
                name="Intel Core i7-13700K",
                price=16500.0,
                stock=10,
                description="Потужний 16-ядерний процесор 13-го покоління для ігор та важких завдань.",
                category_id=categories["Процесори"].id,
                manufacturer="Intel",
                specs="Сокет LGA1700, 16 ядер, 24 потоки, тактова частота до 5.4 ГГц."
            ),
            ProductFactory.create_product(
                category_name="Процесори",
                name="AMD Ryzen 7 7800X3D",
                price=18200.0,
                stock=8,
                description="Найкращий ігровий процесор з технологією 3D V-Cache.",
                category_id=categories["Процесори"].id,
                manufacturer="AMD",
                specs="Сокет AM5, 8 ядер, 16 потоків, кєш L3 96MB."
            ),
            ProductFactory.create_product(
                category_name="Відеокарти",
                name="NVIDIA GeForce RTX 4070 Super 12GB",
                price=29500.0,
                stock=5,
                description="Відеокарта з підтримкою DLSS 3.5 та трасування променів.",
                category_id=categories["Відеокарти"].id,
                manufacturer="ASUS",
                specs="12GB GDDR6X, 192-bit, PCI-E 4.0."
            ),
            ProductFactory.create_product(
                category_name="Оперативна пам'ять",
                name="Kingston Fury Beast DDR5 32GB (2x16GB) 6000MHz",
                price=5400.0,
                stock=15,
                description="Швидкісний комплект пам'яті з підтримкою XMP 3.0 та EXPO.",
                category_id=categories["Оперативна пам'ять"].id,
                manufacturer="Kingston",
                specs="DDR5, 32 ГБ комплект, CL36, 6000 МГц."
            )
        ]

        for prod in products:
            db.session.add(prod)
        
        db.session.commit()
        print("Базу даних успішно створено та наповнено товарами!")

if __name__ == '__main__':
    seed_database()