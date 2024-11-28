import flet as ft

def check_if_all_numeric(e: ft.ControlEvent):
    text = e.control.value
    if text.isdigit() or text == '':
        e.control.error_text = None
        e.control.update()
    else:
        e.control.error_text = "Only numbers are allowed!"
        e.control.update()