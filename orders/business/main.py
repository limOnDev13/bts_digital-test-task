"""The module responsible for the main functions of the business logic."""

from logging import getLogger
from typing import Tuple

from business.queue import CustomersQueue
from customers.models import Customer
from orders.models import Order

from .models import OrderInfo

logger = getLogger("view.business")


def create_new_order(order_info: OrderInfo) -> Tuple[Order, bool]:
    """
    Deliver an order or add a customer to the queue for the selected series.

    The function sends the order to the customer.
    If the selected series is not in stock,
    the function adds the user to the queue.
    When the goods appear in the warehouse and the customer's turn comes,
    a notification letter will be sent to him.
    :param order_info: Info about customer.
    :return: order and True if the product is in stock, otherwise False
    """
    logger.debug("Creating a new order...")
    customer = Customer.objects.get(pk=order_info.customer_id)
    order: Order = Order.objects.create(
        customer=customer, robot_serial=order_info.robot_serial
    )
    queue = CustomersQueue()

    if queue.num_serials(order_info.robot_serial) == 0:
        logger.debug("This serial is not available, adding it to the queue...")
        queue.add(order_info)
        logger.debug("Done")
        return order, False
    else:
        logger.debug("This serial is in stock, sending an order...")
        # The logic of sending an order
        queue.decrease_num(order_info.robot_serial)
        logger.debug("Done")
        return order, True
