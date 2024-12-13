import flet as ft
from gui.main_contents.interfaces import AbstractMainContent
from gui.main_contents.clustering_sections.interfaces import AbstractSection
from .utils import check_if_all_numeric
class SelectFilesSection(AbstractSection):
    def __init__(self, content_page: AbstractMainContent):
        super().__init__(content_page)
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_results)
        self.content_page.page.overlay.append(self.pick_files_dialog)
        self.selected_files = FileList(self)
        self.frequency_entry = ft.TextField(
            label="Signal frequency",
            value=250,
            hint_text="e.g. 250",
            on_change= lambda e: check_if_all_numeric(e))
        self.observers = [self.content_page]
        
        # Content of section
        self.controls = [
            ft.Text("Chose a file with EEG data in csv format"),
            ft.ElevatedButton(
                "Pick files",
                icon=ft.icons.UPLOAD_FILE,
                on_click=lambda _: self.pick_files_dialog.pick_files(
                    allow_multiple=True,
                    initial_directory='/home/kuba/Desktop/reordering/data/all_data/P01/P01_Fitness_Activity_clean_signal.csv'
                )
            ),
            ft.Container(
                ft.Column(
                    controls=[self.selected_files],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    ),
                expand=True,
                bgcolor=ft.colors.WHITE,
                border_radius=ft.border_radius.all,
            ),
            self.frequency_entry,
        ]
                 
    def pick_files_results(self, e: ft.FilePickerResultEvent):
        if e.files:
            files = [(f.name, f.path) for f in e.files]
            self.update_selected_files(files)

    def update_selected_files(self, files):
        for file in files:
            self.selected_files.add_file(file[0], file[1])
        self.selected_files.update()
        self.files = self.selected_files.get_file_names()
        self.file_update()

    def register_for_file_updates(self, *args):
        for observer in args:
            self.observers.append(observer)

    def file_update(self):
        self.files = self.selected_files.get_file_names()
        for observer in self.observers:
            observer.file_update()

class FileList(ft.ListView):

    def __init__(self, section: AbstractSection):
        super().__init__(height=90)
        self.section = section
        self.controls = []
    
    def add_file(self, name: str, path: str):
        file = FileInterface(self, name, path)
        if file in self.controls:
            return
        self.controls.append(file)

    def delete_file(self, file):
        self.controls.remove(file)
        self.update()
        self.section.file_update()

    def get_file_names(self):
        return [file.name for file in self.controls]
    
    def get_file_paths(self):
        return [file.path for file in self.controls]

class FileInterface(ft.Row):

    def __init__(self, file_list: FileList, name: str, path: str):
        super().__init__(width=90)
        self.file_list = file_list
        self.name = name
        self.path = path
        self.expand = True

        self.controls = [
            ft.Icon(
                ft.icons.INSERT_DRIVE_FILE_OUTLINED
            ),
            ft.Text(self.name),
            ft.IconButton(icon=ft.icons.CANCEL,
                       icon_color=ft.colors.RED_900,
                       on_click=self.delete)
        ]
    
    def delete(self, e):
        self.file_list.delete_file(self)
        del self