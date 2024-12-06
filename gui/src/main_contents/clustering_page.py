from .interfaces import AbstractMainContent
import flet as ft
from .clustering_sections.file_picker import SelectFilesSection
from .clustering_sections.delimiters_section import DelimiterSection
from .clustering_sections.interfaces import AbstractFileObserver
from .clustering_sections.signal_cutting import SignalCuttingSection
from .clustering_sections.clustering_settings import ClusteringSettingsSection

class ClusteringPageContent(AbstractMainContent):

    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.files = []
        self.files_paths = {}
        self.expand=True

        self.use_delimiters = False
        self.use_delimiters_checkbox = ft.Checkbox(
            "Use delimitered file name for data labels", 
            value=False,
            on_change= lambda e: self.show_delimiters_options(e))
        
        self.use_signals_cutting_checkbox = ft.Checkbox(
            "Delete noisy signal from start and end",
            value=False,
            on_change= lambda e: self.show_signal_cutting_options(e)
        )
        # Sections
        self.clustering_settings_section = ClusteringSettingsSection(self)
        self.select_files_section = SelectFilesSection(self)
        self.delimiters_section = DelimiterSection(self)
        self.signal_cutting_section =SignalCuttingSection(self)

        # Observers
        self.__file_observers = []
        self.register_for_file_update(self.delimiters_section)

        # Clustering button
        self.clustering_btn = ft.FilledButton(
            text="Cluster micostates",
            on_click=lambda e: self.cluster(e)
        )
        self.clustering_done_text = ft.Text("", visible=False)

        # Controls
        self.controls = [
            self.select_files_section,
            ft.Divider(height=1, color=ft.colors.BLACK),
            self.clustering_settings_section,
            ft.Divider(height=1, color=ft.colors.BLACK, thickness=2),
            self.use_delimiters_checkbox,
            self.delimiters_section,
            ft.Divider(height=1, color=ft.colors.BLACK),
            self.use_signals_cutting_checkbox,
            self.signal_cutting_section,
            ft.Divider(height=1, color=ft.colors.BLACK),
            ft.Row(
                controls=[
                    self.clustering_btn
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=False
            ),
            self.clustering_done_text

            ]
        self.delimiters_section.visible = False
        self.signal_cutting_section.visible = False

    def show_delimiters_options(self, e: ft.ControlEvent):
        self.delimiters_section.visible = e.control.value
        self.delimiters_section.update()

    def show_signal_cutting_options(self, e: ft.ControlEvent):
        self.signal_cutting_section.visible = e.control.value
        self.signal_cutting_section.update()

    def update_delimiter_label_test(self):
        if self.files:
            self.delimiter_labels_test.value = self.files[0]
        else:
            self.delimiter_labels_test.value = "Select file to test"
        self.update()
    
    def register_for_file_update(self, widget: AbstractFileObserver):
        self.__file_observers.append(widget)

    def file_update(self):
        self.files = self.select_files_section.files
        for observer in self.__file_observers:
            observer.file_update(self.files)

    def update_controller(self, controller):
        self.controller = controller

    def cluster(self, e):
        self.controller.cluster()