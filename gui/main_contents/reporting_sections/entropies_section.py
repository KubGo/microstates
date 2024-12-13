import flet as ft
from .interfaces import AbstractReportingSection

class EntropiesSection(AbstractReportingSection):
    def __init__(self, results):
        super().__init__(results)

        self.entripies_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Maximal entropy")),
                ft.DataColumn(ft.Text("Actual entropy")),
                ft.DataColumn(ft.Text("Markov chain entropy"))
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(round(self.results.h_max, 3),
                                            weight=ft.FontWeight.BOLD,
                                            expand=True)),
                        ft.DataCell(ft.Text(round(self.results.h, 3),
                                            weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(round(self.results.h_mc, 3),
                                            weight=ft.FontWeight.BOLD))
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
            ft.Text(
                "Calculated entropies",
                size=36,
                weight=ft.FontWeight.BOLD,
                expand=True,
            ),
            ft.Divider(thickness=4),
            ft.Row(
                [
                    self.entripies_table,
                ],
            alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Divider(thickness=4)
        ]