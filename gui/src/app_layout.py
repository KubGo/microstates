from flet import (
    Page,
    Row,
    icons,
    colors,
    IconButton,
    alignment
)

from sidebar import SideBar
from home_page import HomePage

class AppLayout(Row):
    def __init__(
        self, 
        #app,
        page: Page,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        # self.app = app
        self.page = page
        self.toggle_nav_bar = IconButton(
            icon=icons.ARROW_CIRCLE_LEFT,
            icon_color=colors.BLUE_GREY_300,
            selected=False,
            selected_icon=icons.ARROW_CIRCLE_RIGHT,
            on_click=self.toggle_nav_rail)
        self.sidebar = SideBar(page)
        self._active_view = HomePage(page)
        self.controls = [
            self.sidebar,
            self.toggle_nav_bar,
            self.active_view
        ]
        self.alignment = alignment.center
        self.vertical_alignment = alignment.top_center
        self.expand= True
    
    @property
    def active_view(self):
        return self._active_view
    
    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.update()
        
    def toggle_nav_rail(self, e):
        self.sidebar.visible = not self.sidebar.visible
        self.toggle_nav_bar.selected = not self.toggle_nav_bar.selected
        self.page.update()