from clustering.results.Results import load_results, Results
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
from flet.plotly_chart import PlotlyChart
import matplotlib.pyplot as plt
import matplotlib
import plotly.express as px
import plotly.graph_objects as go
from .reporting_sections.transition_matrix_section import TransitionMatrixSection

LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
COLORS = [ft.colors.RED, ft.colors.BLUE, ft.colors.GREEN, ft.colors.YELLOW,
          ft.colors.PURPLE, ft.colors.PINK,ft.colors.TEAL, ft.colors.BROWN]

class ResultsTab(ft.Tab):
    def __init__(self, results_path: str):
        super().__init__()
        matplotlib.use("svg")

        self.results = load_results(results_path)
        self.text = f"{self.results.id}- {self.results.activity}"
        self.microstate_figures = self.results.get_microstates_figures()
        microstates_images = [ft.Column(
            [
                MatplotlibChart(figure, isolated=True),
                ft.Text(f"{LABELS[i]}", size=16)
            ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ) for i, figure in enumerate(self.microstate_figures)]
        self.obtained_microstates = ft.Row(
            controls=microstates_images,
            spacing=30,
        )
        
        self.prob_pie_chart = ft.PieChart(
            sections=[
                ft.PieChartSection(
                    prob * 100,
                    title=f"{round(prob * 100, 1)}%",
                    color=COLORS[i],
                    badge=badge(LABELS[i], 40), 
                    badge_position=0.98,
                    radius=100
                )
                for i, prob in enumerate(self.results.empirical_p)
            ],
            sections_space=0,
            center_space_radius=0,
        )
        plt.close('all')

        self.transition_matrix_section = TransitionMatrixSection(self.results)
        
        self.report_content = ft.Column(
            controls=[
                self.obtained_microstates,
                self.prob_pie_chart,
                self.transition_matrix_section
            ],
            scroll=True,
        )
        
        self.content = ft.Container(
            content=self.report_content,
        )


def badge(letter, size):
    return ft.Container(
        ft.Text(letter, weight=ft.FontWeight.BOLD),
        width=size,
        height=size,
        border=ft.border.all(1, ft.colors.BLACK),
        border_radius=size / 2,
        bgcolor=ft.colors.WHITE,
        alignment=ft.alignment.center
    )