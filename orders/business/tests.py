"""A module with tests for business logic."""

import random
from typing import List

from django.conf import settings
from django.test import TestCase

from business.queue import CustomersQueue
from customers.models import Customer
from orders.models import Order

from .main import create_new_order
from .models import OrderInfo


class CreateNewOrderTestCase(TestCase):
    """Test case for testing the func create_new_order."""

    def setUp(self):
        """Set up tests."""
        self.serial = "R2-D2"
        self.customer = Customer.objects.create(email=settings.TEST_EMAIL)
        self.order_info = OrderInfo(
            customer_id=self.customer.pk, robot_serial=self.serial
        )
        self.queue = CustomersQueue()

    def tearDown(self):
        """Tear down tests."""
        self.customer.delete()
        self.queue.clear()

    def test_create_new_order(self):
        """Test the funс with random numbers of robots and orders."""
        num_robots: int = random.randint(0, 10)
        num_orders: int = random.randint(1, 10)

        for _ in range(num_robots):
            self.queue.increase_num(self.serial)

        orders: List[Order] = list()
        for i in range(num_orders):
            order, _ = create_new_order(self.order_info)

            self.assertTrue(Order.objects.filter(pk=order.pk).exists())

        if num_orders <= num_robots:
            self.assertEqual(
                self.queue.num_serials(self.serial), num_robots - num_orders
            )
            self.assertEqual(self.queue.len_queue(self.serial), 0)
        else:
            self.assertEqual(self.queue.num_serials(self.serial), 0)
            self.assertEqual(self.queue.len_queue(self.serial), num_orders - num_robots)

        for order in orders:
            order.delete()

    def test_create_new_order_with_large_number_of_robots(self):
        """Test the func with more robots than orders."""
        num_robots: int = random.randint(3, 10)
        num_orders: int = random.randint(1, num_robots)

        for _ in range(num_robots):
            self.queue.increase_num(self.serial)

        orders: List[Order] = list()
        for i in range(num_orders):
            order, in_stock = create_new_order(self.order_info)

            self.assertTrue(Order.objects.filter(pk=order.pk).exists())
            self.assertTrue(in_stock)
            self.assertEqual(self.queue.num_serials(self.serial), num_robots - i - 1)
            self.assertEqual(self.queue.len_queue(self.serial), 0)

            orders.append(order)

        for order in orders:
            order.delete()

    def test_create_new_order_without_robots(self):
        """Test the func without robots."""
        num_orders: int = random.randint(1, 10)

        orders: List[Order] = list()
        for i in range(num_orders):
            order, in_stock = create_new_order(self.order_info)

            self.assertTrue(Order.objects.filter(pk=order.pk).exists())
            self.assertFalse(in_stock)
            self.assertEqual(self.queue.num_serials(self.serial), 0)
            self.assertEqual(self.queue.len_queue(self.serial), i + 1)

        for order in orders:
            order.delete()
