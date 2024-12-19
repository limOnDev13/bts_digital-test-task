"""A module with models for the business logic of the robots app."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


@dataclass
class RobotInfo:
    """Class for storing info about the robot."""

    serial: str
    model: str
    version: str
    created: str

    def to_dict(self) -> Dict[str, Any]:
        """Return dict with info about the robot."""
        return {
            "serial": self.serial,
            "model": self.model,
            "version": self.version,
            "created": self.created,
        }


@dataclass
class ProducedRobots:
    """Class for storing information about produced robots."""

    model: str
    version: str
    num_robots: int

    @classmethod
    def fields(cls) -> Tuple[str, str, str]:
        """Get fields in the class."""
        return "model", "version", "num_robots"

    @property
    def data_in_list(self) -> List[Any]:
        """Get data in list."""
        return [getattr(self, field) for field in self.fields()]


class ProducedRobotsSummary(ABC):
    """
    An abstract class for saving a summary to a temporary named file.

    Args:
        summary (List[ProducedRobots]): a summary of the robots produced
         that needs to be saved.
    """

    def __init__(self, summary: List[ProducedRobots]):
        self.produced_robots = summary

    @abstractmethod
    def save_file(self, tmp) -> None:
        """
        Save the summary to a temporary file.

        :param tmp: an open temporary file object (using tempfile.NamedTemporaryFile).
        :return: None
        """
        pass
