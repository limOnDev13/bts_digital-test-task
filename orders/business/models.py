"""A module with models for business logic."""

from dataclasses import dataclass


@dataclass
class OrderInfo:
    """A class for storing order information."""

    customer_id: int
    robot_serial: str
