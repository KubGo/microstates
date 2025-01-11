import flet as ft
import matplotlib.pyplot as plt
from gui.main_contents.reporting_sections.interfaces import AbstractReportingSection
from clustering.results.results import ComparisonResults

LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
COLORS = [ft.colors.RED, ft.colors.BLUE, ft.colors.GREEN, ft.colors.YELLOW,
          ft.colors.PURPLE, ft.colors.PINK,ft.colors.TEAL, ft.colors.BROWN]

class ProbabilitiesSection(AbstractReportingSection):
    def __init__(self, results):
        super().__init__(results)

        self.prob_pie_chart =  draw_probabilities_pie_chart(self.results.empirical_p)
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



    
class GroupProbabilitiesSection(AbstractReportingSection):
    def __init__(self, results: ComparisonResults):
        super().__init__(results)
        self.results = results

        names = self.results.names
        charts = []
        for name in names:
            charts.append(ft.Column([
                ft.Text(f"{name}"),
                draw_probabilities_pie_chart(
                    self.results.probabilities[name]
                )
            ]))
        self.controls = [
            ft.Text(
                "Probabilities of microstates",
                size=36,
                weight=ft.FontWeight.BOLD,
                expand=True
            ),
            ft.Divider(thickness=4),
            ft.ResponsiveRow(
                controls=[
                    charts
                ]
            ),
            ft.Divider(thickness=4),
        ]

def draw_probabilities_pie_chart(probabilities: list[float]):
    return ft.PieChart(
                sections=[
                    ft.PieChartSection(
                        prob * 100,
                        title=f"{round(prob * 100, 1)}%",
                        color=COLORS[i],
                        badge=badge(LABELS[i], 40), 
                        badge_position=0.98,
                        radius=100,
                    )
                    for i, prob in enumerate(probabilities)
                ],
                sections_space=0,
                center_space_radius=0,
                expand=True
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