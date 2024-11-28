from .interfaces import AbstractMainContent
import flet as ft
from .clustering_sections.file_picker import SelectFilesSection
from .clustering_sections.delimiters_section import DelimiterSection

class ClusteringPageContent(AbstractMainContent):



    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.files = []
        self.files_paths = {}

        self.use_delimiters = False
        self.use_delimiters_checkbox = ft.Checkbox(
            "Use delimitered file name for data labels", 
            value=False)
        # Sections
        self.select_files_section = SelectFilesSection(self)
        self.delimiters_section = DelimiterSection(self)
        self.controls = [
            self.select_files_section,
            self.use_delimiters_checkbox,
            self.delimiters_section,
            ]

        


    def show_delimiters_options(self, e: ft.ControlEvent):
        changed_value = not self.delimiter_selector.visible
        self.delimiter_selector.visible = changed_value
        self.use_delimiters = changed_value
        if changed_value:
            self.update_delimiter_label_test()
        self.page.update()

    def update_delimiter_label_test(self):
        if self.files:
            self.delimiter_labels_test.value = self.files[0]
        else:
            self.delimiter_labels_test.value = "Select file to test"
        self.update()
