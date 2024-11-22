from flet import (
    Page,
    Column,
    Text,
    FilePicker,
    Row
)

class ClusteringPage(Column):
    
    def __init__(
        self,
        page: Page,
        *args, 
        **kwargs):
        super().__init__(*args, **kwargs)
    
        self.controls = [
            Row([
                Text(
                "Chose a file with EEG data in csv format"
            )
            ])
        ]