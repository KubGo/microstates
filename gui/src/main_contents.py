from abc import ABC, abstractmethod
from flet import Column, Page, Markdown, alignment, MarkdownExtensionSet, Row, Text, FilePicker, ElevatedButton, FilePickerResultEvent, icons, ListView, Container
import flet as ft
from file_read import FileList

class AbstractMainContent(ABC, Column):

    def __init__(self, page: Page):
        super(Column, self).__init__()
        self.page = page


class HomePageContent(AbstractMainContent):

    def __init__(self, page: Page):
        super().__init__(page)
        self.expand = True
        self.alignment = alignment.center
        self.horizontal_alignment = alignment.center

        md_text = """
# Welcome to Microstates app!
This app is a GUI for clustering of microstates. For now, it's in its development phase and there's hardly anything that works here, but I hope that one day it will be working app, that people without any programming knowledge can use to cluster and analyze microstates.
If You want to learn more about microstates, You can use this [GitHub page](https://frederic-vw.github.io/eeg-patterns/).
        """
        self.controls = [
            Markdown(
                md_text,
                extension_set=MarkdownExtensionSet.GITHUB_WEB,
                on_tap_link=lambda e: self.page.launch_url(e.data),
                fit_content=True
            )
        ]


class ClusteringPageContent(AbstractMainContent):

    def pick_files_results(e: FilePickerResultEvent, text: Text):
        text.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!" 
        )
        text.update()

    def __init__(self, page: Page):
        super().__init__(page)
        self.pick_files_dialog = FilePicker(on_result=self.pick_files_results)
        self.page.overlay.append(self.pick_files_dialog)
        self.files = []
        self.files_paths = {}
        self.selected_files = FileList()

        self.controls = [
            Row(
                [
                    Text("Chose a file with EEG data in csv format"),
                ElevatedButton(
                    "Pick files",
                    icon=icons.UPLOAD_FILE,
                    on_click=lambda _: self.pick_files_dialog.pick_files(
                        allow_multiple=True,
                        initial_directory='/home/kuba/Desktop/test/file_1'
                    )
                ),
                Container(
                    Column(
                        controls=[self.selected_files],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                        ),
                    expand=True,
                    bgcolor=ft.colors.WHITE,
                    border_radius=ft.border_radius.all,

                ),
                ft.TextField(
                    label="Signal frequency",
                    value=250,
                    hint_text="e.g. 250",
                    on_change= lambda e: self.check_if_all_numeric(e))
        ])
                
            ]
        
    def pick_files_results(self, e: FilePickerResultEvent):
        files = [(f.name, f.path) for f in e.files]
        self.update_selected_files(files)

    def update_selected_files(self, files):
        for file in files:
            self.selected_files.add_file(file[0], file[1])
        self.selected_files.update()
        
    def check_if_all_numeric(self, e: ft.ControlEvent):
        text = e.control.value
        if text.isdigit() or text == '':
            e.control.error_text = None
            e.control.update()
        else:
            e.control.error_text = "Only numbers are allowed!"
            e.control.update()
