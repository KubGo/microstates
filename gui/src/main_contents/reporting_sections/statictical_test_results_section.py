import flet as ft
from .interfaces import AbstractReportingSection
from decimal import Decimal


class StaticticalTestResultsSection(AbstractReportingSection):
    def __init__(self, results):
        super().__init__(results)

        self.p_values_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Markov test 0 order")),
                ft.DataColumn(ft.Text("Markov test 1 order")),
                ft.DataColumn(ft.Text("Markov test 2 order")),
                ft.DataColumn(ft.Text("Symmetry test")),
                ft.DataColumn(ft.Text("Conditional homogenity test")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{self.results.p_markov_test_0:.3e}",
                                            weight=ft.FontWeight.BOLD,
                                            expand=True)),
                        ft.DataCell(ft.Text(f"{self.results.p_markov_test_1:.3e}",
                                            weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(f"{self.results.p_markov_test_2:.3e}",
                                            weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(f"{self.results.p_symmetry_test:.3e}",
                                            weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(f"{self.results.p_conditional_homogenity:.3e}",
                                            weight=ft.FontWeight.BOLD)),
                    ]
                )
            ],
            bgcolor=ft.colors.GREY_300,
            vertical_lines=ft.BorderSide(3, ft.colors.GREY_700),
            horizontal_lines=ft.BorderSide(3, ft.colors.GREY_700),
            horizontal_margin=25,
            border_radius=5,
        )
        self.controls = [
            ft.Text(f"Calculated statistical tests p-values with alpha={round(self.results.alpha, 3)}",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    expand=True,
                    ),
            ft.Divider(thickness=4),
            self.p_values_table,
            ft.Divider(thickness=4),
        ]