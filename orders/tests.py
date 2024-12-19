import json
import random

from django.http import JsonResponse
from django.test import TestCase
from django.conf import settings
from django.urls import reverse

from .models import Customer
from business.queue import CustomersQueue


class CreateOrderTestCase(TestCase):

    def setUp(self):
        self.customer: Customer = Customer.objects.create(
            email=settings.TEST_EMAIL
        )
        self.robot_serial = "R2-D2"
        self.order_json = {
            "customer_id": self.customer.pk,
            "robot_serial": self.robot_serial
        }
        self.queue = CustomersQueue()

    def tearDown(self):
        self.customer.delete()
        self.queue.clear()

    def test_create_order(self):
        num_robots: int = random.randint(0, 10)
        num_orders: int = random.randint(1, 10)

        for _ in range(num_robots):
            self.queue.increase_num(self.robot_serial)

        for _ in range(num_orders):
            response: JsonResponse = self.client.post(
                reverse("orders:create_orders"),
                json.dumps(self.order_json),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 201)

        if num_robots > num_orders:
            self.assertEqual(self.queue.len_queue(self.robot_serial), 0)
            self.assertEqual(self.queue.num_serials(self.robot_serial), num_robots - num_orders)
        else:
            self.assertEqual(self.queue.len_queue(self.robot_serial), num_orders - num_robots)
            self.assertEqual(self.queue.num_serials(self.robot_serial), 0)

    def test_create_order_with_large_number_of_robots(self):
        num_robots: int = random.randint(3, 10)
        num_orders: int = random.randint(1, num_robots)

        for _ in range(num_robots):
            self.queue.increase_num(self.robot_serial)

        for i in range(num_orders):
            response: JsonResponse = self.client.post(
                reverse("orders:create_orders"),
                json.dumps(self.order_json),
                content_type="application/json",
            )

            self.assertEqual(response.status_code, 201)
            self.assertEqual(self.queue.len_queue(self.robot_serial), 0)
            self.assertEqual(self.queue.num_serials(self.robot_serial), num_robots - i - 1)

    def test_create_order_with_small_number_of_robots(self):
        num_orders: int = random.randint(1, 10)

        for i in range(num_orders):
            response: JsonResponse = self.client.post(
                reverse("orders:create_orders"),
                json.dumps(self.order_json),
                content_type="application/json",
            )

            self.assertEqual(response.status_code, 201)
            self.assertEqual(self.queue.len_queue(self.robot_serial), i + 1)
            self.assertEqual(self.queue.num_serials(self.robot_serial), 0)
