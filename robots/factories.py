from typing import List
import random
from datetime import datetime, timedelta

from factory import LazyAttribute
from factory.django import DjangoModelFactory

from .models import Robot


MODELS: List[str] = [
    "R2", "A3", "X5",
]
VERSIONS: List[str] = [
    "XS", "XL", "XX", "LE", "R1"
]


class RobotFactory(DjangoModelFactory):
    """Robot factory"""

    class Meta:
        model = Robot

    serial = LazyAttribute(lambda o: "-".join((o.model, o.version)))
    model = LazyAttribute(lambda o: random.choice(MODELS))
    version = LazyAttribute(lambda o: random.choice(VERSIONS))
    created = LazyAttribute(lambda o: datetime.now() - timedelta(days=random.randint(0, 14)))