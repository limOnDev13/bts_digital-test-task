"""The module responsible for the operation of the customer queue."""

from logging import getLogger

import redis
from django.conf import settings

from orders.business.models import OrderInfo

logger = getLogger("view.queue")

redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    charset="utf-8",
    decode_responses=True,
)


class CustomersQueue:
    """Class - the queue of customers."""

    def __init__(self):
        self.client = redis_client

    def num_serials(self, serial: str) -> int:
        """Get the number of robots of the selected series in stock."""
        num = self.client.get(serial)
        if num is None:
            self.client.set(serial, 0)
            return 0
        elif isinstance(num, str):
            return int(num)
        else:
            raise ValueError("num is not str.")

    def increase_num(self, serial: str) -> None:
        """Increase the number of robots of this series in stock by 1."""
        self.client.incr(serial)

    def decrease_num(self, serial: str) -> None:
        """Decrease the number of robots of this series in stock by 1."""
        if self.num_serials(serial) > 0:
            self.client.decr(serial)

    def add(self, order_info: OrderInfo) -> None:
        """Add a customer to the queue."""
        self.client.rpush(
            f"queue_{order_info.robot_serial}", str(order_info.customer_id)
        )
        logger.debug("Customer added in queue.")

    def pop(self, serial: str) -> int:
        """
        Delete the first client in the queue.

        :param serial: Robot serial.
        :return: Customer id
        """
        queue_key: str = f"queue_{serial}"
        if not self.client.exists(queue_key):
            raise KeyError(f"There is no queue for the serial {queue_key}")

        customer_id_str = self.client.lpop(queue_key)
        if isinstance(customer_id_str, str):
            customer_id = int(customer_id_str)
        else:
            raise ValueError("customer_id_str is not str.")

        self.decrease_num(serial)

        logger.debug("The customer has received his order.")
        return customer_id

    def len_queue(self, serial: str) -> int:
        """
        Get the queue length for this series.

        :param serial: Robot serial.
        :return: Queue length for this series.
        """
        if not self.client.exists(f"queue_{serial}"):
            return 0

        len_queue = self.client.llen(f"queue_{serial}")
        if isinstance(len_queue, int):
            return len_queue
        else:
            raise ValueError("len_queue is not int.")

    def clear(self):
        """Clear all keys in redis."""
        for key in self.client.scan_iter():
            self.client.delete(key)
