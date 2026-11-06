from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, order_id: int, status: str):
        pass

class EmailNotificationObserver(Observer):
    def update(self, order_id: int, status: str):
        print(f"[EMAIL SERVICE] Сповіщення для покупця: Замовлення #{order_id} змінило статус на '{status}'.")

class AdminAuditObserver(Observer):
    def update(self, order_id: int, status: str):
        print(f"[ADMIN AUDIT LOG] Замовлення #{order_id} оновлено до стану: '{status}'.")

class OrderStatusSubject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, order_id: int, status: str):
        for observer in self._observers:
            observer.update(order_id, status)