from .interfaces import AbstractMainContent
import flet as ft
from .reports_tabs import ResultsTab
from pathlib import Path
from gui.results_observers import ResultsInfo

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
        self.session_results = SessionResults(self)

        self.select_reports_section = ft.ResponsiveRow(
            [
                ft.Column(col={"md": 6}, controls=[self.session_results]),
                ft.Column(col={"md": 3}, controls=[
                    ft.ElevatedButton(
                    "Select results file",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click= lambda _: self.pick_results_dialog.pick_files(
                        allow_multiple=False,
                        allowed_extensions=['pickle',],
                        initial_directory='/home/kuba/repositories/microstates/prototyping/guitest/P01/K-means/Fitness/results/08_12_24_model.pickle'
                    ),
                )]),
            ], 
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
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
            self.add_new_report(file_path)

    def add_new_report(self, file_path: str):
        tab = ResultsTab(file_path)
        if self.placeholder_tab in self.reports_tabs.tabs:
            self.reports_tabs.tabs.remove(self.placeholder_tab)
        self.reports_tabs.tabs.append(tab)
        new_tab_index = self.reports_tabs.tabs.index(tab)
        self.reports_tabs.selected_index = new_tab_index
        self.reports_tabs.update()


class SessionResults(ft.Container):
    def __init__(self, reports_page: ReportsPage):
        super().__init__()
        self.current_session_list = ft.ListView(
            controls=[],
            spacing=10,
            padding=ft.Padding(10, 10, 50, 10)
        )
        self.bgcolor = ft.colors.WHITE38
        self.border = ft.border.all(2, color=ft.colors.BLACK)
        self.border_radius = ft.border_radius.all(5)
        self.reports_page = reports_page
        self.place_holder = ft.Text("No results in current session.")
        self.current_session_list.controls = [self.place_holder]
        self.height = 100
        # self.padding = ft.Padding(bottom=0, left=20, right=20, top=0)
        self.margin = ft.Margin(20, 0, 50, 0)
        self.scroll = ft.ScrollMode.ADAPTIVE
        self.content = self.current_session_list

    def add_result(self, results: ResultsInfo):
        btn = ft.FilledButton(text=results.results_name,
                              on_click=lambda e : self.reports_page.add_new_report(
                                  results.results_path,
                              ),
                              expand=False,
                              )
        if self.place_holder is not None:
            self.current_session_list.controls = []
            self.place_holder = None
        self.current_session_list.controls.append(btn)
