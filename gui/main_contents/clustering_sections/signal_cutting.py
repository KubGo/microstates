from .interfaces import AbstractSection
from .utils import check_if_all_numeric
import flet as ft

class SignalCuttingSection(AbstractSection):

    def __init__(self, content_page):
        super().__init__(content_page)
        
        # Delete from start
        self.checkbox_start_signal = ft.Checkbox(
            label="Delete from signal start",
            value=False,
            on_change= lambda e: self.use_start_signal_time(e)
        )
        self.signal_start_entry = ft.TextField(
            value="5",
            label="Time from signal's start to delete",
            suffix_text="seconds",
            disabled= True,
            on_change=lambda e: check_if_all_numeric(e)
        )
        self.start_signal = ft.Column([
            self.checkbox_start_signal,
            self.signal_start_entry
        ])
        # Delete from end
        self.checkbox_end_signal = ft.Checkbox(
            label="Delete from signal end",
            value=False,
            on_change= lambda e: self.use_end_signal_time(e)
        )
        self.signal_end_entry = ft.TextField(
            value="5",
            label="Time from signal's end to delete",
            suffix_text="seconds",
            disabled= True,
            on_change= lambda e: check_if_all_numeric(e)
        )
        self.end_signal = ft.Column([
            self.checkbox_end_signal,
            self.signal_end_entry
        ])
        self.controls = [
            self.start_signal,
            self.end_signal
        ]

    def use_start_signal_time(self, e: ft.ControlEvent):
        self.signal_start_entry.disabled = not e.control.value
        self.signal_start_entry.update()
    
    def use_end_signal_time(self, e: ft.ControlEvent):
        self.signal_end_entry.disabled = not e.control.value
        self.signal_end_entry.update()
