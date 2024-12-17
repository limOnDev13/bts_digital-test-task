from tempfile import NamedTemporaryFile
from datetime import datetime, timedelta, date
from typing import List

from .models import ProducedRobots, ProducedRobotsSummary
from .xlsx import ProducedRobotsXLSX
from .queries import produced_robots


def _get_monday() -> datetime:
    now = datetime(
        year=date.today().year,
        month=date.today().month,
        day=date.today().day,
        hour=0,
        minute=0,
        second=0
    )
    return now - timedelta(days=now.weekday())


def summary_about_produced_robots(
        tmp: NamedTemporaryFile,
        file_generator_class: ProducedRobotsSummary = ProducedRobotsXLSX
) -> None:
    summary: List[ProducedRobots] = [
        ProducedRobots(**robot)
        for robot in produced_robots(_get_monday(), datetime.now())
    ]
    file_generator = file_generator_class(summary)
    file_generator.save_file(tmp)

