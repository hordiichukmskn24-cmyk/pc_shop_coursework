from models.product import Product

class ProductFactory:
    """Фабричний метод для створення товарів"""
    
    @staticmethod
    def create_product(category_name: str, name: str, price: float, stock: int, description: str, category_id: int, image_file: str = 'default.jpg', manufacturer: str = None, specs: str = None) -> Product:
        if price < 0:
            raise ValueError("Ціна товару не може бути від'ємною!")
        if stock < 0:
            raise ValueError("Кількість товару не може бути від'ємною!")

        formatted_specs = specs or ""
        if category_name.lower() == "процесори":
            formatted_specs = f"[CPU Component] {formatted_specs}"
        elif category_name.lower() == "відеокарти":
            formatted_specs = f"[GPU Component] {formatted_specs}"

        return Product(
            name=name,
            price=price,
            stock=stock,
            description=description,
            category_id=category_id,
            image_file=image_file,
            manufacturer=manufacturer,
            specs=formatted_specs
        )