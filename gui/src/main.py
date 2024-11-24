import flet
from flet import (
    Page,
    Theme,
)

from app_layout import AppLayout
from microstates_app import MicrostatesApp

def main(page: Page):
    MicrostatesApp(page)
    
if __name__ == "__main__":
    flet.app(main)