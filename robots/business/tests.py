import random
from datetime import datetime, timedelta

from django.test import TestCase

from robots.factories import RobotFactory

from .queries import produced_robots


class TestNumberOfRobotsProduced(TestCase):
    """Test case for number_of_robots_produced"""

    def setUp(self):
        self.start_date = datetime.now() - timedelta(days=7)
        self.end_date = datetime.now()
        self.old_robots = [
            RobotFactory.create(created=self.start_date - timedelta(days=1))
            for _ in range(random.randint(50, 100))
        ]
        self.new_robots = [
            RobotFactory.create(created=self.end_date)
            for _ in range(random.randint(50, 50))
        ]

    def tearDown(self):
        for robot in self.old_robots:
            robot.delete()
        for robot in self.new_robots:
            robot.delete()

    def test_number_of_robots_produced(self):
        qs = produced_robots(self.start_date, self.end_date)

        result: int = 0
        for robot in qs:
            result += robot["num_robots"]

        self.assertEqual(len(self.new_robots), result)
