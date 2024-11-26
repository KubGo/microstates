import flet as ft
from flet import Row, IconButton, Icon, icons, Text, colors, ListView

class FileList(ListView):

    def __init__(self):
        super().__init__(height=90)
        self.controls = []
    
    def add_file(self, name: str, path: str):
        file = FileInterface(self, name, path)
        if file in self.controls:
            return
        self.controls.append(file)

    def delete_file(self, file):
        self.controls.remove(file)
        self.update()




class FileInterface(Row):

    def __init__(self, file_list: FileList, name: str, path: str):
        super().__init__(width=90)
        self.file_list = file_list
        self.name = name
        self.path = path
        self.expand = True

        self.controls = [
            Icon(
                icons.INSERT_DRIVE_FILE_OUTLINED
            ),
            Text(self.name),
            IconButton(icon=icons.CANCEL,
                       icon_color=colors.RED_900,
                       on_click=self.delete)
        ]
    
    def delete(self, e):
        self.file_list.delete_file(self)
        del self