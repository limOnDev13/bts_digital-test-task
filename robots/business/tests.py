"""A module with tests for the business logic of the robots app."""

import random
from datetime import datetime, timedelta
from typing import List

from django.conf import settings
from django.test import TestCase

from business.queue import CustomersQueue
from customers.models import Customer
from orders.business.models import OrderInfo
from robots.factories import RobotFactory
from robots.models import Robot

from .main import create_new_robot
from .models import RobotInfo
from .queries import produced_robots


class TestNumberOfRobotsProduced(TestCase):
    """Test case for number_of_robots_produced."""

    def setUp(self):
        """Set up tests."""
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
        """Tear down tests."""
        for robot in self.old_robots:
            robot.delete()
        for robot in self.new_robots:
            robot.delete()

    def test_number_of_robots_produced(self):
        """Test func number_of_robots_produced."""
        qs = produced_robots(self.start_date, self.end_date)

        result: int = 0
        for robot in qs:
            result += robot["num_robots"]

        self.assertEqual(len(self.new_robots), result)


class CreateRobotTestCase(TestCase):
    """Test case for testing the func create_new_robot."""

    def setUp(self):
        """Set up tests."""
        self.robot_info = RobotInfo(
            serial="R2-D2", model="R2", version="D2", created=str(datetime.now())
        )
        self.customer = Customer.objects.create(email=settings.TEST_EMAIL)
        self.order_info = OrderInfo(
            customer_id=self.customer.pk, robot_serial=self.robot_info.serial
        )
        self.queue = CustomersQueue()

    def tearDown(self):
        """Tear down tests."""
        self.queue.clear()
        if self.customer.pk is not None:
            self.customer.delete()

    def test_create_new_robot_without_queue(self):
        """Test the func without queue customers."""
        robot: Robot = create_new_robot(self.robot_info)
        self.assertTrue(Robot.objects.filter(pk=robot.pk).exists())
        self.assertEqual(self.queue.num_serials(robot.serial), 1)
        self.assertEqual(self.queue.len_queue(robot.serial), 0)

        robot.delete()

    def test_create_new_robot_with_big_queue(self):
        """Test the function with more orders than robots."""
        num_orders: int = random.randint(3, 10)
        num_robots: int = random.randint(1, num_orders - 1)

        for _ in range(num_orders):
            self.queue.add(self.order_info)

        robots: List[Robot] = list()
        for i in range(num_robots):
            robot: Robot = create_new_robot(self.robot_info)

            self.assertTrue(Robot.objects.filter(pk=robot.pk).exists())
            # There are fewer robots than orders
            self.assertEqual(self.queue.num_serials(robot.serial), 0)
            self.assertEqual(self.queue.len_queue(robot.serial), num_orders - i - 1)
            robots.append(robot)

        for robot in robots:
            robot.delete()

    def test_create_new_robot_with_small_queue(self):
        """Test the function with more robots than orders."""
        num_orders: int = random.randint(1, 3)
        num_robots: int = random.randint(num_orders, num_orders + random.randint(1, 10))

        for _ in range(num_orders):
            self.queue.add(self.order_info)

        robots: List[Robot] = list()
        for i in range(num_robots):
            robot: Robot = create_new_robot(self.robot_info)

            self.assertTrue(Robot.objects.filter(pk=robot.pk).exists())

        self.assertEqual(self.queue.len_queue(self.robot_info.serial), 0)
        self.assertEqual(
            self.queue.num_serials(self.robot_info.serial), num_robots - num_orders
        )

        for robot in robots:
            robot.delete()

    def test_create_robot_when_customer_has_left(self):
        """Test the function with removed customers."""
        num_orders: int = random.randint(1, 3)
        num_robots: int = random.randint(num_orders, num_orders + random.randint(1, 10))

        for _ in range(num_orders):
            self.queue.add(self.order_info)

        # Delete customer
        self.customer.delete()

        robots: List[Robot] = list()
        for i in range(num_robots):
            robot: Robot = create_new_robot(self.robot_info)

            self.assertTrue(Robot.objects.filter(pk=robot.pk).exists())

        self.assertEqual(self.queue.len_queue(self.robot_info.serial), 0)
        self.assertEqual(self.queue.num_serials(self.robot_info.serial), num_robots)

        for robot in robots:
            robot.delete()
