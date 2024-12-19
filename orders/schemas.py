"""A module with pydantic schemas of the "orders" app."""

from pydantic import BaseModel, Field, field_validator

from customers.models import Customer


class OrderSchema(BaseModel):
    """The scheme of the new order."""

    customer_id: int
    robot_serial: str = Field(max_length=5)

    @field_validator("customer_id")
    @classmethod
    def validate_customer_in_db(cls, value: int):
        """Validate that this customer is in the database."""
        if not Customer.objects.filter(pk=value).exists():
            raise ValueError(f"Customer with id {value} does not exists.")
        return value
