import flet as ft
from gui.main_contents.reporting_sections.interfaces import AbstractReportingSection
from decimal import Decimal
from clustering.results.results import ComparisonResults


class StaticticalTestResultsSection(AbstractReportingSection):
    def __init__(self, results):
        super().__init__(results)

        self.p_values_table = get_p_values_table(
            markov_0=self.results.p_markov_test_0,
            markov_1=self.results.p_markov_test_1,
            markov_2=self.results.p_markov_test_2,
            symmetry=self.results.p_symmetry_test,
            homogenity=self.results.p_conditional_homogenity
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
        
        


class GroupsStatisticalTestsResultsSection(AbstractReportingSection):
    def __init__(self, results: ComparisonResults):
        super().__init__(results)

        names = results.names
        statistical_test_results = results.test_p_values
        self.controls = [
            ft.Text(f"Calculated statistical tests p-values with alpha={round(self.results.alpha, 3)}",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    expand=True,
                    ),
            ft.Divider(thickness=4),
        ]
        for name in names:
            stats = statistical_test_results[name]
            self.controls.append(ft.Column(
                [
                    ft.Text(name),
                    get_p_values_table(
                        markov_0=stats['markov0'],
                        markov_1=stats['markov1'],
                        markov_2=stats['markov2'],
                        homogenity=stats['homogenity'],
                        symmetry=stats['symmetry']
                    )
                ]
            ))
        self.controls.append(ft.Divider(thickness=4))
        
def get_p_values_table(markov_0: float,
                       markov_1: float,
                       markov_2: float,
                       symmetry: float,
                       homogenity: float) -> ft.DataTable:    
    return ft.DataTable(
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
                        ft.DataCell(ft.Text(f"{markov_0:.3e}",
                                            weight=ft.FontWeight.BOLD,
                                            expand=True)),
                        ft.DataCell(ft.Text(f"{markov_1:.3e}",
                                            weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(f"{markov_2:.3e}",
                                            weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(f"{symmetry:.3e}",
                                            weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(f"{homogenity:.3e}",
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