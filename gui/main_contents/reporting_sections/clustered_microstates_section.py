import flet as ft
from flet.matplotlib_chart import MatplotlibChart
from .interfaces import AbstractReportingSection
import matplotlib.pyplot as plt

LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

class ClusteredMicrostatesSeciton(AbstractReportingSection):
    def __init__(self, results):
        super().__init__(results)

        self.microstate_figures = self.results.get_microstates_figures()
        microstates_images = [ft.Column(
            [
                MatplotlibChart(figure, isolated=True),
                ft.Text(f"{LABELS[i]}", size=16)
            ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ) for i, figure in enumerate(self.microstate_figures)]

        self.controls = [
                ft.Text("Obtained microstates",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    expand=True,
                    ),
            ft.Divider(thickness=4),
            ft.Row(controls=microstates_images,
            spacing = 30),
            ft.Divider(thickness=4),

        ]
        plt.close('all')