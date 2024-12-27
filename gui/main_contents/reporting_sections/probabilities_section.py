import flet as ft
import matplotlib.pyplot as plt
from .interfaces import AbstractReportingSection


LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
COLORS = [ft.colors.RED, ft.colors.BLUE, ft.colors.GREEN, ft.colors.YELLOW,
          ft.colors.PURPLE, ft.colors.PINK,ft.colors.TEAL, ft.colors.BROWN]

class ProbabilitiesSection(AbstractReportingSection):
    def __init__(self, results):
        super().__init__(results)

        self.prob_pie_chart = ft.PieChart(
            sections=[
                ft.PieChartSection(
                    prob * 100,
                    title=f"{round(prob * 100, 1)}%",
                    color=COLORS[i],
                    badge=self.badge(LABELS[i], 40), 
                    badge_position=0.98,
                    radius=100,
                )
                for i, prob in enumerate(self.results.empirical_p)
            ],
            sections_space=0,
            center_space_radius=0,
            expand=True
        )
        self.controls = [
            ft.Text(
                "Probabilities of microstates",
                size=36,
                weight=ft.FontWeight.BOLD,
                expand=True
            ),
            ft.Divider(thickness=4),
            ft.Row(
                controls=[
                    self.prob_pie_chart
                ]
            ),
            ft.Divider(thickness=4),
        ]


    def badge(self, letter, size):
        return ft.Container(
            ft.Text(letter, weight=ft.FontWeight.BOLD),
            width=size,
            height=size,
            border=ft.border.all(1, ft.colors.BLACK),
            border_radius=size / 2,
            bgcolor=ft.colors.WHITE,
            alignment=ft.alignment.center
        )