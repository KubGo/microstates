from flet import (
    Page,
    Row,
    Column,
    icons,
    colors,
    IconButton,
    alignment,
    Container
)

from sidebar import SideBar
from main_contents import AbstractMainContent, HomePageContent, ClusteringPageContent

class AppLayout(Row):
    def __init__(
        self, 
        page: Page,
        sidebar: SideBar,
        mainContent: AbstractMainContent,
        *args,
        **kwargs
    ):
        super(Row, self).__init__(*args, **kwargs)
        self.page = page
        self.toggle_nav_bar = IconButton(
            icon=icons.ARROW_CIRCLE_LEFT,
            icon_color=colors.BLUE_GREY_300,
            selected=False,
            selected_icon=icons.ARROW_CIRCLE_RIGHT,
            on_click=self.toggle_nav_rail)
        self.sidebar = sidebar
        self._active_view = mainContent
        self.body = Container(
            content=self.active_view,
            margin=10,
            padding=10,
            alignment=alignment.center,
            expand=True
            )
        self.controls = [
            self.sidebar,
            self.toggle_nav_bar,
            self.body
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
        self.updateMainContent()
        
    def toggle_nav_rail(self, e):
        self.sidebar.visible = not self.sidebar.visible
        self.toggle_nav_bar.selected = not self.toggle_nav_bar.selected
        self.page.update()
