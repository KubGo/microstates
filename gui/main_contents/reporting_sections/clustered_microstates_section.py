import flet as ft
from flet.matplotlib_chart import MatplotlibChart
from gui.main_contents.reporting_sections.interfaces import AbstractReportingSection
import matplotlib.pyplot as plt
from clustering.results.visuals import plot_microstate, LABELS
from clustering.results.results import ComparisonResults

class ClusteredMicrostatesSeciton(AbstractReportingSection):
    def __init__(self, results):
        super().__init__(results)

        self.microstate_figures = [
            plot_microstate(microstate) for microstate in self.results.cluster_centers
        ]
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
        
class GroupsMicrostatesSection(AbstractReportingSection):
    def __init__(self, results: ComparisonResults):
        super().__init__(results)
        self.results = results
        
        self.microstates_figures = self.results.microstates_maps
        self.names = self.results.names
        labels = [
            ft.Text('Group'),
        ]
        for name in self.names:
            labels.append(ft.Text(name))
            
        microstates_images = [ft.Column(
            controls=labels,
            expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )]
        for i in range(self.results.n_microstates):
            microstates = [ft.Text(LABELS[i], size=16)]
            for name in self.names:
                microstates.append(MatplotlibChart(
                    self.microstates_figures[name][i]
                ))
            microstates_images.append(
                ft.Column(
                    controls=microstates,
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ))
        
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
