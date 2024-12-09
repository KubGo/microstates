import flet as ft
from flet.matplotlib_chart import MatplotlibChart
from .interfaces import AbstractReportingSection
import matplotlib.pyplot as plt

LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

class ClusteredMicrostatesSeciton(AbstractReportingSection):
    def __init__(self, results):
        super().__init__(results)
        self.spacing = 30

        self.microstate_figures = self.results.get_microstates_figures()
        microstates_images = [ft.Column(
            [
                MatplotlibChart(figure, isolated=True),
                ft.Text(f"{LABELS[i]}", size=16)
            ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ) for i, figure in enumerate(self.microstate_figures)]

        self.controls = microstates_images
        plt.close('all')