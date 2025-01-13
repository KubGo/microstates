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
        self.expand = True
        self.microstates_maps = self.results.microstates_maps
        self.names = self.results.names
        labels = ft.Row([
                    ft.Text(
                        value='Group',
                        expand=1,
                        text_align=ft.TextAlign.CENTER),
                ],
                vertical_alignment=ft.CrossAxisAlignment.START,
                alignment=ft.alignment.top_center,
                expand=True)
        for i in range(results.n_microstates):
            labels.controls.append(ft.Text(
                value=f"{LABELS[i]}",
                expand=2,
                size=16,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD))
        microstates_images = []

        for name in self.names:
            microstates_row = ft.Row(
                controls=[ft.Text(
                    value=name, 
                    expand=True, 
                    size=16,
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD)],
                expand=1,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
            for microstate in self.microstates_maps[name]:
                microstates_row.controls.append(MatplotlibChart(
                                    plot_microstate(microstate),
                                    expand=2,
                                ))
            microstates_images.append(microstates_row)

        
        self.controls = [
                ft.Text("Obtained microstates",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    expand=True,
                    ),
            ft.Divider(thickness=4),
            labels
        ] + microstates_images
