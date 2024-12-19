"""The module is a django command for filling the database with random customers."""

from django.core.management import BaseCommand

from customers.factories import CustomerFactory


class Command(BaseCommand):
    help = "Create random customers."

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Count of customers")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        self.stdout.write(f"Creating {count} random customers...")

        for num in range(count):
            customer = CustomerFactory.create()
            self.stdout.write(
                f"Create #{num} customer:\n" f"pk={customer.pk} email={customer.email}"
            )
