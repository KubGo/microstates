import flet as ft
from abc import ABC
from clustering.results import Results

class AbstractReportingSection(ft.Row, ABC):

    def __init__(self, results: Results):
        super(ft.Row, self).__init__()
        self.results = results


