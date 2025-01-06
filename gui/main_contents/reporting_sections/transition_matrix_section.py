import flet as ft
from flet.matplotlib_chart import MatplotlibChart
from gui.main_contents.reporting_sections.interfaces import AbstractReportingSection
import seaborn as sn
import matplotlib.pyplot as plt
from clustering.results.visuals import plot_transition_matrix


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
                ]
            ),
            ft.Divider(thickness=4),
        ]
        plt.close('all')
