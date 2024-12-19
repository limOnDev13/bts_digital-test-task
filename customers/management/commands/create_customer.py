"""The module is a django command for creating a new customer."""

from django.core.management import BaseCommand

from customers.factories import CustomerFactory


class Command(BaseCommand):
    help = "Create a new customer."

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="Email")

    def handle(self, *args, **kwargs):
        email = kwargs["email"]
        self.stdout.write(f"Creating customer with email {email}...")
        customer = CustomerFactory.create(email=email)
        self.stdout.write(f"Done, {customer.pk=}")
