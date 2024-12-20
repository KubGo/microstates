from .interfaces import AbstractMainContent
import flet as ft
from .reports_tabs import ResultsTab
from pathlib import Path

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
        self.session_results = SessionResults()

        self.select_reports_section = ft.Row(
            [
                self.session_results,
                ft.ElevatedButton(
                    "Select results file",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click= lambda _: self.pick_results_dialog.pick_files(
                        allow_multiple=False,
                        allowed_extensions=['pickle',],
                        initial_directory='/home/kuba/repositories/microstates/prototyping/guitest/P01/K-means/Fitness/results/08_12_24_model.pickle'
                    ),
                )
            ], 
            alignment= ft.MainAxisAlignment.START,
            spacing=20,

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
            if self.placeholder_tab in self.reports_tabs.tabs:
                self.reports_tabs.tabs.remove(self.placeholder_tab)
            self.add_new_report(file_path)

    def add_new_report(self, file_path: str):
        tab = ResultsTab(file_path)
        self.reports_tabs.tabs.append(tab)
        new_tab_index = self.reports_tabs.tabs.index(tab)
        self.reports_tabs.selected_index = new_tab_index
        self.reports_tabs.update()


class SessionResults(ft.ListView):
    def __init__(self):
        super().__init__()
        self.place_holder = ft.Text("No results in current session.")
        self.controls = [self.place_holder]
        self.width= 400

    def add_result(self, path: str):
        path = Path(path)
        name = path.stem
        btn = ft.FilledButton(text=name)
        if self.place_holder is not None:
            self.controls = []
            self.place_holder = None
        self.controls.append(btn)
