import flet as ft
from .interfaces import AbstractSection, AbstractFileObserver
from .utils import check_if_all_numeric

class DelimiterSection(AbstractSection):

    def __init__(self, content_page):
        super().__init__(content_page)

        self.words = []

        self.delimiter_selector = ft.RadioGroup(
            content=ft.Column([
                ft.Text("Delimiter:"),
                ft.Row([
                ft.Radio(value="_", label="_", ),
                ft.Radio(value="-", label="-"),
                ft.Radio(value="|", label="|")
                ])
            ]), value='_',
            on_change=lambda e : self.delimiter_change(e))
        self.id_index_entry = ft.TextField(
                value="1",
                label='Index of the identifier',
                on_change= lambda e: self.id_entry_change(e)
                )
        self.activity_index_entry = ft.TextField(
                value="2",
                label="Index of the activity",
                on_change= lambda e: self.activity_entry_change(e)
            )
        self.example = ExampleText(self)

        # Content of section
        self.controls = [
            self.delimiter_selector,
            self.id_index_entry,
            self.activity_index_entry,
            self.example
        ]
    
    def file_update(self, files):
        self.example.file_update(files)
        self.update()

    def delimiter_change(self, e):
        self.delimiter_selector.value = e.control.value
        self.delimiter_selector.update()
        self.file_update(self.content_page.files)


    def id_entry_change(self, e):
        check_if_all_numeric(e)
        text = e.control.value
        self.example.update_id(text, self.words)

    def activity_entry_change(self, e):
        check_if_all_numeric(e)
        text = e.control.value
        self.example.update_activity(text, self.words)

class ExampleText(AbstractFileObserver, ft.Column):

    def __init__(self, section: DelimiterSection):
        super(ft.Column, self).__init__()
        self.section = section
        self.expand = True
        self.horizontal_alignment = ft.alignment.center
        self.place_holder_text = "Select a file"
        self.file_name = ft.Text(self.place_holder_text, size=20, weight=ft.FontWeight.BOLD)
        self.id = ft.Text('', color=ft.colors.WHITE)
        self.activity = ft.Text('', color=ft.colors.WHITE)
        self.delimiter = '_'
        self.controls = [
            self.file_name,
            ft.Container(content=
                ft.Row([
                ft.Text("Id: ", color=ft.colors.WHITE),
                self.id
            ]),
            bgcolor='#006f27',
            margin= 2,
            padding= 10,
            border_radius=10,
            )
            ,
            ft.Container(
                content=ft.Row([
                ft.Text("Activity: ", color=ft.colors.WHITE),
                self.activity
            ]),
            bgcolor='#006f27',
            margin= 2,
            padding= 10,
            border_radius=10
            )
            
        ]

    def file_update(self, files):
        if not files:
            self.reset_values()
            return
        else:
            file = files[0]
        # Update file name
        self.update_file_name(file)
        # Update for delimiter selected
        delimiter = self.section.delimiter_selector.value
        self.delimiter = delimiter

        words = file.split(delimiter)
        if len(words) <= 1:
            self.wrong_delimiter(delimiter)
            self.section.words = []
            return
        self.section.words = words
        # Update id and activity example texts
        self.update_id(self.section.id_index_entry.value, words)
        self.update_activity(self.section.activity_index_entry.value, words)
        
    def update_file_name(self, file_name:str):
        self.file_name.value = file_name
        self.file_name.update()
    
    def update_id(self, index: str, words: list):
        if not words:
            self.wrong_delimiter(self.delimiter)
            return
        new_value = ""
        if not index.isdigit():
            new_value = "Use only digits"
        else:
            index = int(index)
            if index < 1 or index > len(words):
                new_value = f"Index out of bounds (1-{len(words)})"
            else:
                new_value = words[index - 1]
        self.id.value = new_value
        self.id.update()

    def update_activity(self, index, words):
        new_value = ""
        if not index.isdigit():
            new_value = "Use only digits"
        else:
            index = int(index)
            if index < 1 or index > len(words):
                new_value = f"Index out of bounds (1-{len(words)})"
            else:
                new_value = words[index - 1]
        self.activity.value = new_value
        self.activity.update()
    
    def wrong_delimiter(self, delimiter):
        self.id.value = f"\"{delimiter}\" not in file name"
        self.activity.value = f"\"{delimiter}\" not in file name"
        self.update()
    
    def reset_values(self):
        self.file_name.value = self.place_holder_text
        self.id.value = ''
        self.activity.value = ''
        self.update()
