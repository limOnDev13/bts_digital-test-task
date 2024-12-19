"""The module is a django command for filling the database with random robots."""

from django.core.management import BaseCommand

from robots.factories import RobotFactory


class Command(BaseCommand):
    help = "Create random robots."

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Count of robots")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        self.stdout.write(f"Creating {count} random robots...")

        for num in range(count):
            robot = RobotFactory.create()
            self.stdout.write(
                f"Create #{num} robot:\n"
                f"pk={robot.pk} serial={robot.pk} "
                f"model={robot.model} version={robot.version} "
                f"created={robot.created}\n"
            )
