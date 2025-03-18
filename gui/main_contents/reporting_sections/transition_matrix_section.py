import flet as ft
from flet.matplotlib_chart import MatplotlibChart
from gui.main_contents.reporting_sections.interfaces import AbstractReportingSection
import seaborn as sn
import matplotlib.pyplot as plt
from clustering.results.visuals import plot_transition_matrix
from clustering.results.results import ComparisonResults

class TransitionMatrixSection(AbstractReportingSection):

    def __init__(self, results):
        super().__init__(results)
        fig = plot_transition_matrix(self.results.transition_matrix)
        self.controls = [
            ft.Text(
                "Transition matrix",
                size=36,
                weight=ft.FontWeight.BOLD,
                expand=True,
            ),
            ft.Divider(thickness=4),
            ft.Row(
                controls=[
                    MatplotlibChart(fig,
                                    expand=True,
                                    isolated=True)
                ],
                height=500,
            ),
            ft.Divider(thickness=4),
        ]
        plt.close('all')

class GroupsTransitionMatriciesSection(AbstractReportingSection):
    def __init__(self, results: ComparisonResults):
        super().__init__(results)
        self.results = results
        names = results.names
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        transition_matricies = results.transition_matrices

        images = [
            ft.Column(
                [
                    ft.Text(name,
                        size=16,
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.BOLD,
                        ),
                    MatplotlibChart(plot_transition_matrix(transition_matricies[name]),
                                    expand = True,
                                    isolated=True,
                                    )
                ],
                expand=2,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
            for name in names
        ]

        self.controls = [
            ft.Text(
                "Transition matrix",
                size=36,
                weight=ft.FontWeight.BOLD,
                expand=True,
            ),
            ft.Divider(thickness=4),
            ft.Row(
                controls=images,
                height=500,
            ),
            ft.Divider(thickness=4),
        ]
        plt.close('all')