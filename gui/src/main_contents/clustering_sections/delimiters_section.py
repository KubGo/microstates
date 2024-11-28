import flet as ft
from .interfaces import AbstractSection
from .utils import check_if_all_numeric

class DelimiterSection(AbstractSection):

    def __init__(self, content_page):
        super().__init__(content_page)

        self.delimiter_selector = ft.RadioGroup(
            content=ft.Column([
                ft.Text("Delimiter:"),
                ft.Row([
                ft.Radio(value="_", label="_", ),
                ft.Radio(value="-", label="-"),
                ft.Radio(value="|", label="|")
                ])
            ]), value='_')
        self.id_index_entry = ft.TextField(
                value="1",
                label='Index of the identifier',
                on_change= lambda e: check_if_all_numeric(e)
                )
        self.activity_index_entry = ft.TextField(
                value="2",
                label="Index of the activity",
                on_change= lambda e: check_if_all_numeric(e)
            )
        self.example = ft.Text("No file selected")

        # Content of section
        self.controls = [
            self.delimiter_selector,
            self.id_index_entry,
            self.activity_index_entry,
            self.example
        ]