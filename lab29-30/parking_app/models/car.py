"""
Модель данных для представления автомобиля на стоянке
"""

from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Car:
    """Класс для представления автомобиля на стоянке"""
    car_brand: str
    car_number: str
    owner_name: str
    entry_time: datetime
    hourly_rate: float
    discount: int
    exit_time: Optional[datetime] = None
    payment_status: str = "Не оплачено"
    debt: float = 0.0
    cost: float = 0.0
    id: str = field(default_factory=lambda: datetime.now().strftime("%Y%m%d%H%M%S"))

    def calculate_current_cost(self, current_time: datetime = None) -> float:
        """Расчет текущей стоимости стоянки"""
        if current_time is None:
            current_time = datetime.now()

        if self.exit_time is not None:
            end_time = self.exit_time
        else:
            end_time = current_time

        time_diff = end_time - self.entry_time
        hours = time_diff.total_seconds() / 3600
        cost = hours * self.hourly_rate
        discount_amount = cost * (self.discount / 100)
        final_cost = cost - discount_amount
        return max(0, round(final_cost, 2))

    def get_duration(self, current_time: datetime = None) -> float:
        """Расчет длительности пребывания на стоянке в часах"""
        if current_time is None:
            current_time = datetime.now()

        if self.exit_time is not None:
            end_time = self.exit_time
        else:
            end_time = current_time

        time_diff = end_time - self.entry_time
        return round(time_diff.total_seconds() / 3600, 2)

    def to_dict(self) -> dict:
        """Преобразование объекта в словарь для сохранения"""
        return {
            "id": self.id,
            "car_brand": self.car_brand,
            "car_number": self.car_number,
            "owner_name": self.owner_name,
            "entry_time": self.entry_time.isoformat(),
            "hourly_rate": self.hourly_rate,
            "discount": self.discount,
            "exit_time": self.exit_time.isoformat() if self.exit_time else None,
            "payment_status": self.payment_status,
            "debt": self.debt,
            "cost": self.cost
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Car':
        """Создание объекта из словаря"""
        car = cls(
            car_brand=data["car_brand"],
            car_number=data["car_number"],
            owner_name=data["owner_name"],
            entry_time=datetime.fromisoformat(data["entry_time"]),
            hourly_rate=data["hourly_rate"],
            discount=data["discount"],
            payment_status=data["payment_status"],
            debt=data["debt"],
            id=data.get("id", datetime.now().strftime("%Y%m%d%H%M%S"))
        )

        if data["exit_time"]:
            car.exit_time = datetime.fromisoformat(data["exit_time"])

        if "cost" in data:
            car.cost = data["cost"]

        return car
