"""A module with factory classes for the customers application."""

import factory
from factory.django import DjangoModelFactory

from .models import Customer


class CustomerFactory(DjangoModelFactory):
    """Customer factory."""

    class Meta:
        """Meta class."""

        model = Customer
        django_get_or_create = ("email",)

    email = factory.faker.Faker("email")
