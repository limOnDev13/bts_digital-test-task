from datetime import datetime
from typing import Sequence
from logging import getLogger

from django.db.models import Count, QuerySet

from robots.models import Robot

logger = getLogger("view.query")


def produced_robots(start_date: datetime, end_date: datetime) -> QuerySet:
    """Get info about the produced robots between start_date and end_date."""
    logger.debug("Start getting robots")
    q = (Robot.objects.filter(created__gte=start_date, created__lte=end_date)
         .values("model", "version").annotate(num_versions=Count("version")))
    result = q.all()

    logger.debug("Result: %s", str(result))
    return result
