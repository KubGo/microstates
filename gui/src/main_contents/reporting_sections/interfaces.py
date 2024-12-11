import flet as ft
from abc import ABC
from clustering.results import Results

class AbstractReportingSection(ft.Column, ABC):

    def __init__(self, results: Results):
        super(ft.Column, self).__init__()
        self.results = results
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.expand = True
