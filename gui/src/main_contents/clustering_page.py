from .interfaces import AbstractMainContent
import flet as ft
from .clustering_sections.file_picker import SelectFilesSection

class ClusteringPageContent(AbstractMainContent):



    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.files = []
        self.files_paths = {}
        self.select_files_section = SelectFilesSection(self)
        self.use_delimiters = False
        self.delimiter_labels_test = ft.Text("No file selected")
        self.delimiter_selector = ft.Row(
            controls=[
                ft.RadioGroup(content=ft.Column([
                    ft.Text("Delimiter:"),
                    ft.Row([
                    ft.Radio(value="_", label="_", ),
                    ft.Radio(value="-", label="-"),
                    ft.Radio(value="|", label="|")
                    ])
                ]), value='_'),
                ft.TextField(
                    value="1",
                    label='Index of the identifier',
                    on_change= lambda e: self.check_if_all_numeric(e)
                    ),
                ft.TextField(
                    value="2",
                    label="Index of the activity",
                    on_change= lambda e: self.check_if_all_numeric(e)
                ),
                self.delimiter_labels_test
            ],
        )
        self.controls = [
            self.select_files_section,
            ft.Checkbox(
            "Use delimitered file name for data labels", 
            value=False,
            on_change= lambda e: self.show_delimiters_options(e)),
            self.delimiter_selector,
            ]
        self.delimiter_selector.visible = self.use_delimiters

        


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
