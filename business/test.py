"""A module with tests for basic business logic."""

import random

import redis
from django.conf import settings
from django.test import TestCase

from orders.business.models import OrderInfo

from .queue import CustomersQueue


class CustomerQueueTestCase(TestCase):
    """Test case for testing CustomerQueue."""

    def setUp(self):
        """Set up tests."""
        self.queue = CustomersQueue()
        self.queue.clear()
        self.client = redis.StrictRedis(
            host=settings.REDIS_HOST,
            charset="utf-8",
            decode_responses=True,
        )
        self.serial = "R2-D2"
        self.queue_name = f"queue_{self.serial}"
        self.order_info = OrderInfo(customer_id=1, robot_serial=self.serial)
        self.client.set(self.serial, 0)

    def tearDown(self):
        """Tear down tests."""
        self.client.delete(self.serial)
        self.queue.clear()

    def test_increase_num(self):
        """Test the method CustomersQueue.increase_num."""
        test_num: int = random.randint(5, 10)

        for _ in range(test_num):
            self.queue.increase_num(self.serial)

        self.assertEqual(int(self.client.get(self.serial)), test_num)

    def test_decrease_num(self):
        """Test the method CustomersQueue.decrease_num."""
        test_num: int = random.randint(5, 10)

        for _ in range(test_num):
            self.queue.increase_num(self.serial)

        self.assertEqual(int(self.client.get(self.serial)), test_num)

        self.queue.decrease_num(self.serial)
        self.assertEqual(int(self.client.get(self.serial)), test_num - 1)

        for _ in range(test_num - 1):
            self.queue.decrease_num(self.serial)

        self.assertEqual(int(self.client.get(self.serial)), 0)

        for _ in range(random.randint(5, 10)):
            self.queue.decrease_num(self.serial)
        self.assertEqual(int(self.client.get(self.serial)), 0)

    def test_num_serials(self):
        """Test the method CustomersQueue.num_serials."""
        test_num: int = random.randint(5, 10)

        for _ in range(test_num):
            self.queue.increase_num(self.serial)
        self.assertEqual(self.queue.num_serials(self.serial), test_num)

        not_existing_serial: str = "XX"
        if self.client.exists(not_existing_serial):
            self.client.delete(not_existing_serial)
        self.assertEqual(self.queue.num_serials(not_existing_serial), 0)

    def test_add(self):
        """Test the method CustomersQueue.add."""
        len_queue = random.randint(5, 10)

        for _ in range(len_queue):
            self.queue.add(self.order_info)

        self.assertTrue(self.client.exists(self.queue_name))
        self.assertEqual(self.client.llen(self.queue_name), len_queue)

    def test_pop(self):
        """Test the method CustomersQueue.pop."""
        len_queue = random.randint(5, 10)

        for _ in range(len_queue):
            self.queue.add(self.order_info)

        for i in range(len_queue):
            self.assertEqual(self.client.llen(self.queue_name), len_queue - i)
            self.assertEqual(self.queue.pop(self.serial), 1)

    def test_len_queue(self):
        """Test the method CustomersQueue.len_queue."""
        len_queue = random.randint(5, 10)

        for _ in range(len_queue):
            self.queue.add(self.order_info)

        self.assertEqual(self.queue.len_queue(self.serial), len_queue)

        not_existing_queue: str = "queue_XX-11"
        if self.client.exists(not_existing_queue):
            self.client.delete(not_existing_queue)
        self.assertEqual(self.queue.len_queue(not_existing_queue), 0)
