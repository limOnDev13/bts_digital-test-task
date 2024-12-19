"""A module with pydantic schemas for the robots application."""

from datetime import datetime
from string import ascii_uppercase, digits
from typing import Set

from pydantic import BaseModel, Field, field_validator

MODELS: Set[str] = {f"{let}{dig}" for let in ascii_uppercase for dig in digits}


class RobotSchema(BaseModel):
    """Robot schema."""

    model: str = Field(max_length=2)
    version: str = Field(max_length=2)
    created: datetime

    @field_validator("model")
    @classmethod
    def validate_model_in_db(cls, value: str):
        """Validate that this model is in the database."""
        # Since there is no separate table with existing models,
        # there will be a stub in the form of a set of names
        # consisting of the first capital letter and the second digit
        if value not in MODELS:
            raise ValueError(f"Model {value} does not exist.")
        return value
