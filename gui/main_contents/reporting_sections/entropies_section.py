import flet as ft
from gui.main_contents.reporting_sections.interfaces import AbstractReportingSection
from clustering.results.results import ComparisonResults

class EntropiesSection(AbstractReportingSection):
    def __init__(self, results):
        super().__init__(results)

        self.entripies_table = get_entropies_table(
            self.results.h,
            self.results.h_max,
            self.results.h_mc,
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

class GroupsEntropiesSection(AbstractReportingSection):
    def __init__(self, results: ComparisonResults):
        super().__init__(results)
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.results = results
        self.names = self.results.names
        self.entropies = self.results.entropies
        header = [
            ft.Text("Calculated entropies",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    expand=True,
            ),
            ft.Divider(thickness=4)]
        entropies_tables = []
        for name in self.names:
            entropies_tables.append(ft.Column(
                [ft.Text(f"{name}",
                        size=16,
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.BOLD,
                        ),
                get_entropies_table(
                    self.entropies[name]['h'],
                    self.entropies[name]['h_max'],
                    self.entropies[name]['h_mc']
                )],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=2,
            ))
        tables = [ft.Row(entropies_tables)]
        self.controls = header + tables + [ft.Divider(thickness=4)]
        

def get_entropies_table(h, h_max, h_mc): 
    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Maximal entropy")),
            ft.DataColumn(ft.Text("Actual entropy")),
            ft.DataColumn(ft.Text("Markov chain entropy"))
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(round(h_max, 3),
                                        weight=ft.FontWeight.BOLD,
                                        expand=True)),
                    ft.DataCell(ft.Text(round(h, 3),
                                        weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Text(round(h_mc, 3),
                                        weight=ft.FontWeight.BOLD))
                ]
            )
        ],
        bgcolor=ft.colors.SECONDARY_CONTAINER,
        vertical_lines=ft.BorderSide(3, ft.colors.ON_SECONDARY_CONTAINER ),
        horizontal_lines=ft.BorderSide(3, ft.colors.ON_SECONDARY_CONTAINER),
        horizontal_margin=25,
        border_radius=5,
    )