import flet as ft
from flet import (
    Page,
    Theme,
)

from app_layout import AppLayout
from microstates_app import MicrostatesApp

def main(page: Page):
    page.theme = Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_visibility=True,
            thumb_visibility=True,
            thickness=10,
            radius=5
        ),
        color_scheme_seed="teal"
    )
    page.update()
    MicrostatesApp(page)
    
if __name__ == "__main__":
    ft.app(main)