from dataclasses import dataclass


@dataclass
class OrderInfo:
    customer_id: int
    robot_serial: str
