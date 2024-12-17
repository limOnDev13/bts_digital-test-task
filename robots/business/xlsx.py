from tempfile import NamedTemporaryFile
from typing import List, Set

from openpyxl import Workbook

from .models import ProducedRobots, ProducedRobotsSummary


class ProducedRobotsXLSX(ProducedRobotsSummary):
    def __init__(self, summary: List[ProducedRobots]):
        super().__init__(summary)
        self.wb = Workbook()

    def create_sheets_with_headers(self):
        models: Set[str] = {robot.model for robot in self.produced_robots}
        for model in models:
            ws = self.wb.create_sheet(model)
            ws.append(ProducedRobots.fields())

    def write_in_workbook(self):
        for robot in self.produced_robots:
            self.wb[robot.model].append(robot.data_in_list)

    def save_file(self, tmp: NamedTemporaryFile) -> None:
        self.create_sheets_with_headers()
        self.write_in_workbook()
        self.wb.save(tmp.name)