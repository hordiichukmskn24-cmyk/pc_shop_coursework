from abc import ABC, abstractmethod

class ShippingStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, total_price: float) -> float:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

class CourierDelivery(ShippingStrategy):
    def calculate_cost(self, total_price: float) -> float:
        return 150.0 if total_price < 5000 else 0.0

    def get_name(self) -> str:
        return "Кур'єрська доставка"

class PostalDelivery(ShippingStrategy):
    def calculate_cost(self, total_price: float) -> float:
        return 80.0

    def get_name(self) -> str:
        return "Доставка у відділення Пошти"

class PickupDelivery(ShippingStrategy):
    def calculate_cost(self, total_price: float) -> float:
        return 0.0

    def get_name(self) -> str:
        return "Самовивіз з магазину"

class OrderCheckoutContext:
    def __init__(self, shipping_strategy: ShippingStrategy):
        self._shipping_strategy = shipping_strategy

    def set_strategy(self, shipping_strategy: ShippingStrategy):
        self._shipping_strategy = shipping_strategy

    def calculate_final_price(self, order_subtotal: float) -> float:
        shipping_cost = self._shipping_strategy.calculate_cost(order_subtotal)
        return order_subtotal + shipping_cost