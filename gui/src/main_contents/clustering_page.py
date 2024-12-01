from .interfaces import AbstractMainContent
import flet as ft
from .clustering_sections.file_picker import SelectFilesSection
from .clustering_sections.delimiters_section import DelimiterSection
from .clustering_sections.interfaces import AbstractFileObserver

class ClusteringPageContent(AbstractMainContent):

    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.files = []
        self.files_paths = {}

        self.use_delimiters = False
        self.use_delimiters_checkbox = ft.Checkbox(
            "Use delimitered file name for data labels", 
            value=False,
            on_change= lambda e: self.show_delimiters_options(e))
        # Sections
        self.select_files_section = SelectFilesSection(self)
        self.delimiters_section = DelimiterSection(self)

        # Observers
        self.__file_observers = []
        self.register_for_file_update(self.delimiters_section)

        # Controls
        self.controls = [
            self.select_files_section,
            self.use_delimiters_checkbox,
            self.delimiters_section,
            ]
        self.delimiters_section.visible = False

    def show_delimiters_options(self, e: ft.ControlEvent):
        self.delimiters_section.visible = e.control.value
        self.delimiters_section.update()

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

