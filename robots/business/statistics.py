from datetime import date, datetime, timedelta
from typing import List, Type

from .models import ProducedRobots, ProducedRobotsSummary
from .queries import produced_robots
from .xlsx import ProducedRobotsXLSX


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
