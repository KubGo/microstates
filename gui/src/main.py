import flet
from flet import (
    Page,
    Theme,
)

from app_layout import AppLayout


def main(page: Page):
    page.theme = Theme(color_scheme_seed='blue')

    test =  AppLayout(page)
    page.add(test)
    page.update()
    
if __name__ == "__main__":
    flet.app(main)