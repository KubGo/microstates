from .interfaces import AbstractMainContent
import flet as ft
from .reports_tabs import ResultsTab

class ReportsPage(AbstractMainContent):
    def __init__(self, page):
        super().__init__(page)
        self.reports = []
        self.pick_results_dialog = ft.FilePicker(on_result=self.pick_result)
        self.page.overlay.append(self.pick_results_dialog)
        self.placeholder_tab = ft.Tab(
            text="No report selected",
            content=ft.Container(
                content=ft.Text("Select already generated reports or reports .pickle file"),
            )
        )
        self.reports_tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                self.placeholder_tab,
            ],
            animation_duration=400,
            expand=True,
        )

        self.select_reports_section = ft.Row(
            [
                ft.ElevatedButton(
                    "Select results file",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click= lambda _: self.pick_results_dialog.pick_files(
                        allow_multiple=False,
                        allowed_extensions=['pickle',],
                        initial_directory='/home/kuba/repositories/microstates/prototyping/guitest/P01/K-means/Fitness/results/08_12_24_model.pickle'
                    )
                )
            ]
        )
        self.top_text = ft.Text("Reports", 
                                text_align=ft.MainAxisAlignment.CENTER,
                                size=24,
                                weight=ft.FontWeight.BOLD)
        self.controls = [
            self.top_text,
            self.select_reports_section,
            self.reports_tabs
        ]
        
    def pick_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            file_name = e.files[0].name
            file_path = e.files[0].path
            report_tab = ResultsTab(file_path)
            if self.placeholder_tab in self.reports_tabs.tabs:
                self.reports_tabs.tabs.remove(self.placeholder_tab)
            self.reports_tabs.tabs.append(report_tab)
            new_tab_index = self.reports_tabs.tabs.index(report_tab)
            self.reports_tabs.selected_index = new_tab_index
            self.reports_tabs.update()


class SessionResults(ft.ListView):
    def __init__(self, ):
        super().__init__()
