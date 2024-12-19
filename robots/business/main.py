from datetime import date, datetime, timedelta
from logging import getLogger
from typing import List, Optional, Type

from business.email_sender import send_email
from business.queue import CustomersQueue
from customers.models import Customer
from robots.models import Robot

from .models import ProducedRobots, ProducedRobotsSummary, RobotInfo
from .queries import produced_robots
from .xlsx import ProducedRobotsXLSX

logger = getLogger("view.business")


def _get_monday() -> datetime:
    """Get the Monday of the current week with the time 00:00:00."""
    now = datetime(
        year=date.today().year,
        month=date.today().month,
        day=date.today().day,
        hour=0,
        minute=0,
        second=0,
    )
    return now - timedelta(days=now.weekday())


def summary_about_produced_robots(
    tmp,
    file_generator_class: Type[ProducedRobotsSummary] = ProducedRobotsXLSX,
) -> None:
    """
    Return a summary of the total robot production figures for the last week.

    The function takes an open named temporary file
    and saves a summary to it using the ProducedRobotsSummary class.
    :param tmp: an open temporary file object (using tempfile.NamedTemporaryFile).
    :param file_generator_class: a class for creating a summary file
    :return: None
    """
    summary: List[ProducedRobots] = [
        ProducedRobots(**robot)
        for robot in produced_robots(_get_monday(), datetime.now())
    ]
    file_generator = file_generator_class(summary)
    file_generator.save_file(tmp)


def create_new_robot(robot_info: RobotInfo) -> Robot:
    logger.debug("Creating a new robot...")
    robot: Robot = Robot.objects.create(**robot_info.to_dict())
    queue = CustomersQueue()

    if queue.len_queue(robot.serial) > 0:
        logger.debug(
            "There is a queue of buyers for this series. Queue length: %d",
            queue.len_queue(robot.serial),
        )
        customer_id: int = queue.pop(robot.serial)
        customer: Optional[Customer] = Customer.objects.filter(pk=customer_id).first()

        # While the robot was being created, customers could leave the queue
        while customer is None:
            logger.warning(f"Customer with id {customer_id} not exists.")

            if queue.len_queue(robot.serial) > 0:
                customer_id = queue.pop(robot.serial)
                customer = Customer.objects.filter(pk=customer_id).first()
            else:
                queue.increase_num(robot.serial)
                break
        else:
            # If we didn't catch a break,
            # then there was an existing customer in the queue
            send_email(email=customer.email, model=robot.model, version=robot.version)
    else:
        logger.debug("There are no customers in the queue for this model")
        queue.increase_num(robot.serial)

    return robot
